from itertools import combinations
from half_path_rank import interior_sets
def exact(p,B,x):
    el=sorted(set(B)-{1}); m=len(el); k=m//2; tail=sum(1<<a for a in el); ok=tot=0
    for sub in combinations(el,k):
        c=(1+sum(sub))%p
        if c in (0,1,x): continue
        tot+=1; first=sum(1<<a for a in sub); forb=3|(1<<c)|(1<<x)
        L=interior_sets(p,first,1,c,forb); R=interior_sets(p,tail^first,c,0,forb)
        ok+= any(not (S&T) for S in L for T in R)
    return ok,tot
for p,B,x in [(13,[1,2,4,6,7,8,11],5),(13,[1,2,3,5,6,7,8,9,11],10),(17,[1,4,8,12,13,14,16],5),(17,[1,2,4,6,7,9,11,13,15],10),(17,[1,3,6,7,8,9,11,12,14,15,16],13)]:
    print(p,B,x,"splits admitting an FV ordering:",exact(p,B,x))
