"""Deformed exterior algebra: odd generators xi_1..xi_m, eta_1..eta_m (anticommuting among and between) tensor the Weyl algebra (normal ordered X^i D^j, [D,X]=1).
u_k = sum_{i>=k} xi_i X^{i-k}/(i-k)!,  v_k = sum_{a>=k} eta_a D^{a-k}/(a-k)!,  Z(c) = sum_k c_k u_k v_k,  F_m(c) = top coefficient of Z^m."""
import itertools, math, random
from fractions import Fraction
from math import comb, factorial
def weyl_mul(A,B):
    out={}
    for (a,b),c1 in A.items():
        for (c,d),c2 in B.items():
            for s in range(min(b,c)+1):
                co=c1*c2*factorial(s)*comb(b,s)*comb(c,s)
                key=(a+c-s,b+d-s); out[key]=out.get(key,0)+co
    return {k:v for k,v in out.items() if v}
def weyl_add(A,B,s=1):
    out=dict(A)
    for k,v in B.items(): out[k]=out.get(k,0)+s*v
    return {k:v for k,v in out.items() if v}
def gsign(ma,mb):
    s=0; t=mb
    while t:
        y=(t&-t).bit_length()-1; t&=t-1
        s+=bin(ma>>(y+1)).count("1")
    return -1 if s&1 else 1
def gw_mul(A,B):
    out={}
    for ma,wa in A.items():
        for mb,wb in B.items():
            if ma&mb: continue
            w=weyl_mul(wa,wb); sg=gsign(ma,mb)
            if sg<0: w={k:-v for k,v in w.items()}
            m=ma|mb; out[m]=weyl_add(out.get(m,{}),w)
    return {k:v for k,v in out.items() if v}
def gw_add(A,B,s=1):
    out={m:dict(w) for m,w in A.items()}
    for m,w in B.items():
        out[m]=weyl_add(out.get(m,{}),w,s)
    return {k:v for k,v in out.items() if v}
def gw_scale(A,c): return {m:{k:v*c for k,v in w.items()} for m,w in A.items()}
def u(k,m):
    return {1<<(i-1):{(i-k,0):Fraction(1,factorial(i-k))} for i in range(k,m+1)}
def v(k,m):
    return {1<<(m+a-1):{(0,a-k):Fraction(1,factorial(a-k))} for a in range(k,m+1)}
def Z(c,m):
    tot={}
    for k in range(1,m+1):
        if c[k-1]!=0: tot=gw_add(tot,gw_scale(gw_mul(u(k,m),v(k,m)),c[k-1]))
    return tot
def Zpow(c,m,e):
    P=Z(c,m); R=P
    for _ in range(e-1): R=gw_mul(R,P)
    return R
def F(c,m):
    top=(1<<(2*m))-1
    R=Zpow(c,m,m)
    return R.get(top,{})
if __name__=="__main__":
    # (1) cross relation  v_k u_l = - sum_s u_{l+s} v_{k+s}/s!
    m=3; ok=True
    for k in range(1,m+1):
        for l in range(1,m+1):
            lhs=gw_mul(v(k,m),u(l,m)); rhs={}
            for s in range(0,m+1):
                if l+s<=m and k+s<=m:
                    rhs=gw_add(rhs,gw_scale(gw_mul(u(l+s,m),v(k+s,m)),Fraction(-1,factorial(s))))
            if gw_add(lhs,rhs,-1): ok=False
    print("(1) v_k u_l = -sum_s u_(l+s) v_(k+s)/s!  for m=3, all k,l:",ok)
    # (2) Z(c*) = sum xi_i eta_a [D^a/a!, X^i/i!]
    for m in (3,4):
        cstar=[Fraction(1,factorial(k)) for k in range(1,m+1)]
        lhs=Z(cstar,m); rhs={}
        for i in range(1,m+1):
            for a in range(1,m+1):
                # [D^a/a!, X^i/i!] normal ordered
                A={(0,a):Fraction(1,factorial(a))}; B={(i,0):Fraction(1,factorial(i))}
                com=weyl_add(weyl_mul(A,B),weyl_mul(B,A),-1)
                mask=(1<<(i-1))|(1<<(m+a-1))
                # xi_i eta_a : ordering xi then eta (bit order: xi bits lower) -> sign +
                rhs=gw_add(rhs,{mask:com})
        print(f"(2) m={m}: Z(c*) equals sum xi_i eta_a [D^a/a!, X^i/i!]: {not gw_add(lhs,rhs,-1)}")
    # (3) F_m values vs formulas
    random.seed(3)
    for _ in range(3):
        c=[Fraction(random.randint(-5,5),random.randint(1,4)) for _ in range(4)]
        F2=F(c[:2],2); F3=F(c[:3],3); F4=F(c[:4],4)
        e2=c[0]*(c[0]-2*c[1])
        e3=-Fraction(3,2)*c[0]*(c[0]-2*c[1])*(c[1]-2*c[2])
        e4=Fraction(1,3)*c[0]*(c[1]-2*c[2])*(c[0]**2-3*c[0]*c[1]-6*c[0]*c[2]+18*c[0]*c[3]+18*c[1]*c[2]-36*c[1]*c[3])
        print("(3) c=",[str(x) for x in c]," F2:",F2,"vs",e2,"| F3:",F3,"vs",e3,"| F4:",F4,"vs",e4)
