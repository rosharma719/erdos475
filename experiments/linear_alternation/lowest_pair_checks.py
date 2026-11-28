import sys, random
from fractions import Fraction
from math import factorial, comb
from deformed_ext import *
def parity(A):
    for m_ in A: return bin(m_).count("1")%2
    return 0
def mulg(a,b): return gw_mul(a,b)
def sc(a,b):                                    # super commutator a b - (-1)^{|a||b|} b a
    s=-1 if (parity(a) and parity(b)) else 1
    return gw_add(mulg(a,b),mulg(b,a),-s)
def scal(a,c): return gw_scale(a,Fraction(c))
def one(): return {0:{(0,0):Fraction(1)}}
def zero(): return {}
def pieces(m):
    n=m-1
    P=u(1,m); Q=v(1,m)
    C={}; B={}
    for j in range(1,n+1):
        UV=mulg(u(j+1,m),v(j+1,m))
        C=gw_add(C,scal(UV,Fraction(1,factorial(j))))
        B=gw_add(B,scal(UV,Fraction(1,factorial(j+1))))
    return P,Q,C,B
def Zfact(m):
    c=[Fraction(1,factorial(k)) for k in range(1,m+1)]
    return Z(c,m)
def bernoulli(nmax):
    B=[Fraction(0)]*(nmax+1); B[0]=Fraction(1)
    for mm in range(1,nmax+1):
        B[mm]=-sum(comb(mm+1,k)*B[k] for k in range(mm))/(mm+1)
    return B
for m in (3,4,5):
    P,Q,C,B=pieces(m); n=m-1
    # PQ+QP = -C ; P^2=Q^2=0
    anti=gw_add(mulg(P,Q),mulg(Q,P))
    print(f"m={m}: PQ+QP = -C: {not gw_add(anti,scal(C,-1),-1) if False else (gw_add(anti,C)=={})};  P^2=0: {mulg(P,P)=={}};  Q^2=0: {mulg(Q,Q)=={}};  Z_m = PQ + B: {gw_add(Zfact(m),gw_add(mulg(P,Q),B),-1)=={}}")
    # [P,C]=[Q,C]=0
    print(f"        [P,C]=0: {sc(P,C)=={}}, [Q,C]=0: {sc(Q,C)=={}};  S=PQ+C/2: S^2 = C^2/4: {gw_add(mulg(gw_add(mulg(P,Q),scal(C,Fraction(1,2))),gw_add(mulg(P,Q),scal(C,Fraction(1,2)))),scal(mulg(C,C),Fraction(1,4)),-1)=={}}")
    # Bernoulli (3): B - C/2 = - sum_k B_2k/(2k)! L^{2k-1} C ,  L shifts U_iV_j -> U_{i+1}V_{j+1} (here: bilinear diagonal terms U_iV_i/i!)
    Bn=bernoulli(2*n+2)
    # apply L^s to C: sum_j U_{j+s}V_{j+s}/j!
    def Ls(s):
        tot={}
        for j in range(1,n+1):
            if j+s<=n: tot=gw_add(tot,scal(mulg(u(j+s+1,m),v(j+s+1,m)),Fraction(1,factorial(j))))
        return tot
    rhs={}
    k=1
    while 2*k-1<=n:
        rhs=gw_add(rhs,scal(Ls(2*k-1),-Bn[2*k]/factorial(2*k))); k+=1
    lhs=gw_add(B,scal(C,Fraction(-1,2)))
    print(f"        Bernoulli rank extension (3): B - C/2 = -sum B_2k/(2k)! L^(2k-1) C : {gw_add(lhs,rhs,-1)=={}}")

print("--- recurrence (8): Z^k = A_k + P U_k + V_k Q + P H_k Q, reconstructed from the recursion vs direct powers")
def recon(P,Q,A,U,V,H):
    tot=A
    tot=gw_add(tot,mulg(P,U)); tot=gw_add(tot,mulg(V,Q)); tot=gw_add(tot,mulg(mulg(P,H),Q))
    return tot
for m in (3,4,5,6):
    P,Q,C,B=pieces(m); Zm=Zfact(m)
    A=one(); U=zero(); V=zero(); H=zero(); Zk=one()
    dQB=sc(Q,B); BC=gw_add(B,C,-1)
    res=[]; Hs=[]
    for k in range(0,m):
        Zk_direct=Zk
        ok=(gw_add(recon(P,Q,A,U,V,H),Zk_direct,-1)=={})
        res.append(ok); Hs.append(H)
        # step
        An=gw_add(mulg(A,B),mulg(V,dQB))
        Un=gw_add(mulg(U,B),mulg(H,dQB))
        Vn=gw_add(scal(sc(P,A),-1),mulg(V,BC))
        Hn=gw_add(gw_add(A,sc(P,U)),mulg(H,BC))
        A,U,V,H=An,Un,Vn,Hn
        Zk=mulg(Zk,Zm)
    # H_1, H_2, H_3
    h1=Hs[1]; h2=Hs[2] if m>=3 else None
    print(f"m={m}: recursion reproduces Z^k for k=0..{m-1}: {all(res)};  H_1 = 1: {h1==one()};  H_2 = 2B - C: {gw_add(h2,gw_add(scal(B,2),C,-1),-1)=={}}")
    if m>=4:
        h3=Hs[3]
        exp3=gw_add(gw_add(scal(mulg(B,B),3),scal(mulg(B,C),-2)),gw_add(scal(mulg(C,B),-1),mulg(C,C)))
        exp3=gw_add(exp3,sc(P,sc(Q,B)))
        print(f"       H_3 = 3B^2 - 2BC - CB + C^2 + delta_P delta_Q B: {gw_add(h3,exp3,-1)=={}}")
    # detection: Z^{m-1} != 0  <=>  H_{m-1} != 0
    Zpow_top=Zfact(m); Zk=one()
    for _ in range(m-1): Zk=mulg(Zk,Zpow_top)
    Hlast=H if False else Hs[m-1]
    print(f"       Z_m^(m-1) != 0: {bool(Zk)};  H_(m-1) != 0: {bool(Hlast)}")
