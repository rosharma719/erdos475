import itertools, cmath
import numpy as np
from math import comb, gcd
from geomorder import sgn
def contrib(m,p,t,S,Delta):
    r=m-1; tt=[t[x] for x in p]; s=list(itertools.accumulate(tt))
    c=np.prod(s)*np.prod([s[j]-s[i] for i in range(r) for j in range(i+1,r)])*sgn(p)
    poly=np.poly1d([1,S])
    for si in s: poly=poly*np.poly1d([1,S-si])
    return poly*(c/Delta)
for m in (4,5,6,7,8):
    r=m-1; zeta=cmath.exp(2j*cmath.pi/m); t=[zeta**i for i in range(1,m)]
    S=sum(t); Delta=np.prod([t[j]-t[i] for i in range(r) for j in range(i+1,r)])*np.prod(t)
    tot=np.poly1d([0]); geo=np.poly1d([0]); nonzero=0
    geoset=set(tuple((k*i)%m-1 for i in range(1,m)) for k in range(1,m) if gcd(k,m)==1)
    for p in itertools.permutations(range(r)):
        c=contrib(m,p,t,S,Delta)
        if max(abs(x) for x in c.c)>1e-9: nonzero+=1
        tot=tot+c
        if p in geoset: geo=geo+c
    print(f"m={m}: orderings with nonzero contribution {nonzero}/{len(list(itertools.permutations(range(r)))) if m<8 else 5040}; total B = {np.round(tot.c.real,6)}; geometric part = {np.round(geo.c.real,6)}; rest = {np.round((tot-geo).c.real,6)}")
