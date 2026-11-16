"""Secondary audit in a *separate* output namespace; source ZIP inputs are never modified.
Evidence available: normalized CSV (not original saved HTML)."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from collections import Counter
import csv,json,hashlib
P=Path(__file__).resolve().parent
read=lambda p: list(csv.DictReader((P/p).open(encoding='utf-8-sig',newline='')))
def write(name,rows):
 with (P/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
claims=read('lesson4_matcher_input_frozen.csv')
original=read('gold_main_proposed.csv')
evidence=read('lesson4_evidence_normalized_draft.csv')
preds=read('matcher_predictions.csv')
idx={r['evidence_id']:r for r in evidence}
assert len(claims)==51 and len(original)==44 and len(idx)==12852 and len(preds)==88
oldsha={name:hashlib.sha256((P/name).read_bytes()).hexdigest().upper() for name in ['lesson4_matcher_input_frozen.csv','lesson4_evidence_normalized_draft.csv','gold_main_proposed.csv','matcher_predictions.csv']}

def ref(release, table,row,col):return f'{release}:{table}:R{row}:C{col}'
def value(id):return Decimal(idx[id]['canonical_value'])
def round_to(v,step=Decimal('1000')):return (v/step).quantize(Decimal('1'),rounding=ROUND_HALF_UP)*step
# The BLS phrase 'over the prior 12 months' refers to Sep 2025 -> Sep 2026,
# i.e. the 12 completed monthly changes BEFORE October 2026.
# Current revised Sep 2026 (November edition) and prior Sep 2025 (October edition)
# are separate-version observations; this must be disclosed and treated as a provisional proxy.
fixes={
 'CLAIM-020':(3,48000,'Total nonfarm'),
 'CLAIM-022':(122,15000,'Professional and business services'),
 'CLAIM-028':(150,31000,'Health care'),
}
notes={
 'CLAIM-020':'Sep 2025 -> Sep 2026, 580,000/12 = 48,333.3 monthly; 48,000 displayed. Cross-edition seasonal-adjustment caveat.',
 'CLAIM-022':'Sep 2025 -> Sep 2026, 175,000/12 = 14,583.3 monthly; 15,000 displayed. Cross-edition seasonal-adjustment caveat.',
 'CLAIM-028':'Sep 2025 -> Sep 2026, 368,600/12 = 30,716.7 monthly; 31,000 displayed. Cross-edition seasonal-adjustment caveat.',
}
revised=[]; audit=[]
for r in original:
 c=dict(r); id=r['claim_id']; original_label=c['gold_label']; status='CONSISTENT_WITH_NORMALIZED_EVIDENCE'
 if id in fixes:
  row,reported,subject=fixes[id]
  p=ref('2026-10-02','ces_table1',row,6)
  q=ref('2026-11-06','ces_table1',row,8)
  for eid,period in [(p,'Sept. 2025'),(q,'Sept. 2026')]:
   e=idx[eid]
   assert e['seasonal_adjustment']=='SA' and e['period_label'].startswith(period), (id,e)
   assert subject.lower() in e['row_label'].lower(),(id,e['row_label'])
  calc=(value(q)-value(p))/12
  assert round_to(calc)==reported,(id,calc,reported)
  c['gold_label']='DERIVED'
  c['accepted_evidence_groups']=json.dumps([[p,q]])
  c['derivation']=notes[id]
  status='RECLASSIFY_CROSS_EDITION_DERIVATION'
 elif original_label=='OUT_OF_CORPUS':
  status='HISTORICAL_PERIOD_ABSENT_FROM_PERMITTED_TABLES'
 # Check proof metadata consistency: all IDs unique per group, numeric, plausible seasonal / unit fields.
 groups=json.loads(c['accepted_evidence_groups'])
 for group in groups:
  assert len(set(group))==len(group),(id,group)
  for eid in group:
   assert eid in idx and idx[eid]['value_type']=='NUMERIC' and idx[eid]['canonical_value'],(id,eid)
   assert idx[eid]['release'] in ['2026-11-06','2026-10-02']
   assert idx[eid]['seasonal_adjustment'] in ['SA','NSA','UNSPECIFIED','REVIEW',''],(id,eid)
 c['review_status']='SECONDARY_AUDIT_PROVISIONAL'
 c['annotation_note']='Reviewed against normalized evidence records; source HTML provenance and independent expert adjudication not verified.'
 revised.append(c)
 audit.append(dict(claim_id=id,claim_text=c['claim_text'],original_label=original_label,audit_label=c['gold_label'],audit_conclusion=status,accepted_evidence_groups=c['accepted_evidence_groups'],evidence_values=' | '.join(f"{eid}={idx[eid]['canonical_value']} ({idx[eid]['period_label']}; {idx[eid]['seasonal_adjustment']}; {idx[eid]['unit_code']})" for g in groups[:1] for eid in g),audit_note=c['derivation'],source_limit='Based on frozen normalized evidence only; original HTML and alternate acceptable proofs not independently checked.'))
write('gold_main_audit_v1.csv',revised)
write('audit_44_main_v1.csv',audit)
newgold={r['claim_id']:r for r in revised}
output=[]
for p in preds:
 g=newgold[p['claim_id']]
 valid=json.loads(g['accepted_evidence_groups'])
 proposed=json.loads(p['predicted_evidence_group'])
 if not proposed:outcome='CORRECT_ABSTAIN' if g['gold_label']=='OUT_OF_CORPUS' else 'OVER_ABSTAIN'
 elif g['gold_label']=='OUT_OF_CORPUS':outcome='UNJUSTIFIED_LINK'
 else:outcome='CORRECT_LINK' if any(set(proposed)==set(v) and len(proposed)==len(v) for v in valid) else 'WRONG_LINK'
 if outcome=='WRONG_LINK':
  src=[idx[x] for x in proposed]; true=idx[valid[0][0]]
  if all(e['table_id']==true['table_id'] and e['row']==true['row'] for e in src):category='WRONG_PERIOD_OR_ATTRIBUTE'
  elif len(proposed)<len(valid[0]):category='INCOMPLETE_DERIVATION'
  else:category='NUMERIC_COLLISION_OR_WRONG_INDICATOR'
 elif outcome=='UNJUSTIFIED_LINK':category='CORPUS_SCOPE_FAILURE'
 elif outcome=='OVER_ABSTAIN':category='UNHANDLED_ATTRIBUTE_OR_CALCULATION'
 elif outcome=='CORRECT_ABSTAIN':category='VALID_SCOPE_ABSTENTION'
 else:category='NONE'
 output.append({**p,'gold_label':g['gold_label'],'accepted_evidence_groups':g['accepted_evidence_groups'],'outcome':outcome,'failure_category':category,'gold_note':g['derivation']})
write('comparison_scored_audit_v1.csv',output)
summary=[]
for method in ['Simple Matching','Attribute-Aware Matching']:
 s=[r for r in output if r['method']==method];n=len(s);counts=Counter(r['outcome'] for r in s)
 linkable=sum(r['gold_label'] in ('DIRECT','DERIVED') for r in s)
 ooc=sum(r['gold_label']=='OUT_OF_CORPUS' for r in s)
 summary.append(dict(method=method,evaluable_claims=n,linkable_claims=linkable,out_of_corpus=ooc,
  correct_link=counts['CORRECT_LINK'],wrong_link=counts['WRONG_LINK'],over_abstain=counts['OVER_ABSTAIN'],correct_abstain=counts['CORRECT_ABSTAIN'],unjustified_link=counts['UNJUSTIFIED_LINK'],
  correct_link_rate_all=f"{counts['CORRECT_LINK']/n:.4f}",correct_link_rate_linkable=f"{counts['CORRECT_LINK']/linkable:.4f}",wrong_link_rate_all=f"{(counts['WRONG_LINK']+counts['UNJUSTIFIED_LINK'])/n:.4f}",abstention_rate_all=f"{(counts['OVER_ABSTAIN']+counts['CORRECT_ABSTAIN'])/n:.4f}",out_of_corpus_abstain_rate=f"{counts['CORRECT_ABSTAIN']/ooc:.4f}"))
write('comparison_summary_audit_v1.csv',summary)
assert all(hashlib.sha256((P/name).read_bytes()).hexdigest().upper()==sha for name,sha in oldsha.items())
print('ORIGINAL INPUT HASHES PRESERVED',oldsha)
print('LABELS',Counter(x['gold_label'] for x in revised))
print('COUNTS',json.dumps(summary,indent=2))
print('RECATEGORIZED')
for r in audit:
 if r['audit_conclusion'].startswith('RECLASSIFY'):print(r['claim_id'],r['audit_note'],r['accepted_evidence_groups'])
