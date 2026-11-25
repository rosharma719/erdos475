# For each nonsymmetric instance: best margin max_split(rhoA+rhoE-D), and whether some split has a full-rank half.
import sys
from itertools import combinations
from math import comb
from random import Random
from half_path_rank import interior_sets, exterior_masks, certified_ranks
p=int(sys.argv[1]); sizes=[int(a) for a in sys.argv[2:]]
for n in sizes:
    rng=Random(1); m,k,d=n-1,(n-1)//2,n-3; D=comb(d,k-1); masks=exterior_masks(d)
    tot=full=0; worst=None; hist={}
    for el in combinations(range(2,p),m):
        if (sum(el)+1)%p: continue
        B={1,*el}
        if all(p-b in B for b in B): continue
        tail=sum(1<<a for a in el)
        for x in range(2,p):
            if 2*x%p==1: continue
            tot+=1; best=-10**9; f=False
            for sub in combinations(el,k):
                c=(1+sum(sub))%p
                if c in (0,1,x): continue
                first=sum(1<<a for a in sub); forb=3|(1<<c)|(1<<x)
                L=interior_sets(p,first,1,c,forb); R=interior_sets(p,tail^first,c,0,forb)
                if not L or not R: continue
                ground=[v for v in range(p) if not forb>>v&1]
                a=b=0
                for _ in range(4):
                    a2,b2=certified_ranks(L,R,ground,masks,10**9,rng); a,b=max(a,a2),max(b,b2)
                best=max(best,a+b-D)
                if a==D or b==D: f=True
            full+=f; hist[best]=hist.get(best,0)+1
            if worst is None or best<worst[0]: worst=(best,sorted(B),x)
    print(f"p={p} n={n} D={D} inst={tot} some-half-full={full} margin-hist={dict(sorted(hist.items())[:6])} worst={worst}",flush=True)
