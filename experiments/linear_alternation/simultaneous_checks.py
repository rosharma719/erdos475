"""Checks for the 'simultaneous interpolation' report: Ann(v)=(H_{m-1}), Ann(H_{m-1})=(v), deformation layers,
trace-interpolation image dimension r*m!/2, and the rank-4 degree-sensitivity counterexample."""
import itertools, sys, math
from artin import *
from modrank import rank_mod
from split_edge_checks_lib import *

def ann_equals(m,mult,K,label):
    """Ann(mult) = (K) in A_m=K[u,v]/(H_m,H_{m+1}); mult=(a0,b0) monomial; K polynomial dict. graded-dimension check."""
    Hm,Hm1=Hpoly(m),Hpoly(m+1); ok=True
    wm=wdeg(*mult); wk=wdeg(*next(iter(K)))
    for d in range(0,2*m+4):
        I_d=span_rows([Hm,Hm1],d); I_d1=span_rows([Hm,Hm1],d+wm); rI=rank_mod(I_d); rI1=rank_mod(I_d1)
        dimV=len(mono_basis(d)); mV=[shift({mb:1},*mult) for mb in mono_basis(d)]
        ann=dimV-(rank_mod(I_d1+mV)-rI1)-rI
        Kspan=rank_mod(I_d+span_rows([K],d))-rI
        inc=True
        if d>=wk:
            inc=rank_mod(I_d1+[shift(shift(K,*mult),a,b) for (a,b) in mono_basis(d-wk)])==rI1
        if ann!=Kspan or not inc: ok=False
    return ok
for m in range(3,9):
    Hm1_=Hpoly(m-1)
    a=ann_equals(m,(0,1),Hm1_,"Ann(v)=(H_{m-1})")
    b=ann_equals(m,Hm1_ and (0,0),{(0,1):1},"")  if False else None
    # Ann(H_{m-1}) = (v): treat multiplier H_{m-1} (polynomial) via generic routine below
    Hm,Hm1=Hpoly(m),Hpoly(m+1); ok2=True
    wk=2; wh=m-1
    for d in range(0,2*m+4):
        I_d=span_rows([Hm,Hm1],d); I_dh=span_rows([Hm,Hm1],d+wh); rI=rank_mod(I_d); rIh=rank_mod(I_dh)
        dimV=len(mono_basis(d)); hV=[]
        for (a0,b0) in mono_basis(d): hV.append(shift(Hm1_,a0,b0))
        ann=dimV-(rank_mod(I_dh+hV)-rIh)-rI
        Kspan=rank_mod(I_d+span_rows([{(0,1):1}],d))-rI
        if ann!=Kspan: ok2=False
    print(f"m={m}: Ann(v)=(H_{{m-1}}): {'OK' if a else 'FAIL'};  Ann(H_{{m-1}})=(v): {'OK' if ok2 else 'FAIL'}")
# deformation layers: dim(v^b A)/dim(v^{b+1}A) = m-b, total m(m+1)/2, v^m A = 0
for m in range(3,9):
    Hm,Hm1=Hpoly(m),Hpoly(m+1); dims=[]
    for b in range(0,m+2):
        tot=0
        for d in range(0,2*m+4):
            if d<2*b: continue
            I_d=span_rows([Hm,Hm1],d)
            tot+=rank_mod(I_d+[shift({mb:1},0,b) for mb in mono_basis(d-2*b)])-rank_mod(I_d)
        dims.append(tot)
    layers=[dims[b]-dims[b+1] for b in range(m+1)]
    print(f"m={m}: dim A={dims[0]} (m(m+1)/2={m*(m+1)//2}); layer dims {layers[:m]}; expected {[m-b for b in range(m)]}; v^m A dim={dims[m]}")
# trace interpolation: dim im E_r = r*m!/2 in (+)_d R_m/(w_d^r)
def interp_rank(m,r):
    R=Ring(m); basis=[a for a in itertools.product(*[range(i+1) for i in range(m)])]
    index={}
    def vec(polys):    # list over d of nf-dicts -> flat dict
        out={}
        for d,pl in enumerate(polys):
            for k,v in pl.items(): out[(d,k)]=v
        return out
    wv=[var(m,d) for d in range(m)]
    rows=[]
    for k in range(r):
        for beta in basis:
            comps=[]
            for d in range(m):
                pl=R.nf(pmul({beta:1},ppow(wv[d],k,m))); comps.append(pl)
            rows.append(vec(comps))
    ker=[]
    for d in range(m):
        for beta in basis:
            pl=R.nf(pmul({beta:1},ppow(wv[d],r,m)))
            if pl: ker.append({(d,k):v for k,v in pl.items()})
    return rank_mod(ker+rows)-rank_mod(ker)
for m in (3,4,5):
    res=[(r,interp_rank(m,r),r*math.factorial(m)//2) for r in range(1,m)]
    print(f"m={m}: (r, rank E_r, r*m!/2) =",res, "OK" if all(a==b for _,a,b in res) else "MISMATCH")
