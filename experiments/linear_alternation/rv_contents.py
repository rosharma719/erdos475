"""R_m(a,b)=L_m(0,a,b), V_m(a,b)=L_m(-b,a,b) from the two-root coefficients q_{m,d,r}=kappa(J_d,A_{d,r}); contents of R_m and V_m."""
import sys, time
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def polydiv(num,den):                 # univariate in a, Fractions, exact
    num=num[:]; out=[Fraction(0)]*(len(num)-len(den)+1)
    for i in range(len(out)-1,-1,-1):
        c=num[i+len(den)-1]/den[-1]; out[i]=c
        for j,dv in enumerate(den): num[i+j]-=c*dv
    assert all(x==0 for x in num), "not divisible"
    return out
def padd(p,q):
    n=max(len(p),len(q)); return [(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(n)]
def pmul(p,q):
    o=[Fraction(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): o[i+j]+=x*y
    return o
def pscale(p,c): return [c*x for x in p]
def hpoly(n):                          # h_n(a,1) = 1+a+..+a^n  (n>=0)
    return [Fraction(1)]*(n+1) if n>=0 else [Fraction(0)]
def s2(u,v):                           # s_(u,v)(a,1) = a^v h_{u-v}
    return [Fraction(0)]*v+hpoly(u-v)
def qq(m,d,r):
    J=tuple(c for c in range(1,m+1) if c!=d); A=tuple(c for c in range(1,m+2) if c not in (r,m+1+d-r)); return kappa(J,A)
def content_of(p):
    from math import lcm
    den=1
    for x in p: den=lcm(den,Fraction(x).denominator)
    ints=[int(x*den) for x in p]
    return reduce(gcd,[abs(v) for v in ints]),den
def RV(m):
    # R: -C1(a,1)/(a+1)^2, C1 = sum_r q_{m,1,r} s_(m-r,r-1)
    C1=[Fraction(0)]
    for r in range(1,(m+1)//2+1): C1=padd(C1,pscale(s2(m-r,r-1),qq(m,1,r)))
    R=polydiv(pscale(C1,-1),pmul([1,1],[1,1]))
    # V: P~(-1,a,1)/((a+1) a): P~(t,a,1)=sum t^d sum_r q s_(m-r,r-d)
    P=[Fraction(0)]
    for d in range(1,m+1):
        for r in range(d,(m+d)//2+1):
            P=padd(P,pscale(s2(m-r,r-d),qq(m,d,r)*(-1)**d))
    V=polydiv(P,pmul([1,1],[0,1]))
    return R,V
if __name__=="__main__":
    M=int(sys.argv[1])
    for m in range(4,M+1):
        t0=time.time(); R,V=RV(m)
        cr,dr=content_of(R); cv,dv=content_of(V)
        print(f"rank {m}: deg R={len(R)-1}, content(R_m)={cr} (denominator {dr}); deg V={len(V)-1}, content(V_m)={cv} (denominator {dv})  ({time.time()-t0:.0f}s)",flush=True)
