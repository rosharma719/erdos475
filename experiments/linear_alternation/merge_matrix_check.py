import itertools, io, contextlib, math, sys
from fractions import Fraction
from math import comb, factorial, gcd
from functools import reduce
with contextlib.redirect_stdout(io.StringIO()):
    import pascal_checks as PC
    import witt_checks as WC
kappa=PC.kappa
dstar=WC.dstar; fac=WC.fac
def W_basis(m):
    """sets K of size m-2, entries >=2 distinct, with excess sum(k-1) = N_m"""
    N=m*(m-1)//2; out=[]
    def rec(start,left,size,cur):
        if size==0:
            if left==0: out.append(tuple(cur))
            return
        a=start
        while (a-1)*size+0<=left:
            cur.append(a); rec(a+1,left-(a-1),size-1,cur); cur.pop(); a+=1
    rec(2,N,m-2,[])
    return sorted(out)
# dimension P(m-1)-1
def pnum(n):
    p=[1]+[0]*n
    for k in range(1,n+1):
        for i in range(k,n+1): p[i]+=p[i-k]
    return p[n]
print("dim W_{m-2}^{N_m} vs P(m-1)-1:",[(m,len(W_basis(m)),pnum(m-1)-1) for m in range(4,13)])
# merge vector b_m = d* e_{U_m} restricted to indices >=2
for m in (6,):
    U=tuple(range(2,m+1)); ds=dstar(U)
    basis=W_basis(m)
    print(f"m={m}: basis (sorted) {basis}")
    print("   d*e_U (adjoint of d; coefficients in the factorial-pairing adjoint):",{k:str(v) for k,v in ds.items()})
    order=[(2,3,4,10),(2,3,5,9),(2,3,6,8),(2,4,5,8),(2,4,6,7),(3,4,5,7)]
    print("   merge coefficients in the report's order:",[str(ds.get(K,0)) for K in order])
    # matrix A_{I,J} = kappa(J,I)
    A=[[kappa(J,I) for J in order] for I in order]
    for r in A: print("   ",r)
    from schur_checks import det
    print("   det A =",det(A), "  report 18208418112 =",18208418112)
    b=[-1,2,-1,-3,2,4]
    Ab=[sum(A[i][j]*b[j] for j in range(6)) for i in range(6)]
    AtB=[sum(A[j][i]*b[j] for j in range(6)) for i in range(6)]
    print("   A b (A_{I,J}=kappa(J,I), report's b_6) =",Ab,"   A^T b =",AtB,"  report: [10,52,74,102,92,88]")
    # column of M(e_U) on sets containing 1: kappa(U,{1}+K)
    v=[kappa(U,(1,)+K) for K in order]; print("   kappa(U_m,{1}+K) for K in report order:",v)
    print("   kappa(U_m,U_m) =",kappa(U,U))
