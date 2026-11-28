import random, sys, time
from fractions import Fraction
from math import factorial, gcd, lcm
from functools import reduce
from deformed_ext import *
def Fs(c,m):
    r=F(c,m)
    assert set(r.keys())<={(0,0)}, r       # top coefficient is a scalar
    return r.get((0,0),Fraction(0))
def grad_formula(c,m):                     # (5): dF/dc_d = m * top( u_d v_d Z^{m-1} )
    Zp=Zpow(c,m,m-1); top=(1<<(2*m))-1; out=[]
    for d in range(1,m+1):
        prod=gw_mul(gw_mul(u(d,m),v(d,m)),Zp)
        r=prod.get(top,{}); assert set(r.keys())<={(0,0)}
        out.append(m*r.get((0,0),Fraction(0)))
    return out
def grad_fd(c,m):                          # exact derivative via interpolation of the degree-m polynomial in c_d
    out=[]
    for d in range(m):
        pts=[]
        for t in range(m+1):
            cc=c[:]; cc[d]=cc[d]+t; pts.append(Fs(cc,m))
        # derivative at t=0 of Lagrange interpolant through (t, pts[t])
        n=m; tot=Fraction(0)
        for j in range(n+1):
            if j==0: dl=sum(Fraction(1,0-k) for k in range(1,n+1))
            else:
                num=Fraction(1)
                for k in range(n+1):
                    if k!=j and k!=0: num*=(0-k)
                den=Fraction(1)
                for k in range(n+1):
                    if k!=j: den*=(j-k)
                dl=num/den
            tot+=pts[j]*dl
        out.append(tot)
    return out
random.seed(5)
for m in (3,4):
    c=[Fraction(random.randint(-4,4),random.randint(1,3)) for _ in range(m)]
    print(f"(5) m={m}: gradient formula == exact derivative: {grad_formula(c,m)==grad_fd(c,m)}")
# recursion (9)
for m in (3,4,5):
    c=[Fraction(random.randint(-4,4),random.randint(1,3)) for _ in range(m)]
    base=c[:m-1]
    ok=True
    L=Fs(base+[Fraction(0)],m); Fm1=Fs(base,m-1)
    for t in (Fraction(1,2),Fraction(-3),Fraction(7,5)):
        lhs=Fs(base+[t],m); rhs=L+(-1)**(m-1)*m*t*Fm1
        if lhs!=rhs: ok=False
    print(f"(9) m={m}: F_m = L_m + (-1)^(m-1) m c_m F_(m-1): {ok}")
# factorial point
print("--- factorial point c* = (1/k!):  F_m(c*), nonvanishing of Z^(m-1), gradient")
def pf(n):
    n=abs(int(n)); s={};d=2
    if n==0: return {0:1}
    while d*d<=n:
        while n%d==0: s[d]=s.get(d,0)+1; n//=d
        d+=1
    if n>1: s[n]=s.get(n,0)+1
    return s
rows={}
for m in range(2,int(sys.argv[1])+1 if len(sys.argv)>1 else 7):
    t0=time.time()
    cs=[Fraction(1,factorial(k)) for k in range(1,m+1)]
    Fv=Fs(cs,m); g=grad_formula(cs,m)
    den=reduce(lcm,[x.denominator for x in g],1); gi=[int(x*den) for x in g]; gg=reduce(gcd,[abs(x) for x in gi])
    prim=[x//gg for x in gi] if gg else gi
    rows[m]=(g,cs)
    print(f"m={m}: F_m(c*)={Fv};  grad F_m(c*) (scaled to primitive ints) = {prim}  content-denominator {den}, gcd {gg};  [{time.time()-t0:.1f}s]",flush=True)
