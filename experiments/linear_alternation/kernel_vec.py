import sys
from fractions import Fraction
from math import factorial
from dual_checks import op, c_coef, to_ext, from_ext
import sympy
def Pmat(n):
    cols=[]
    for i in range(1,n+1):
        v={((i,),(i,)):Fraction(1)}
        for k in range(1,n-1): v=from_ext(op(c_coef,to_ext(v,n),n),n)
        cols.append(v)
    rows=sorted({r for v in cols for r in v})
    return sympy.Matrix([[sympy.Rational(v.get(r,0).numerator,v.get(r,0).denominator) if r in v else 0 for v in cols] for r in rows])
for n in range(3,int(sys.argv[1])+1):
    M=Pmat(n); ns=M.nullspace(); assert len(ns)==1
    k=ns[0]; k=k/k[n-1]
    print("n=",n,"kernel/ k_n:",[str(x) for x in k])
    print("    times (i+1)!:",[str(k[i-1]*factorial(i+1)) for i in range(1,n+1)])
    print("    times i!:",[str(k[i-1]*factorial(i)) for i in range(1,n+1)])
