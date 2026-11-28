"""Schur endpoint pairing E_{m,d,mu} = lambda_m(w_1^d Q_m s_mu(y_1..y_{m-1})) vs kappa(I, J_d); merge vector and compressed matrix."""
import itertools, io, contextlib, math, sys
from fractions import Fraction
from math import comb, factorial, gcd
from functools import reduce
with contextlib.redirect_stdout(io.StringIO()):
    import pascal_checks as PC
    import witt_checks as WC
kappa=PC.kappa; parts=PC.parts
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def Fint(a):
    m=len(a); f=1
    for i in range(m):
        s=a[i]
        for j in range(i+1,m):
            s+=a[j]
            if i==0 and j==m-1: continue
            f*=s
    return f
def partitions(n,maxparts,maxpart=None):
    if maxpart is None: maxpart=n
    if n==0: yield (); return
    if maxparts==0: return
    for a in range(min(n,maxpart),0,-1):
        for rest in partitions(n-a,maxparts-1,a): yield (a,)+rest
def hlist(vals,kmax):
    h=[1]+[0]*kmax
    for k in range(1,kmax+1):
        # h_k via generating function product 1/(1-v t)
        pass
    # compute via DP over variables
    h=[1]+[0]*kmax
    for v in vals:
        for k in range(1,kmax+1): h[k]+=v*h[k-1]
    return h
def det(M):
    n=len(M)
    if n==0: return 1
    # fraction-free Bareiss
    A=[[Fraction(x) for x in r] for r in M]; sgn_=1; d=Fraction(1)
    for c in range(n):
        piv=next((r for r in range(c,n) if A[r][c]!=0),None)
        if piv is None: return 0
        if piv!=c: A[c],A[piv]=A[piv],A[c]; sgn_=-sgn_
        d*=A[c][c]
        for r in range(c+1,n):
            f=A[r][c]/A[c][c]
            for k in range(c,n): A[r][k]-=f*A[c][k]
    return sgn_*d
def schur(mu,vals):
    l=len(mu); 
    if l==0: return 1
    h=hlist(vals,sum(mu)+l)
    H=lambda k: h[k] if 0<=k<len(h) else 0
    return det([[H(mu[i]-i+j) for j in range(l)] for i in range(l)])
def E_all(m):
    """E_{m,d,mu} for d=1..m, mu partitions of m-d with <= m-1 parts, via alternation over all perms"""
    pt=list(range(1,m+1)); dlt=1
    for i in range(m):
        for j in range(i+1,m): dlt*=pt[j]-pt[i]
    tests=[(d,mu) for d in range(1,m+1) for mu in partitions(m-d,m-1)]
    tot=[0]*len(tests)
    for p in itertools.permutations(range(m)):
        s=sgn(p); w=[pt[k] for k in p]; Q=Fint(w[:m-1]) if m>=3 else 1
        y=[]; acc=0
        for k in range(m-1): acc+=w[k]; y.append(acc)
        base=s*Q
        cache={}
        for idx,(d,mu) in enumerate(tests):
            key=mu
            if key not in cache: cache[key]=schur(mu,y)
            tot[idx]+=base*w[0]**d*cache[key]
    out={}
    for (d,mu),t in zip(tests,tot):
        assert t%dlt==0; out[(d,mu)]=t//dlt
    return out
def Iset(mu,m):
    mu=list(mu)+[0]*(m-1-len(mu))        # mu_1>=...>=mu_{m-1}
    return tuple(j+mu[m-1-j] for j in range(1,m))     # i_j = j + mu_{m-j}
# (1) E vs kappa(I,J_d)
for m in range(3,7):
    E=E_all(m); bad=0; signs=set()
    for (d,mu),val in E.items():
        I=Iset(mu,m); J=tuple(x for x in range(1,m+1) if x!=d)
        kv=kappa(I,J) if sum(I)==sum(J) else 0
        if val==0 and kv==0: continue
        if val==kv: signs.add(1)
        elif val==-kv: signs.add(-1)
        else: bad+=1
    print(f"(1) m={m}: {len(E)} Schur tests E_(m,d,mu); equal to +-kappa(I,J_d): mismatches {bad}; sign pattern {sorted(signs)}  [(-1)^(C(m+1,2)-1) = {(-1)**(comb(m+1,2)-1)}]")
    g1=reduce(gcd,[abs(v) for (d,mu),v in E.items() if d==1]); gall=reduce(gcd,[abs(v) for v in E.values()])
    print(f"    d=1 endpoint Schur packet gcd = {g1} ({sum(1 for (d,mu) in E if d==1)} tests);  combined over all d, mu: gcd = {gall}")
