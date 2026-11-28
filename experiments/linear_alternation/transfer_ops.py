import sys, itertools, pickle, os, time
from fractions import Fraction
exec(open('transfer_checks.py').read().split('if __name__=="__main__":')[0])
def make(m):
    n=m-1; P,Q,C,B=pieces(m); BC=gw_add(B,C,-1)
    def T(f):   # f: Lambda element {(A,B):c} (A,B tuples)
        ef=to_ext(f,n)
        rv=Rv(ef,n); ru=Ru(ef,n)
        g=Phi(from_ext(rv,n),m)                     # U-component as algebra element
        dg=sc(P,g) if g else {}
        part=Phiinv(dg,m) if dg else {}
        res=fadd(to_ext(part,n), Ru(rv,n)); res=fadd(res,Kop(ef,n))
        fa=Phi(f,m)
        prod=mulg(fa,BC) if fa else {}
        pr=to_ext(Phiinv(prod,m),n) if prod else {}
        return from_ext(fadd(res,pr),n)
    return T
if __name__=="__main__":
    for m in (3,4,5,6):
        n=m-1; T=make(m); comps=components(m,n)
        ok=[]
        for k in range(1,n):
            Hk=Phiinv(comps[k][3],m) if comps[k][3] else {}
            Hn=Phiinv(comps[k+1][3],m) if comps[k+1][3] else {}
            ok.append(fadd(to_ext(T(Hk),n),to_ext(Hn,n),-1)=={})
        print("m=",m,"T(H_k)=H_{k+1} for k=1..n-1:",ok,flush=True)
