"""Theorem (3)/(4): Phi(theta) = (1+theta)^{p-1} f(lambda) + eps (1-theta)^{p-1} f(1/lambda),  lambda=(1-theta)/(1+theta),
f_{m,p}(lambda) = c_{C_lambda}(A), A = U^vee = {p-m-1..p-3}, eps = (-1)^{r+w}.  Compare with the Weyl-eigenvalue polynomial
Phi~(y) = sum_d d K(J_d,J_d) y^{d-1}, y=(theta-1)/2 : proportional?"""
import sys, io, contextlib, itertools
from fractions import Fraction
from duality_checks import cT
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def Clam(r,lam,p):
    C=[[0]*r for _ in range(r)]
    for i in range(r):
        C[i][i]=1
        if i<r-1: C[i][i+1]=p-1
    C[r-1][0]=lam%p
    return C
def run(m,p):
    r=m-1; U=tuple(range(2,m+1)); w=sum(U); A=tuple(range(p-m-1,p-2))
    assert len(A)==r
    eps=(-1)**(r+w)
    f={lam:cT(Clam(r,lam,p),A,p) for lam in range(p)}
    K=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
    rows=[]; ratios=set(); allzero=True
    for theta in range(p):
        if (1+theta)%p==0 or (1-theta)%p==0: continue
        lam=(1-theta)*pow(1+theta,-1,p)%p; linv=pow(lam,-1,p)
        Phi=(pow(1+theta,p-1,p)*f[lam]+eps*pow(1-theta,p-1,p)*f[linv])%p
        y=(theta-1)*pow(2,-1,p)%p
        Pt=sum(d*K[d-1]*pow(y,d-1,p) for d in range(1,m+1))%p
        rows.append((theta,Phi,Pt))
        if Phi or Pt: allzero=False
        if Pt: ratios.add(Phi*pow(Pt,-1,p)%p)
        elif Phi: ratios.add('Phi!=0,Pt=0')
    return eps,f,rows,ratios,allzero
for m,p in [(3,5),(3,7),(3,11),(4,7),(4,11)]:
    eps,f,rows,ratios,allzero=run(m,p)
    print(f"m={m}, p={p}: eps={eps}; f(lambda) for lambda=0..p-1: {[f[l] for l in range(p)]};  values (theta, Phi, Phi~): {rows};  ratios Phi/Phi~: {sorted(ratios,key=str)}  all zero: {allzero}",flush=True)
