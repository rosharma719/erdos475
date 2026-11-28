import itertools, math, io, contextlib, sys
from fractions import Fraction
from math import comb, factorial, gcd
from functools import reduce
with contextlib.redirect_stdout(io.StringIO()):
    import pairing_matrix_checks as PM
    import pascal_checks as PC
sgn,Fint,esym=PM.sgn,PM.Fint,PM.esym
# ---- (1) V_m(l) = lambda(Q_m prod_{i}(y_i + L)), L = sum l_j w_j : polynomial of degree <= m in l; check harmonicity / e_1(d)V=0
def monos_upto(n,dmax):
    out=[]
    def rec(i,left,cur):
        if i==n: out.append(tuple(cur)); return
        for a in range(left+1): rec(i+1,left-a,cur+[a])
    rec(0,dmax,[]); return out
def Vcoeffs(m):
    pt=list(range(1,m+1)); dlt=1
    for i in range(m):
        for j in range(i+1,m): dlt*=pt[j]-pt[i]
    mons=monos_upto(m,m); acc={a:0 for a in mons}
    for p in itertools.permutations(range(m)):
        s=sgn(p); w=[pt[k] for k in p]; Q=Fint(w[:m-1])
        y=[]; t=0
        for k in range(m-1): t+=w[k]; y.append(t)
        e=esym(y,m-1)
        for a in mons:
            k=sum(a); 
            if k==0:
                continue                    # e_m(y)=0 because y_0=0
                continue
            pw=1
            for x,ex in zip(w,a): pw*=x**ex
            acc[a]+=s*Q*e[m-k]*pw
    co={}
    for a in mons:
        k=sum(a); mult=factorial(k)
        for x in a: mult//=factorial(x)
        assert acc[a]%dlt==0
        co[a]=mult*acc[a]//dlt
    return co
for m in (4,5,6):
    co=Vcoeffs(m); bad_lap=0; bad_e1=0
    for b in monos_upto(m,m):
        # coefficient of l^b in Laplacian: sum_j (b_j+2)(b_j+1) coef(b+2e_j)
        lap=0; e1=0
        for j in range(m):
            b2=list(b); b2[j]+=2; b2=tuple(b2)
            if b2 in co: lap+=(b[j]+2)*(b[j]+1)*co[b2]
            b1=list(b); b1[j]+=1; b1=tuple(b1)
            if b1 in co: e1+=(b[j]+1)*co[b1]
        if lap: bad_lap+=1
        if e1: bad_e1+=1
    print(f"(1) m={m}: V_m has {sum(1 for v in co.values() if v)} nonzero monomials; Laplacian nonzero coefficients: {bad_lap};  e_1(d)V nonzero coefficients: {bad_e1}")
# ---- (2) cofactor decomposition of the boundary polynomial: diagonal (I=A) part vs off-diagonal part
kappa=PC.kappa
def parts_(m,r):
    U=tuple(range(2,m+1)); diag=0; off=0; nd=0; no=0
    for I in itertools.combinations(U,r):
        Ic=tuple(x for x in U if x not in I)
        for A in itertools.combinations(U,r):
            if sum(A)!=sum(I): continue
            Ac=tuple(x for x in U if x not in A)
            t=(-1)**(r+sum(Ic))*kappa(A,I)*kappa(Ac,Ic)
            if A==I: diag+=t; nd+=1
            else: off+=t; no+=1
    return diag,off,nd,no
print("(2) cofactor decomposition  c_{m,r+1} = diag(I=A) part + off-diagonal part:")
for m in range(3,9):
    rows=[parts_(m,r) for r in range(m)]
    cont=lambda v: reduce(gcd,[abs(x) for x in v])
    D=[x[0] for x in rows]; O=[x[1] for x in rows]; Cv=[a+b for a,b in zip(D,O)]
    print(f"  m={m}: c={Cv}")
    print(f"        diag part={D}  (content {cont(D)});  off-diag part={O}  (content {cont(O)});  #diag terms {[x[2] for x in rows]}, #offdiag {[x[3] for x in rows]}")
