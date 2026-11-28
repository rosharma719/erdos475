"""Integral content of the class [Q_m] in R_m^{D_m}: gcd over all degree-m monomials g of lambda_m(Q_m g)."""
import itertools, sys, math
from math import gcd
from functools import reduce
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def Fint(a):
    m=len(a); f=1
    for i in range(m):
        s=a[i]
        for j in range(i+1,m):
            s+=a[j]
            if i==0 and j==m-1: continue
            f*=s
    return f
def monos(n,d):
    def rec(k,left):
        if k==1: yield (left,); return
        for a in range(left+1):
            for r in rec(k-1,left-a): yield (a,)+r
    return list(rec(n,d))
for m in range(int(sys.argv[2]) if len(sys.argv)>2 else 4,int(sys.argv[1])+1):
    pt=list(range(1,m+1)); dlt=1
    for i in range(m):
        for j in range(i+1,m): dlt*=pt[j]-pt[i]
    G=monos(m,m)
    tot=[0]*len(G)
    for p in itertools.permutations(range(m)):
        s=sgn(p); w=[pt[k] for k in p]; q=s*Fint(w[:m-1])
        for idx,g in enumerate(G):
            v=q
            for e,x in zip(g,w):
                if e: v*=x**e
            tot[idx]+=v
    vals=[t//dlt for t in tot]; assert all(t%dlt==0 for t in tot)
    c=reduce(gcd,[abs(x) for x in vals])
    print(f"m={m}: content of [Q_m] (gcd over {len(G)} degree-m monomials) = {c}",flush=True)
