"""F_A(t_1..t_r) = [x^A] Alt_x det((x_i - t_i x_{i+1})^{a_j}), x_{r+1}=x_1.  Lemma: [t_1^k..t_r^k] F_A = (-1)^{rk} r! prod_a C(a,k), 0<=k<=min A."""
import itertools
from math import comb, factorial
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def pmul(P,Q,r):
    out={}
    for (ex1,et1),c1 in P.items():
        for (ex2,et2),c2 in Q.items():
            key=(tuple(a+b for a,b in zip(ex1,ex2)),tuple(a+b for a,b in zip(et1,et2)))
            out[key]=out.get(key,0)+c1*c2
    return {k:v for k,v in out.items() if v}
def row_power(i,a,r,perm):
    """(x_{perm i} - t_i x_{perm (i+1)})^a as poly in (x-exps, t-exps); alternation handled by permuting x indices"""
    out={}
    for k in range(a+1):
        ex=[0]*r; et=[0]*r
        ex[perm[i]]+=a-k; ex[perm[(i+1)%r]]+=k; et[i]+=k
        out[(tuple(ex),tuple(et))]=out.get((tuple(ex),tuple(et)),0)+comb(a,k)*(-1)**k
    return out
def F_coeff(A,k):
    r=len(A); tot=0; target_t=tuple([k]*r)
    for perm in itertools.permutations(range(r)):       # Alt over x-variables: x_i -> x_{perm(i)}
        s=sgn(perm)
        for tau in itertools.permutations(range(r)):
            poly={((0,)*r,(0,)*r):1}
            for i in range(r): poly=pmul(poly,row_power(i,A[tau[i]],r,perm),r)
            c=poly.get((tuple(A),target_t),0)
            tot+=s*sgn(tau)*c
    return tot
ok=True
for A in [(2,3,5),(1,3,4),(2,4,5),(1,2,3,4),(2,3,4,6)]:
    r=len(A)
    for k in range(0,min(A)+1):
        lhs=F_coeff(A,k); rhs=(-1)**(r*k)*factorial(r)
        for a in A: rhs*=comb(a,k)
        if lhs!=rhs: ok=False; print("  mismatch",A,k,lhs,rhs)
print("diagonal-flow lemma [t^k..t^k] F_A = (-1)^{rk} r! prod C(a,k) on sets of size 3-4, all 0<=k<=min A:",ok)
