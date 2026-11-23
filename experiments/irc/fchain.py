"""Recursive construction for F(al,be,T) when al+be ≡ 1 (mod 3) at every level (base: small brute force).
Rule: zigzag be,-(al-1),be-1,...,-(al-r) (2r vertices), detour through -al, then the inner instance
[-(al-r-1), be-r]\{0,1}, entered at its bottom; reflect x->1-x to turn it into a top-start instance."""
import itertools,sys
sys.setrecursionlimit(10000)
from functools import lru_cache
@lru_cache(None)
def brute(al,be):
    V=set(range(-al,be+1))-{0,1}; L=set(range(2,al+be))
    if len(V)-1!=len(L): return None
    path=[be];used=set()
    def rec():
        if len(path)==len(V): return list(path)
        x=path[-1]
        for l in sorted(L-used,reverse=True):
            for y in (x+l,x-l):
                if y in V and y not in path:
                    path.append(y);used.add(l)
                    r=rec()
                    if r: return r
                    path.pop();used.discard(l)
        return None
    r=rec(); return tuple(r) if r else None
def T(al,be):
    s=al+be
    if s<=30:
        b=brute(al,be); return list(b) if b else None
    if (s-1)%3: return None
    r=(s-1)//3
    Z=[]
    for i in range(r): Z+= [be-i, -(al-1-i)]
    # Z ends at -(al-r); detour -al ; inner bottom start -(al-r-1)
    al2,be2=al-r-1,be-r
    # inner with bottom start: reflect y=1-x : [-al2,be2] -> [1-be2, 1+al2], i.e. F(be2-1, al2+1) top start
    sub=T(be2-1,al2+1)
    if sub is None: return None
    inner=[1-y for y in sub]       # starts at 1-(al2+1) = -al2 ✓
    return Z+[-al]+inner
def check(al,be,p):
    V=set(range(-al,be+1))-{0,1}
    return p is not None and p[0]==be and set(p)==V and len(p)==len(V) and sorted(abs(p[i+1]-p[i]) for i in range(len(p)-1))==list(range(2,al+be))
for k in [1,4,6,19,60,181,546]:
    p=T(k+1,k+1); print("k",k,"H_k via chain:",check(k+1,k+1,p))
