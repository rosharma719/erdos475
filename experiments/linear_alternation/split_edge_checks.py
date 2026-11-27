"""Checks of the 'merged-edge' report: Thm1 presentation relations, Thm2 annihilator Ann(u)=(K_m) in K[u,v]/(H_m,H_{m+1}),
rank-5 counterexample (T_5(q)=0 but q!=0)."""
import itertools, cmath, math, sys
from artin import *
P=1000003
def Hpoly(j):                       # H_j(u,v) as dict {(a,b):c} meaning u^a v^b
    h=[{(0,0):1},{(1,0):1}]
    for k in range(2,j+1):
        t={}
        for (a,b),c in h[k-1].items(): t[(a+1,b)]=t.get((a+1,b),0)+c
        for (a,b),c in h[k-2].items(): t[(a,b+1)]=t.get((a,b+1),0)-c
        h.append({k_:v for k_,v in t.items() if v})
    return h[j]
def rank_mod(rows):
    rows=[dict(r) for r in rows if r]; piv={}; rk=0
    for r in rows:
        r={k:v%P for k,v in r.items() if v%P}
        while r:
            k=min(r)
            if k in piv:
                pr=piv[k]; f=r[k]
                for kk,vv in pr.items(): r[kk]=(r.get(kk,0)-f*vv)%P
                r={a:b for a,b in r.items() if b}
            else:
                inv=pow(r[k],P-2,P); r={a:b*inv%P for a,b in r.items()}; piv[k]=r; rk+=1; break
    return rk
def wdeg(a,b): return a+2*b
def mono_basis(d): return [(d-2*b,b) for b in range(d//2+1)]
def shift(poly,a0,b0): return {(a+a0,b+b0):c for (a,b),c in poly.items()}
def span_rows(gens,d):              # all mono*gen in degree d
    rows=[]
    for g in gens:
        gd=wdeg(*next(iter(g)))
        if gd>d: continue
        for (a,b) in mono_basis(d-gd): rows.append(shift(g,a,b))
    return rows
for m in range(3,9):
    Hm,Hm1=Hpoly(m),Hpoly(m+1)
    # K_m
    num=Hm if m%2==1 else Hm1
    K={(a-1,b):c for (a,b),c in num.items()}; assert all(a>=0 for (a,b) in K)
    ok=True
    for d in range(0,2*m+3):
        I_d=span_rows([Hm,Hm1],d); I_d1=span_rows([Hm,Hm1],d+1)
        rI=rank_mod(I_d); rI1=rank_mod(I_d1)
        dimV=len(mono_basis(d))
        uV=[shift({mb:1},1,0) for mb in mono_basis(d)]
        ann=dimV-(rank_mod(I_d1+uV)-rI1)-rI                   # dim Ann(u)_d in A_m (quotient by I_d)
        Kspan=rank_mod(I_d+span_rows([K],d))-rI               # dim (K_m)_d in A_m
        # (K) subset Ann(u): u*K*mono in I_{d+1}
        inc=rank_mod(I_d1+[shift(K,a+1,b) for (a,b) in mono_basis(d-wdeg(*next(iter(K))))] if d>=wdeg(*next(iter(K))) else I_d1)==rI1
        if ann!=Kspan or not inc: ok=False; print("  mismatch m",m,"d",d,ann,Kspan,inc)
    print(f"Thm2 m={m}: Ann(u)=(K_m) in graded dimensions through degree {2*m+2}:", "OK" if ok else "FAIL")
# ---- Thm1 relations at roots of unity
for m in range(3,8):
    r=[cmath.exp(2j*cmath.pi*k/(m+1)) for k in range(m+1)]; h,x0,z=r[0],r[1],r[2:]; u,v=h+x0,h*x0
    def Hn(j):
        a,b=1,u
        if j==0: return 1
        for _ in range(j-1): a,b=b,u*b-v*a
        return b
    e=lambda zs,k:sum(math.prod(c) for c in itertools.combinations(zs,k))
    err=max([abs(e(z,j)-(-1)**j*Hn(j)) for j in range(1,m)]+[abs(Hn(m))])   # roots of unity have e_{m+1}=+-1, so H_{m+1}!=0 there
    print(f"Thm1 relations m={m}: max err {err:.1e}")
# ---- rank-5 counterexample: q = w1 (w0^4 + 4 w0^2 e2 + 3 e2^2), T_5(q)=W(x)(h+x0)q(h+x0,x1..x4)
R5=Ring(5); n=5
def e2(vars_):
    t={}
    for i,j in itertools.combinations(range(len(vars_)),2): t=padd(t,pmul(vars_[i],vars_[j]))
    return t
w=[var(5,i) for i in range(5)]; E2=e2(w)
q=pmul(w[1],padd(padd(ppow(w[0],4,5),pmul(const(5,4),pmul(ppow(w[0],2,5),E2))),pmul(const(5,3),pmul(E2,E2))))
print("rank5: nf(q) in R_5 nonzero terms:",len(R5.nf(q)),"  (q = w0^4 w1 mod ideal:",R5.nf(q)==R5.nf(pmul(ppow(w[0],4,5),w[1])),")")
R6=Ring(6); N=6                                # variables: 0=h, 1..5 = x0..x4  (x4 index5)
h_=var(6,0); x=[var(6,i+1) for i in range(5)]
u=padd(h_,x[0])
Wp=const(6,1)
for j in range(2,5): Wp=pmul(Wp,lin(6,range(1,1+j)))
vs=[u,x[1],x[2],x[3],x[4]]
E2u=e2(vs)
qq=pmul(x[1],padd(padd(ppow(u,4,6),pmul(const(6,4),pmul(ppow(u,2,6),E2u))),pmul(const(6,3),pmul(E2u,E2u))))
T=pmul(pmul(Wp,u),qq)
print("rank5: T_5(q) in R_6 has",len(R6.nf(T)),"nonzero terms (expected 0)")
