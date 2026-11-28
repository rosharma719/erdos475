import itertools, cmath
import numpy as np
from math import comb, gcd
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
for m in (5,7):
    r=m-1; zeta=cmath.exp(2j*cmath.pi/m); t=[zeta**i for i in range(1,m)]
    S=sum(t); Delta=np.prod([t[j]-t[i] for i in range(r) for j in range(i+1,r)])*np.prod(t)
    for k in range(1,m):
        if gcd(k,m)!=1: continue
        # ordering: t-indices (k*i mod m)-1 for i=1..r
        p=[(k*i)%m-1 for i in range(1,m)]
        tt=[t[x] for x in p]; s=list(itertools.accumulate(tt))
        c=np.prod(s)*np.prod([s[j]-s[i] for i in range(r) for j in range(i+1,r)])*sgn(p)
        poly=np.poly1d([1,S])
        for si in s: poly=poly*np.poly1d([1,S-si])
        contrib=poly*(c/Delta)
        q=zeta**k
        for T in (comb(m,2),comb(m-1,2),comb(m+1,2)):
            pred=(np.poly1d([1-q,-1])**m - np.poly1d([(-1)**m]))*(m*(-1)**comb(m-1,2)/(1-q)**T)
            diff=max(abs(x) for x in (contrib-pred).c) if True else None
            print(f"m={m} k={k} T={T}: |contribution - formula (3)| = {diff:.2e}")
