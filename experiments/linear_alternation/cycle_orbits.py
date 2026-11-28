import itertools, cmath, pickle
import numpy as np
from math import comb, gcd, factorial
from fractions import Fraction
import sympy
K=pickle.load(open('kappa_cache.pkl','rb'))
def vand(x):
    r=1
    for i in range(len(x)):
        for j in range(i+1,len(x)): r*= (x[j]-x[i])
    return r
def Ba(a,m):
    v=[sum(a[:i]) for i in range(m)]
    rho=vand(v)/vand(a)
    Q=np.poly1d([1])
    for vi in v: Q=Q*np.poly1d([1,-vi])
    Qs=Q(np.poly1d([1,-1]))   # Q(z-1)
    return Qs*((-1)**(m-1)*m*rho), v, rho, Q
def coeffs(p,m): c=list(p.c[::-1]); return c+[0]*(m+1-len(c))
X=sympy.symbols('X')
for m in (4,5,6,7):
    mu=[cmath.exp(2j*cmath.pi*k/m) for k in range(m)]
    others=mu[1:]
    tot=np.poly1d([0]); geo=np.poly1d([0]); rhos={}
    prim=[mu[k] for k in range(1,m) if gcd(k,m)==1]
    geos=set()
    for q in prim:
        geos.add(tuple(round(((cmath.phase(q**i)/(2*cmath.pi))*m))%m for i in range(1,m)))
    for perm in itertools.permutations(range(1,m)):
        a=[mu[k] for k in perm]+[1]
        B,v,rho,Q=Ba(a,m); tot=tot+B
        if tuple(perm) in geos: geo=geo+B
    full=[complex(x) for x in coeffs(tot,m)]
    kap=K[m]
    print(f"m={m}: full sum z-coeffs = {[round(x.real,6) for x in full]}  (kappa: {kap})")
    T=comb(m+1,2)
    Gf=np.poly1d([0])
    for q in prim:
        Gf=Gf+ (np.poly1d([q-1,1])**m - np.poly1d([1]))*((-1)**(m-1)*m/(q-1)**T)
    print(f"     geometric part matches G_m formula: {np.allclose(coeffs(geo,m),coeffs(Gf,m))}; G_m = {[round(complex(x).real,4) for x in coeffs(Gf,m)]}")
    # Bezout functional
    h=len(prim)
    R=sympy.rem(X**(T-1), sympy.expand(sympy.cyclotomic_poly(m,X+1)), X)
    r=[sympy.Poly(R,X).coeff_monomial(X**j) for j in range(h)]
    def Lam(poly):
        c=coeffs(poly,m)
        return sum(sympy.Rational(r[k-1])/comb(m,k)*sympy.Rational(str(Fraction(complex(c[k]).real).limit_denominator(10**5))) for k in range(1,h+1))
    print(f"     remainder coeffs {r};  Lambda(G_m) = {Lam(Gf)} (claim {(-1)**(m-1)*m*h});  Lambda(full) = {Lam(tot)}")
