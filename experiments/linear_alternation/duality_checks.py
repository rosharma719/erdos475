"""c_T(J) := [t^J] Alt_t Delta_J(T t) over F_p (T invertible), J increasing subset of {0..p-1}, |J|=r.
Test (2): c_T(J) = det(T)^{p-1} c_{T^{-1}}(J^vee),  J^vee = sorted {p-1-j}."""
import itertools, random, sys
from math import factorial, comb
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def coeff_prod(T,b,e,p):
    """[t^e] prod_i (sum_l T[i][l] t_l)^{b_i} over F_p; DP over rows with exponent vectors bounded by e"""
    r=len(T); states={tuple([0]*r):1}
    for i in range(r):
        new={}
        # expansion of (sum_l T[i][l] t_l)^{b_i}: all compositions of b_i into r parts
        comps=[]
        def rec(l,left,cur):
            if l==r-1: comps.append(tuple(cur+[left])); return
            for a in range(left+1): rec(l+1,left-a,cur+[a])
        rec(0,b[i],[])
        terms=[]
        for c in comps:
            coef=factorial(b[i])
            for x in c: coef//=factorial(x)
            for l,x in enumerate(c): coef*=pow(T[i][l],x,p) if x else 1
            coef%=p
            if coef: terms.append((c,coef))
        for st,v in states.items():
            for c,coef in terms:
                ns=tuple(s+x for s,x in zip(st,c))
                if all(n<=ee for n,ee in zip(ns,e)):
                    new[ns]=(new.get(ns,0)+v*coef)%p
        states=new
    return states.get(tuple(e),0)
def cT(T,J,p):
    r=len(J); tot=0
    for sig in set(itertools.permutations(J)):               # distinct exponent vectors e = permutation of J
        # sign of the permutation sorting J into sig
        idx=[J.index(x) for x in sig]; s=sgn(idx)
        c=0
        for tau in itertools.permutations(range(r)):
            b=[J[tau[i]] for i in range(r)]
            c+=sgn(tau)*coeff_prod(T,b,sig,p)
        tot+=s*c
    return tot%p
def det(M,p):
    r=len(M)
    if r==1: return M[0][0]%p
    return sum((-1)**j*M[0][j]*det([row[:j]+row[j+1:] for row in M[1:]],p) for j in range(r))%p
def inv(M,p):
    r=len(M); d=det(M,p); di=pow(d,-1,p)
    adj=[[((-1)**(i+j)*det([row[:i]+row[i+1:] for k,row in enumerate(M) if k!=j],p))%p for j in range(r)] for i in range(r)]
    return [[adj[i][j]*di%p for j in range(r)] for i in range(r)]
random.seed(1)
for p in (5,7):
    for r in (2,3):
        bad=0;n=0;nz=0
        for _ in range(12 if r==2 else 6):
            while True:
                T=[[random.randrange(p) for _ in range(r)] for _ in range(r)]
                if det(T,p): break
            J=tuple(sorted(random.sample(range(p),r)))
            Jv=tuple(sorted(p-1-j for j in J))
            lhs=cT(T,J,p); rhs=pow(det(T,p),p-1,p)*cT(inv(T,p),Jv,p)%p
            n+=1; nz+= (lhs!=0)
            if lhs!=rhs: bad+=1
        print(f"p={p}, r={r}: duality (2) c_T(J) = det(T)^(p-1) c_(T^-1)(J^vee): {n} random (T,J), mismatches {bad} (nonzero lhs in {nz})",flush=True)
