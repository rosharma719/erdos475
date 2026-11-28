"""Checks for the 'coefficient-extraction obstruction' report:
 (a) rank-5 degree-8 counterexample (T_d(q)=0 for all cuts but q != 0); (c) Catalan trace pairing + rank formula;
 (d) Vandermonde cofactor identities; (e) boundary packet Q_m A_0 nonvanishing (content over g) for even m."""
import itertools, math, sys
from fractions import Fraction
from sat_lib import *
# ---------------- (a)
m=5
els=group(m,lambda k,c:1)                       # trivial character at rank 5 (chi_Q = +1 for odd m)
rows="""00017 -410
00026 -1605
00035 -3640
00044 -5110
00116 -639
00125 -1470
00134 -3290
00143 -3640
00152 -1204
00161 -933
00224 560
00233 280"""
q={}
for line in rows.splitlines():
    a,c=line.split(); a=tuple(int(x) for x in a)
    for b,s in orbit_sum(a,els,m).items(): q[b]=q.get(b,0)+int(c)*s
q={k:v for k,v in q.items() if v}
Rm=Ring(5); Ru=Ring(6)
nfq=Rm.nf(q); T=Ru.nf(transfer(5,q))
exp={(0,1,2,3,4):0}
print(f"(a) rank-5 degree-8 polynomial: {len(q)} monomials; nf(q) in R_5 has {len(nfq)} terms: {sorted(nfq.items())}")
print(f"    T_5(q) (cut 0; other cuts by rotation covariance) in R_6: {len(T)} nonzero terms")

# ---------------- (c) Catalan trace pairing and rank formula in A_m = K[u,v]/(H_m,H_{m+1})
from split_edge_checks_lib import Hpoly, wdeg, mono_basis, shift, span_rows
def mulp(p,q_):
    o={}
    for (a,b),c in p.items():
        for (a2,b2),c2 in q_.items(): o[(a+a2,b+b2)]=o.get((a+a2,b+b2),0)+c*c2
    return {k:v for k,v in o.items() if v}
def gpoly(m):
    g={}
    for j in range(m):
        for k,v in mulp(Hpoly(j),{(m-1-j,0):1}).items(): g[k]=g.get(k,0)+v
    return {k:v for k,v in g.items() if v}
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
def socle_value(poly,m):                # coefficient c with poly = c v^(m-1) in A_m (degree 2m-2), exact rationals
    d=2*m-2; mons=mono_basis(d)         # u^(d-2b) v^b
    rel=span_rows([Hpoly(m),Hpoly(m+1)],d)
    # solve poly - c*v^(m-1) in span(rel): Gaussian elimination over Q on columns
    cols=sorted(set(k for r in rel for k in r)|set(poly)|{(0,m-1)})
    M=[[Fraction(r.get(k,0)) for k in cols] for r in rel]
    tgt=[Fraction(poly.get(k,0)) for k in cols]; sv=[Fraction(1) if k==(0,m-1) else Fraction(0) for k in cols]
    # reduce target modulo rel, then modulo nothing: find c s.t. reduced(tgt) = c * reduced(sv)
    piv=[]; B=[]
    for r in M:
        r=r[:]
        for (pc,pr) in piv:
            if r[pc]!=0:
                f=r[pc]; r=[a-f*b for a,b in zip(r,pr)]
        nz=next((i for i,x in enumerate(r) if x!=0),None)
        if nz is not None:
            r=[x/r[nz] for x in r]
            piv=[(pc,[a-pr[nz]*b for a,b in zip(pr_,r)] ) if False else (pc,pr_) for pc,pr_ in piv]
            piv.append((nz,r))
    def red(v):
        v=v[:]
        for (pc,pr) in piv:
            if v[pc]!=0:
                f=v[pc]; v=[a-f*b for a,b in zip(v,pr)]
        return v
    rt,rs=red(tgt),red(sv)
    j=next(i for i,x in enumerate(rs) if x!=0); c=rt[j]/rs[j]
    assert all(rt[i]==c*rs[i] for i in range(len(rt))), "not proportional"
    return c
def catalan(k): return math.comb(2*k,k)//(k+1)
okC=True
for m in range(3,10):
    g=gpoly(m)
    for k in range(0,(m-1)//2+1):
        val=socle_value(mulp(g,{(m-1-2*k,k):1}),m)
        if val!=catalan(m-k): okC=False; print("  Catalan mismatch",m,k,val,catalan(m-k))
print("(c) lambda(g_m u^(m-1-2k) v^k) = Catalan(m-k) for m=3..9, 0<=k<=(m-1)/2:", "OK" if okC else "FAIL")
bad=0; tests=0
for m in range(3,15):
    g=gpoly(m); Hm,Hm1=Hpoly(m),Hpoly(m+1)
    for p in (10**6+3,11,13,17,19,23,29,31,37):
        if p<=m+1 and p!=10**6+3: continue
        for d in range(0,m):
            a=d//2+1; b=(m-1-d)//2+1
            tgt=d+m-1
            I=span_rows([Hm,Hm1],tgt)
            rows=[mulp(g,{mb:1}) for mb in mono_basis(d)]
            r=rank_p(I+rows,p)-rank_p(I,p)
            pred=min(a,b) if p>10**5 else min(a,b,max(0,a+b-1-m+(p-1)//2))
            tests+=1
            if r!=pred: bad+=1; print(f"  rank mismatch m={m} p={p} d={d}: computed {r}, formula {pred}")
print(f"    rank formula min(a,b,max(0,a+b-1-m+(p-1)/2)) checked on {tests} (m,p,d) cases (m=3..14, p in 11..37 with p>m+1, plus characteristic ~0): mismatches {bad}")
# ---------------- (d) cofactor identities
def Qv(w):
    m=len(w); y=[Fraction(0)]
    for i in range(m-1): y.append(y[-1]+w[i])
    num=Fraction(1)
    for i in range(m):
        for j in range(i+1,m): num*=y[j]-y[i]
    den=Fraction(1)
    for x in w: den*=x
    return num/den
import random
random.seed(5)
okD=True
for m in range(3,8):
    n=m+1
    for trial in range(5):
        Y=[Fraction(x) for x in random.sample(range(-30,30),n)]
        x=[Y[(i+1)%n]-Y[i] for i in range(n)]          # includes closing edge x_{n-1}=Y_0-Y_{n-1}
        qs=[]
        for i in range(n):
            L=[Y[j] for j in range(n) if j!=i]
            w=[L[k+1]-L[k] for k in range(m-1)]+[L[0]-L[m-1]]
            qs.append(Qv(w))
        for k in range(0,m+1):
            S=sum((-1)**i*Y[i]**k*qs[i]*(1/x[(i-1)%n]+1/x[i]) for i in range(n))
            exp=0 if k<m else (-1)**m*Qv(x)
            if S!=exp: okD=False
print("(d) sum_i (-1)^i Y_i^k q_i (1/x_{i-1}+1/x_i) = 0 for k<m and (-1)^m Q_{m+1} for k=m  [m=3..7, exact rationals]:", "OK" if okD else "FAIL")
# ---------------- (e) boundary packet content: lambda_m(Q_m A_0 g), g of degree 2, even m
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def F_interval(w):                          # Q_m as polynomial F_{m-1}(w_0..w_{m-2})
    mm=len(w)-1; f=1
    for i in range(mm):
        s=w[i]
        for j in range(i+1,mm):
            s+=w[j]
            if i==0 and j==mm-1: continue
            f*=s
    return f
def content(m):
    pt=list(range(1,m+1)); d=1
    for i in range(m):
        for j in range(i+1,m): d*=pt[j]-pt[i]
    gm=[mm for mm in itertools.product(range(3),repeat=m) if sum(mm)==2]
    tot=[0]*len(gm)
    for p in itertools.permutations(range(m)):
        w=[pt[k] for k in p]; s=sgn(p)
        y=0; A0=1
        for j in range(m):
            y+=w[j-1] if j>0 else 0
            if j>=2: A0*=y
        v=s*F_interval(w)*A0
        for idx,mm in enumerate(gm):
            t=v
            for e,x_ in zip(mm,w): t*=x_**e
            tot[idx]+=t
    vals=[t//d for t in tot]; assert all(t%d==0 for t in tot)
    g=0
    for x_ in vals: g=math.gcd(g,abs(x_))
    return g,vals
for m in (4,6,8):
    g,vals=content(m)
    pr=[q_ for q_ in range(2,200) if g and g%q_==0 and all(q_%r for r in range(2,q_))]
    print(f"(e) m={m}: content gcd_g lambda_m(Q_m A_0 g) = {g}; nonzero values {sum(1 for x_ in vals if x_)}/{len(vals)}; mod 11 nonzero: {any(x_%11 for x_ in vals)}")
