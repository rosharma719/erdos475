import itertools, cmath
import numpy as np
from math import comb
from cycle_orbits import Ba, coeffs
def hasse(Q,k):
    d=Q
    for _ in range(k): d=np.polyder(d)
    return d/np.prod(range(1,k+1)) if k>0 else d
for m in (4,5,6,7):
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
    ok6=True; nstab=0; total=np.zeros(m+1,dtype=complex); mom=np.zeros(m+1,dtype=complex)
    for a,orb in orbits:
        h=m//len(orb); B,v,rho,Q=Ba(a,m)
        orbsum=np.poly1d([0])
        for i in range(m): orbsum=orbsum+Q(np.poly1d([a[i],v[i]]))
        total+=np.array(coeffs(orbsum*((-1)**(m-1)*m*rho/h),m))
        for k in range(m+1):
            mom[k]+=(-1)**(m-1)*m*rho/h*sum(a[i]**k*hasse(Q,k)(v[i]) for i in range(m))
        if h>1:
            nstab+=1; l=m//h
            lam=a[l]/a[0]; c=v[l]/(1-lam)
            # (6): Q(c+x) = prod_{j<l} (x^h - (v_j-c)^h)
            lhs=Q(np.poly1d([1,c])); rhs=np.poly1d([1])
            for j in range(l): rhs=rhs*(np.poly1d([1]+[0]*h)-np.poly1d([(v[j]-c)**h]))
            if not np.allclose(coeffs(lhs,m),coeffs(rhs,m),atol=1e-8): ok6=False
    print(f"m={m}: orbits with nontrivial stabilizer: {nstab}; block factorization (6) holds: {ok6}; moment identity (8) matches orbit sum: {np.allclose(total,mom,atol=1e-6)}")
