"""Build traceable expert-proposed annotation from two attached frozen CSVs.
Does not read matcher outputs. Requires human audit before final gold freeze.
"""
import csv, json, hashlib
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
ROOT=Path(__file__).resolve().parent; OUT=ROOT
CL=ROOT/'lesson4_matcher_input_frozen.csv'; EV=ROOT/'lesson4_evidence_normalized_draft.csv'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,arr):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f, fieldnames=list(arr[0])); w.writeheader(); w.writerows(arr)
claims=read(CL); evidence=read(EV); eidx={r['evidence_id']:r for r in evidence}
assert len(claims)==51 and len(evidence)==12852
NOV='2026-11-06'; OCT='2026-10-02'
def id(tb,row,col,rel=NOV):return f'{rel}:{tb}:R{row}:C{col}'
def groups(*groups):return [[id(*v) for v in group] for group in groups]
# Claim ID maps to expert-proposed label, proof group(s), calculation and evidence-scope explanation.
# Groups explicitly include only minimum sufficient proof sets; alternate equivalents are not exhaustively enumerated.
G={}
def D(n, tb, r, c, note='',alts=()):
 G[n]=('DIRECT', groups([(tb,r,c)]+[]), note)
 if alts: G[n]=('DIRECT', groups([(tb,r,c)], *[[(t,rr,cc)] for t,rr,cc in alts]), note)
def M(n, cells, note=''):
 G[n]=('DERIVED',[ [id(*spec) for spec in cells] ],note)
def O(n, note):G[n]=('OUT_OF_CORPUS',[],note)
O(4,'The two releases do not supply monthly unemployment rates back to March 2026; the full since-March range cannot be audited.')
for n,r in [(5,14),(6,15),(7,16),(8,17),(9,18),(10,19),(11,20)]:D(n,'cps_empsit_sum',r,5,'October 2026 unemployment rate in named demographic group; percent as printed.')
D(12,'cps_empsit_a09',8,10,'1,963,000 rounds to 2.0 million; qualitative changed-little phrasing not separately tested.')
D(13,'cps_empsit_a09',18,10,'October 2026 seasonally adjusted percent distribution, 27 weeks or more: 27.6 percent.')
D(14,'cps_empsit_sum',5,5,'October 2026 participation rate: 61.9 percent.')
D(15,'cps_empsit_sum',7,5,'October 2026 employment-population ratio: 59.3 percent.',alts=[('cps_empsit_a01',8,10)])
M(16,[('cps_empsit_sum',41,5),('cps_empsit_sum',41,6)],'Level=4,840,000, month-over-month change=339,000; 4.8 million is reported rounding.')
G[16]=('DERIVED',[G[16][1][0],[id('cps_empsit_sum',41,4),id('cps_empsit_sum',41,5)]],G[16][2])
D(17,'cps_empsit_a01',12,10,'October 2026 seasonally adjusted, 6,024,000 rounds to 6.0 million.')
D(18,'cps_empsit_sum',47,5,'October 2026 marginally attached, 1,639,000 rounds to 1.6 million.')
D(19,'cps_empsit_sum',48,5,'October 2026 discouraged workers: 448,000.')
O(20,'No monthly series covering the prior 12 months in fixed tables; a 12-month average cannot be reconstructed.')
D(21,'ces_table10',19,5,'Professional and business services over-the-month job change 70,000.',alts=[('ces_table1',122,10)])
O(22,'Prior 12 individual monthly professional/business services changes are absent.')
D(23,'ces_table1',123,10,'32,900 employment change rounds to 33,000.')
D(24,'ces_table1',134,10,'28,100 employment change rounds to 28,000.')
D(25,'ces_table1',133,10,'8,700 employment change rounds to 9,000.')
M(26,[('ces_table1',122,6),('ces_table1',122,9)],'Seasonally adjusted October 2025=22,335,000; October 2026=22,604,000; difference 269,000. The qualitative recent-low assertion is not evaluated.')
D(27,'ces_table1',150,10,'41,600 health-care jobs rounds to 42,000.')
O(28,'Prior 12 individual monthly health-care changes are absent.')
D(29,'ces_table1',159,10,'Hospital jobs +16,000.')
D(30,'ces_table1',157,10,'Home health care +10,500 rounds half-up to +11,000.')
D(31,'ces_table1',155,10,'Outpatient care centers +4,800 rounds to +5,000.')
D(33,'ces_table1',94,10,'Couriers and messengers +17,400 rounds to +17,000.')
D(34,'ces_table1',86,10,'Air transportation +3,500 rounds half-up to +4,000.')
O(35,'No February 2026 reference month in the eligible tables; cumulative gain from February is unobservable.')
O(36,'No February 2026 reference month in the eligible tables; cumulative couriers gain is unobservable.')
D(37,'ces_table10',8,5,'Manufacturing October 2026 monthly employment change +19,000.',alts=[('ces_table1',26,10)])
O(38,'No December 2025 reference month in eligible tables; cumulative gain from December is unobservable.')
D(39,'ces_table1',34,10,'Computer and electronic products +6,700 rounds to +7,000.')
D(40,'ces_table1',33,10,'Machinery manufacturing +3,900 rounds to +4,000.')
D(41,'ces_table1',31,10,'Primary metal manufacturing +3,700 rounds to +4,000.')
M(43,[('ces_table3',3,2),('ces_table3',3,5)],'From $36.85 Oct 2025 to $38.00 Oct 2026: +3.1208%, reported +3.1%.')
M(44,[('ces_table8',3,4),('ces_table8',3,5)],'From $32.63 to $32.75: +$0.12; +0.3678% rounds to 0.4%.')
M(45,[('ces_table2',3,4),('ces_table2',3,5)],'September and October private average workweek both 34.4 hours.')
M(46,[('ces_table2',7,4),('ces_table2',7,5)],'September and October manufacturing average workweek both 40.5 hours.')
M(47,[('ces_table2',24,4),('ces_table2',24,5)],'Manufacturing overtime from 3.0 to 3.1 hours.')
M(48,[('ces_table7',3,4),('ces_table7',3,5)],'Production and nonsupervisory average workweek: 33.9 to 33.8 hours.')
M(51,[('ces_table10',3,4,OCT),('ces_table10',3,3,NOV),('ces_table10',3,5,OCT),('ces_table10',3,4,NOV)],'August revision 186000-133000=53000; September revision 60000-29000=31000; sum=84000.')
main=[r for r in claims if r['set']=='MAIN'];assert len(main)==44 and len(G)==44 and set(G)=={int(r['claim_id'][-3:]) for r in main}
results=[]
for c in main:
 n=int(c['claim_id'][-3:]); label, proof, note=G[n]
 for gr in proof:
  for ref in gr:
   e=eidx[ref];assert e['value_type']=='NUMERIC',ref
   assert e['canonical_value']!='',ref
 results.append(dict(claim_id=c['claim_id'],claim_text=c['claim_text'],gold_label=label,accepted_evidence_groups=json.dumps(proof),derivation=note,review_status='PROPOSED_NEEDS_AUDIT',annotation_note='Numerical component checked; qualitative qualifiers outside numeric scope where noted.'))
write(OUT/'gold_main_proposed.csv',results)
with (OUT/'gold_main_proposed.json').open('w',encoding='utf-8') as f:json.dump(results,f,indent=2,ensure_ascii=False)
from collections import Counter
print('Gold proposed',Counter(r['gold_label'] for r in results))
for r in results:
 print(r['claim_id'],r['gold_label'],r['accepted_evidence_groups'],r['derivation'])
print('sha frozen input',hashlib.sha256(CL.read_bytes()).hexdigest().upper())
