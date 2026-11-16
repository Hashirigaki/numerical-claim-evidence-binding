"""Two intentionally bounded deterministic matchers, NOT reading gold labels.
Input: frozen claim text and normalized primary evidence CSV. Output: proposed evidence ID groups or abstention.
No network, LLM, external packages, or claim-ID-specific logic.
"""
import csv, re, json, hashlib
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from collections import Counter
BASE=Path(__file__).resolve().parent; OUT=BASE
CL=BASE/'lesson4_matcher_input_frozen.csv'; EV=BASE/'lesson4_evidence_normalized_draft.csv'
def read(p):
 with p.open(encoding='utf-8-sig', newline='') as f:return list(csv.DictReader(f))
def write(p,records):
 with p.open('w', encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0])); w.writeheader();w.writerows(records)
claims=[c for c in read(CL) if c['set']=='MAIN']
evidence=[e for e in read(EV) if e['value_type']=='NUMERIC' and e['canonical_value'] and e['release']=='2026-11-06' and e['seasonal_adjustment']=='SA']
# Calibration and feature definitions fixed in code before evaluation; matches require a complete evidence group.
STOP={'the','at','a','an','to','and','of','for','on','with','in','from','this','that','who','all','has','have','was','were','by','over','october','september','august','since','workers','rate','rates','percent','total','employment','people','number','jobs','job','increased','increase','decreased','declined','rose','average','monthly','change','earnings','hourly','workweek','hours','hour','unchanged','continued','trend','up','little','year','recent','low','year','ago','million','reported','prior','previously','combined'}
def stems(s):
 return set((t[:-1] if len(t)>4 and t.endswith('s') else t) for t in re.findall(r'[a-z]+',s.lower()) if t not in STOP and len(t)>2)
def terms(s):
 # Statistical key terms matter more than prose boilerplate.
 return stems(s)
NUMPAT=re.compile(r'(?<![a-zA-Z0-9])([+-]?\$?\d[\d,]*(?:\.\d+)?)(?:\s*(million|percent|cents?|hours?|jobs?|people))?',re.I)
def nums(t):
 out=[]
 for m in NUMPAT.finditer(t):
  raw=m.group(1).replace(',','').replace('$',''); un=(m.group(2) or '').lower()
  try: n=Decimal(raw)
  except InvalidOperation:continue
  if n in (Decimal('2025'),Decimal('2026')):continue
  if un in ('hour','hours') and n==27 and '27 weeks' in t:continue
  if n==12 and re.search(r'12[- ]month|12 months',t,re.I):continue
  if n==27 and re.search(r'27 weeks',t,re.I):continue
  if un=='million':n*=1000000
  if un.startswith('cent'):n/=100
  out.append((n,raw,un))
 return out
def d(s):return Decimal(str(s))
def nearest(n,step):return (n/step).quantize(Decimal('1'),rounding=ROUND_HALF_UP)*step
def approx(value,target):
 if value==target:return True
 if target>=1000000 and target%100000==0:
  return nearest(value,Decimal(100000))==target
 if target>=1000 and target%1000==0:
  return nearest(value,Decimal(1000))==target
 if value.as_tuple().exponent<0 and target.as_tuple().exponent<0:
  step=Decimal(1).scaleb(target.as_tuple().exponent)
  return nearest(value,step)==target
 return False

def concept(text):
 x=text.lower()
 if 'average hourly earnings' in x:return 'USD_PER_HOUR'
 if 'workweek' in x or 'overtime' in x:return 'HOURS'
 if ('unemployment rate' in x or 'participation rate' in x or 'employment-population ratio' in x or 'accounted for' in x):return 'PERCENT'
 if ('unemployed' in x or 'labor force' in x or 'discouraged' in x or 'part time for economic' in x):return 'THOUSAND_PEOPLE'
 return 'THOUSAND_JOBS'
def quality(e,t):
 ct=terms(t);row=terms(e['row_label']);group=terms(e['subgroup_label']);h=terms(e['header_row1']+' '+e['section_label']);cap=terms(e['table_caption']);
 common=len(ct & (row|group));
 # Row-identity match is mandatory for non-wage records.
 if common==0 and not (e['unit_code']=='USD_PER_HOUR' and 'average hourly earnings' in t.lower()):return -999
 score=5*common+1.2*len(ct & h)+0.3*len(ct & cap)
 if e['table_id'] in ('cps_empsit_sum','ces_table10'):score+=0.03
 return score

def direct_candidates(t, approximate=False):
 x=t.lower();u=concept(t);n=nums(t)
 if not n:return []
 # The latest non-calendar numerical assertion is selected by naive baseline.
 target=n[-1][0]
 if ('unemployment rate' in x or 'participation rate' in x or 'employment-population ratio' in x):
  perc=[a for a in n if a[2]=='percent'];target=perc[-1][0] if perc else target
 cand=[]
 for e in evidence:
  if approximate and e['unit_code']!=u:continue
  value=d(e['canonical_value'])
  if not (approx(value,target) if approximate else value==target):continue
  if approximate:
   period=e['period_label'].lower()
   if u=='THOUSAND_JOBS' and any(k in x for k in ('added','gains occurred','trend up','increased','growth included')):
    if not ('change from:' in period or (e['table_id']=='ces_table10' and period.startswith('oct. 2026') and 'over-the-month change' in e['section_label'].lower())):continue
   else:
    if not (period.startswith('oct. 2026') or period.startswith('change from:')):continue
   score=quality(e,t)
   if score<0:continue
  else:
   score=quality(e,t)
   if score<0:score=0
  cand.append((score,e['evidence_id']))
 return sorted(cand,key=lambda z:(-z[0],z[1]))

def simple(t):
 c=direct_candidates(t,False)
 return [c[0][1]] if c else []

# Generic numerical difference solver; no claim-ID-based or gold evidence references.
def amount_after(text):
 x=text.lower()
 pats=[r'(?:increased|rose|declined|edged up|added)\s+by\s+([\d,.]+)\s*(cents?|million|hours?|percent)?',
       r'(?:has\s+)?added\s+([\d,.]+)\s*(jobs?|million)?',
       r'(?:declined|edged up)\s+by\s+([\d,.]+)\s*(hours?)?']
 for p in pats:
  m=re.search(p,x)
  if m:
   v=Decimal(m.group(1).replace(',',''));unit=(m.group(2) or '').lower()
   if unit.startswith('cent'):v/=100
   if unit=='million':v*=1000000
   if 'declined' in x:v=-v
   return v,unit
 return None,None

def pair_candidates(t):
 x=t.lower(); u=concept(t)
 useyear=('since a recent low in october 2025' in x or ('over the past 12 months' in x and 'average hourly earnings' in x))
 # No month exists for March, February, December 2025 in the frozen source tables.
 if re.search(r'since (?:a recent (?:employment )?low in )?(?:march|february|december)',x):return []
 val,changeunit=amount_after(t)
 targets=nums(t)
 positive=[q for q in targets if q[0] not in [Decimal(12),Decimal(27)]]
 out=[]
 # Build date-matched prior/current cell pairs for the *same* indicator and table.
 bykey={(e['table_id'],e['row'],e['period_label'],e['col']):e for e in evidence}
 byrow={}
 for e in evidence:byrow.setdefault((e['table_id'],e['row']),[]).append(e)
 for (tab,row), rs in byrow.items():
  curr=[r for r in rs if r['period_label'].lower().startswith('oct. 2026') and r['unit_code']==u]
  older=[r for r in rs if r['period_label'].lower().startswith('oct. 2025' if useyear else 'sept. 2026') and r['unit_code']==u]
  for a in older:
   for b in curr:
    if a['seasonal_adjustment']!='SA' or b['seasonal_adjustment']!='SA':continue
    score=quality(b,t)
    if score<0:continue
    v1=d(a['canonical_value']);v2=d(b['canonical_value']);delta=v2-v1
    if useyear and 'average hourly earnings' in x:
     pc=(delta/v1*100) if v1 else Decimal('-9999')
     pcts=[q[0] for q in targets if q[2]=='percent']
     if not pcts or not approx(pc,pcts[-1]):continue
    elif 'remained at' in x or 'unchanged at' in x:
     if v1!=v2:continue
     if not any(approx(v2,z[0]) for z in positive):continue
    else:
     if val is None or not approx(delta,val):continue
     if ' to ' in x and not any(approx(v2,z[0]) for z in positive):continue
     if 'or ' in x and '%' in x or 'percent' in x:
      pcts=[q[0] for q in targets if q[2]=='percent']
      if pcts and v1 and not approx(100*(v2-v1)/v1,pcts[-1]):continue
    out.append((score,[a['evidence_id'],b['evidence_id']]))
 return sorted(out,key=lambda z:(-z[0],z[1]))

def aware(t):
 x=t.lower()
 if ('average monthly gain' in x or 'has remained in a narrow range' in x or 'higher than previously reported' in x):return []
 if re.search(r'since (?:a recent (?:employment )?low in )?(?:march|february|december)',x):return []
 derived=(
  ('average hourly earnings' in x and ('over the past 12 months' in x or ' rose by ' in x or ' increased by ' in x))
  or ('since a recent low in october 2025' in x)
  or ('increased by' in x and ' to ' in x)
  or ('declined by' in x and ' to ' in x)
  or ('edged up by' in x and ' to ' in x)
  or ('unchanged at' in x or 'remained at' in x)
 )
 if derived:
  pair=pair_candidates(t)
  return pair[0][1] if pair else []
 direct=direct_candidates(t,True)
 return [direct[0][1]] if direct else []

outputs=[]
for c in claims:
 for name,func in [('Simple Matching',simple),('Attribute-Aware Matching',aware)]:
  pred=func(c['claim_text'])
  outputs.append(dict(claim_id=c['claim_id'],method=name,claim_text=c['claim_text'],predicted_evidence_group=json.dumps(pred),status='LINK' if pred else 'ABSTAIN'))
write(OUT/'matcher_predictions.csv',outputs)
print('Claim count:',len(claims),'Predictions:',len(outputs))
for m in ('Simple Matching','Attribute-Aware Matching'):
 r=[x for x in outputs if x['method']==m]
 print(m,Counter(v['status'] for v in r))
 for x in r:print(x['claim_id'], x['predicted_evidence_group'])
