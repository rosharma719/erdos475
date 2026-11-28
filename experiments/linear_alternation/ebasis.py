import itertools, random, sys, pickle
from fractions import Fraction
import sympy
K=pickle.load(open('kappa_cache.pkl','rb'))
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def Bcoeffs(t,m):
    r=len(t); S=sum(t); tot=[Fraction(0)]*(m+1)
    Delta=Fraction(1)
    for i in range(r):
        for j in range(i+1,r): Delta*=(t[j]-t[i])
    for x in t: Delta*=x
    for p in itertools.permutations(range(r)):
        tt=[t[k] for k in p]; s=list(itertools.accumulate(tt))
        c=Fraction(sgn(p))
        for x in s: c*=x
        for i in range(r):
            for j in range(i+1,r): c*=(s[j]-s[i])
        if c==0: continue
        poly=[S,Fraction(1)]
        for si in s:
            new=[Fraction(0)]*(len(poly)+1)
            for d,co in enumerate(poly): new[d]+=co*(S-si); new[d+1]+=co
            poly=new
        for d,co in enumerate(poly): tot[d]+=co*c
    return [x/Delta for x in tot]
def parts(n,maxp=None):
    if maxp is None: maxp=n
    if n==0: yield (); return
    for k in range(min(n,maxp),0,-1):
        for rest in parts(n-k,k): yield (k,)+rest
def esym(t,k):
    return sum(sympy.prod(c) for c in itertools.combinations(t,k)) if k<=len(t) else 0
random.seed(1)
for m in range(int(sys.argv[2]) if len(sys.argv)>2 else 4,int(sys.argv[1])+1):
    r=m-1; pts=[]
    for _ in range(7):
        t=[Fraction(random.randint(-30,30),random.randint(1,5)) for _ in range(r)]
        while len(set(t))<r or 0 in t: t=[Fraction(random.randint(-30,30),random.randint(1,5)) for _ in range(r)]
        pts.append((t,Bcoeffs(t,m)))
    out=[]
    for j in range(1,5):
        if j>r: break
        P=list(parts(j))
        # coefficient of z^{m-j}? B is in z; packet uses w=z-1. Use z-coefficients as computed, degree m-j
        rows=[[sympy.Rational(sympy.prod(esym(t,k) for k in lam)) for lam in P] for t,_ in pts]
        rhs=[sympy.Rational(B[m-j]) for _,B in pts]
        A=sympy.Matrix(rows); bvec=sympy.Matrix(rhs)
        sol=A[:len(P),:].LUsolve(bvec[:len(P),:]) if True else None
        resid=(A*sol-bvec).norm()
        out.append((j,{''.join(map(str,l)):sol[i] for i,l in enumerate(P)},resid==0))
    print(f"m={m}:")
    for j,d,ok in out: print(f"   z^(m-{j}) coefficient in e-basis {d}  consistent: {ok}",flush=True)
