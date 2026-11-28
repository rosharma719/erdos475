import itertools, cmath
import numpy as np
from math import gcd
from cycle_orbits import Ba, coeffs
for m in (5,6,7):
    mu=[cmath.exp(2j*cmath.pi*k/m) for k in range(m)]
    def key(a): return tuple(round(cmath.phase(x)/(2*cmath.pi)*m)%m for x in a)
    seen=set(); orbits=[]
    for perm in itertools.permutations(range(1,m)):
        a=[mu[k] for k in perm]+[1]
        if key(a) in seen: continue
        orb=set()
        for i in range(m):
            b=a[i+1:]+a[:i+1]; b=[x/b[-1] for x in b]; orb.add(key(b))
        seen|=orb; orbits.append((a,orb))
    ok=True; rhosum=0
    for a,orb in orbits:
        h=m//len(orb)
        direct=np.poly1d([0])
        for kk in orb:
            b=[mu[k] for k in kk]; direct=direct+Ba(b,m)[0]
        B,v,rho,Q=Ba(a,m)
        formula=np.poly1d([0])
        for i in range(m): formula=formula+Q(np.poly1d([a[i],v[i]]))
        formula=formula*((-1)**(m-1)*m*rho/h)
        if not np.allclose(coeffs(direct,m),coeffs(formula,m),atol=1e-6): ok=False
        rhosum+=rho/h
    print(f"m={m}: {len(orbits)} orbits; orbit formula (2) holds for all: {ok}; sum rho/h = {abs(rhosum):.2e} (claim (5): 0)")
