import sys
from fractions import Fraction
from math import factorial
from dual_checks import op, c_coef, to_ext, from_ext
import sympy
def T(f,n): return from_ext(op(c_coef,to_ext(f,n),n),n)
def Tpow(f,n,k):
    for _ in range(k): f=T(f,n)
    return f
def coords(f,n):
    out={}
    for (A,B),c in f.items():
        assert A==B and len(A)==n-1; d=[x for x in range(1,n+1) if x not in A][0]; out[d]=c
    return [out.get(d,Fraction(0)) for d in range(1,n+1)]
def seed(n): return {((i,),(i,)):Fraction(1-i,factorial(i+1)) for i in range(1,n+1)}
def sectors_ok(n):
    # block triangularity: T never removes U_n or V_n
    import itertools
    bad=0
    for k in range(0,n):
        for A in itertools.combinations(range(1,n+1),k):
            for B in itertools.combinations(range(1,n+1),k):
                if sum(A)!=sum(B): continue
                im=T({(A,B):Fraction(1)},n)
                for (A2,B2) in im:
                    if (n in A and n not in A2) or (n in B and n not in B2): bad+=1
    return bad==0
for n in range(4,int(sys.argv[1])+1):
    v=coords(Tpow(seed(n),n,n-2),n)
    w=coords(Tpow({((n,),(n,)):Fraction(1)},n,n-2),n)
    vprev=coords(Tpow(seed(n-1),n-1,n-3),n-1)
    c=Fraction(-(n-1),factorial(n+1))
    corr=[v[i]-c*w[i] for i in range(n)]
    # is w = +- q_n v_{n-1}, i.e. w[d]=+-vprev[d] for d<n ?
    ratio_w=set(w[i]/vprev[i] for i in range(n-1) if vprev[i]!=0)
    # projection of corr onto w
    M=sympy.Matrix([[sympy.Rational(x.numerator,x.denominator) for x in w],[sympy.Rational(x.numerator,x.denominator) for x in corr]])
    parallel=M.rank()<=1
    mu=None
    if parallel:
        i=next(i for i in range(n) if w[i]!=0); mu=corr[i]/w[i]
    print(f"n={n}: block-triangular {sectors_ok(n) if n<=6 else 'skip'};  w_n/(q_n v_(n-1)) = {ratio_w};  correction parallel to w_n: {parallel}" + (f", corr = {mu} * w, total scalar c+mu = {c+mu} = {sympy.factorint(abs((c+mu).numerator)) if c+mu else 0}/{sympy.factorint((c+mu).denominator) if c+mu else ''}" if parallel else ""))
    if not parallel:
        # transverse part: component of v orthogonal-ish: report 2x2 minors gcd large-prime part of [w|v]
        from math import gcd
        from functools import reduce
        den=1
        for x in v+w: den=den*x.denominator//gcd(den,x.denominator)
        a=[int(x*den) for x in v]; b=[int(x*den) for x in w]
        mins=[a[i]*b[j]-a[j]*b[i] for i in range(n) for j in range(i+1,n)]
        g=reduce(gcd,[abs(x) for x in mins],0)
        big=g
        for p in sympy.primerange(2,n+3):
            while big and big%p==0: big//=p
        print(f"      v_n not parallel to w_n; large-prime (>n+2) part of gcd of 2x2 minors of [v|w]: {big}")
