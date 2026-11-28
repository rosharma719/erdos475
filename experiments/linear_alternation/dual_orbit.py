import sys
from fractions import Fraction
from math import factorial
from dual_checks import op, d_coef, c_coef, to_ext, from_ext
import sympy
def pair(f,g,n):
    tot=Fraction(0)
    for m1,c1 in f.items():
        for m2,c2 in g.items():
            if set(m1)&set(m2): continue
            new=m1+m2; inv=sum(1 for i in range(len(new)) for j in range(i+1,len(new)) if new[i]>new[j])
            tot+=c1*c2*(-1)**inv
    return tot
def gen(n,idx,kind):  # id of U_idx / V_idx
    return idx if kind=='U' else n+idx
n=int(sys.argv[1]); start=int(sys.argv[2])
f={(start,n+start):Fraction(1)}     # U_start V_start in ext coordinates
print("n=",n,"start q_",start)
for k in range(1,n-1):
    f=op(d_coef,f,n)
    print(" step",k,": support size",len(f))
    if len(f)<=0:
        for m,c in sorted(f.items()):
            Us=tuple(x for x in m if x<=n); Vs=tuple(x-n for x in m if x>n)
            print("   U",Us,"V",Vs,c, sympy.factorint(abs(c.numerator)),"/",sympy.factorint(c.denominator))
# pair with H2
H2={(i,n+i):Fraction(1-i,factorial(i+1)) for i in range(1,n+1)}
print(" <H2, g> =",pair(H2,f,n))
