import sys, sympy
from fractions import Fraction
from math import factorial
from word_patterns import patterns, interp, H
from deformed_ext import Zpow
def G_actual(m,d):
    c=[Fraction(1,factorial(k)) for k in range(1,m+1)]
    R=Zpow(c,m,m-1)
    full=(1<<(2*m))-1
    mask=full & ~(1<<(d-1)) & ~(1<<(m+d-1))
    W=R.get(mask,{})
    return sympy.expand(sum(sympy.Rational(v.numerator,v.denominator)*sympy.ff(H,a) for (i,a),v in W.items()))
def mult_at(poly,r):
    k=0
    while poly!=0 and sympy.expand(poly.subs(H,r))==0:
        poly=sympy.quo(poly,H-r,H); k+=1
    return k
for m in range(2,int(sys.argv[1])+1):
    for d in range(1,m+1):
        hs=list(range(0,m*(m+1)//2+3))
        SAB,SBA=patterns(m,d,hs); pa=interp(SAB); pb=interp(SBA)
        eps=(-1)**(m-1); G=sympy.expand(pa+eps*pb)
        line=f"m={m} d={d}: deg(SAB,SBA)=({sympy.degree(pa,H)},{sympy.degree(pb,H)}) bound 2m-2={2*m-2}; "
        top=[mult_at(pa,-j) for j in range(1,m+2)]; bot=[mult_at(pb,j) for j in range(0,m+1)]
        line+=f"S_AB vanishes at h=-1,-2,..: {sum(1 for x in top if x)} consecutive-ish {top}; S_BA at h=0,1,..: {bot}; deg G={sympy.degree(G,H) if G!=0 else '-'}"
        if m<=4:
            Ga=G_actual(m,d); line+=f"; G = +-Z^(m-1) coeff: {sympy.expand(G-Ga)==0 or sympy.expand(G+Ga)==0}"
        print(line,flush=True)
