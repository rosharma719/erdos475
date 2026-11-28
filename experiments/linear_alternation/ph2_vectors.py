import sys, itertools
from fractions import Fraction
from math import factorial
from dual_checks import op, c_coef, to_ext, from_ext
import sympy
def vec(n):
    f={((i,),(i,)):Fraction(1-i,factorial(i+1)) for i in range(1,n+1)}
    for k in range(1,n-1): f=from_ext(op(c_coef,to_ext(f,n),n),n)
    out={}
    for (A,B),c in f.items():
        d=[x for x in range(1,n+1) if x not in A][0]; assert A==B; out[d]=c
    return out
for n in range(3,int(sys.argv[1])+1):
    v=vec(n)
    print("n=",n)
    for d in sorted(v): print("  e_%d:"%d, v[d], sympy.factorint(abs(v[d].numerator)) if v[d] else 0, "/", sympy.factorint(v[d].denominator))
