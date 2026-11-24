def V(a,b): return set(range(-a,0))|set(range(2,b+1))
def ok(a,b,p): return p[0]==b and len(p)==a+b-1 and set(p)==V(a,b) and sorted(abs(p[i+1]-p[i]) for i in range(len(p)-1))==list(range(2,a+b))
def up(a):
    b=3*a+2;v=[b]
    for i in range(1,a): v+=[-a+i,b-i]
    for j in range(a): v+=[2+j,2*a+2-j]
    return v+[-a,a+2]
def low(b):
    a=3*b-4;v=[]
    for i in range(b-1): v+=[b-i,-(a-1-i)]
    for j in range(1,b-2): v+=[-j,-(2*b-3-j)]
    return v+[-(b-2),-a,-(b-1)]
print("upper ray failures a<2000:",sum(not ok(a,3*a+2,up(a)) for a in range(1,2000)))
print("lower ray failures b<2000:",sum(not ok(3*b-4,b,low(b)) for b in range(3,2000)))
# cone necessary condition vs exhaustive small cases
from functools import lru_cache
def exists(a,b):
    vals=sorted(V(a,b));n=len(vals);idx={v:i for i,v in enumerate(vals)};S=a+b
    @lru_cache(None)
    def go(x,uv,ue):
        if bin(uv).count('1')==n: return True
        for y in vals:
            d=abs(y-x)
            if 2<=d<S and not uv>>idx[y]&1 and not ue>>(d-2)&1 and go(y,uv|1<<idx[y],ue|1<<(d-2)): return True
        return False
    return go(b,1<<idx[b],0)
viol=[(a,b) for a in range(1,9) for b in range(2,14) if a+b<=15 and exists(a,b) and not (b<=3*a+2 and a<=3*b-4)]
print("cone violations among solvable (a+b<=15):",viol)
