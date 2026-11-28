"""Check the 'single transfer' report: components U,V,A reconstructed from H via R_u,R_v,K; T_n; terminal vanishing; surjectivity; seed rigidity."""
import sys, itertools
from fractions import Fraction
from math import factorial, comb
from deformed_ext import *
import importlib
exec(open('lowest_pair_checks.py').read().split("for m in (3,4,5):")[0])   # pieces, sc, mulg, ...
def Uel(j,m): return u(j+1,m)
def Vel(j,m): return v(j+1,m)
def Phi_mono(A,B,m):
    r=one()
    for a in sorted(A): r=mulg(r,Uel(a,m))
    for b in sorted(B): r=mulg(r,Vel(b,m))
    return r
def Phi(f,m):
    tot={}
    for (A,B),c in f.items(): tot=gw_add(tot,scal(Phi_mono(A,B,m),c))
    return tot
def Phiinv(g,m):
    n=m-1; g={k:dict(v) for k,v in g.items()}
    out={}
    keys=[(A,B) for r in range(n+1) for A in itertools.combinations(range(1,n+1),r) for s in range(n+1) for B in itertools.combinations(range(1,n+1),s)]
    keys.sort(key=lambda ab:sum(ab[0])+sum(ab[1]))
    for A,B in keys:
        mask=0
        for a in A: mask|=1<<a        # xi_{a+1} bit a
        for b in B: mask|=1<<(m+b)    # eta_{b+1} bit m+b
        c=g.get(mask,{}).get((0,0),0)
        if c:
            out[(A,B)]=c
            g=gw_add(g,scal(Phi_mono(A,B,m),c),-1)
    assert not g, "Phiinv residual"
    return out
# exterior algebra on U_1..U_n, V_1..V_n  (ids 1..n, n+1..2n); monomial = sorted tuple of ids
def ext_mul_gen(gid,mono):
    if gid in mono: return None,0
    pos=sum(1 for x in mono if x<gid)
    new=tuple(sorted(mono+(gid,)))
    return new,(-1)**pos
def lmul(gid,f):
    out={}
    for mono,c in f.items():
        new,s=ext_mul_gen(gid,mono)
        if s: out[new]=out.get(new,0)+s*c
    return {k:v for k,v in out.items() if v}
def deriv(f,n,kind):   # E_u (kind 0) or E_v (kind 1): shift generator id +1 within its block
    out={}
    for mono,c in f.items():
        for idx,x in enumerate(mono):
            blk=(x-1)//n; 
            if blk!=kind: continue
            y=x+1
            if (y-1)//n!=kind or y in mono: continue
            lst=list(mono); lst[idx]=y
            # sort with sign
            sign=1; arr=lst[:]
            for i in range(len(arr)):
                for j in range(len(arr)-1-i):
                    if arr[j]>arr[j+1]: arr[j],arr[j+1]=arr[j+1],arr[j]; sign=-sign
            out[tuple(arr)]=out.get(tuple(arr),0)+sign*c
    return {k:v for k,v in out.items() if v}
def fadd(f,g,s=1):
    out=dict(f)
    for k,v in g.items(): out[k]=out.get(k,0)+s*v
    return {k:v for k,v in out.items() if v}
def fscal(f,c): return {k:v*c for k,v in f.items() if v*c}
def fpow(f,n,kind,s):
    for _ in range(s): f=deriv(f,n,kind)
    return f
def to_ext(f,n): return {tuple(list(A)+[n+b for b in B]):c for (A,B),c in f.items()}
def from_ext(f,n): return {(tuple(x for x in mono if x<=n),tuple(x-n for x in mono if x>n)):c for mono,c in f.items()}
def Ru(f,n):
    tot={}
    for s in range(1,n+1): tot=fadd(tot,fscal(lmul(s,fpow(f,n,1,s)),Fraction(1,factorial(s+1))))
    return tot
def Rv(f,n):
    tot={}
    for s in range(1,n+1): tot=fadd(tot,fscal(lmul(n+s,fpow(f,n,0,s)),Fraction(1,factorial(s+1))))
    return tot
def Kop(f,n):
    tot={}
    for s in range(1,n+1):
        for j in range(1,s+1):
            g=lmul(s,lmul(n+j,fpow(f,n,1,s-j)))   # U_s ^ V_j ^ E_v^{s-j} f   (V_j generator id n+j)
            tot=fadd(tot,fscal(g,Fraction(comb(s,j),factorial(s+1))))
            
    return tot
def components(m,kmax):
    """run recurrence; return list of (A,U,V,H) as gw elements in sub-algebra"""
    P,Q,C,B=pieces(m)
    A=one(); U={}; V={}; H={}
    dQB=sc(Q,B); BC=gw_add(B,C,-1); out=[]
    for k in range(kmax+1):
        out.append((A,U,V,H))
        An=gw_add(mulg(A,B),mulg(V,dQB)); Un=gw_add(mulg(U,B),mulg(H,dQB))
        Vn=gw_add(scal(sc(P,A),-1),mulg(V,BC)); Hn=gw_add(gw_add(A,sc(P,U)),mulg(H,BC))
        A,U,V,H=An,Un,Vn,Hn
    return out
if __name__=="__main__":
    for m in (3,4,5):
        n=m-1
        comps=components(m,n)
        print("m=",m,"n=",n)
        for k in range(1,n+1):
            A,U,V,H=comps[k]
            hA,hU,hV,hH=[to_ext(Phiinv(x,m),n) if x else {} for x in (A,U,V,H)]
            res={}
            for name,tgt,cands in (("U",hU,{"Rv":Rv(hH,n),"Ru":Ru(hH,n)}),("V",hV,{"Rv":Rv(hH,n),"Ru":Ru(hH,n)}),
                                   ("A",hA,{"RuRv+K":fadd(Ru(Rv(hH,n),n),Kop(hH,n)),"RvRu+K":fadd(Rv(Ru(hH,n),n),Kop(hH,n)),"RuRv":Ru(Rv(hH,n),n),"K":Kop(hH,n)})):
                for cn,cv in cands.items():
                    for sg in (1,-1):
                        if fadd(tgt,cv,-sg)=={} : res.setdefault(name,[]).append((cn,sg))
            print(" k=",k,"H nonzero:",bool(hH),res)
