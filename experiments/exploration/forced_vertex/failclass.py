import sys
from itertools import combinations
from half_path_rank import interior_sets
p=int(sys.argv[1])
for n in map(int,sys.argv[2:]):
    m=n-1;k=m//2; cnt={'Aempty':0,'Eempty':0,'both_empty':0,'cross':0}; ex=None
    for el in combinations(range(2,p),m):
        if (sum(el)+1)%p: continue
        B={1,*el}
        if all(p-b in B for b in B): continue
        tail=sum(1<<a for a in el)
        for x in range(2,p):
            if 2*x%p==1: continue
            for sub in combinations(el,k):
                c=(1+sum(sub))%p
                if c in (0,1,x): continue
                first=sum(1<<a for a in sub); forb=3|(1<<c)|(1<<x)
                L=interior_sets(p,first,1,c,forb); R=interior_sets(p,tail^first,c,0,forb)
                if any(not (S&T) for S in L for T in R): continue
                if not L and not R: cnt['both_empty']+=1
                elif not L: cnt['Aempty']+=1
                elif not R: cnt['Eempty']+=1
                else:
                    cnt['cross']+=1
                    if ex is None: ex=(sorted(B),x,sorted(sub),c,len(L),len(R))
    print(p,n,cnt,"cross example:",ex,flush=True)
