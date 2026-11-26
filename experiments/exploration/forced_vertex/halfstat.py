# Q1: does some split have BOTH halves with rank > D/2 ?  Q2: over all splits with nonempty halves, min rank ratio.
import sys
from itertools import combinations
from math import comb
from random import Random
from half_path_rank import interior_sets, exterior_masks, certified_ranks
p=int(sys.argv[1]); sizes=[int(a) for a in sys.argv[2:]]
for n in sizes:
    rng=Random(2); m,k,d=n-1,(n-1)//2,n-3; D=comb(d,k-1); masks=exterior_masks(d)
    tot=both=0; allsplit_ok=0; minratio=9; worst=None
    for el in combinations(range(2,p),m):
        if (sum(el)+1)%p: continue
        B={1,*el}
        if all(p-b in B for b in B): continue
        tail=sum(1<<a for a in el)
        for x in range(2,p):
            if 2*x%p==1: continue
            tot+=1; f=False; every=True
            for sub in combinations(el,k):
                c=(1+sum(sub))%p
                if c in (0,1,x): continue
                first=sum(1<<a for a in sub); forb=3|(1<<c)|(1<<x)
                L=interior_sets(p,first,1,c,forb); R=interior_sets(p,tail^first,c,0,forb)
                ground=[v for v in range(p) if not forb>>v&1]
                a=b=0
                for _ in range(4):
                    a2,b2=certified_ranks(L,R,ground,masks,10**9,rng); a,b=max(a,a2),max(b,b2)
                if 2*a>D and 2*b>D: f=True
                else: every=False
                for r_ in (a,b):
                    if r_/D<minratio: minratio=r_/D; worst=(r_,D,sorted(B),x,sorted(sub))
            both+=f; allsplit_ok+=every
    print(f"p={p} n={n} D={D} inst={tot} some-split-both>D/2: {both}  every-split-both>D/2: {allsplit_ok}  min half-rank ratio {minratio:.2f} at {worst}",flush=True)
