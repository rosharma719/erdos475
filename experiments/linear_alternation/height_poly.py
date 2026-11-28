import sys
from fractions import Fraction
from math import factorial
from deformed_ext import F
import sympy
h=sympy.symbols('h')
def ff(a): 
    r=sympy.Integer(1)
    for j in range(a): r*= (h-j)
    return r
for m in range(2,int(sys.argv[1])+1):
    c=[Fraction(1,factorial(k)) for k in range(1,m+1)]
    W=F(c,m)
    assert all(i==a for (i,a) in W), W
    poly=sympy.expand(sum(sympy.Rational(v.numerator,v.denominator)*ff(a) for (i,a),v in W.items()))
    print("m=",m,"deg",sympy.degree(poly,h)," ",sympy.factor(poly))
