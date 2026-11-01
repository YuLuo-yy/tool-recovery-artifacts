"""Verify provenance and replay observations without model access."""
from pathlib import Path
import csv,gzip,json,sys
from collections import Counter
M=Path(sys.argv[1]);U=M/'updates'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
rows=lambda p:list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))

def target(operation,args,prior,response):
    if operation=='task_comment':return sum(r.get('content')==args['content'] for r in response)
    if operation=='gmail_send':return sum(len(r['email_ids']) for r in response if r.get('subject')==args['subject'])
    if operation=='amazon_cart_add':
        qty=lambda x:sum(r['quantity'] for r in x['cart_items'] if r['product_id']==args['product_id'])
        return qty(response)-qty(prior)
    raise ValueError(operation)

def replay(operation,args,prior,original,events,D):
    # Inputs here intentionally exclude hidden commitment, hidden d and native gold scores.
    candidates={0,1} if original.get('error')=='timeout' else {1}
    trace=[];read_number=0;first=0 if candidates=={1} else None
    for position,e in enumerate(events,1):
        if e['tool']==prior['tool']:
            read_number+=1;count=target(operation,args,prior['response'],e['response'])
            candidates={k for k in candidates if k==count or (read_number<=D and count==0)}
        else:candidates={k+1 for k in candidates}
        trace.append(sorted(candidates))
        if first is None and candidates=={1}:first=position
    support='supported' if candidates=={1} else 'contradicted' if 1 not in candidates else 'ambiguous'
    return trace,sorted(candidates),support,first

obs=json.loads(gzip.decompress((U/'s15/public_observations.json.gz').read_bytes()))
timing={r['episode_slot_id']:r for r in rows(U/'s15/S15_EPISODE_TIMING.csv')}
frozen={r['episode_slot_id']:r for r in rows(M/'current/s15/source/EPISODE_SUMMARY.csv')}
assert len(obs)==len(timing)==len(frozen)==3024
assert {r['episode_slot_id'] for r in obs}==set(timing)==set(frozen)
focus=[];early=[]
for r in obs:
    eid=r['episode_slot_id'];t=timing[eid];f=frozen[eid]
    events=[{'tool':e['tool'],'response':e['response']} for e in r['events']]
    trace,candidates,support,first=replay(r['operation'],r['arguments'],r['prior_read'],r['original_response'],events,r['public_bound'])
    expected=r['expected']
    assert trace==expected['trace'] and candidates==expected['candidate_goal_counts'] and support==expected['public_goal_evidence_support'],eid
    assert expected['full_state_certificate'] is False
    assert support==t['public_goal_evidence_support'] and json.loads(t['candidate_goal_counts'])==candidates
    assert str(first)==t['first_target_supported_position'] or (first is None and t['first_target_supported_position']=='')
    reader=r['prior_read']['tool'];reads=[(i,e) for i,e in enumerate(r['events'],1) if e['tool']==reader]
    writes=[i for i,e in enumerate(r['events'],1) if e['tool']!=reader]
    fresh=next((i for i,e in reads if not e['hidden_stale']),None)
    guarantee=reads[r['public_bound']][0] if len(reads)>r['public_bound'] else None
    write=writes[0] if writes else None
    path=''.join('R' if e['tool']==reader else 'W' for e in r['events'])
    assert path==f['path']==t['path'] and len(reads)==int(f['reads']) and len(writes)==int(f['writes'])
    for value,key in [(fresh,'first_fresh_read_position'),(guarantee,'first_guaranteed_read_position'),(write,'first_write_position')]:
        assert t[key] in [str(value),'' if value is None else str(value)],(eid,key)
    assert r['public_bound']==int(f['stale_bound'])
    assert fresh==expected['first_fresh_read_position'] and write==expected['first_recovery_write_position']
    if f['condition_id']=='main-after_commit-B4-d2-D3-R3W2' and f['operation']=='amazon_cart_add':
        assert path=='RRR' and first==3 and guarantee is None and support=='supported'
        focus.append(eid)
    if t['panel']=='main' and t['stage']=='after_commit' and not writes and guarantee is None and support=='supported':early.append(t)
assert len(focus)==16 and len(early)==808
assert Counter(t['operation'] for t in early)==Counter(read(U/'s15/S15_EARLY_TARGET_SUPPORT.json')['counts_by_operation'])
rules=rows(U/'s15/S15_RULE_SUFFICIENCY.csv')
assert len(rules)==3024
for r in rules:
    D,B,R,W,C=[int(r[k]) for k in ['D','B','R','W','M']];before=r['stage']=='before_commit'
    enough=r['stage']=='clean' or (R>=D+1 and B>=D+1+int(before) and W>=int(before) and C>=D+2+int(before))
    assert enough==(r['sufficient_for_correct_complete']=='True')==(r['observed_correct_complete']=='True')
assert sum(r['observed_correct_complete']=='True' and r['stage']!='clean' for r in rules)==1344
freeze=read(U/'provenance/S13_FREEZE_EVIDENCE.json')
registry=rows(U/'provenance/S13_SAMPLING_REGISTRY.csv')
assert len(freeze['frozen_file_manifest'])==1629 and len(registry)==54
assert freeze['paid_calls_at_freeze']==0
selected=json.loads(gzip.decompress((M/'legacy/s13_witnesses/s13-normal-task_comment-01.episodes.json.gz').read_bytes()))
selected={r['episode_slot_id']:r for r in selected}
for r in read(U/'evidence/FIGURE2_TRACE_EVIDENCE.json'):
    p=selected[r['episode_slot_id']]
    for key in ['case_slot','budget','report','strict_state_success','reads','writes']:assert r[key]==p[key]
    assert [(e['tool'],e['response']) for e in r['events']]==[(e['tool'],e['response']) for e in p['events']]
result={'passed':True,'S15_public_observations':3024,'cart_target_support_examples':len(focus),'early_target_support':len(early),'rule_conditions':len(rules),'S13_provenance_manifest_entries':1629,'S13_registry_slots':54,'new_model_requests':0}
(U/'LAST_UPDATE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
