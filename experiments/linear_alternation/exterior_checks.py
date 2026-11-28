import itertools, io, contextlib, math, random, sys, time
from fractions import Fraction
from math import comb, factorial, gcd
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])      # F (=kappa), T, Cb, vand, Phi ...
# ---------- exterior algebra on e_0..e_N (basis = sorted tuples)
def E_vec(vec,N,mod=None):
    out={}
    for B,c in vec.items():
        for j,b in enumerate(B):
            nb=b+1
            if nb>N: continue
            if j+1<len(B) and B[j+1]==nb: continue
            NB=B[:j]+(nb,)+B[j+1:]
            out[NB]=out.get(NB,0)+c
    if mod: out={k:v%mod for k,v in out.items() if v%mod}
    return {k:v for k,v in out.items() if v}
def Epow(vec,k,N,mod=None):
    for _ in range(k): vec=E_vec(vec,N,mod)
    return vec
def wedge_e(i,vec,mod=None):
    out={}
    for B,c in vec.items():
        if i in B: continue
        pos=sum(1 for b in B if b<i)
        NB=tuple(sorted(B+(i,)))
        out[NB]=out.get(NB,0)+(-1)**pos*c
    if mod: out={k:v%mod for k,v in out.items() if v%mod}
    return {k:v for k,v in out.items() if v}
def vadd(a,b,s=1,mod=None):
    out=dict(a)
    for k,v in b.items(): out[k]=out.get(k,0)+s*v
    if mod: return {k:v%mod for k,v in out.items() if v%mod}
    return {k:v for k,v in out.items() if v}
# ---------- (B) rank-descent identity (1):  K_U = +- sum_a (-1)^a E^a (e_0 ^ K_{U\a})
def parts_dist(n,k,minv=1):
    def rec(n,k,minv):
        if k==0:
            if n==0: yield ()
            return
        if k==1:
            if n>=minv: yield (n,)
            return
        a=minv
        while a*k+k*(k-1)//2<=n:
            for rest in rec(n-a,k-1,a+1): yield (a,)+rest
            a+=1
    yield from rec(n,k,minv)
def Krow(A):
    """K_A = sum_B kappa(A,B) e_B over positive increasing B of size |A| with sum A"""
    return {B:F(A,B) for B in parts_dist(sum(A),len(A)) if F(A,B)}
for m in (4,5,6):
    U=tuple(range(2,m+1)); r=m-1; NN=10**6
    KU=Krow(U); rhs={}
    for a in U:
        Ka=Krow(tuple(x for x in U if x!=a))
        rhs=vadd(rhs,Epow(wedge_e(0,Ka),a,NN),(-1)**a)
    # compare: positive part and e_0 part
    pos={k:v for k,v in rhs.items() if 0 not in k}; zero={k:v for k,v in rhs.items() if 0 in k}
    same=(pos==KU); neg=(pos=={k:-v for k,v in KU.items()})
    print(f"(1) m={m}: e_0-components of RHS vanish: {not zero};  positive part equals K_U: {same}, equals -K_U: {neg}")

# ---------- (C),(D): surjectivity (T_2+T_3) and coupled image (T~_2+T~_3) in the truncated exterior space, over F_p
from modrank import rank_mod
import modrank
def subsets_weight(n_idx,size,weight):
    out=[]
    def rec(start,left,sz,cur):
        if sz==0:
            if left==0: out.append(tuple(cur))
            return
        for a in range(start,n_idx+1):
            if a*sz>left+ (sz*(sz-1))//2*0 and False: break
            if a>left: break
            cur.append(a); rec(a+1,left-a,sz-1,cur); cur.pop()
    rec(0,weight,size,[])
    return out
def rank_p(rows,p):
    piv={}; rk=0
    for r in rows:
        r={k:v%p for k,v in r.items() if v%p}
        while r:
            k=min(r)
            if k in piv:
                f=r[k]
                for kk,vv in piv[k].items(): r[kk]=(r.get(kk,0)-f*vv)%p
                r={a:b for a,b in r.items() if b}
            else:
                inv=pow(r[k],p-2,p); piv[k]={a:b*inv%p for a,b in r.items()}; rk+=1; break
    return rk
def ranks(m,p):
    N=m+1; w=sum(range(2,m+1))
    target=subsets_weight(N,m-1,w)
    src5=subsets_weight(N,m-2,w-5); src6=subsets_weight(N,m-2,w-6)
    def T2(v): return Epow(wedge_e(0,Epow(v,3,N,p),p),2,N,p)
    def T3(v): return Epow(wedge_e(0,Epow(v,2,N,p),p),3,N,p) if True else None
    def Tt2(v): return Epow(wedge_e(1,Epow(v,2,N,p),p),2,N,p)
    def Tt3(v): return Epow(wedge_e(0,Epow(v,3,N,p),p),3,N,p)
    indep=[]; coup=[]
    for B in src5:
        v={B:1}; indep+=[T2(v),T3(v)]; coup.append(Tt2(v))
    for B in src6:
        v={B:1}; coup.append(Tt3(v))
    pos=[{k:v for k,v in r.items() if 0 not in k} for r in indep]
    return len(target),rank_p(indep,p),rank_p(coup,p),sum(1 for B in target if 0 not in B)
print("(C),(D): (m, p) -> [dim of weight-w part of Lambda^{m-1}V,  rank of T2+T3,  rank of coupled T~2+T~3]; report table: (5,7):4,4,3 (7,11):7,7,7 (9,11):10,10,9 (10,13):12,12,12 (11,13):14,14,13 (14,17):21,21,21 (15,17):24,24,23 (17,19):30,30,29 (17,23):30,30,30")
for m,p in [(5,7),(7,11),(9,11),(10,13),(11,13),(14,17),(15,17)]:
    t0=time.time(); d,ri,rc,dpos=ranks(m,p)
    print(f"  (m={m}, p={p}): dim {d}, rank(T2+T3) = {ri}, rank(coupled) = {rc}   (p = m+2: {p==m+2})   ({time.time()-t0:.1f}s)",flush=True)

print("--- variant: sources restricted to positive exponents (no e_0), as for genuine determinant rows")
def ranks_pos(m,p):
    N=m+1; w=sum(range(2,m+1))
    target=subsets_weight(N,m-1,w)
    src5=[B for B in subsets_weight(N,m-2,w-5) if 0 not in B]; src6=[B for B in subsets_weight(N,m-2,w-6) if 0 not in B]
    def T2(v): return Epow(wedge_e(0,Epow(v,3,N,p),p),2,N,p)
    def T3(v): return Epow(wedge_e(0,Epow(v,2,N,p),p),3,N,p)
    def Tt2(v): return Epow(wedge_e(1,Epow(v,2,N,p),p),2,N,p)
    def Tt3(v): return Epow(wedge_e(0,Epow(v,3,N,p),p),3,N,p)
    indep=[]; coup=[]
    for B in src5:
        v={B:1}; indep+=[T2(v),T3(v)]; coup.append(Tt2(v))
    for B in src6:
        v={B:1}; coup.append(Tt3(v))
    return len(target),rank_p(indep,p),rank_p(coup,p)
for m,p in [(5,7),(7,11),(9,11),(10,13),(11,13),(14,17),(15,17),(17,19),(17,23)]:
    d,ri,rc=ranks_pos(m,p)
    print(f"  (m={m}, p={p}): dim {d}, rank(T2+T3) = {ri}, rank(coupled) = {rc}   (p = m+2: {p==m+2})",flush=True)
