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
