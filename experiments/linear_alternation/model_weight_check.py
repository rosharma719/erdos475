"""Monomial-weight saturation: T_d^model(q) = (h+x) h^{m-2} q(w with w_d -> h+x) in R_{m+1}.
Claim: if T_d^model(q)=0 for all d then q=0 in R_m, for every homogeneous q of degree < N_m (no symmetry assumed).
Test: for each degree k < N_m, rank of the (all-cuts transfer) map on ALL monomials of degree k equals rank of the joint map (transfer, class in R_m)."""
import sys, itertools
from artin import *
from modrank import rank_mod
def monos(n,d):
    def rec(k,left):
        if k==1: yield (left,); return
        for a in range(left+1):
            for r in rec(k-1,left-a): yield (a,)+r
    return list(rec(n,d))
def run(m):
    N=m*(m-1)//2; R=Ring(m); U=Ring(m+1); n=m+1
    h=var(n,0); x=var(n,1); hx=padd(h,x)
    hpow=ppow(h,m-2,n); pref=pmul(hx,hpow)
    res=[]
    for k in range(0,N):
        rowsT=[]; rowsJ=[]
        for beta in monos(m,k):
            comps={}
            for d in range(m):
                # variables of the upper ring: 0=h, 1=x, others: edges w_i (i != d) at indices 2..m
                idx={}; j=2
                for i in range(m):
                    if i==d: continue
                    idx[i]=j; j+=1
                t=const(n,1)
                for i in range(m):
                    if beta[i]==0: continue
                    base=hx if i==d else var(n,idx[i])
                    t=pmul(t,ppow(base,beta[i],n))
                v=U.nf(pmul(pref,t))
                for kk,vv in v.items(): comps[(0,d,kk)]=vv
            Lv={(1,0,kk):vv for kk,vv in R.nf({beta:1}).items()}
            rowsT.append(comps); rowsJ.append({**comps,**Lv})
        rT=rank_mod(rowsT); rJ=rank_mod(rowsJ); rL=rank_mod([{(1,0,kk):vv for kk,vv in R.nf({b:1}).items()} for b in monos(m,k)])
        res.append((k,rT,rL,rJ,rT==rJ))
    return res
for m in range(3,int(sys.argv[1])+1):
    r=run(m)
    print(f"m={m}: (degree k, rank T, rank L, joint rank, saturation) =",r, "ALL HOLD" if all(x[4] for x in r) else "FAILS")
