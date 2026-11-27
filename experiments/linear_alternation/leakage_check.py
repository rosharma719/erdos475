import sys, time, itertools
from fractions import Fraction
from math import factorial, gcd, lcm
from functools import reduce
src=open('hypersurface_checks.py').read()
exec(src[:src.index("random.seed(5)")])
def pf(n):
    n=abs(int(n)); s={};d=2
    if n==0: return {0:1}
    while d*d<=n:
        while n%d==0: s[d]=s.get(d,0)+1; n//=d
        d+=1
    if n>1: s[n]=s.get(n,0)+1
    return s
for m in range(3,int(sys.argv[1])+1):
    t0=time.time()
    cprime=[Fraction(1,factorial(k)) for k in range(1,m)]
    gm1=grad_formula(cprime,m-1)                          # g_{m-1} = grad F_{m-1}(c')
    full0=grad_formula(cprime+[Fraction(0)],m)            # grad F_m at (c',0); first m-1 entries = ell_m
    ell=full0[:m-1]; last=full0[m-1]
    cstar=[Fraction(1,factorial(k)) for k in range(1,m+1)]
    gst=grad_formula(cstar,m)
    t=Fraction(1,factorial(m))
    pred=[ell[i]+(-1)**(m-1)*m*t*gm1[i] for i in range(m-1)]
    ok10= pred==gst[:m-1] and gst[m-1]==0 and last==(-1)**(m-1)*m*Fs(cprime,m-1)
    # 2x2 minors of (ell, g)
    minors=[ell[i]*gm1[j]-ell[j]*gm1[i] for i in range(m-1) for j in range(i+1,m-1)]
    parallel=all(x==0 for x in minors)
    den=reduce(lcm,[x.denominator for x in minors],1) if minors else 1
    ints=[int(x*den) for x in minors]; g=reduce(gcd,[abs(x) for x in ints]) if ints else 0
    big=[q for q in pf(g) if q>m+1] if g else ['zero']
    print(f"m={m}: (10) gradient formula along the line holds: {ok10};  ell_m and g_(m-1) parallel: {parallel};  gcd of 2x2 minors (numerators over common denominator {den}) = {g}; prime factors > m+1: {big}   [{time.time()-t0:.1f}s]",flush=True)
    if m<=5:
        print(f"      g_(m-1) = {[str(x) for x in gm1]};  ell_m = {[str(x) for x in ell]}")
