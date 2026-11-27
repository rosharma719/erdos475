import sys, sympy
from fractions import Fraction
from math import factorial, comb
from hole_recurrence import L, C, prop
def run(m):
    base=tuple(range(1,m+1))
    def seed(a):  # exponent a survives: holes = base minus a
        h=tuple(x for x in base if x!=a); return {(h,h):Fraction(1)}
    def iterate(F):
        for r in range(2,m):
            s=(-1)**(r-1+comb(m+1,2))
            F={k:v*s for k,v in L(F).items()}
        return F
    s1=(-1)**(0+comb(m+1,2))
    vecs={a:iterate({k:v*s1 for k,v in seed(a).items()}) for a in range(1,m+1)}
    B=vecs[m]
    A={}
    for a in range(1,m):
        for k,v in vecs[a].items(): A[k]=A.get(k,0)+factorial(a)*v
    A={k:v for k,v in A.items() if v}
    lam=prop(A,B)
    print(f"m={m}: B = L^(m-2) delta_m nonzero: {bool(B)};  A proportional to B: {lam is not None}, lambda = {lam}", end="")
    if lam is not None and lam!='both0':
        tot=lam+factorial(m); print(f";  lambda + m! = {tot} = {sympy.factorint(tot.numerator) if tot else 0}/{sympy.factorint(tot.denominator)}", end="")
    print(flush=True)
    # dimension of span of all seed images
    keys=sorted(set(k for v in vecs.values() for k in v))
    M=sympy.Matrix([[sympy.Rational(vecs[a].get(k,0)) for k in keys] for a in range(1,m+1)])
    print(f"     rank of {{L^(m-2) delta_a : a=1..m}} = {M.rank()}  (B content: {sympy.factorint(int(sympy.gcd([sympy.Rational(x) for x in B.values()])) ) if B else 0})")
for m in range(4,int(sys.argv[1])+1): run(m)
