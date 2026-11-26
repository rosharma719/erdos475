# exact: for each instance, fraction of admissible balanced splits with a disjoint (A-path,E-path) pair
import sys
from itertools import combinations
from half_path_rank import interior_sets
p=int(sys.argv[1])
for n in map(int,sys.argv[2:]):
    m=n-1;k=m//2; inst=allok=0; minf=(2,None); bad_splits=0; tot_splits=0
    for el in combinations(range(2,p),m):
        if (sum(el)+1)%p: continue
        B={1,*el}
        if all(p-b in B for b in B): continue
        tail=sum(1<<a for a in el)
        for x in range(2,p):
            if 2*x%p==1: continue
            inst+=1; ok=tot=0
            for sub in combinations(el,k):
                c=(1+sum(sub))%p
                if c in (0,1,x): continue
                tot+=1; first=sum(1<<a for a in sub); forb=3|(1<<c)|(1<<x)
                L=interior_sets(p,first,1,c,forb); R=interior_sets(p,tail^first,c,0,forb)
                ok+= any(not (S&T) for S in L for T in R)
            allok+= ok==tot; bad_splits+=tot-ok; tot_splits+=tot
            if ok/tot<minf[0]: minf=(ok/tot,ok,tot,sorted(B),x)
    print(f"p={p} n={n} inst={inst} all-splits-work={allok} failing splits {bad_splits}/{tot_splits} min frac {minf}",flush=True)
