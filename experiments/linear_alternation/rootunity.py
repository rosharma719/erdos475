import itertools, cmath, pickle, sys
from fractions import Fraction
from math import factorial
import sympy
K=pickle.load(open('kappa_cache.pkl','rb'))
z=sympy.symbols('z')
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def B_at_roots(m):
    r=m-1; zeta=cmath.exp(2j*cmath.pi/m); t=[zeta**i for i in range(1,m)]
    # D(t,z) = (z+S) prod s_i prod_{i<j}(s_j-s_i) prod_i (z+S-s_i): polynomial in z of degree r+1; compute coefficients numerically
    import numpy as np
    S=sum(t); tot=np.zeros(m+1,dtype=complex)
    for p in itertools.permutations(range(r)):
        tt=[t[k] for k in p]; s=list(itertools.accumulate(tt))
        c=np.prod(s)*np.prod([s[j]-s[i] for i in range(r) for j in range(i+1,r)])
        poly=np.poly1d([1,S])                     # z+S
        for si in s: poly=poly*np.poly1d([1,S-si])
        coeffs=poly.c[::-1]*c*sgn(p)            # ascending in z
        tot[:len(coeffs)]+=coeffs
    Delta=np.prod([t[j]-t[i] for i in range(r) for j in range(i+1,r)])*np.prod(t)
    return tot/Delta
for m in range(3,int(sys.argv[1])+1):
    B=B_at_roots(m)
    re=[complex(x) for x in B]
    rat=[Fraction(x.real).limit_denominator(10**6) for x in re]
    imag=max(abs(x.imag) for x in re)
    kap=K[m]
    print(f"m={m}: max |imag| {imag:.1e};  z-coeffs (deg 0..m) = {[str(x) for x in rat]}")
    print(f"      kappa_(m,d) d=1..m = {kap}")
    nz=[(j,x) for j,x in enumerate(rat) if x]
    print("      ratios coeff_j / kappa_(m,?) attempts: j -> coeff/(kappa_(m,j) * j!) =",[str(x/(kap[j-1]*factorial(j))) if 1<=j<=m and kap[j-1] else '-' for j,x in enumerate(rat)])
