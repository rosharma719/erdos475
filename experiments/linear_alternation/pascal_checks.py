"""Checks of the 'Pascal recurrence' report. kappa(A,I) = coeff of (x^A/A!) e_I in P_k (divided-power prefix wedge)."""
import itertools, math, re
from fractions import Fraction
from functools import lru_cache
from math import comb, gcd, factorial
# ---------- reference vectors c_{m,j} from the earlier exact results
C={}
for line in open('results_reported.txt'):
    m=int(re.match(r'm=(\d+)',line).group(1)); C[m]=[int(v) for v in re.search(r'\[(.*)\]',line).group(1).split(',') if v.strip()]
# (1) near-top Artin coefficients b and c
ok=True
for m,c in C.items():
    b={i:-sum(c[:i-1]) for i in range(2,m+1)}                         # b_i = -sum_{j<i} c_j
    back=[-b[2]]+[b[j]-b[j+1] for j in range(2,m)]+[b[m]]
    ok&=(back==c)
    gb=0
    for v in b.values(): gb=gcd(gb,abs(v))
    gc=0
    for v in c: gc=gcd(gc,abs(v))
    ok&=(gb==gc)
print("(1) c_1=-b_2, c_j=b_j-b_{j+1}, c_m=b_m, b_i=-sum_{j<i}c_j, gcd(b)=gcd(c): consistent on m=3..14:",ok)
# (2) first-two-coefficient gcd table
print("(2) gcd(c_1,c_2) for m=3..14:",[gcd(abs(C[m][0]),abs(C[m][1])) for m in range(3,15)])
print("    full content            :",[ (lambda v: __import__('functools').reduce(gcd,[abs(x) for x in v]))(C[m]) for m in range(3,15)])
# (3) direct kappa from the definition for small k (polynomial arithmetic with Fractions)
def pmul(p,q):
    o={}
    for a,c in p.items():
        for b,d in q.items():
            k=tuple(x+y for x,y in zip(a,b)); o[k]=o.get(k,0)+c*d
    return o
def ppowsum(k,j):                      # (x_1+..+x_k)^j restricted: handled via multinomial
    out={}
    def rec(i,left,cur,coef):
        if i==k-1:
            out[tuple(cur+[left])]=coef*1; return
        for a in range(left+1):
            rec(i+1,left-a,cur+[a],coef)
    # use multinomial coefficients
    out={}
    for e in itertools.product(range(j+1),repeat=k):
        if sum(e)==j:
            mc=factorial(j)
            for x in e: mc//=factorial(x)
            out[e]=mc
    return out
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def det(M):
    n=len(M)
    if n==0: return 1
    return sum((-1)**j*M[0][j]*det([r[:j]+r[j+1:] for r in M[1:]]) for j in range(n))
def kappa_direct(A,I):
    k=len(A)
    tot={}                                            # polynomial in x_1..x_k
    for perm in itertools.permutations(range(k)):
        s=sgn(perm)
        # prefix sums as polynomials: prefix t = sum of x_{perm[0..t]}
        entries=[[None]*k for _ in range(k)]
        for t in range(k):
            for si,i in enumerate(I):
                # (x_{perm[0]}+..+x_{perm[t]})^i / i!
                coeffs=ppowsum(t+1,i)
                poly={}
                for e,cc in coeffs.items():
                    full=[0]*k
                    for pos,ex in zip(perm[:t+1],e): full[pos]=ex
                    poly[tuple(full)]=Fraction(cc,factorial(i))
                entries[t][si]=poly
        # determinant of polynomial matrix (Leibniz)
        d={}
        for tau in itertools.permutations(range(k)):
            term={tuple([0]*k):Fraction(sgn(tau))}
            for t in range(k): term=pmul(term,entries[t][tau[t]])
            for kk,v in term.items(): d[kk]=d.get(kk,0)+s*v
        for kk,v in d.items(): tot[kk]=tot.get(kk,0)+v
    key=tuple(A)
    return tot.get(key,Fraction(0))*math.prod(factorial(a) for a in A)
# (4) Pascal recurrence
def parts(n,k,minv=1):
    if k==0:
        if n==0: yield ()
        return
    for a in range(minv,n//k+1 if k>0 else 0):
        pass
    def rec(n,k,minv):
        if k==0:
            if n==0: yield ()
            return
        if k==1:
            if n>=minv: yield (n,)
            return
        a=minv
        while a*k+k*(k-1)//2<=n:
            for rest in rec(n-a,k-1,a+1): yield (a,)+rest
            a+=1
    yield from rec(n,k,minv)
@lru_cache(None)
def kappa(A,I):
    k=len(A)
    if k==0: return 1
    if sum(A)!=sum(I): return 0
    tot=0
    for l in range(k):
        il=I[l]; Irest=I[:l]+I[l+1:]
        for Cc in parts(sum(I)-il,k-1):
            M=[[comb(a,c) for c in (0,)+Cc] for a in A]
            d=det(M)
            if d: tot+=(-1)**l*d*kappa(Cc,Irest)
    return tot
bad=0; n=0
for k in (1,2,3):
    for I in itertools.combinations(range(2,8),k):
        for A in parts(sum(I),k):
            if max(A)>sum(I): continue
            kd=kappa_direct(A,I); kr=kappa(A,I); n+=1
            if kd!=kr: bad+=1; print("  mismatch",A,I,kd,kr)
print(f"(4) Pascal recurrence vs direct definition: {n} (A,I) pairs with k=1,2,3, I ⊆ {{2..7}}: mismatches {bad}")
# (5) complementary contraction formula vs c_{m,j}
def contraction(m,r,restrictA=True):
    U=tuple(range(2,m+1)); tot=0
    for I in itertools.combinations(U,r):
        Ic=tuple(x for x in U if x not in I)
        for A in parts(sum(I),r):
            if restrictA and not set(A)<=set(U): continue
            Ac=tuple(x for x in U if x not in A)
            if len(Ac)!=m-1-r: continue
            tot+=(-1)**(r+sum(Ic))*kappa(A,I)*kappa(Ac,Ic)
    return tot
for m in range(3,9):
    got=[contraction(m,r) for r in range(0,m)]
    ref=C[m]
    rel="equal" if got==ref else ("negated" if got==[-x for x in ref] else "DIFFERENT")
    print(f"(5) m={m}: complementary-contraction vector vs c_m: {rel}   got={got if rel=='DIFFERENT' else ''}")
# (6) c_1 and c_2 formulas
for m in range(3,9):
    U=tuple(range(2,m+1)); S=sum(U)
    c1=(-1)**S*kappa(U,U)
    c2=(-1)**(S+1)*sum((-1)**a*kappa(tuple(x for x in U if x!=a),tuple(x for x in U if x!=a)) for a in U)
    print(f"(6) m={m}: (-1)^S kappa(U,U) = {c1}, c_1 = {C[m][0]};   formula for c_2 = {c2}, c_2 = {C[m][1]}")
# (7) Jacobi complementary minors of the Pascal matrix
n=7; ok=True; signs=set()
Pm=[[comb(a,b) for b in range(n)] for a in range(n)]
for k in range(1,5):
    for Aa in itertools.combinations(range(n),k):
        for D in itertools.combinations(range(n),k):
            Ac=[x for x in range(n) if x not in Aa]; Dc=[x for x in range(n) if x not in D]
            m1=det([[Pm[a][d] for d in D] for a in Aa]); m2=det([[Pm[a][d] for d in Ac] for a in Dc])
            if m1!=0 or m2!=0:
                signs.add((m1==m2, m1==-m2, (sum(Aa)+sum(D))%2))
print("(7) Jacobi: det P_{A,D} vs det P_{D^c,A^c} on 7x7 Pascal (flags: equal, negated, parity of sum A + sum D):",sorted(signs))
