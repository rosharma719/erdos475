import itertools, cmath, pickle
import numpy as np
from math import gcd
import mpmath as mp
from cycle_orbits import Ba, coeffs
K=pickle.load(open('kappa_cache.pkl','rb'))
def fullB(n):
    mu=[cmath.exp(2j*cmath.pi*k/n) for k in range(n)]
    tot=np.zeros(n+1,dtype=complex); data=[]
    for perm in itertools.permutations(range(1,n)):
        a=[mu[k] for k in perm]+[1]
        B,v,rho,Q=Ba(a,n); tot+=np.array(coeffs(B,n)); data.append((a,v,B,Q))
    return tot,data
print("(1) confluent rank descent:")
for n in (3,4,5,6):
    up,_=fullB(n+1); low,data=fullB(n)
    rhs=np.zeros(n+2,dtype=complex); geoA=[]
    for a,v,B,Q in data:
        dQ=np.polyder(Q); A=sum(dQ(x) for x in v); Bm=sum(x*dQ(x) for x in v)
        poly=B*(np.poly1d([A,-A-Bm]))     # (z-1)A - B
        c=coeffs(poly,n+1); rhs[:len(c)]+=np.array(c)
    print(f"  n={n}: B_(n+1) = sum P_a((z-1)A_a - B_a): {np.allclose(rhs[:n+2],up[:n+2],atol=1e-6)}")
# (2) geometric moments
for n in (5,7):
    mu=[cmath.exp(2j*cmath.pi*k/n) for k in range(n)]
    for k in range(1,n):
        if gcd(k,n)!=1: continue
        q=mu[k]; a=[q**i for i in range(1,n)]+[1]
        B,v,rho,Q=Ba(a,n); dQ=np.polyder(Q)
        A=sum(dQ(x) for x in v); Bm=sum(x*dQ(x) for x in v)
        print(f"  geometric n={n} k={k}: A_a={abs(A):.1e}, B_a - n^2/(q-1)^n = {abs(Bm-n*n/(q-1)**n):.1e}")
# (4) stable specialization via limit eps->0
mp.mp.dps=60
def Bspec(m,t):
    r=len(t); S=sum(t); tot=[mp.mpc(0)]*(m+1)
    import itertools as it
    def sgn(p):
        s=1
        for i in range(len(p)):
            for j in range(i+1,len(p)):
                if p[i]>p[j]: s=-s
        return s
    Delta=mp.mpc(1)
    for i in range(r):
        for j in range(i+1,r): Delta*=(t[j]-t[i])
    for x in t: Delta*=x
    for p in it.permutations(range(r)):
        tt=[t[k] for k in p]; s=[sum(tt[:i+1]) for i in range(r)]
        c=mp.mpc(1)
        for x in s: c*=x
        for i in range(r):
            for j in range(i+1,r): c*=(s[j]-s[i])
        c*=sgn(p)
        poly=[S,mp.mpc(1)]     # ascending: z+S
        for si in s:
            new=[mp.mpc(0)]*(len(poly)+1)
            for d,co in enumerate(poly): new[d]+=co*(S-si); new[d+1]+=co
            poly=new
        for d,co in enumerate(poly): tot[d]+=co*c
    return [x/Delta for x in tot]
print("(8) deg(B_m - B_{m;n}) <= m-n:")
for m in (5,6,7):
    zeta=mp.exp(2j*mp.pi/m); full=Bspec(m,[zeta**i for i in range(1,m)])
    for n in range(m-1,max(2,m-3),-1):
        k=m-n; eta=mp.exp(2j*mp.pi/n); eps=mp.mpf('1e-25')
        t=[eta**i for i in range(1,n)]+[eps*(j+1)*mp.mpc(1,0.3*(j+1)) for j in range(k)]
        sp=Bspec(m,t)
        diff=[abs(a-b) for a,b in zip(full,sp)]
        top=max([d for d in range(len(diff)) if diff[d]>1e-10],default=-1)
        print(f"  m={m}, n={n} ({k} zero edges): highest degree where B_m and B_(m;n) differ = {top}  (bound m-n = {m-n})")
# (10) two-coefficient gcd
print("(10):")
for m in range(6,15):
    dm=m-1 if m%4 in (0,3) else m-2
    k=K[m]; g=gcd(abs(k[dm-1]),abs(k[dm-3]))
    import sympy
    print(f"  m={m}: indices {dm},{dm-2}: gcd {g} {dict(sympy.factorint(g))}  primes>m+1: {[p for p in sympy.factorint(g) if p>m+1]}")
