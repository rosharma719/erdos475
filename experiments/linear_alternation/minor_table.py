import itertools, sys, time
from fractions import Fraction
from math import gcd, factorial
from functools import reduce
from dual_checks import op, c_coef, to_ext, from_ext
import sympy
def balanced(n,k):
    return [(A,B) for A in itertools.combinations(range(1,n+1),k) for B in itertools.combinations(range(1,n+1),k) if sum(A)==sum(B)]
def det(M):
    M=[r[:] for r in M]; n=len(M); d=Fraction(1)
    for i in range(n):
        p=next((r for r in range(i,n) if M[r][i]!=0),None)
        if p is None: return Fraction(0)
        if p!=i: M[i],M[p]=M[p],M[i]; d=-d
        d*=M[i][i]
        for r in range(i+1,n):
            f=M[r][i]/M[i][i]
            if f:
                for c in range(i,n): M[r][c]-=f*M[i][c]
    return d
def bigpart(x,n):
    x=abs(int(x))
    if x==0: return 0
    for p in sympy.primerange(2,n+2):
        while x%p==0: x//=p
    return x
n=int(sys.argv[1]); t0=time.time()
bases={k:balanced(n,k) for k in range(1,n)}
def apply_T(vec,k):    # vec dict {(A,B):c} in B_k
    return from_ext(op(c_coef,to_ext(vec,n),n),n)
# P: columns images of U_iV_i
cols=[]
for i in range(1,n+1):
    v={((i,),(i,)):Fraction(1)}
    for k in range(1,n-1): v=apply_T(v,k)
    cols.append(v)
rowsB=bases[n-1]; ridx={r:i for i,r in enumerate(rowsB)}
Mx=[[Fraction(0)]*n for _ in rowsB]
for j,v in enumerate(cols):
    for r,c in v.items(): Mx[ridx[r]][j]=c
# keep nonzero rows
Mx=[r for r in Mx if any(r)]
print("n=",n,"P shape",len(Mx),"x",n,"time",round(time.time()-t0,1),flush=True)
# maximal minors: (n-1)x(n-1)
nr=len(Mx)
den=1
for r in Mx:
    for x in r: den=den*x.denominator//gcd(den,x.denominator)
minors=[]
for skip in range(n):
    sub=[[r[c]*den for c in range(n) if c!=skip] for r in Mx]
    minors.append(det(sub) if nr==n-1 else None)
if nr==n-1:
    g=reduce(gcd,[int(abs(m)) for m in minors if m!=0],0)
    print(" maximal-minor gcd (scaled): big part =",bigpart(g,n)," full:",sympy.factorint(g) if g else 0)
# seed space
H2=[Fraction(1-i,factorial(i+1)) for i in range(1,n+1)]
qn=[Fraction(0)]*(n-1)+[Fraction(1)]
def mv(M,v): return [sum(r[j]*v[j] for j in range(n)) for r in M]
a=mv(Mx,H2); b=mv(Mx,qn)
d2=1
for x in a+b: d2=d2*x.denominator//gcd(d2,x.denominator)
a=[int(x*d2) for x in a]; b=[int(x*d2) for x in b]
m2=[a[i]*b[j]-a[j]*b[i] for i in range(len(a)) for j in range(i+1,len(a))]
g2=reduce(gcd,[abs(m) for m in m2],0)
print(" 2x2 minors of [P(H2)|P(qn)]: gcd big part =",bigpart(g2,n)," factorint:",sympy.factorint(g2) if g2 else 0)
if n==5:
    Ms=sympy.Matrix([[sympy.Rational(x.numerator,x.denominator) for x in r] for r in Mx])
    ns=Ms.nullspace()[0]; den_=sympy.ilcm(*[sympy.fraction(x)[1] for x in ns]); v=[int(x*den_) for x in ns]; g=reduce(gcd,[abs(x) for x in v]); v=[x//g for x in v]
    print(" primitive kernel vector:",v," mod 17:",[x%17 for x in v])
print(" total time",round(time.time()-t0,1))
