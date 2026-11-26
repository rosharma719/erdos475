# per instance: fraction of admissible splits (c not in {0,t,x}) whose rank test certifies; report min fraction & instance
import sys
from itertools import combinations
from math import comb
from random import Random
from half_path_rank import interior_sets, exterior_masks, certified_ranks
p=int(sys.argv[1]); sizes=[int(a) for a in sys.argv[2:]]
for n in sizes:
    rng=Random(3); m,k,d=n-1,(n-1)//2,n-3; D=comb(d,k-1); masks=exterior_masks(d)
    fr=[]; worst=None
    for el in combinations(range(2,p),m):
        if (sum(el)+1)%p: continue
        B={1,*el}
        if all(p-b in B for b in B): continue
        tail=sum(1<<a for a in el)
        for x in range(2,p):
            if 2*x%p==1: continue
            good=tot=0
            for sub in combinations(el,k):
                c=(1+sum(sub))%p
                if c in (0,1,x): continue
                tot+=1
                first=sum(1<<a for a in sub); forb=3|(1<<c)|(1<<x)
                L=interior_sets(p,first,1,c,forb); R=interior_sets(p,tail^first,c,0,forb)
                if not L or not R: continue
                ground=[v for v in range(p) if not forb>>v&1]
                a=b=0
                for _ in range(4):
                    a2,b2=certified_ranks(L,R,ground,masks,10**9,rng); a,b=max(a,a2),max(b,b2)
                    if a+b>D: break
                good+= a+b>D
            f=good/tot; fr.append(f)
            if worst is None or f<worst[0]: worst=(f,good,tot,sorted(B),x)
    fr.sort()
    print(f"p={p} n={n} inst={len(fr)} min frac={worst[0]:.3f} ({worst[1]}/{worst[2]}) at B={worst[3]} x={worst[4]}; median {fr[len(fr)//2]:.2f}",flush=True)
