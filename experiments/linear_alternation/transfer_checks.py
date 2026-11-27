"""Checks of the 2026-11-27/28 transfer report: Thm1 (insertion), Thm3 (centered power sums), Thm4 (Poincare transfer)."""
import itertools, random
from fractions import Fraction
from math import factorial
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def Q(u):                       # cyclic Vandermonde kernel, zero-sum edges u_0..u_{m-1}
    m=len(u); y=[0]
    for i in range(m-1): y.append(y[-1]+u[i])
    num=1
    for i in range(m):
        for j in range(i+1,m): num*=y[j]-y[i]
    den=1
    for v in u: den*=v
    assert num%den==0
    return num//den
def lam(f,n):                    # Alt(f)/Delta at points 1..n, f(vars) callable, deg f must be C(n,2)
    pt=list(range(1,n+1)); d=1
    for i in range(n):
        for j in range(i+1,n): d*=pt[j]-pt[i]
    tot=0
    for p in itertools.permutations(range(n)):
        tot+=sgn(p)*f(tuple(pt[k] for k in p))
    assert tot%d==0
    return tot//d
random.seed(7)
# Thm 1:  Q_{m+1}(h,x) = +-W_m(x)(h+x0) Q_m(h+x0,x1..)
for m in range(3,9):
    ok=True
    for _ in range(20):
        x=[random.randint(-9,9) or 1 for _ in range(m)]
        h=-sum(x)
        if h==0 or any(v==0 for v in x) or h+x[0]==0: continue
        W=1
        for j in range(2,m):
            W*=sum(x[:j])
        lhs=Q([h]+x); rhs=W*(h+x[0])*Q([h+x[0]]+x[1:])
        if lhs not in (rhs,-rhs): ok=False
    print("Thm1 m=",m,"ok" if ok else "FAIL")
# Thm 3: centered power sums p_k(x+h/m) = ((m+1)-(m+1)^k)/m^k h^k whenever p_j(x,h)=0 (zero-sum with all e_k=0) -> use roots of unity
import cmath
for m in range(3,7):
    z=[cmath.exp(2j*cmath.pi*k/(m+1)) for k in range(1,m+1)]; h=1.0+0j     # the m+1 roots with h=1 -> power sums vanish
    x=[cmath.exp(2j*cmath.pi*k/(m+1)) for k in range(1,m+1)]
    err=max(abs(sum((xi+h/m)**k for xi in x)-((m+1)-(m+1)**k)/m**k*h**k) for k in range(1,m+1))
    print("Thm3 m=",m,"max err",f"{err:.1e}")
# Thm 4: lambda_{m+1}(h^{m-r} G) = (-1)^r (m-r)!/m! lambda_m(E_r G), G deg N_m+r in x_0..x_{m-1}
def monos(m,deg):
    def rec(k,left):
        if k==1: yield (left,); return
        for a in range(left+1):
            for r in rec(k-1,left-a): yield (a,)+r
    return list(rec(m,deg))
def apply_Er(G,r,m):
    out={}
    for mon,c in G.items():
        for S in itertools.combinations(range(m),r):
            e=list(mon); coef=c; okk=True
            for i in S:
                if e[i]==0: okk=False;break
                coef*=e[i]; e[i]-=1
            if okk: out[tuple(e)]=out.get(tuple(e),0)+coef
    return out
def ev(P,pt):
    t=0
    for mon,c in P.items():
        v=c
        for a,b in zip(mon,pt): v*=b**a
        t+=v
    return t
for m in (3,4):
    N=m*(m-1)//2
    for r in range(0,m+1):
        ms=monos(m,N+r); G={mn:random.randint(-3,3) for mn in random.sample(ms,min(6,len(ms)))}
        lhs=lam(lambda v: v[m]**(m-r)*ev(G,v[:m]),m+1)
        rhs=Fraction((-1)**r*factorial(m-r),factorial(m))*lam(lambda v: ev(apply_Er(G,r,m),v),m)
        print(f"Thm4 m={m} r={r}: lhs={lhs} rhs={rhs}", "OK" if lhs==rhs else "MISMATCH")
