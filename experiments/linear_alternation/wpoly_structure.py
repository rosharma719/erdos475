import sys, time
from fractions import Fraction
from math import comb, factorial, gcd
from functools import reduce
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def pmul(p,q):
    o=[Fraction(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q): o[i+j]+=a*b
    return o
def binom_poly(k):
    p=[Fraction(1)]
    for i in range(k): p=pmul(p,[Fraction(-i),Fraction(1)])
    return [c/factorial(k) for c in p]
def Wpoly(m):
    K=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
    W=[Fraction(0)]*m
    for d in range(1,m+1):
        for i,c in enumerate(binom_poly(d-1)): W[i]+=d*K[d-1]*c
    return trim(W)
def trim(p):
    p=p[:]
    while p and p[-1]==0: p.pop()
    return p
def to_z(W):                     # h=(z-1)/2
    out=[Fraction(0)]*len(W); base=[Fraction(1)]
    for k,c in enumerate(W):
        for i,x in enumerate(base): out[i]+=c*x
        base=pmul(base,[Fraction(-1,2),Fraction(1,2)])
    return trim(out)
def pdivmod(a,b):
    a=a[:]; q=[Fraction(0)]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and a:
        c=a[-1]/b[-1]; d=len(a)-len(b); q[d]=c
        for i,x in enumerate(b): a[i+d]-=c*x
        a=trim(a)
    return trim(q),a
def pgcd(a,b):
    while b:
        a,b=b,pdivmod(a,b)[1]
    return [x/a[-1] for x in a] if a else a
def normalize(p):
    """primitive integer polynomial (content removed) with positive leading coeff"""
    from math import lcm
    den=1
    for x in p: den=lcm(den,x.denominator)
    ints=[int(x*den) for x in p]; g=reduce(gcd,[abs(v) for v in ints])
    ints=[v//g for v in ints]
    if ints[-1]<0: ints=[-v for v in ints]
    return ints,g,den
Ws={}
M=int(sys.argv[1])
for m in range(3,M+1):
    Ws[m]=to_z(Wpoly(m))
    ints,g,den=normalize(Ws[m])
    print(f"m={m}: W_m(z) = (content {g}/{den}) * primitive {ints}",flush=True)
print("--- ratios and gcds between consecutive/related ranks")
for m in range(4,M+1):
    for s in (1,2,3,4):
        if m-s>=3:
            q,rem=pdivmod(Ws[m],Ws[m-s])
            if not rem: 
                print(f"  W_{m} = ({[str(x) for x in q]}) * W_{m-s}")
            g=pgcd(Ws[m],Ws[m-s])
            if len(g)>1: print(f"  gcd(W_{m}, W_{m-s}) has degree {len(g)-1}: {[str(x) for x in g]}")
