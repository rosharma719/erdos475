import itertools, sys, mpmath as mp
from math import gcd
from functools import reduce
import sympy
mp.mp.dps=80
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def f(x,m):   # residual cycle polynomial, x indexed 1..m
    r=mp.mpc(1)
    for i in range(2,m+1):
        for j in range(i+1,m+1):
            if (i,j)==(2,m): continue
            r*=sum(x[k] for k in range(i,j+1))
    return r
def P_value(m,a,b,u,v):
    N=m-2
    coeffs=[sum(u**k*v**(j-k) for k in range(j+1)) for j in range(N+1)]   # x^{N-j} coefficient h_j
    ys=mp.polyroots(coeffs,maxsteps=400,extraprec=400)
    D=mp.mpc(1)
    for i in range(N):
        for j in range(i+1,N): D*=(ys[j]-ys[i])
    tot=mp.mpc(0)
    others=[k for k in range(1,m+1) if k not in (a,b)]
    perms=[(p,sgn(p)) for p in itertools.permutations(range(N))]
    for p,s in perms:
        x={a:u,b:v}
        for idx,k in enumerate(others): x[k]=ys[p[idx]]
        tot+=s*f(x,m)
    return tot/D
m=int(sys.argv[1]); d=m-3
allc=[]; res={}
for a,b in itertools.combinations(range(1,m+1),2):
    # interpolate homogeneous deg d: P(1,v) at d+1 points v
    pts=[mp.mpf(k+2)/7 for k in range(d+1)]
    vals=[P_value(m,a,b,mp.mpf(1),v) for v in pts]
    A=mp.matrix([[v**j for j in range(d+1)] for v in pts])
    c=mp.lu_solve(A,mp.matrix([mp.re(x) for x in vals]))
    ints=[int(mp.nint(c[j])) for j in range(d+1)]
    err=max(abs(c[j]-ints[j]) for j in range(d+1))
    res[(a,b)]=ints; allc+=ints
    print(f"m={m} (a,b)=({a},{b}): coeffs of v^j: {ints}  (max nonint err {mp.nstr(err,3)})",flush=True)
g=reduce(gcd,[abs(x) for x in allc],0)
print(f"m={m}: joint content of all binary certificates = {g} {sympy.factorint(g) if g else ''}")
