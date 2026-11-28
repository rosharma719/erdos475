import sympy
from fractions import Fraction
from math import comb, factorial
from hole_recurrence import L
from seed_rigidity import eq_rank1, eq_rank2, f
m=6; p=13; base=tuple(range(1,m+1))
def upper(seed):
    F={}
    for a in range(1,m+1):
        h=tuple(x for x in base if x!=a); F[(h,h)]=Fraction((-1)**comb(m+1,2))*seed[a-1]
    for r in range(2,m):
        F={k:v*(-1)**(r-1+comb(m+1,2)) for k,v in L(F).items()}
    out=[]
    for d in range(1,m+1):
        v=F.get(((d,),(d,)),0); out.append(int(v)%p if Fraction(v).denominator==1 else ('frac',v))
    return out
s=[-5,3,-4,-3,0,-2]
print("G_6 f mod 13 (holes d=1..6):",upper(s))
print("genuine factorial upper packet mod 13:",upper([factorial(a) for a in range(1,m+1)]))
sub={f[j]:s[j] for j in range(m)}
print("rank-one constraints mod 13:",[int(sympy.expand(e.subs(sub)))%p for e in eq_rank1(m)])
print("rank-two constraints mod 13:",[int(sympy.expand(e.subs(sub)))%p for e in eq_rank2(m)])
