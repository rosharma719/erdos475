"""Rank-5 detection (-2) and rank-6 witness (-198, rank-7 value -7646) from the 2026-11-28 report."""
import itertools
from transfer_checks import lam, sgn
def Hs(u):
    m=len(u); y=[0]
    for i in range(m-1): y.append(y[-1]+u[i])
    H0=1;H1=1
    for j in range(2,m): H0*=(y[0]-y[j]); H1*=(y[1]-y[j])
    return H0,H1,y
# ---- rank 5
def q5(x):
    return sum(x[i]*(x[(i+1)%5]**2*x[(i+2)%5]**2 + x[(i-1)%5]**2*x[(i-2)%5]**2) for i in range(5))
def f5(x):
    H0,H1,_=Hs(x); return x[1]**2*q5(x)*(H1-H0)
print("rank5 lambda_5(x1^2 q (H1-H0)) =",lam(f5,5))
# ---- rank 6 witness
rows="""011133 1122
000036 119
000045 -5033
000126 1015
000135 -88
000144 -113
000153 3533
000162 760
000225 -290
000234 1328
000243 -471
000252 3069
000315 -571
001035 -2526
001044 -1617
001125 -1332
001134 -864
001143 -858
001152 -1224
001215 396
001224 -108
001233 204"""
W=[(tuple(int(c) for c in a),int(b)) for a,b in (r.split() for r in rows.splitlines())]
m=6
def group(revkind):
    els=[]
    for r in range(m):
        els.append((lambda i,r=r:(i+r)%m, (-1)**r))
        if revkind==0: els.append((lambda i,r=r:(r-i)%m, (-1)**(r+1)))
        else: els.append((lambda i,r=r:(r+1-i)%m if False else (r-1-i)%m, (-1)**(r+1)))
    return els
def orbit_terms(a,els):
    d={}
    for g,s in els:
        b=[0]*m
        for i in range(m): b[g(i)]=a[i]
        b=tuple(b)
        d.setdefault(b,set()).add(s)
    return {b:list(s)[0] for b,s in d.items() if len(s)==1}, any(len(s)>1 for s in d.values())
for revkind in (0,1):
    els=group(revkind)
    terms=[]; zero=0
    for a,c in W:
        t,bad=orbit_terms(a,els)
        if bad: zero+=1; continue
        terms.append((c,t))
    def q6(x):
        tot=0
        for c,t in terms:
            for b,s in t.items():
                v=s*c
                for e,xx in zip(b,x): v*=xx**e
                tot+=v
        return tot
    print(f"revkind={revkind}: orbit sums vanishing by sign clash: {zero}/{len(W)}")
    try:
        print("  lambda_6(x0 x1^5 q) =",lam(lambda x:x[0]*x[1]**5*q6(x),6))
    except AssertionError: print("  non-integral")
    # rank-7 value: lambda_7(h^4 x0^2 x1 T_6(q)),  T_6(q)=W_6(x)(h+x0) q(h+x0,x1..x5);  variables (h,x0..x5)
    def f7(v):
        h,x=v[0],list(v[1:])
        Wv=1
        for j in range(2,m): Wv*=sum(x[:j])
        return h**4*x[0]**2*x[1]*Wv*(h+x[0])*q6([h+x[0]]+x[1:])
    # note: lam() puts variable order as given; h is first here
    print("  lambda_7(h^4 x0^2 x1 T_6 q) =",lam(f7,7))
    # divided-difference packets: lambda_6(g q (H1-H0)), g monomials of degree 2
    mons=[mm for mm in itertools.product(range(3),repeat=m) if sum(mm)==2]
    vals=[]
    for mm in mons:
        def fg(x,mm=mm):
            H0,H1,_=Hs(x); v=q6(x)*(H1-H0)
            for e,xx in zip(mm,x): v*=xx**e
            return v
        vals.append(lam(fg,6))
    print("  DD packets (first edge), all degree-2 g: nonzero count =",sum(1 for v in vals if v))
    mons1=[mm for mm in itertools.product(range(2),repeat=m) if sum(mm)==1]
    vals=[]
    for mm in mons1:
        def fz(x,mm=mm):
            _,_,y=Hs(x); fp=1
            for j in range(1,m): fp*=(y[0]-y[j])
            v=q6(x)*fp
            for e,xx in zip(mm,x): v*=xx**e
            return v
        vals.append(lam(fz,6))
    print("  zero-edge insertion packets lambda_6(g q f'(y0)), deg g=1:",vals)
