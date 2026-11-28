import itertools, sympy
from fractions import Fraction
from sympy.polys.matrices import DomainMatrix
from sympy import GF
from onesided import X, L
from terminal_joint import basis2, onehole
for m in (6,7,8):
    bas=[b for b in basis2(m) if b[0]==b[1]]
    M=sympy.Matrix([onehole(X({b:Fraction(1)},m),m)+onehole(L({b:Fraction(1)}),m) for b in bas]).T
    bad=[p for p in sympy.primerange(m+2,200) if DomainMatrix.from_Matrix(M).convert_to(GF(p)).rank()<2*m-2]
    print(f"m={m}: diagonal joint map rank 2m-2 mod every prime m+1<p<200 : {not bad} {bad}")
g=[-696729600,646963200,663552000,82944000,0]
from math import factorial
print("genuine rank-6 packet satisfies sum (-1)^d d! g_d = 0:", sum((-1)**d*factorial(d)*g[d-1] for d in range(1,6))==0)
