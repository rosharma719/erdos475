import itertools, io, contextlib, math, random, sys
from fractions import Fraction
from math import comb, factorial
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])        # gives F (=kappa), T, Cb, vand, ...
def fac(S): return math.prod(factorial(x) for x in S)
# ---- (1) height barrier: crossing g<p -> h>=p has weight 0 mod p for all exponents in 1..p-1
for p in (5,7,11,13):
    bad=0; cnt=0
    for g in range(p):
        for i in range(1,p):
            for a in range(1,p):
                h=g+i-a
                if h>=p:
                    cnt+=1; w=Cb(g+i,i)-Cb(h,i)
                    if w%p: bad+=1
    print(f"(1) p={p}: upward crossings tested {cnt}, weights not divisible by p: {bad}")
# ---- (2) reversed-step identity  w = h! a!/(g! i!) w'
ok=True
for g in range(0,15):
    for i in range(1,9):
        for a in range(1,9):
            h=g+i-a
            if h<0: continue
            w=Cb(g+i,i)-Cb(h,i); w2=Cb(h+a,a)-Cb(g,a)
            if w*factorial(g)*factorial(i)!=factorial(h)*factorial(a)*w2: ok=False
print("(2) w = h!a!/(g!i!) * w' :",ok)
# ---- (3) midpoint identity
def shuffle_sign(S1,S2):
    seq=list(S1)+list(S2); s=1
    for x in range(len(seq)):
        for y in range(x+1,len(seq)):
            if seq[x]>seq[y]: s=-s
    return s
def midpoint(A,I,k):
    tot=Fraction(0); tot_nobar={}
    for A1 in itertools.combinations(A,k):
        A2=tuple(x for x in A if x not in A1)
        for I1 in itertools.combinations(I,k):
            I2=tuple(x for x in I if x not in I1)
            h=sum(I1)-sum(A1)
            if h<0: continue
            term=Fraction(shuffle_sign(A1,A2)*shuffle_sign(I1,I2))*Fraction(fac(A2),factorial(h)*fac(I2))*F(A1,I1)*F(I2,A2)
            tot+=term; tot_nobar[h]=tot_nobar.get(h,0)+term
    return tot,tot_nobar
random.seed(9)
bad=0;n=0
for r in (2,3,4,5):
    for _ in range(40):
        A=tuple(sorted(random.sample(range(1,10),r))); I=tuple(sorted(random.sample(range(1,10),r)))
        if sum(A)!=sum(I): continue
        for k in range(1,r):
            tot,_=midpoint(A,I,k); n+=1
            if tot!=F(A,I): bad+=1
print(f"(3) midpoint identity over Q (all heights, split size k=1..r-1): {n} cases, mismatches {bad}")
# mod p with barrier: exponents in 1..p-1, keep only 0<=h<p
for p in (7,11):
    bad=0;n=0;dropped=0
    for r in (3,4,5):
        tries=0
        while tries<60:
            tries+=1
            A=tuple(sorted(random.sample(range(1,p),r))); I=tuple(sorted(random.sample(range(1,p),r)))
            if sum(A)!=sum(I): continue
            k=r//2
            tot,by=midpoint(A,I,k)
            kept=sum(v for h,v in by.items() if h<p)
            n+=1
            def modp(x):
                x=Fraction(x); return (x.numerator*pow(x.denominator,-1,p))%p
            if modp(kept)!=F(A,I)%p: bad+=1
            if any(h>=p for h in by): dropped+=1
    print(f"    p={p}: mod-p midpoint with height<p restriction: {n} cases, mismatches {bad}  (cases with some dropped h>=p: {dropped})")
# ---- (4) coefficient transform  R_m in (u,v)
def hpoly_uv(n):          # h_n(a,b) = sum_l (-1)^l C(n-l,l) u^{n-2l} v^l  -> dict {(i,l):c}
    return {(n-2*l,l):(-1)**l*comb(n-l,l) for l in range(n//2+1)}
def qq(m,d,r):
    J=tuple(c for c in range(1,m+1) if c!=d); A=tuple(c for c in range(1,m+2) if c not in (r,m+1+d-r)); return F(J,A)
from math import gcd
from functools import reduce
for m in range(3,11):
    r=m-1; ks=[qq(m,1,j+1) for j in range(r//2+1)]
    C1={}
    for j,kj in enumerate(ks):
        for (i,l),c in hpoly_uv(r-2*j).items(): C1[(i,l+j)]=C1.get((i,l+j),0)+kj*c
    # R = -C1/u^2 : need every term divisible by u^2
    Ruv={}
    ok_div=all(i>=2 for (i,l),c in C1.items() if c)
    for (i,l),c in C1.items():
        if c: Ruv[(i-2,l)]=-c
    # transform formula: coefficient of u^{r-2-2l} v^l  = C_{m,l} = - sum_j (-1)^{l-j} C(r-l-j, l-j) k_j ... compare
    form={}
    for l in range(0,(r-2)//2+1):
        form[(r-2-2*l,l)]=-sum((-1)**(l-j)*comb(r-l-j,l-j)*ks[j] for j in range(0,l+1) if j<len(ks))
    same = {k:v for k,v in form.items() if v}=={k:v for k,v in Ruv.items() if v}
    cont=reduce(gcd,[abs(x) for x in ks])
    print(f"(4) m={m}: k_j={ks}; u^2 | C1: {ok_div}; R_m(u,v)={ {k:int(v) for k,v in sorted(Ruv.items()) if v} }; transform formula matches: {same}; gcd(k_j)={cont}")
