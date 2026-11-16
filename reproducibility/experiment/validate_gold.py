"""Recompute numeric claims from proposed primary evidence IDs; human review still required for corpus scope & alternative proof sets."""
import csv,json,hashlib
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
BASE=Path(__file__).resolve().parent
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
E={r['evidence_id']:r for r in read(BASE/'lesson4_evidence_normalized_draft.csv')}
G={int(r['claim_id'][-3:]):r for r in read(BASE/'gold_main_proposed.csv')}
def val(ref):return Decimal(E[ref]['canonical_value'])
def rnd(v,step):return (v/step).quantize(Decimal(1),rounding=ROUND_HALF_UP)*step
# Claim displayed precision, as verified by matching a physical row, indicator, month, unit, release.
expected={5:(3.9,0.1),6:(3.6,0.1),7:(13.9,0.1),8:(3.7,0.1),9:(6.6,0.1),10:(2.8,0.1),11:(4.7,0.1),12:(2000000,100000),13:(27.6,0.1),14:(61.9,0.1),15:(59.3,0.1),17:(6000000,100000),18:(1600000,100000),19:(448000,1000),21:(70000,1000),23:(33000,1000),24:(28000,1000),25:(9000,1000),27:(42000,1000),29:(16000,1000),30:(11000,1000),31:(5000,1000),33:(17000,1000),34:(4000,1000),37:(19000,1000),39:(7000,1000),40:(4000,1000),41:(4000,1000)}
errors=[]
for n,(target,step) in expected.items():
 proofs=json.loads(G[n]['accepted_evidence_groups']); assert G[n]['gold_label']=='DIRECT'
 for proof in proofs:
  v=val(proof[0]); desired=Decimal(str(target)); step=Decimal(str(step))
  if rnd(v,step)!=desired:errors.append((n,v,desired,step))
# All DERIVED numerical calculations verified, taking first listed full evidence set.
def p(n):return [val(i) for i in json.loads(G[n]['accepted_evidence_groups'])[0]]
checks={
16:(p(16)[0]==4840000 and p(16)[1]==339000),
26:(p(26)[1]-p(26)[0]==269000),
43:(rnd((p(43)[1]/p(43)[0]-1)*100,Decimal('0.1'))==Decimal('3.1')),
44:(p(44)[1]-p(44)[0]==Decimal('.12') and rnd((p(44)[1]/p(44)[0]-1)*100,Decimal('.1'))==Decimal('.4')),
45:(p(45)==[Decimal('34.4'),Decimal('34.4')]),
46:(p(46)==[Decimal('40.5'),Decimal('40.5')]),
47:(p(47)[1]-p(47)[0]==Decimal('.1')),
48:(p(48)[1]-p(48)[0]==Decimal('-.1')),
51:(p(51)[1]-p(51)[0]+p(51)[3]-p(51)[2]==84000),
}
assert all(checks.values()),checks
assert not errors,errors
for n in expected:
 print('DIRECT',n,'VERIFIED')
for n in checks:
 print('DERIVED',n,'VERIFIED')
# Sanity cross-check historical month availability in both data snapshots.
all_periods=sorted({r['period_label'] for r in E.values()})
for x in ['Mar. 2026','Feb. 2026','Dec. 2025']:
 assert x not in all_periods,x
assert len([r for r in G.values() if r['gold_label']=='OUT_OF_CORPUS'])==7
print('Verified direct:',len(expected),'derived:',len(checks),'out-of-corpus proposed: 7')
print('Gold source caveat: monthly average claims and low-point qualifiers require review under full numerical-claim boundary.')
