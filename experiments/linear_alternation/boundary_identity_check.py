"""Is B_m = Q_m * prod_{j=1}^{m-1} y_j  (Q_m = F_{m-1}(w_1..w_{m-1}))  the same class in R_m as the interval polynomial F_m of the linear packet?
Compare c'_{m,j} = lambda_m(w_j B_m) with c_{m,j} = lambda_m(w_j F_m) (brute force over all m! permutations, exact integers)."""
import itertools, sys, math
from math import gcd
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def Fint(a):                      # all intervals of length>=2 except the full one
    m=len(a); f=1
    for i in range(m):
        s=a[i]
        for j in range(i+1,m):
            s+=a[j]
            if i==0 and j==m-1: continue
            f*=s
    return f
def run(m):
    pt=list(range(1,m+1)); d=1
    for i in range(m):
        for j in range(i+1,m): d*=pt[j]-pt[i]
    cF=[0]*m; cB=[0]*m
    for p in itertools.permutations(range(m)):
        s=sgn(p); w=[pt[k] for k in p]
        F=Fint(w)
        Q=Fint(w[:m-1]) if m-1>=2 else 1          # Q_m = F_{m-1}(w_1..w_{m-1})
        pref=1; y=0
        for j in range(m-1):
            y+=w[j]; pref*=y                       # y_1..y_{m-1}
        B=Q*pref
        for j in range(m):
            cF[j]+=s*w[j]*F; cB[j]+=s*w[j]*B
    assert all(x%d==0 for x in cF+cB)
    return [x//d for x in cF],[x//d for x in cB]
for m in range(4,int(sys.argv[1])+1):
    cF,cB=run(m)
    rel="equal" if cF==cB else ("negatives" if cF==[-x for x in cB] else "DIFFERENT")
    g=0
    for x in cB: g=gcd(g,abs(x))
    print(f"m={m}: c'(B_m) vs c(F_m): {rel};  content {g};  sum={sum(cB)};  reversal c_(m+1-j) = (-1)^N c_j: {all(cB[m-1-j]==(-1)**(m*(m-1)//2)*cB[j] for j in range(m))}")
    if m<=8: print("   c' =",cB)
