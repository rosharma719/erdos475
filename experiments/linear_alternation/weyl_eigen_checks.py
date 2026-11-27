import itertools, io, contextlib, math, random
from fractions import Fraction
from math import comb
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def Wop_eigen(A,I,h0,order):
    """eigenvalue of sum_{sigma,tau} sgn sgn prod_j T_{a_sigma(j), i_tau(j)} on e_{h0}; order='right': j=r applied first"""
    r=len(A); tot=0
    for s in itertools.permutations(range(r)):
        for t in itertools.permutations(range(r)):
            seq=list(range(r-1,-1,-1)) if order=='right' else list(range(r))
            h=h0; prod=1
            for j in seq:
                a=A[s[j]]; i=I[t[j]]
                w=T(i,a,h) if h>=0 else 0
                # T() returns 0 when new height negative; here heights >= a required for D^a to act (handled by T via negative check)
                prod*=w; h=h+i-a
                if prod==0: break
            tot+=sgn(s)*sgn(t)*prod
    return tot
for m in (3,4,5):
    U=tuple(range(2,m+1))
    Kd={d:kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)}
    for order in ('right','left'):
        ok=True; vals=[]
        for h0 in range(0,8):
            ev=Wop_eigen(U,U,h0,order)
            pred=sum(d*comb(h0,d-1)*Kd[d] for d in range(1,m+1))
            vals.append((ev,pred))
            if ev!=pred: ok=False
        print(f"(10) m={m}, product order {order}: eigenvalue = sum_d d C(h,d-1) K(J_d,J_d) for h=0..7: {ok}   {vals[:4]}")
    cons=Wop_eigen(tuple(range(1,m)),tuple(range(1,m)),3,'right')
    print(f"     W({{1..{m-1}}},{{1..{m-1}}}) eigenvalue at h=3 (claimed identically 0): {cons}")
# (11) Alt F_d = (-1)^{m-d} K(J_d,J_d) Delta(x) prod x
random.seed(8)
for m in (3,4,5):
    x=[Fraction(v) for v in random.sample(range(1,15),m)]
    dlt=vand(x); px=Fraction(1)
    for v in x: px*=v
    res=[]
    for d in range(1,m+1):
        J=tuple(c for c in range(1,m+1) if c!=d); tot=Fraction(0)
        for p in itertools.permutations(range(m)):
            xs=[x[i] for i in p]; s=0; ss=[]
            for i in range(m-1): s+=xs[i]; ss.append(s)
            M=[[sj**c for c in J] for sj in ss]
            tot+=sgn(p)*xs[m-1]**d*detF(M)
        K=kappa(J,J); pred=(-1)**(m-d)*K*dlt*px
        res.append((d,tot==pred,tot==-pred))
    print(f"(11) m={m}: Alt F_d = (-1)^(m-d) K(J_d,J_d) Delta prod x  per d (d, equal, negated): {res}")
