"""Score immutable matcher prediction CSV against separately constructed proposed gold.
IMPORTANT: These results are PROVISIONAL until gold is audited and rules are frozen.
"""
import csv,json,hashlib
from pathlib import Path
from collections import Counter,defaultdict
BASE=Path(__file__).resolve().parent
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,arr):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)
gold={r['claim_id']:r for r in read(BASE/'gold_main_proposed.csv')};preds=read(BASE/'matcher_predictions.csv')
assert len(gold)==44 and len(preds)==88
E={r['evidence_id']:r for r in read(BASE/'lesson4_evidence_normalized_draft.csv')}
output=[]
for p in preds:
 g=gold[p['claim_id']];valid=json.loads(g['accepted_evidence_groups']);proposed=json.loads(p['predicted_evidence_group'])
 if g['gold_label']=='AMBIGUOUS':outcome='EXCLUDED_AMBIGUOUS'
 elif not proposed:
  outcome='CORRECT_ABSTAIN' if g['gold_label']=='OUT_OF_CORPUS' else 'OVER_ABSTAIN'
 elif g['gold_label']=='OUT_OF_CORPUS': outcome='UNJUSTIFIED_LINK'
 else:outcome='CORRECT_LINK' if any(set(proposed)==set(v) and len(proposed)==len(v) for v in valid) else 'WRONG_LINK'
 if outcome=='WRONG_LINK':
  src=[E[r] for r in proposed];true=E[valid[0][0]]
  if all(e['table_id']==true['table_id'] and e['row']==true['row'] for e in src):fail='WRONG_PERIOD_OR_ATTRIBUTE'
  elif len(proposed)<len(valid[0]):fail='INCOMPLETE_DERIVATION'
  else:fail='NUMERIC_COLLISION_OR_WRONG_INDICATOR'
 elif outcome=='UNJUSTIFIED_LINK':fail='CORPUS_SCOPE_FAILURE'
 elif outcome=='OVER_ABSTAIN':fail='UNHANDLED_ATTRIBUTE_OR_CALCULATION'
 elif outcome=='CORRECT_ABSTAIN':fail='VALID_SCOPE_ABSTENTION'
 else:fail='NONE'
 output.append({**p,'gold_label':g['gold_label'],'accepted_evidence_groups':g['accepted_evidence_groups'],'outcome':outcome,'failure_category':fail,'gold_note':g['derivation']})
write(BASE/'comparison_scored_provisional.csv',output)
summary=[]
for method in ['Simple Matching','Attribute-Aware Matching']:
 s=[r for r in output if r['method']==method];n=len(s)
 counts=Counter(r['outcome'] for r in s)
 linkable=sum(r['gold_label'] in ('DIRECT','DERIVED') for r in s)
 outcorpus=sum(r['gold_label']=='OUT_OF_CORPUS' for r in s)
 summary.append(dict(method=method,evaluable_claims=n,linkable_claims=linkable,out_of_corpus=outcorpus,correct_link=counts['CORRECT_LINK'],wrong_link=counts['WRONG_LINK'],over_abstain=counts['OVER_ABSTAIN'],correct_abstain=counts['CORRECT_ABSTAIN'],unjustified_link=counts['UNJUSTIFIED_LINK'],correct_link_rate_all=f"{counts['CORRECT_LINK']/n:.4f}",correct_link_rate_linkable=f"{counts['CORRECT_LINK']/linkable:.4f}",wrong_link_rate_all=f"{(counts['WRONG_LINK']+counts['UNJUSTIFIED_LINK'])/n:.4f}",abstention_rate_all=f"{(counts['OVER_ABSTAIN']+counts['CORRECT_ABSTAIN'])/n:.4f}",out_of_corpus_abstain_rate=f"{counts['CORRECT_ABSTAIN']/outcorpus:.4f}"))
 print('\n',method,'counts',counts,'gold linkable',linkable,'OOC',outcorpus)
 for x in s:
  if x['outcome']!='CORRECT_LINK':print(x['claim_id'],x['outcome'],x['failure_category'],x['predicted_evidence_group'])
write(BASE/'comparison_summary_provisional.csv',summary)
print('\nSummary:',summary)
print('SHA GOLD',hashlib.sha256((BASE/'gold_main_proposed.csv').read_bytes()).hexdigest().upper())
print('SHA PRED',hashlib.sha256((BASE/'matcher_predictions.csv').read_bytes()).hexdigest().upper())
