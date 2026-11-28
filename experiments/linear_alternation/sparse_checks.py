import itertools, sys, io, contextlib
from fractions import Fraction
from math import comb, gcd, factorial
from functools import reduce
# ---- (a) sparse inverse of B_theta
def matinv(M):
    n=len(M); A=[[Fraction(x) for x in r]+[Fraction(int(i==j)) for j in range(n)] for i,r in enumerate(M)]
    for c in range(n):
        piv=next(r for r in range(c,n) if A[r][c]!=0); A[c],A[piv]=A[piv],A[c]
        A[c]=[v/A[c][c] for v in A[c]]
        for r in range(n):
            if r!=c and A[r][c]!=0:
                f=A[r][c]; A[r]=[a-f*b for a,b in zip(A[r],A[c])]
    return [r[n:] for r in A]
def detF(M):
    n=len(M); A=[[Fraction(x) for x in r] for r in M]; d=Fraction(1)
    for c in range(n):
        piv=next((r for r in range(c,n) if A[r][c]!=0),None)
        if piv is None: return Fraction(0)
        if piv!=c: A[c],A[piv]=A[piv],A[c]; d=-d
        d*=A[c][c]
        for r in range(c+1,n):
            f=A[r][c]/A[c][c]
            for k in range(c,n): A[r][k]-=f*A[c][k]
    return d
ok=True
for r in range(2,8):
    for theta in (Fraction(0),Fraction(1,3),Fraction(2),Fraction(-1,2),Fraction(5,7)):
        B=[[ (1 if i<=j else -1)+theta for j in range(r)] for i in range(r)]
        lam=(1-theta)/(1+theta)
        C=[[Fraction(0)]*r for _ in range(r)]
        for i in range(r):
            C[i][i]=Fraction(1)
            if i<r-1: C[i][i+1]=Fraction(-1)
        C[r-1][0]=lam
        inv=matinv(B)
        if any(inv[i][j]!=C[i][j]/2 for i in range(r) for j in range(r)): ok=False
        if detF(B)!=Fraction(2)**(r-1)*(1+theta): ok=False
print("(a) B_theta^{-1} = C_lambda/2 and det B_theta = 2^{r-1}(1+theta), r=2..7, five theta values:",ok)
# ---- (b),(d): centered polynomial of the eigenvalue W_m(h) = sum_d d C(h,d-1) K(J_d,J_d)
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def pf(n):
    s={};d=2
    while d*d<=n:
        while n%d==0: s[d]=s.get(d,0)+1; n//=d
        d+=1
    if n>1: s[n]=s.get(n,0)+1
    return s
def polymul(p,q):
    o=[Fraction(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q): o[i+j]+=a*b
    return o
def binom_poly(k):                    # C(h,k) as polynomial in h
    p=[Fraction(1)]
    for i in range(k): p=polymul(p,[Fraction(-i,1),Fraction(1)])
    return [c/factorial(k) for c in p]
def subs_lin(p,a,b):                  # p(a*y+b)
    out=[Fraction(0)]*len(p); 
    base=[Fraction(1)]
    for k,c in enumerate(p):
        term=[c*x for x in base]
        for i,x in enumerate(term): out[i]+=x
        base=polymul(base,[Fraction(b),Fraction(a)])
        if len(base)>len(out): out+= [Fraction(0)]*(len(base)-len(out))
    return out
for m in range(3,12):
    K=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
    W=[Fraction(0)]*m
    for d in range(1,m+1):
        bp=binom_poly(d-1)
        for i,c in enumerate(bp): W[i]+=d*K[d-1]*c
    # W(-h-1) as polynomial: substitute h -> -h-1
    Wm=subs_lin(W,-1,-1)
    Wm+= [Fraction(0)]*(len(W)-len(Wm))
    rel=None
    if all(Wm[i]==W[i] for i in range(len(W))): rel=+1
    elif all(Wm[i]==-W[i] for i in range(len(W))): rel=-1
    # centered variable z=2h+1: h=(z-1)/2
    Wz=subs_lin(W,Fraction(1,2),Fraction(-1,2))
    nz=[(i,c) for i,c in enumerate(Wz) if c!=0]
    top2=nz[-2:] if len(nz)>=2 else nz
    # clear denominators of the top two nonzero coefficients
    from math import lcm
    den=1
    for i,c in top2: den=lcm(den,c.denominator)
    ints=[int(c*den) for i,c in top2]
    g2=reduce(gcd,[abs(x) for x in ints]) if ints else 0
    lead=abs(ints[-1]) if ints else 0
    print(f"m={m}: W_m(-h-1)=({rel})W_m(h);  deg W_m = {len(nz) and nz[-1][0]};  nonzero z-powers {[i for i,c in nz]};  top-two coefficient gcd (cleared) = {g2} -> primes>m+1: {[q for q in pf(g2) if q>m+1] if g2 else '-'};  leading coeff primes>m+1: {[q for q in pf(lead) if q>m+1] if lead else '-'}")
