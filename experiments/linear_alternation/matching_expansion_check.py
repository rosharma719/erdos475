"""(1) kappa(A,I) = sum over nonneg integer matrices M (row sums I, col sums A) with a unique perfect matching of
sgn(pi_M) * l(D_M) * W(M),  W = prod_s a_s! / prod m_rs!,  l = # linear extensions of the contracted DAG.
(2) component expansion of C^_m(z) = sum_r C(n,r) c_{m,r+1} z^r."""
import itertools, math, re, sys, time
from fractions import Fraction
from math import comb, factorial
from functools import lru_cache
sys.argv=[sys.argv[0]]
import pascal_checks as PC           # reuse kappa (Pascal recurrence) and reference vectors C  (module prints its own checks on import)
kappa=PC.kappa; C=PC.C
def tables(rows,cols):
    """all nonneg integer matrices with given row sums and column sums"""
    k=len(rows)
    def rec(r,remcols):
        if r==k:
            if all(c==0 for c in remcols): yield []
            return
        def fill(s,left,cur):
            if s==len(cols):
                if left==0:
                    yield tuple(cur)
                return
            for x in range(min(left,remcols[s])+1):
                cur.append(x); yield from fill(s+1,left-x,cur); cur.pop()
        for row in fill(0,rows[r],[]):
            newrem=[c-x for c,x in zip(remcols,row)]
            for rest in rec(r+1,newrem): yield [row]+rest
    yield from rec(0,list(cols))
def perm_sign(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def analyse(M):
    """return (pi, sign, components list as lists of row indices, ell) if unique perfect matching else None"""
    k=len(M); found=[]
    for p in itertools.permutations(range(k)):
        if all(M[r][p[r]]>0 for r in range(k)):
            found.append(p)
            if len(found)>1: return None
    if not found: return None
    pi=found[0]; inv={pi[r]:r for r in range(k)}
    succ=[set() for _ in range(k)]             # vertex r (row r / col pi[r]); edge r -> r' if M[r][pi[r']]>0
    for r in range(k):
        for s in range(k):
            if M[r][s]>0 and s!=pi[r]: succ[r].add(inv[s])
    # linear extensions of DAG (count) via DP on subsets
    pred=[0]*k
    for r in range(k):
        for t in succ[r]: pred[t]|=1<<r
    @lru_cache(None)
    def count(mask):
        if mask==(1<<k)-1: return 1
        return sum(count(mask|(1<<v)) for v in range(k) if not mask>>v&1 and pred[v]&~mask==0)
    ell=count(0)
    # weak components
    comp=list(range(k))
    def find(x):
        while comp[x]!=x: comp[x]=comp[comp[x]]; x=comp[x]
        return x
    for r in range(k):
        for t in succ[r]: comp[find(r)]=find(t)
    groups={}
    for r in range(k): groups.setdefault(find(r),[]).append(r)
    return pi,perm_sign(pi),list(groups.values()),ell
def weight(M,cols):
    w=Fraction(math.prod(factorial(a) for a in cols))
    for row in M:
        for x in row: w/=factorial(x)
    return w
# ---- (1)
bad=0;n=0
for k in (1,2,3,4):
    for I in itertools.combinations(range(2,8),k):
        for A in PC.parts(sum(I),k):
            if max(A)>sum(I): continue
            tot=0
            for M in tables(I,A):
                res=analyse(M)
                if res is None: continue
                pi,sg,gr,ell=res
                tot+=sg*ell*weight(M,A)
            n+=1
            if tot!=kappa(A,I): bad+=1; print("  mismatch",A,I,tot,kappa(A,I))
print(f"(1) unique-matching expansion vs Pascal recurrence: {n} (A,I) pairs, k=1..4, I ⊆ {{2..7}}: mismatches {bad}")
# ---- (2)
for m in range(3,int(sys.argv[1]) if len(sys.argv)>1 else 6):
    pass
def boundary_poly(m):
    U=tuple(range(2,m+1)); nn=m-1
    poly=[Fraction(0)]*(nn+1); ident=[Fraction(0)]*(nn+1); cnt=0
    for M in tables(U,U):
        res=analyse(M)
        if res is None: continue
        cnt+=1
        pi,sg,gr,ell=res
        mu=sg*ell*weight(M,U)
        # product over components of ((-z)^k + (-1)^s), s = sum of row margins U[r] of the component's vertices
        prod=[Fraction(1)]
        for g in gr:
            k=len(g); s=sum(U[r] for r in g)
            fac=[Fraction(0)]*(k+1); fac[k]+=(-1)**k; fac[0]+=(-1)**s
            new=[Fraction(0)]*(len(prod)+k)
            for i,a in enumerate(prod):
                for j,b in enumerate(fac): new[i+j]+=a*b
            prod=new
        for i,a in enumerate(prod): poly[i]+=mu*a
        if all(M[r][r]==U[r] for r in range(nn)):
            for i,a in enumerate(prod): ident[i]+=mu*a
    return poly,ident,cnt
for m in (3,4,5,6):
    t0=time.time()
    poly,ident,cnt=boundary_poly(m); nn=m-1
    lhs=[comb(nn,r)*C[m][r] for r in range(nn+1)]
    rel="equal" if poly==lhs else ("negated" if poly==[-x for x in lhs] else "DIFFERENT")
    print(f"(2) m={m}: unique-matching tables {cnt}; component expansion vs sum_r C(n,r)c_(r+1) z^r: {rel}   ({time.time()-t0:.0f}s)",flush=True)
    if m==3: print("    identity-matching contribution:",[str(x) for x in ident]," rest:",[str(a-b) for a,b in zip(poly,ident)])
    nfact=math.factorial(nn)
    expect=[Fraction(0)]*(nn+1); pr=[Fraction(nfact)]
    for i in range(2,m+1):
        fac=[Fraction((-1)**i),Fraction(-1)]; new=[Fraction(0)]*(len(pr)+1)
        for a,x in enumerate(pr):
            for b,y in enumerate(fac): new[a+b]+=x*y
        pr=new
    print("    identity contribution equals n! prod((-1)^i - z):", ident==pr)
