import itertools, io, contextlib, math, random, sys, time
from fractions import Fraction
from math import comb, gcd, factorial
from functools import lru_cache, reduce
sys.setrecursionlimit(10000)
def Cb(n,k): return comb(n,k) if 0<=k<=n else 0
def T(i,a,h):
    hn=h+i-a
    if hn<0: return 0
    return Cb(h+i,i)-Cb(hn,i)
@lru_cache(None)
def F(A,I):
    k=len(A)
    if k==0: return 1
    h=sum(I)-sum(A)
    if h<0: return 0
    tot=0
    for x,i in enumerate(I):
        for y,a in enumerate(A):
            hp=h-i+a
            if hp<0: continue
            tt=T(i,a,hp)
            if tt: tot+=(-1)**(x+y)*tt*F(A[:y]+A[y+1:],I[:x]+I[x+1:])
    return tot
kappa=F
# --- Schur functions
def hlist(vals,kmax):
    h=[1]+[0]*kmax
    for v in vals:
        for k in range(1,kmax+1): h[k]+=v*h[k-1]
    return h
def detF(M):
    n=len(M)
    if n==0: return Fraction(1)
    A=[[Fraction(x) for x in r] for r in M]; sg=1; d=Fraction(1)
    for c in range(n):
        piv=next((r for r in range(c,n) if A[r][c]!=0),None)
        if piv is None: return Fraction(0)
        if piv!=c: A[c],A[piv]=A[piv],A[c]; sg=-sg
        d*=A[c][c]
        for r in range(c+1,n):
            f=A[r][c]/A[c][c]
            for k in range(c,n): A[r][k]-=f*A[c][k]
    return sg*d
def schur(mu,vals):
    l=len(mu)
    if l==0: return Fraction(1)
    h=hlist(vals,sum(mu)+l); H=lambda k: h[k] if 0<=k<len(h) else 0
    return detF([[H(mu[i]-i+j) for j in range(l)] for i in range(l)])
def lam_of(A):
    k=len(A); return tuple(A[k-j]-(k-j+1) for j in range(1,k+1))     # lambda_j = a_{k+1-j}-(k+1-j)
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def vand(pts):
    d=Fraction(1)
    for a in range(len(pts)):
        for b in range(a+1,len(pts)): d*=pts[b]-pts[a]
    return d
def Phi(t,x):
    k=len(x); tot=Fraction(0)
    for p in itertools.permutations(range(k)):
        s=0; pts=[Fraction(0)]
        for i in p: s+=x[i]; pts.append(s)
        pts.append(Fraction(t)); tot+=sgn(p)*vand(pts)
    return tot
# (1) Schur expansion of P_k = Phi/(Delta(x) prod x)
random.seed(11)
for m in (3,4,5,6):
    k=m-1; ok=True; signs=set()
    for _ in range(3):
        x=[Fraction(v) for v in random.sample(range(1,15),k)]; t=Fraction(random.randint(15,40))
        den=vand(x)
        for v in x: den*=v
        Pk=Phi(t,x)/den
        rhs=Fraction(0)
        for d in range(1,m+1):
            J=tuple(c for c in range(1,m+1) if c!=d)
            # all increasing sets A of size k with sum A = sum J
            for A in itertools.combinations(range(1,m+k+3),k):
                if sum(A)!=sum(J): continue
                kv=kappa(J,A)
                if kv==0: continue
                rhs+=(-1)**(m+d)*t**d*kv*schur(lam_of(A),x)
        if Pk==rhs: signs.add(1)
        elif Pk==-rhs: signs.add(-1)
        else: ok=False
    print(f"(1) m={m}: P_k(t;x) = sum_d (-1)^(m+d) t^d sum_A kappa(J_d,A) s_lambda(A)(x): consistent {ok}, global sign {sorted(signs)}")
# (2) two-root coefficients q_{m,d,r}
def q(m,d,r):
    J=tuple(c for c in range(1,m+1) if c!=d); A=tuple(c for c in range(1,m+2) if c not in (r,m+1+d-r))
    return kappa(J,A)
print("(2) packet size floor((m+1)^2/4) vs counted number of (d,r):",all(sum(1 for d in range(1,m+1) for r in range(d,(m+d)//2+1))==(m+1)**2//4 for m in range(3,16)))
for m in range(3,9):
    qs=[q(m,1,r) for r in range(1,(m+1)//2+1)]
    if m%2==1: rel=sum((-1)**(r-1)*qs[r-1] for r in range(1,len(qs)+1))
    else: rel=sum((-1)**(r-1)*(m+2-2*r)*qs[r-1] for r in range(1,len(qs)+1))
    print(f"    m={m}: q_(m,1,r) = {qs};  projected merge relation sum = {rel}")
