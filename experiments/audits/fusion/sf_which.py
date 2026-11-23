"""For each zero-sum non-atom A: which atoms B (with Z=A\\B zero-sum) work for EVERY valid Z-cycle?
Report: #A where ALL atoms work; #A where all MIN-SIZE atoms work; #A where all MAX-size atoms work; failures of each rule."""
import sys
from itertools import combinations
from sf_fast import minimal, valid_cycles, border_orders, fuses
p=int(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3])
stats={'all':0,'min':0,'max':0,'ge3':0,'tot':0}; badmax=[]; badge3=[]; badmin=[]; badall=[]
for n in range(lo,hi+1):
    for A in combinations(range(1,p),n):
        if sum(A)%p or minimal(A,p): continue
        cands=[B for r in range(2,n-1) for B in combinations(A,r) if minimal(B,p) and sum(x for x in A if x not in B)%p==0]
        res={}
        for B in cands:
            Z=tuple(x for x in A if x not in B); BO=border_orders(B)
            res[B]=all(fuses(z,BO,p) for z in valid_cycles(Z,p))
        stats['tot']+=1
        mn=min(map(len,cands)); mx=max(map(len,cands))
        if all(res.values()): stats['all']+=1
        else: badall.append((A,[B for B in res if not res[B]][:3]))
        if all(res[B] for B in cands if len(B)==mn): stats['min']+=1
        else: badmin.append((A,[B for B in res if len(B)==mn and not res[B]][:3]))
        if all(res[B] for B in cands if len(B)==mx): stats['max']+=1
        else: badmax.append(A)
        if all(res[B] for B in cands if len(B)>=3): stats['ge3']+=1
        else: badge3.append((A,[B for B in res if len(B)>=3 and not res[B]][:3]))
print('p',p,stats); print('every-atom failures (first):',badall[:6]); print('min-atom-rule failures:',badmin[:3]); print('MAX-rule failures:',badmax[:6]); print('size>=3 failures:',badge3[:6])
