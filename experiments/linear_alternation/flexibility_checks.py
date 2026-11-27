"""Schur-slice flexibility: E(S_X s_lambda) = [z^{q-1}]  W * s_mu(a,b,z),  mu = lambda', W = a+b+z; express in binary Schur basis."""
import itertools, math, sys
from fractions import Fraction
# 3-variable polynomials: dict {(i,j,k): coeff}, variables (a,b,z)
def pmul(p,q):
    o={}
    for e1,c1 in p.items():
        for e2,c2 in q.items():
            e=(e1[0]+e2[0],e1[1]+e2[1],e1[2]+e2[2]); o[e]=o.get(e,0)+c1*c2
    return {k:v for k,v in o.items() if v}
def padd(p,q,s=1):
    o=dict(p)
    for k,v in q.items(): o[k]=o.get(k,0)+s*v
    return {k:v for k,v in o.items() if v}
def hk(n):
    if n<0: return {}
    return {(i,j,n-i-j):1 for i in range(n+1) for j in range(n+1-i)}
def det3(M):
    n=len(M)
    if n==0: return {(0,0,0):1}
    if n==1: return M[0][0]
    out={}
    for j in range(n):
        minor=[row[:j]+row[j+1:] for row in M[1:]]
        term=pmul(M[0][j],det3(minor))
        out=padd(out,term,(-1)**j)
    return out
def schur3(mu):
    mu=[x for x in mu if x>0]; l=len(mu)
    if l>3: return {}
    return det3([[hk(mu[i]-i+j) for j in range(l)] for i in range(l)])
def binary_schur_basis(deg):
    """s_{(deg-j,j)}(a,b) as polys in (a,b,z) with z-exponent 0, j=0..deg//2"""
    out={}
    for j in range(deg//2+1):
        u=deg-j; # (ab)^j h_{u-j}(a,b)
        p={(j+i,j+(u-j-i),0):1 for i in range(u-j+1)}
        out[(u,j)]=p
    return out
def decompose(poly,deg):
    basis=binary_schur_basis(deg); res={}
    rem=dict(poly)
    # triangular: highest a-exponent first
    for (u,j) in sorted(basis.keys(),key=lambda t:-t[0]):
        lead=(u,deg-u,0)
        c=rem.get(lead,0)
        if c:
            res[(u,j)]=c; rem=padd(rem,{k:c*v for k,v in basis[(u,j)].items()},-1)
    assert not rem, f"not a combination of binary Schur functions: {rem}"
    return res
def extract(mu,q):
    s=schur3(mu); W={(1,0,0):1,(0,1,0):1,(0,0,1):1}
    prod=pmul(W,s)
    sl={(i,j,0):c for (i,j,k),c in prod.items() if k==q-1}
    return decompose(sl,q-1)
ok=True
for q in range(3,9):
    fam={}
    for r in range((q-1+1)//2,q-1):
        mu=(q-2,r,q-1-r); got=extract(mu,q)
        exp={(r,q-1-r):1}
        fam[mu]=got
        if got!=exp: ok=False; print("  mismatch",q,mu,got,exp)
    mu=(q-1,q-2,0); got=extract(mu,q); exp={(q-1,0):2,(q-2,1):2} if q>=3 else None
    fam[mu]=got
    if got!=exp: ok=False; print("  special mismatch",q,mu,got,exp)
    # span
    basis_keys=sorted({k for v in fam.values() for k in v})
    print(f"q={q}: extracted vectors {fam}   binary Schur basis size {(q-1)//2+1}")
print("all extraction formulas hold:",ok)
# explicit rank-6 example: R_6 = 28 s_(3) + 32 s_(2,1);  tilde G = G - 14 P_2 - 4 P_1  -> E = 28 s3 + 32 s21 - 14(2 s3 + 2 s21) - 4 s21 = 0
print("rank-6 correction arithmetic: s_(3) coefficient",28-14*2," s_(2,1) coefficient",32-14*2-4*1)
