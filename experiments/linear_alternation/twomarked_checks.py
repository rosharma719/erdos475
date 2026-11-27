"""(1) d_x Q_{m+1} = (a+b) V_m(a,b) at the complementary point e_j(x) = (-1)^j h_j(a,b);  (2) extra-vertex descent recurrence;  (3) Plucker obstruction numbers."""
import itertools, cmath, math, random, sys
from fractions import Fraction
src=open('rv_contents.py').read()
exec(src[:src.index('if __name__=="__main__":')])
# ---------- (1)
def polyval(p,a): return sum(c*a**i for i,c in enumerate(p))
def hh(n,a,b): return sum(a**i*b**(n-i) for i in range(n+1)) if n>=0 else 0
def sgnp(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
random.seed(4)
for m in (4,5,6):
    R,V=RV(m)
    a=complex(random.uniform(0.5,2),random.uniform(-1,1)); b=complex(random.uniform(0.5,2),random.uniform(-1,1))
    # x_i: roots of sum_{j=0}^{m-1} h_j(a,b) z^{m-1-j}   (so that e_j(x) = (-1)^j h_j(a,b))
    import numpy as np
    coeffs=[hh(j,a,b) for j in range(m)]
    x=list(np.roots(coeffs))
    k=m-1
    tot=0
    for p in itertools.permutations(range(k)):
        xs=[x[i] for i in p]; s=0; pts=[0j]
        for v in xs: s+=v; pts.append(s)
        pts.append(-b)
        D=1
        for i in range(len(pts)):
            for j in range(i+1,len(pts)): D*=pts[j]-pts[i]
        prod=1
        for v in xs: prod*=v
        tot+=sgnp(p)*D/(a*b*prod)
    Dx=1
    for i in range(k):
        for j in range(i+1,k): Dx*=x[j]-x[i]
    lhs=tot/Dx
    # V_m(a,b) homogeneous degree m-3: V(a,b)=b^(m-3) V(a/b,1)
    Vab=b**(m-3)*polyval([complex(c) for c in V],a/b)
    rhs=(a+b)*Vab
    print(f"(1) m={m}: divided symmetrization of Q_(m+1) = {lhs:.6g};  (a+b)V_m(a,b) = {rhs:.6g};  ratio = {lhs/rhs:.6g}")
# ---------- (2) extra-vertex descent: G_{k,l}(T;X)=Alt_X[Delta(0,s_1..s_k) prod_nu prod_{j=1}^{k-1}(t_nu - s_j)]/(Delta(X) prod x)
def Gfun(T,X):
    k=len(X); l=len(T); tot=Fraction(0)
    for p in itertools.permutations(range(k)):
        s=0; pts=[Fraction(0)]; ss=[]
        for i in p: s+=X[i]; pts.append(s); ss.append(s)
        D=vand(pts)
        for t in T:
            for j in range(k-1): D*=(t-ss[j])
        tot+=sgn(p)*D
    den=vand(X)
    for v in X: den*=v
    return tot/den
for k in (2,3,4):
    for ell in (1,2):
        X=[Fraction(v) for v in random.sample(range(1,13),k)]; T=[Fraction(random.randint(15,40)) for _ in range(ell)]
        S=sum(X); lhs=Gfun(T,X); rhs=Fraction(0)
        for idx,u in enumerate(X):
            Xr=X[:idx]+X[idx+1:]
            fp=Fraction(1)
            for v in X:
                if v!=u: fp*=(u-v)
            w=Fraction(1)
            for t in T: w*=(t-S+u)
            if k-1==0: g=Fraction(1)
            else: g=Gfun([S]+T,Xr) if k-1>=1 else Fraction(1)
            rhs+=w/fp*g
        rhs*=S
        print(f"(2) k={k}, l={ell}: G_(k,l)(T;X) = {lhs};  recurrence RHS = {rhs};  equal: {lhs==rhs}  (negated: {lhs==-rhs})")
# G_{k,1} = S L_k check
for k in (2,3,4):
    X=[Fraction(v) for v in random.sample(range(1,13),k)]; t=Fraction(random.randint(15,40))
    S=sum(X)
    den=vand(X)
    for v in X: den*=v
    Lk=Phi(t,X)/(den*S*t*(t-S))
    print(f"    k={k}: G_(k,1)(t;X) = S L_k(t;X): {Gfun([t],X)==S*Lk}")
# ---------- (3) Plucker obstruction
from fractions import Fraction as Fr
x3=[1,2,4]; S=7
def v(t): return [Fr(t)**j for j in range(1,6)]
def vq(t):                           # reduce modulo v(7): kill coordinate 1
    base=v(t); w7=v(S); f=base[0]/w7[0]
    return [base[j]-f*w7[j] for j in range(1,5)]      # exponents 2..5
pij={}
for p in itertools.permutations(range(3)):
    s1=x3[p[0]]; s2=s1+x3[p[1]]
    u1=vq(s1); u2=vq(s2); sg=sgnp(p)
    for i in range(4):
        for j in range(i+1,4):
            pij[(i+2,j+2)]=pij.get((i+2,j+2),0)+sg*(u1[i]*u2[j]-u1[j]*u2[i])
print("(3) Plucker coordinates p_ij of the quotient two-vector:",{k:str(v) for k,v in pij.items()})
pl=pij[(2,3)]*pij[(4,5)]-pij[(2,4)]*pij[(3,5)]+pij[(2,5)]*pij[(3,4)]
print("    p23 p45 - p24 p35 + p25 p34 =",pl,"=",math.prod([2,2,2,2,2,2,2,2])*27*5*7,"(2^8*3^3*5*7) ?",pl==2**8*27*5*7)
