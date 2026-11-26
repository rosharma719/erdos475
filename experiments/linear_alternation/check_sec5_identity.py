"""Check  lambda_{m+1}(t^{m-d} W G_{m+1}) = -K_m(W)  (report sec.5), W random monomials of degree d<=m.
LHS: exact, Alt_{n}(f)(x)/Delta_n(x) at x=1..n, n=m+1 (deg f = N_n). t = x_n.
RHS: Alt_m(W F_m)(r)/Delta_m(r) at r=(zeta^1..zeta^m), zeta primitive (m+1)-th root of 1 (complex floats)."""
import itertools, random, cmath, sys
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def Fm(a):                       # all intervals length>=2 except full
    m=len(a); f=1
    for i in range(m):
        s=a[i]
        for j in range(i+1,m):
            s=s+a[j]
            if i==0 and j==m-1: continue
            f*=s
    return f
def Wval(mon,a):
    v=1
    for k,e in enumerate(mon): v*=a[k]**e
    return v
def delta(x):
    d=1
    for i in range(len(x)):
        for j in range(i+1,len(x)): d*=x[j]-x[i]
    return d
def lam_cyclic(m,mon,d):
    n=m+1; x=list(range(1,n+1)); tot=0
    for p in itertools.permutations(range(n)):
        a=[x[k] for k in p]; t=a[-1]; tail=a[:-1]
        G=sum(tail)*Fm(tail)
        tot+=sgn(p)*t**(m-d)*Wval(mon,tail)*G
    assert tot%delta(x)==0
    return tot//delta(x)
def K(m,mon):
    z=cmath.exp(2j*cmath.pi/(m+1)); r=[z**k for k in range(1,m+1)]; tot=0
    for p in itertools.permutations(range(m)):
        a=[r[k] for k in p]; tot+=sgn(p)*Wval(mon,a)*Fm(a)
    return tot/delta(r)
random.seed(1)
for m in (3,4,5):
    for _ in range(6):
        d=random.randint(1,m); mon=[0]*m
        for _ in range(d): mon[random.randrange(m)]+=1
        L=lam_cyclic(m,mon,d); R=-K(m,mon)
        print(f"m={m} mon={mon} lhs={L} rhs={R.real:.4f}{R.imag:+.1e}j", "OK" if abs(L-R)<1e-6*max(1,abs(L)) else "MISMATCH")
