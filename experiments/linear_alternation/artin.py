"""Exact coinvariant algebra R_n = Z[x_0..x_{n-1}]/(e_1..e_n) with Artin basis (exponent of x_i <= i)."""
from functools import lru_cache
from collections import defaultdict
def comps(k,d):
    if d==1: yield (k,);return
    for x in range(k+1):
        for y in comps(k-x,d-1): yield (x,)+y
class Ring:
    def __init__(s,n):
        s.n=n; s.rules=[[c for c in comps(i+1,n-i) if c[0]!=i+1] for i in range(n)]
        s.red=lru_cache(None)(s._red)
    def _red(s,a):
        n=s.n; i=next((i for i,k in enumerate(a) if k>i),n)
        if i==n: return {a:1}
        out=defaultdict(int)
        for c in s.rules[i]:
            b=list(a); b[i]-=i+1
            for j,v in enumerate(c,i): b[j]+=v
            for z,v in s.red(tuple(b)).items(): out[z]-=v
        return {z:v for z,v in out.items() if v}
    def nf(s,P):
        out=defaultdict(int)
        for mon,c in P.items():
            for z,v in s.red(mon).items(): out[z]+=c*v
        return {z:v for z,v in out.items() if v}
def pmul(P,Q):
    out=defaultdict(int)
    for a,c in P.items():
        for b,d in Q.items(): out[tuple(x+y for x,y in zip(a,b))]+=c*d
    return {k:v for k,v in out.items() if v}
def padd(P,Q,s=1):
    out=defaultdict(int,P)
    for k,v in Q.items(): out[k]+=s*v
    return {k:v for k,v in out.items() if v}
def var(n,i): 
    e=[0]*n; e[i]=1; return {tuple(e):1}
def const(n,c): return {(0,)*n:c}
def lin(n,idx):
    P={}
    for i in idx: P=padd(P,var(n,i))
    return P
def ppow(P,k,n):
    R=const(n,1)
    for _ in range(k): R=pmul(R,P)
    return R
