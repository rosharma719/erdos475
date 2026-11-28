import itertools, io, contextlib, sys
from fractions import Fraction
from math import comb, factorial
# ---------- (1) H(t) = G(-t) = sum_h W(h) t^h = sum_d d kappa_d t^{d-1} (1-t)^{p-d}  (mod p)
src=open('sparse_theorem_check.py').read()
exec(src[:src.index("for m,p in [(3,5)")])      # gives run(m,p), kappa, ...
def polypow_mod(base,e,p):
    out=[1]
    for _ in range(e):
        new=[0]*(len(out)+len(base)-1)
        for i,a in enumerate(out):
            for j,b in enumerate(base): new[i+j]=(new[i+j]+a*b)%p
        out=new
    return out
for k in range(0,0): pass
# identity sum_{h<p} C(h,k) t^h = t^k (1-t)^{p-1-k} mod p
okid=True
for p in (5,7,11,13):
    for k in range(0,p):
        lhs=[comb(h,k)%p for h in range(p)]
        rhs=[0]*k+polypow_mod([1,p-1],p-1-k,p)
        rhs=(rhs+[0]*p)[:p]
        if lhs!=rhs[:p]: okid=False
print("(1a) sum_{h<p} C(h,k) t^h = t^k (1-t)^(p-1-k) mod p for p=5,7,11,13, all k:",okid)
for m,p in [(3,7),(4,11),(4,13),(5,7)]:
    eps,f,rows,ratios,allzero=run(m,p)
    K=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
    bad=0; cnt=0
    for t in range(p):
        if t==0: continue                      # lam=-t != 0
        lam=(-t)%p; linv=pow(lam,-1,p)
        G=(f[lam]+eps*f[linv])%p               # lam^{p-1}=1
        H=sum(d*K[d-1]*pow(t,d-1,p)*pow((1-t)%p,p-d,p) for d in range(1,m+1))%p
        cnt+=1
        if G!=H: bad+=1
    print(f"(1) m={m}, p={p}: G(-t) = sum_d d kappa_d t^(d-1)(1-t)^(p-d) at {cnt} nonzero t in F_p: mismatches {bad}")
# ---------- (2) image of (g2,g3) -> (1-t^2) g2 + (1-t^3) g3 equals {H in P_N^eps : H(1)=0}
def recip_basis(n,eta):
    """basis of {q: deg<=n, q(t)=eta t^n q(1/t)} as coefficient lists"""
    B=[]
    for k in range(n//2+1):
        v=[0]*(n+1); 
        if k==n-k:
            if eta==1: v[k]=1; B.append(v)
        else:
            v[k]=1; v[n-k]=eta; B.append(v)
    return B
def rank_Q(rows):
    A=[[Fraction(x) for x in r] for r in rows if any(r)]
    rk=0; ncol=len(A[0]) if A else 0
    for c in range(ncol):
        piv=next((i for i in range(rk,len(A)) if A[i][c]!=0),None)
        if piv is None: continue
        A[rk],A[piv]=A[piv],A[rk]
        for i in range(len(A)):
            if i!=rk and A[i][c]!=0:
                f_=A[i][c]/A[rk][c]; A[i]=[a-f_*b for a,b in zip(A[i],A[rk])]
        rk+=1
    return rk
def mul(g,poly,N):
    out=[0]*(N+1)
    for i,c in enumerate(g):
        for j,d in enumerate(poly):
            if i+j<=N: out[i+j]+=c*d
    return out
ok2=True
for N in range(4,15):
    for eps in (1,-1):
        imgs=[]
        for g2 in recip_basis(N-2,-eps): imgs.append(mul(g2,[1,0,-1],N))
        for g3 in recip_basis(N-3,-eps): imgs.append(mul(g3,[1,0,0,-1],N))
        r=rank_Q(imgs)
        dimP=len(recip_basis(N,eps)); target=dimP-(1 if eps==1 else 0)      # H(1)=0 is automatic for eps=-1
        if r!=target: ok2=False; print("  N",N,"eps",eps,"rank",r,"target",target)
print("(2) image of (g2,g3) -> (1-t^2)g2+(1-t^3)g3 has dimension dim{H in P_N^eps: H(1)=0}  for N=4..14, eps=+-1:",ok2)
# kernel: g2=(1+t+t^2)q, g3=-(1+t)q
kerok=True
for N in range(5,12):
    for eps in (1,-1):
        # q with deg<=N-4 such that g2,g3 land in required reciprocal spaces: test existence of nonzero kernel dimension
        dim_src=len(recip_basis(N-2,-eps))+len(recip_basis(N-3,-eps)); dim_img=len(recip_basis(N,eps))-(1 if eps==1 else 0)
        # kernel dimension = dim_src - rank
        imgs=[mul(g2,[1,0,-1],N) for g2 in recip_basis(N-2,-eps)]+[mul(g3,[1,0,0,-1],N) for g3 in recip_basis(N-3,-eps)]
        kdim=dim_src-rank_Q(imgs)
        # explicit kernel family: q reciprocal of suitable type with deg <= N-4
        # (1-t^2)(1+t+t^2)q - (1-t^3)(1+t)q = 0 identically
        a=mul([1,1,1],[1,0,-1],N); b=mul([1,1],[1,0,0,-1],N)
        if any(x!=y for x,y in zip(a,b)): kerok=False
print("(2b) (1-t^2)(1+t+t^2) = (1-t^3)(1+t) (so the stated kernel family lies in the kernel):",kerok)
