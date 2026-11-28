import itertools, io, contextlib
from fractions import Fraction
from math import factorial, gcd, lcm
from functools import reduce
from deformed_ext import *
def mulg(a,b): return gw_mul(a,b)
def scal(a,c): return gw_scale(a,Fraction(c))
# (12) Y f Y = u_{m-1} u_m v_{m-1} v_m E_u E_v f   for f = u_a v_b
for m in (4,5):
    Y=gw_add(mulg(u(m-1,m),v(m-1,m)),scal(mulg(u(m,m),v(m,m)),Fraction(1,2)))
    sq=mulg(Y,Y)
    ok=True; n=0; nonzero=0
    for a in range(1,m+1):
        for b in range(1,m+1):
            f=mulg(u(a,m),v(b,m))
            lhs=mulg(mulg(Y,f),Y)
            if a+1<=m and b+1<=m:
                rhs=mulg(mulg(mulg(mulg(u(m-1,m),u(m,m)),v(m-1,m)),v(m,m)),mulg(u(a+1,m),v(b+1,m)))
            else: rhs={}
            n+=1; nonzero+=bool(lhs)
            if gw_add(lhs,rhs,-1): ok=False
    print(f"(12) m={m}: Y^2 = 0: {sq=={}};  Y f Y = u_(m-1)u_m v_(m-1)v_m E_uE_v f for f = u_a v_b, all a,b: {ok} ({n} cases, {nonzero} with nonzero value)")
# (6) alternating sum identity sum_d (-1)^{d-1} kappa_{m,d} = 0  and adjacent-gradient minors
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
kap={}
for m in range(3,12):
    kap[m]=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
print("(6) sum_d (-1)^(d-1) kappa_(m,d) for m = 3..11:",[sum((-1)**(d-1)*kap[m][d-1] for d in range(1,m+1)) for m in range(3,12)])
def G(m):
    return [sum((-1)**(e-d)*factorial(e)//factorial(e-d)*kap[m][e-1] for e in range(d,m+1)) for d in range(1,m+1)]
print("adjacent-gradient minors, G_{m,d} = sum_{e>=d} (-1)^{e-d} e!/(e-d)! kappa_{m,e}:")
table={}
for m in range(4,12):
    g1=G(m); g0=G(m-1)+[0]
    minors=[g1[i]*g0[j]-g1[j]*g0[i] for i in range(m) for j in range(i+1,m)]
    gg=reduce(gcd,[abs(x) for x in minors]) if minors else 0
    table[m]=gg
    print(f"  m={m}: gcd of 2x2 minors of (G_m, G_(m-1) padded) = {gg}")
print("report: 4:4, 5:0, 6:64, 7:2240, 8:192, 9:3024, 10:9216, 11:2816")
