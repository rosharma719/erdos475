"""Normal form of the residual cycle polynomial f_m in Z[x_1..x_m]/(e_1..e_m) via the triangular
basis h_k(x_k..x_m) (leading monomial x_k^k, lex x_1>...>x_m); content gamma_m = gcd of coefficients."""
import sys, time
from math import gcd
from functools import reduce, lru_cache
from itertools import combinations_with_replacement
m=int(sys.argv[1])
def hpoly(k,start):   # h_k(x_start..x_m) as list of exponent tuples (full length m)
    vars_=list(range(start,m)); out=[]
    for combo in combinations_with_replacement(vars_,k):
        e=[0]*m
        for v in combo: e[v]+=1
        out.append(tuple(e))
    return out
H={}
@lru_cache(maxsize=None)
def red(mono):
    # returns dict normal form of monomial
    for k in range(m):           # variable index k has bound k+1 (x_{k+1}^{k+1})
        if mono[k]>=k+1:
            base=list(mono); base[k]-= (k+1)
            res={}
            for j in range(0,k+1):     # -sum_{j<=k} x_k^j h_{k+1-j}(x_{k+1}..)
                for e in H.setdefault((k+1-j,k+1),hpoly(k+1-j,k+1)):
                    nm=list(base); nm[k]+=j
                    nm=[a+b for a,b in zip(nm,e)]
                    for kk,vv in red(tuple(nm)).items():
                        res[kk]=res.get(kk,0)-vv
            return {kk:vv for kk,vv in res.items() if vv}
    return {mono:1}
def mul_linear(P,idxs):   # multiply by sum_{i in idxs} x_i
    out={}
    for mono,c in P.items():
        for i in idxs:
            nm=list(mono); nm[i]+=1
            for kk,vv in red(tuple(nm)).items(): out[kk]=out.get(kk,0)+c*vv
    return {k:v for k,v in out.items() if v}
t0=time.time()
P={tuple([0]*m):1}
for i in range(2,m+1):
    for j in range(i+1,m+1):
        if (i,j)==(2,m): continue
        P=mul_linear(P,list(range(i-1,j)))
g=reduce(gcd,[abs(v) for v in P.values()],0)
print(f"m={m}: nonzero normal-form coefficients {len(P)}, content gamma_m = {g}  ({time.time()-t0:.0f}s)")
