"""f_{A,b}(lambda): terms of [t^A] Alt_t Delta_A(C_lambda t) whose last-row exponent is b; test f_{A,b}(lam) = (-1)^{r-1+L-b} lam^b f_{A,b}(1/lam) over Z."""
import itertools
from math import factorial
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def coeff_row_products(r,b,e):
    """[t^e] prod_{i=1}^{r} (row_i)^{b_i}, row_i = t_i - t_{i+1} (i<r), row_r = lam*t_1 + t_r ; returns {lam_power: coeff}"""
    states={(tuple([0]*r),0):1}
    for i in range(r):
        new={}
        # row i: terms: (coef, var index, lam power)
        if i<r-1: lin=[(1,i,0),(-1,i+1,0)]
        else: lin=[(1,0,1),(1,r-1,0)]
        # expand lin^b_i : choose how many times each of the 2 terms
        for k in range(b[i]+1):
            coef=factorial(b[i])//(factorial(k)*factorial(b[i]-k))
            (c1,v1,l1),(c2,v2,l2)=lin
            c=coef*(c1**k)*(c2**(b[i]-k)); dv=[0]*r; dv[v1]+=k; dv[v2]+=b[i]-k
            dl=l1*k+l2*(b[i]-k)
            for (st,lp),v in states.items():
                ns=tuple(s+x for s,x in zip(st,dv))
                if all(n<=ee for n,ee in zip(ns,e)):
                    key=(ns,lp+dl); new[key]=new.get(key,0)+v*c
        states=new
    out={}
    for (st,lp),v in states.items():
        if st==tuple(e) and v: out[lp]=out.get(lp,0)+v
    return out
def f_comp(A,b):
    r=len(A); res={}
    for sig in set(itertools.permutations(A)):
        idx=[A.index(x) for x in sig]; s=sgn(idx)
        for tau in itertools.permutations(range(r)):
            if A[tau[r-1]]!=b: continue
            ex=[A[tau[i]] for i in range(r)]
            for lp,c in coeff_row_products(r,ex,sig).items():
                res[lp]=res.get(lp,0)+s*sgn(tau)*c
    return {k:v for k,v in res.items() if v}
bad=0;n=0;nontriv=0
for A in [(1,2,3),(2,3,4),(1,3,5),(2,3,5),(1,2,4,5),(2,3,4,5),(1,3,4,6),(0,2,3,5),(3,4,5,6),(1,2,3,4,6)]:
    r=len(A); L=sum(A)
    for b in A:
        f=f_comp(A,b); n+=1
        # reciprocal: coefficients of lam^k  vs lam^(b-k)
        sign=(-1)**(r-1+L-b)
        rec={b-k:sign*v for k,v in f.items()}
        if f: nontriv+=1
        if rec!=f: bad+=1; print("  mismatch A=",A,"b=",b,f,rec)
    tot={}
    for b in A:
        for k,v in f_comp(A,b).items(): tot[k]=tot.get(k,0)+v
print(f"(6) componentwise reciprocity f_(A,b)(lam) = (-1)^(r-1+L-b) lam^b f_(A,b)(1/lam): {n} (A,b) cases ({nontriv} with f != 0), mismatches {bad}")

def f_total(A):
    tot={}
    for b in A:
        for k,v in f_comp(A,b).items(): tot[k]=tot.get(k,0)+v
    return {k:v for k,v in tot.items() if v}
bad=0;n=0
for A in [(1,2,3),(2,3,4),(1,3,5),(2,3,5),(1,2,4,5),(2,3,4,5),(1,3,4,6),(3,4,5,6),(1,2,3,4,6),(2,3,5,6),(1,4,5,7)]:
    r=len(A); L=sum(A); M=max(A)
    fa=f_total(A); lhs=fa.get(M,0)
    Ap=tuple(x for x in A if x!=M)
    rhs=(-1)**(r-1+L-M)*f_total(Ap).get(0,0) if len(Ap)>0 else None
    n+=1
    if lhs!=rhs: bad+=1; print("  mismatch",A,lhs,rhs)
print(f"(5) [lam^M] f_A = (-1)^(r-1+L-M) f_(A minus M)(0): {n} sets, mismatches {bad}")
