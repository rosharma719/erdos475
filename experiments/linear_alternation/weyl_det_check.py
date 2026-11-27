"""Exterior-coefficient Weyl matrices.  X = sum alpha_i U_i,  Y = sum beta_a D^a  (alpha, beta odd Grassmann generators), heights 0..N-1.
Test which of H1 = YX - XY, H2 = XY + YX has tr(H^k)=0, and whether (H^k)_{00} recovers kappa(A,I)."""
import itertools, sys
from math import comb
# ---- Grassmann algebra: element = dict{mask: int}, generators 0..G-1
def gmul(a,b):
    out={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            if ma&mb: continue
            # sign: number of pairs (x in ma, y in mb) with x>y
            s=0; t=mb
            while t:
                y=(t&-t).bit_length()-1; t&=t-1
                s+=bin(ma>>(y+1)).count("1")
            c=ca*cb*(-1 if s&1 else 1)
            out[ma|mb]=out.get(ma|mb,0)+c
    return {k:v for k,v in out.items() if v}
def gadd(a,b,s=1):
    out=dict(a)
    for k,v in b.items(): out[k]=out.get(k,0)+s*v
    return {k:v for k,v in out.items() if v}
def mmul(A,B):
    n=len(A); C=[[{} for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if not A[i][k]: continue
            for j in range(n):
                if B[k][j]: C[i][j]=gadd(C[i][j],gmul(A[i][k],B[k][j]))
    return C
def madd(A,B,s=1):
    n=len(A); return [[gadd(A[i][j],B[i][j],s) for j in range(n)] for i in range(n)]
def build(U,N):
    n=len(U)
    X=[[{} for _ in range(N)] for _ in range(N)]; Y=[[{} for _ in range(N)] for _ in range(N)]
    for ix,i in enumerate(U):
        for h in range(N):
            if h+i<N: X[h+i][h]=gadd(X[h+i][h],{1<<ix:comb(h+i,i)})
    for ia,a in enumerate(U):
        for h in range(N):
            if h-a>=0: Y[h-a][h]=gadd(Y[h-a][h],{1<<(n+ia):1})
    return X,Y
def trace(A): 
    t={}
    for i in range(len(A)): t=gadd(t,A[i][i])
    return t
U=(2,3); N=7
X,Y=build(U,N)
XY=mmul(X,Y); YX=mmul(Y,X)
print("tr(XY) =",trace(XY)," tr(YX) =",trace(YX),"  (so tr(XY) = -tr(YX)?)", trace(gadd(trace(XY),trace(YX)))=={} if False else gadd(trace(XY),trace(YX))=={})
for name,H in (("H1 = YX - XY",madd(YX,XY,-1)),("H2 = XY + YX",madd(XY,YX,1))):
    P=H; res=[]
    for k in range(1,5):
        res.append(trace(P)=={})
        P=mmul(P,H)
    print(f"{name}: tr(H^k)==0 for k=1..4: {res}")

# ---- commutator form H = sum alpha_i beta_a [D^a,U_i] = -(XY+YX); (H^k)_{00} should be eps(k) * sum kappa(A,I) alpha_I beta_A
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import pascal_checks as PC
kappa=PC.kappa
def run(U,N,kmax):
    n=len(U); X,Y=build(U,N); H=madd(mmul(X,Y),mmul(Y,X),1)
    H=[[{k:-v for k,v in e.items()} for e in row] for row in H]            # H = -(XY+YX)
    P=H; ok=True; rows=[]
    for k in range(1,kmax+1):
        entry=P[0][0]; eps=(-1)**(k*(k-1)//2)
        # compare every coefficient alpha_I beta_A with eps*kappa(A,I)
        for I in itertools.combinations(range(n),k):
            for A in itertools.combinations(range(n),k):
                mask=0
                for x in I: mask|=1<<x
                for y in A: mask|=1<<(n+y)
                # coefficient of alpha_I beta_A in canonical order (alphas ascending then betas ascending) is exactly the mask coefficient
                coef=entry.get(mask,0)
                Iv=tuple(U[x] for x in I); Av=tuple(U[y] for y in A)
                exp=eps*kappa(Av,Iv) if sum(Iv)==sum(Av) else 0
                if coef!=exp: ok=False; rows.append((k,Iv,Av,coef,exp))
        P=mmul(P,H)
    return ok,rows[:3]
for U,N,kmax in (((2,3),6,2),((2,3,4),10,3)):
    ok,rows=run(U,N,kmax)
    print(f"(H^k)_00 for H = sum alpha_i beta_a [D^a,U_i], U={U}, heights<{N}, k<={kmax}: coefficients equal eps(k)*kappa(A,I): {ok} {rows if not ok else ''}")
