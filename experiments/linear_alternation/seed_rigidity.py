import sys, sympy
from fractions import Fraction
from math import factorial, comb
from hole_recurrence import L
f=sympy.symbols('f1:15')
def eq_rank1(m):
    return [sum((-1)**j*comb(k,j)**2*factorial(k-j)*f[j-1] for j in range(1,k+1))+f[k-1] for k in range(1,m+1)]
def V(a,b): return -sum((-1)**j*(comb(b,j)-comb(a,j))**2*factorial(a+b-j)*f[j-1] for j in range(1,b+1))
def eq_rank2(m):
    return [sum((-1)**(1+j)*comb(b,j)**2*factorial(b-j)*V(1,j) for j in range(2,b+1))-V(1,b) for b in range(2,m+1)]
def F2_from_recurrence(m,seed):
    base=tuple(range(1,m+1)); F={}
    s1=(-1)**comb(m+1,2)
    for a in range(1,m+1):
        h=tuple(x for x in base if x!=a); F[(h,h)]=s1*seed[a-1]
    G=L(F); s2=(-1)**(1+comb(m+1,2))
    return {k:s2*v for k,v in G.items()}
# (3) vs recurrence, generic integer seed
import random; random.seed(5)
for m in (4,5,6):
    seed=[Fraction(random.randint(-9,9)) for _ in range(m)]
    F2=F2_from_recurrence(m,seed); ok=True
    for a in range(1,m+1):
        for b in range(a+1,m+1):
            h=tuple(x for x in range(1,m+1) if x not in (a,b))
            val=sympy.Rational(F2.get((h,h),0))
            pred=V(a,b).subs({f[j]:sympy.Rational(seed[j]) for j in range(m)})
            if val!=pred: ok=False
    print(f"(3) rank-two formula V_f(a,b) = diagonal F_2 coordinate from recurrence, m={m}, random seed: {ok}")
fact={f[j]:factorial(j+1) for j in range(14)}
print("(2) genuine seed satisfies rank-one identity k=1..12:",all(sympy.expand(e.subs(fact))==0 for e in eq_rank1(12)))
print("(4) genuine seed satisfies rank-two identity b=2..12:",all(sympy.expand(e.subs(fact))==0 for e in eq_rank2(12)))
print(" m | rank of (2)+(4) over Q | solution dim | solution space | mod-p dims for p in (m+1,60)")
for m in range(3,13):
    eqs=eq_rank1(m)+eq_rank2(m); vars_=list(f[:m])
    A=sympy.Matrix([[sympy.expand(e).coeff(v) for v in vars_] for e in eqs])
    ns=A.nullspace()
    dims=set()
    for p in sympy.primerange(m+2,60):
        Ap=A.applyfunc(lambda x: x%p)
        # rank mod p via sympy GF
        from sympy.polys.matrices import DomainMatrix
        from sympy import GF
        dm=DomainMatrix.from_Matrix(A).convert_to(GF(p))
        dims.add(m-dm.rank())
    sol=[list(v) for v in ns]
    print(f" {m} | {A.rank()} | {len(ns)} | {[ [str(x) for x in v] for v in sol] if m<=7 else len(ns)} | {dims}")
