"""P_{m,d,j} = lambda_m(Q_m w_j^d e_{m-d}(y)),  Q_m = F_{m-1}(w_1..w_{m-1}),  y_k = w_1+..+w_k (y_0=0).
Checks: first row = boundary vector; rank-lowering identity; generating-function descent; quadratic packets; counterexamples."""
import itertools, math, sys
from math import gcd, comb, factorial
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
def esym(vals,kmax):
    e=[1]+[0]*kmax
    for v in vals:
        for k in range(kmax,0,-1): e[k]+=v*e[k-1]
    return e
def lam_generic(m,func):
    """lambda_m of polynomial given as function of the permuted point -> exact"""
    pt=list(range(1,m+1)); d=1
    for i in range(m):
        for j in range(i+1,m): d*=pt[j]-pt[i]
    tot=0
    for p in itertools.permutations(range(m)):
        tot+=sgn(p)*func([pt[k] for k in p])
    assert tot%d==0
    return tot//d
def pairing(m):
    """returns P[d][j] (d=1..m-1, j=1..m), A[i][j], H[i][j] (i,j=1..m) all via one pass over permutations"""
    pt=list(range(1,m+1)); dlt=1
    for i in range(m):
        for j in range(i+1,m): dlt*=pt[j]-pt[i]
    P=[[0]*m for _ in range(m)]; A=[[0]*m for _ in range(m)]; H=[[0]*m for _ in range(m)]
    for p in itertools.permutations(range(m)):
        s=sgn(p); w=[pt[k] for k in p]
        Q=Fint(w[:m-1]) if m>=3 else 1
        y=[]; acc=0
        for k in range(m-1): acc+=w[k]; y.append(acc)       # y_1..y_{m-1}
        e=esym(y,m-1)
        prodk=1
        for k in range(1,m-1): prodk*=y[k]                   # y_2..y_{m-1}
        base=s*Q
        for j in range(m):
            wj=w[j]; pw=1
            for d in range(1,m):
                pw*=wj
                P[d][j]+=base*pw*e[m-d]
        for i in range(m):
            for j in range(m):
                A[i][j]+=base*w[i]*w[j]*prodk
                H[i][j]+=base*w[i]*w[j]*e[m-2]
    for X in (P,A,H):
        for r in X:
            for j in range(m):
                assert r[j]%dlt==0; r[j]//=dlt
    return P,A,H
data={}
M=int(sys.argv[1]) if len(sys.argv)>1 else 8
for m in range(3,M+1): data[m]=pairing(m)
print("first row P_{m,1,.} (boundary vectors):")
for m in range(3,M+1): print(" m=",m,data[m][0][1][:m] if False else data[m][0][1])
# rank-lowering identity
for m in range(4,M+1):
    P=data[m][0]; cprev=data[m-1][0][1]            # boundary vector of rank m-1 (same convention)
    lhs=[P[m-1][j+1]-P[m-1][j] for j in range(m-1)]       # j=1..m-1 -> indices j-1 -> P_{m,m-1,j+1}-P_{m,m-1,j}
    rhs=[(-1)**(m-1)*m*cprev[m-1-j] for j in range(1,m)]   # c_{m-1,m-j}, j=1..m-1 (0-indexed m-j-1)
    rhs=[(-1)**(m-1)*m*cprev[m-j-1] for j in range(1,m)]
    rel="equal" if lhs==rhs else ("negated" if lhs==[-x for x in rhs] else "DIFFERENT")
    print(f"rank-lowering P_(m,m-1,j+1)-P_(m,m-1,j) vs (-1)^(m-1) m c_(m-1,m-j): m={m}: {rel}")
# descent identity: (1-z) sum_r P_{m,m-1,r+1} z^r (-1)^m  =?  C'_{m-1}(1)(1-z^m) - m eps_m z C_{m-1}(z)
def pmul_(a,b):
    o=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): o[i+j]+=x*y
    return o
for m in range(4,M+1):
    P=data[m][0]; cprev=data[m-1][0][1]
    row=P[m-1]                                              # P_{m,m-1,r+1}, r=0..m-1
    lhs=pmul_([1,-1],row)
    Cp1=sum(k*c for k,c in enumerate(cprev))               # C'_{m-1}(1), C(z)=sum c_j z^{j-1}
    eps=(-1)**comb(m-1,2)
    rhs=[0]*(m+1)
    rhs[0]+=Cp1; rhs[m]-=Cp1
    for k,c in enumerate(cprev): rhs[k+1]-=m*eps*c
    res=[]
    for sg in (1,-1):
        L=[sg*x for x in lhs]
        res.append(L==rhs)
    print(f"descent identity m={m}: lhs=(1-z)*row, rhs=C'(1)(1-z^m)-m*eps*z*C_(m-1): equal for sign +:{res[0]}  sign -:{res[1]}   [(-1)^m={(-1)**m}]")
# quadratic packets
def cont(X): return reduce(gcd,[abs(x) for r in X for x in r])
print("m | boundary content | full Hessian content | split quadratic A content | reflected DD content")
for m in range(3,M+1):
    P,A,H=data[m]
    bc=reduce(gcd,[abs(x) for x in P[1]])
    rho=[0]+[ (m+2-j) if j>=2 else j for j in range(1,m+1)][0:0] if False else None
    rho=lambda i: 1 if i==1 else m+2-i                      # fixes edge 1, reverses edges 2..m
    sign=(-1)**(m-2+(m-1)//2)
    J=[[A[i-1][j-1]-sign*A[rho(i)-1][rho(j)-1] for j in range(1,m+1)] for i in range(1,m+1)]
    print(f" {m} | {bc} | {cont(H)} | {cont(A)} | {cont(J)}")
