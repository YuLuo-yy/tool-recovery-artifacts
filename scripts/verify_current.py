"""Recompute S14/S15 and resource cells from released frozen inputs."""
from pathlib import Path
from collections import Counter, defaultdict
import csv, gzip, importlib, json, sys

R=Path(sys.argv[1])
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def rows(p): return list(csv.DictReader(p.open(encoding="utf-8-sig",newline="")))
def integer(v): return int(v == "True") if v in ("True","False") else int(v)
s14=R/"current/reproducibility"
sys.path.insert(0,str(s14))
from s14_frozen_primary import analyse as s14_analyse
scores=json.loads(gzip.decompress((s14/"s14_scores.json.gz").read_bytes()))
actual=s14_analyse(scores)
assert actual==read(s14/"s14_expected_primary.json"),"S14 complete frozen record mismatch"
assert len(scores)==1568
s15=R/"current/s15/source"
sys.path.insert(0,str(s15))
from s15_statistics import analyse
data=rows(s15/"EPISODE_SUMMARY.csv")
for r in data:r["strict_state_success"]=int(r["strict_state_success"])
actual15=analyse(data,read(s15/"REGISTRY.json"),bootstrap=20000)
expected=read(s15/"ANALYSIS_RECOMPUTED.json")
assert actual15==expected,"S15 complete frozen record mismatch, including order/seed/intervals"
assert len(actual15)==4 and all(r["p_holm4"]==1 for r in actual15)
assert sum(r["strict_state_success"] for r in data)==2019
assert sum(r["strict_state_success"] and r["report"]=="complete" for r in data)==1520
assert sum(integer(r["false_complete"]) for r in data)==193
assert sum(integer(r["extra_effect_episode"]) for r in data)==345
assert sum(int(r["model_requests"]) for r in data)==11786
cells=rows(s15/"ALL_CONDITIONS.csv")
for cell in cells:
    group=[r for r in data if r["condition_id"]==cell["condition_id"] and r["operation"]==cell["operation"]]
    assert len(group)==int(cell["valid_worlds"])==16
    for dest,source in [("state_correct","strict_state_success"),("false_complete","false_complete"),
                        ("extra_effect_episodes","extra_effect_episode"),("reads","reads"),("writes","writes"),("model_requests","model_requests")]:
        assert sum(integer(r[source]) for r in group)==int(cell[dest]),(cell["condition_id"],dest)
    assert sum(r["strict_state_success"] and r["report"]=="complete" for r in group)==int(cell["correct_complete"])
    assert dict(Counter(r["path"] for r in group))==json.loads(cell["paths"])
resource=R/"current/resource/source"
episodes=rows(resource/"S14_EPISODE_RESOURCES.csv")
aggregates=rows(resource/"S14_FAULT_RESOURCE_CELLS.csv")
keys=["model","operation","stage","arm"]
numeric=["state_correct","correct_complete","false_complete","extra_effect_episodes","unknown","failed","absent",
         "protocol_errors","reads","writes","tools","model_requests","prompt_tokens","completion_tokens","cached_prompt_tokens"]
for cell in aggregates:
    group=[r for r in episodes if all(r[k]==cell[k] for k in keys)]
    assert len(group)==int(cell["n"])
    for k in numeric: assert sum(int(r[k]) for r in group)==int(cell[k]),(cell,k)
cart=[c for c in aggregates if c["model"]=="b_flash" and c["operation"]=="amazon_cart_add" and c["stage"]=="before_commit"]
byarm={c["arm"]:c for c in cart}
assert int(byarm["R2W2_B4"]["correct_complete"])==3
assert int(byarm["R3W2_B4"]["correct_complete"])==48
assert int(byarm["R2W2_B4"]["model_requests"])==192
assert int(byarm["R3W2_B4"]["model_requests"])==240
result=dict(passed=True,S14_contrasts=2,S15_contrasts=4,bootstrap_draws=20000,
            S14_episodes=1568,S15_episodes=3024,S15_condition_operation_cells=len(cells),
            S14_resource_cells=len(aggregates),model_requests=0,
            S15_holm4=[r["p_holm4"] for r in actual15])
(R/"PUBLIC_VERIFICATION.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result))
