import itertools, random, sys
from fractions import Fraction
def sign(p):
    p=list(p); s=1
    for i in range(len(p)):
        while p[i]!=i:
            j=p[i]; p[i],p[j]=p[j],p[i]; s=-s
    return s
def G(ys,a):
    n=len(ys); tot=0
    for perm in itertools.permutations(range(n)):
        u=[0]
        for i in perm: u.append(u[-1]+ys[i])
        r=1
        for i in range(n+1):
            for j in range(i+1,n+1): r*=(u[j]-u[i])
            if r==0: break
        if r:
            for j in range(1,n): r*=(u[j]+a)
        tot+=sign(perm)*r
    V=1
    for i in range(n):
        for j in range(i+1,n): V*=ys[j]-ys[i]
    return Fraction(tot,V)
n=int(sys.argv[1]); random.seed(1)
for t in range(4):
    ys=random.sample(range(-30,30),n); a=random.randint(-30,30)
    s1=sum(ys); sn=1
    for v in ys: sn*=v
    g=G(ys,a)
    den=sn*s1**(n-2)*(2*a+s1)
    print(ys,a, g, g/den if den else None)
