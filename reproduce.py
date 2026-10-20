"""Credential-free offline verification of the released experiment materials."""
from pathlib import Path, PurePosixPath
import argparse, csv, hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "outputs"
MATERIALS = ROOT / ".materials"

def sha(data): return hashlib.sha256(data).hexdigest()
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def require(ok, message):
    if not ok: raise ValueError(message)
def verify_files(folder, manifest):
    for name, spec in manifest.items():
        p=folder/name
        require(p.is_file(), f"Missing material: {name}")
        require(sha(p.read_bytes())==spec["sha256"], f"Modified material: {name}")
def unpack():
    spec=read(ROOT/"BUNDLE.json")
    require(sha((ROOT/"MATERIALS_MANIFEST.json").read_bytes())==spec["manifest_sha256"],"Modified materials manifest")
    chunks=[]
    for part in spec["parts"]:
        p=ROOT/part["path"]
        require(p.is_file(),f"Missing bundle part: {part['path']}")
        data=p.read_bytes()
        require(len(data)==part["bytes"] and sha(data)==part["sha256"],f"Modified bundle part: {part['path']}")
        chunks.append(data)
    data=b"".join(chunks)
    require(sha(data)==spec["sha256"],"Combined bundle hash mismatch")
    manifest=read(ROOT/"MATERIALS_MANIFEST.json")
    if not MATERIALS.exists():
        from bundle_codec import decrypt_bytes, PASSWORD, SALT
        with zipfile.ZipFile(io.BytesIO(decrypt_bytes(data,PASSWORD,SALT))) as z:
            require(set(z.namelist())==set(manifest),"Bundle file inventory mismatch")
            for name in z.namelist():
                p=PurePosixPath(name)
                require(not p.is_absolute() and ".." not in p.parts and "\\" not in name and ":" not in name,"Unsafe bundle path")
            with tempfile.TemporaryDirectory(prefix="unpack-",dir=ROOT) as temp:
                staging=Path(temp)/"materials"
                z.extractall(staging)
                verify_files(staging,manifest)
                staging.rename(MATERIALS)
    verify_files(MATERIALS,manifest)
    return manifest
def csvread(p): return list(csv.DictReader(p.open(encoding="utf-8-sig",newline="")))
def check(manifest):
    claims=read(MATERIALS/"CLAIMS.json")
    require(len(claims)==25,"Expected 25 claim records")
    for claim in claims:
        for rel in claim["files"]:require((MATERIALS/rel).exists(),f"Missing claim input: {rel}")
    figs=read(MATERIALS/"FIGURE_MAP.json")
    require(len(figs)==21,"Expected 21 manuscript figures")
    rows=csvread(MATERIALS/"current/s15/source/EPISODE_SUMMARY.csv")
    require(len(rows)==3024 and len({r["episode_slot_id"] for r in rows})==3024,"S15 trajectory completeness")
    require(len({r["case_slot"] for r in rows})==48,"S15 reused world count")
    result=dict(passed=True,material_files=len(manifest),claims=25,figures=21,S15_trajectories=3024,
                S15_worlds=48,model_requests=0)
    return result
def run(command,cwd):
    env=os.environ.copy()
    env["PYTHONUTF8"]="1"
    env["PYTHONIOENCODING"]="utf-8"
    guard = (
        "import socket,sys,runpy;from pathlib import Path;"
        "deny=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('Network disabled during reproduction'));"
        "socket.socket=deny;socket.create_connection=deny;"
        "sys.argv=sys.argv[1:];sys.path.insert(0,str(Path(sys.argv[0]).resolve().parent));"
        "runpy.run_path(sys.argv[0],run_name='__main__')"
    )
    proc=subprocess.run([sys.executable,"-c",guard,*command],cwd=cwd,env=env,capture_output=True,text=True,encoding="utf-8")
    print(proc.stdout, end="",flush=True)
    if proc.returncode:
        print(proc.stderr,file=sys.stderr)
        raise RuntimeError(f"Failed: {command[0]}")
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ["check","statistics","figures","witnesses"]:parser.add_argument("--"+name,action="store_true")
    args=parser.parse_args()
    OUTPUT.mkdir(exist_ok=True)
    summary={"check":check(unpack())}
    if args.statistics or args.figures or args.witnesses:
        # All scripts that emit reports run on a disposable copy, never sealed inputs.
        with tempfile.TemporaryDirectory(prefix="work-",dir=OUTPUT) as tmp:
            work=Path(tmp)/"materials"
            shutil.copytree(MATERIALS,work)
            if args.statistics:
                run(["reproduce.py","--full-statistics"],work/"legacy")
                run(["s13_reproduce.py"],work/"legacy")
                run([str(ROOT/"scripts/verify_current.py"),str(work)],ROOT)
                summary["statistics"]={"passed":True,"families":["S11 frozen estimates/intervals","S12 Holm40","S13 Holm5","S14 Holm2","S15 Holm4"]}
            if args.witnesses:
                run(["verify_s13_materials.py"],work/"legacy")
                run(["verify_s14_portable.py"],work/"current/reproducibility")
                if (work/"witness_r2/portable/verify_r2.py").exists():
                    run(["portable/verify_r2.py","--output",str(work/"witness_r2/LAST_R2_VERIFICATION.json")],work/"witness_r2")
                summary["witnesses"]={"passed":True,"scope":"Retained selected native states and events; no live environment execution"}
            if args.figures:
                plot=work/"current/figures"
                for sub in ["figures","qa"]: (plot/sub).mkdir(exist_ok=True)
                run(["plot.py"],plot)
                dest=OUTPUT/"figures";dest.mkdir(exist_ok=True)
                for figure in read(work/"FIGURE_MAP.json"):
                    p=plot/"figures"/figure["file"]
                    require(p.is_file(),f"Missing regenerated figure: {p.name}")
                    shutil.copy2(p,dest/p.name)
                summary["figures"]={"passed":True,"required_figures":21,"output":"outputs/figures"}
            reports=OUTPUT/"reports";reports.mkdir(exist_ok=True)
            for p in work.rglob("*.json"):
                if p.name.startswith("LAST_") or p.name in ["VERIFICATION.json","PUBLIC_VERIFICATION.json"]:
                    name=p.relative_to(work).as_posix().replace("/","__")
                    shutil.copy2(p,reports/name)
    # Inputs must remain byte-identical after every action.
    verify_files(MATERIALS,read(ROOT/"MATERIALS_MANIFEST.json"))
    name="_".join(n for n in ["check","statistics","figures","witnesses"] if getattr(args,n)) or "check"
    (OUTPUT/(name+".json")).write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
