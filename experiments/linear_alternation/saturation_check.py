"""(1) rank-4 degree-sensitivity counterexample; (2) simultaneous saturation ker T_m ⊆ ker L_m on the chi_Q-equivariant
polynomials of degree D_m, ranks 4..6 (all signed orbit sums of degree D_m as spanning set).  Rank over F_1000003."""
import itertools, sys, time
from artin import *
from modrank import rank_mod
def chiQ(m,kind,c):
    return (-1)**(c*(m-1))                     # rotation i->i+c  or reflection i->c-i  (verified numerically, reflection_convention_check.py)
def group(m,char):
    els=[]
    for c in range(m):
        els.append(([(i+c)%m for i in range(m)],char('rot',c)))
        els.append(([(c-i)%m for i in range(m)],char('ref',c)))
    return els
def psign(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def orbit_sum(a,els,m):
    d={}
    for g,s in els:
        b=[0]*m
        for i in range(m): b[g[i]]=a[i]
        d.setdefault(tuple(b),set()).add(s)
    if any(len(v)>1 for v in d.values()): return {}
    return {b:list(v)[0] for b,v in d.items()}
def monos(n,d):
    def rec(k,left):
        if k==1: yield (left,); return
        for a in range(left+1):
            for r in rec(k-1,left-a): yield (a,)+r
    return list(rec(n,d))
def transfer(m,q):                                  # T_m(q) as polynomial in (h,x_0..x_{m-1}) = m+1 variables
    n=m+1; h=var(n,0); x=[var(n,i+1) for i in range(m)]
    u=padd(h,x[0]); Wp=const(n,1)
    for j in range(2,m): Wp=pmul(Wp,lin(n,range(1,1+j)))
    Wu=pmul(Wp,u)
    qp={}
    upow=[const(n,1)]
    for k in range(1,m*m): upow.append(pmul(upow[-1],u))
    for mon,c in q.items():
        t={tuple([0]*n):c}
        t=pmul(t,upow[mon[0]])
        for i in range(1,m): 
            if mon[i]: t=pmul(t,ppow(x[i],mon[i],n))
        qp=padd(qp,t)
    return pmul(Wu,qp)
# ---------- (1) rank-4 degree-sensitivity counterexample
m=4
Rm=Ring(4); Rm1=Ring(5)
for name,char in (("permutation-sign character",lambda k,c:(-1)**c if k=='rot' else psign([(c-i)%m for i in range(m)])),
                  ("true chi_Q",lambda k,c:chiQ(m,k,c))):
    els=group(m,char); q={}
    for a,coef in (((0,1,2,3),5),((0,0,1,5),1)):
        for b,s in orbit_sum(a,els,m).items(): q[b]=q.get(b,0)+coef*s
    q={k:v for k,v in q.items() if v}
    nfq=Rm.nf(q); T=Rm1.nf(transfer(m,q))
    print(f"rank-4 degree-6 q with {name}: terms in q={len(q)}, nf(q) in R_4 = {nfq}, nonzero terms of T_4(q) in R_5 = {len(T)}")
# ---------- (2) simultaneous saturation
for m in range(int(sys.argv[2]) if len(sys.argv)>2 else 4,int(sys.argv[1])+1):
    t0=time.time(); D=m*(m-1)//2-m
    els=group(m,lambda k,c:chiQ(m,k,c)); Rm=Ring(m); Rm1=Ring(m+1)
    seen=set(); rowsT=[]; rowsL=[]; nonzero=0
    for a in monos(m,D):
        if a in seen: continue
        O=orbit_sum(a,els,m)
        for g,_ in els:
            b=[0]*m
            for i in range(m): b[g[i]]=a[i]
            seen.add(tuple(b))
        if not O: continue
        nonzero+=1
        Lv=Rm.nf(O); Tv=Rm1.nf(transfer(m,O))
        rowsT.append({('T',k):v for k,v in Tv.items()}); rowsL.append({('L',k):v for k,v in Lv.items()})
    rT=rank_mod(rowsT); rJ=rank_mod([{**t,**l} for t,l in zip(rowsT,rowsL)]); rL=rank_mod(rowsL)
    print(f"rank {m}: D={D}, {nonzero} orbit sums, rank T={rT}, rank L={rL}, joint rank={rJ}  -> simultaneous saturation {'HOLDS' if rT==rJ else 'FAILS'}   ({time.time()-t0:.0f}s)",flush=True)
