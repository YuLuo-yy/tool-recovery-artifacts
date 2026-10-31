"""Offline reproduction for the V17-aligned v1.1.0 materials."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,shutil,tempfile,zipfile
import legacy_interface as base
ROOT=Path(__file__).resolve().parent
UPDATES=ROOT/'.updates'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()

def unpack_update():
    spec=read(ROOT/'UPDATE_BUNDLE.json')
    base.require(sha((ROOT/'UPDATE_MANIFEST.json').read_bytes())==spec['manifest_sha256'],'Modified update manifest')
    data=(ROOT/spec['path']).read_bytes()
    base.require(len(data)==spec['bytes'] and sha(data)==spec['sha256'],'Modified update bundle')
    manifest=read(ROOT/'UPDATE_MANIFEST.json')
    if not UPDATES.exists():
        from bundle_codec import decrypt_bytes,PASSWORD,SALT
        with zipfile.ZipFile(io.BytesIO(decrypt_bytes(data,PASSWORD,SALT))) as z:
            base.require(set(z.namelist())==set(manifest),'Update inventory mismatch')
            for n in z.namelist():
                p=PurePosixPath(n)
                base.require(not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n,'Unsafe update path')
            with tempfile.TemporaryDirectory(prefix='unpack-update-',dir=ROOT) as tmp:
                dst=Path(tmp)/'updates';z.extractall(dst);base.verify_files(dst,manifest);dst.rename(UPDATES)
    base.verify_files(UPDATES,manifest)
    return manifest

def current_check():
    base_manifest=base.unpack()
    update_manifest=unpack_update()
    base.verify_files(ROOT,read(ROOT/'RELEASE_FILES.json'))
    old=base.check(base_manifest)
    claims=read(ROOT/'CLAIMS_V110.json');figs=read(ROOT/'FIGURE_MAP.json');paper=read(ROOT/'PAPER_VERSION.json')
    base.require(len({r['id'] for r in claims})==len(claims),'Duplicate claim identifier')
    for r in claims:
        for f in r['files']:
            folder=base.MATERIALS if f['bundle']=='base' else UPDATES
            base.require((folder/f['path']).exists(),'Missing current claim material: '+f['path'])
    keys={(r['document'],r['file']) for r in figs}
    base.require(len(keys)==len(figs)==paper['main_figures']+paper['supplement_figures'],'Figure identity mismatch')
    for doc,count in [('main',paper['main_figures']),('supplement',paper['supplement_figures'])]:
        base.require(sorted(r['number'] for r in figs if r['document']==doc)==list(range(1,count+1)),'Figure numbering mismatch')
    return {'passed':True,'release':'v1.1.0','base_material_files':len(base_manifest),'update_material_files':len(update_manifest),'claims':len(claims),'figures':len(figs),'main_figures':paper['main_figures'],'supplement_figures':paper['supplement_figures'],'S15_trajectories':old['S15_trajectories'],'model_requests':0}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for flag in ['check','statistics','figures','witnesses']:parser.add_argument('--'+flag,action='store_true')
    args=parser.parse_args();base.OUTPUT.mkdir(exist_ok=True)
    summary={'check':current_check()}
    if args.statistics or args.figures or args.witnesses:
        with tempfile.TemporaryDirectory(prefix='work-',dir=base.OUTPUT) as tmp:
            work=Path(tmp)/'materials';shutil.copytree(base.MATERIALS,work);shutil.copytree(UPDATES,work/'updates')
            if args.statistics:
                base.run(['reproduce.py','--full-statistics'],work/'legacy')
                base.run(['s13_reproduce.py'],work/'legacy')
                base.run([str(ROOT/'scripts/verify_current.py'),str(work)],ROOT)
                base.run([str(ROOT/'verify_update.py'),str(work)],ROOT)
                summary['statistics']={'passed':True,'families':['S11 frozen estimates/intervals','S12 Holm40','S13 Holm5','S14 Holm2','S15 Holm4'],'new_inference':False}
            if args.witnesses:
                base.run(['verify_s13_materials.py'],work/'legacy')
                base.run(['verify_s14_portable.py'],work/'current/reproducibility')
                base.run(['portable/verify_r2.py','--output',str(work/'witness_r2/LAST_R2_VERIFICATION.json')],work/'witness_r2')
                base.run([str(ROOT/'verify_update.py'),str(work)],ROOT)
                summary['witnesses']={'passed':True,'S15_public_observation_replays':3024,'scope':'Retained states, public-goal response replay and descriptive timing; no live native environment execution'}
            if args.figures:
                base.run([str(ROOT/'render_current.py'),str(work),str(base.OUTPUT/'figures')],ROOT)
                summary['figures']={'passed':True,'required_figures':21,'main':10,'supplement':11,'output':'outputs/figures'}
            dest=base.OUTPUT/'reports';dest.mkdir(exist_ok=True)
            for p in work.rglob('*.json'):
                if p.name.startswith('LAST_') or p.name in ['VERIFICATION.json','PUBLIC_VERIFICATION.json']:
                    shutil.copy2(p,dest/p.relative_to(work).as_posix().replace('/','__'))
    base.verify_files(base.MATERIALS,read(ROOT/'MATERIALS_MANIFEST.json'))
    base.verify_files(UPDATES,read(ROOT/'UPDATE_MANIFEST.json'))
    name='_'.join(n for n in ['check','statistics','figures','witnesses'] if getattr(args,n)) or 'check'
    (base.OUTPUT/(name+'.json')).write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
