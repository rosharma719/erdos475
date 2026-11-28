import itertools
from fractions import Fraction
p=37; m=9
a0=[16,7,34,26,10,12,9,33,1]
print("ninth roots of unity mod 37:", all(pow(x,9,p)==1 for x in a0), "distinct:",len(set(a0))==9, "sum:",sum(a0)%p)
def inv(x): return pow(x%p,p-2,p)
def vand(x):
    r=1
    for i in range(len(x)):
        for j in range(i+1,len(x)): r=r*(x[j]-x[i])%p
    return r
def polymul(A,B):
    out=[0]*(len(A)+len(B)-1)
    for i,x in enumerate(A):
        for j,y in enumerate(B): out[i+j]=(out[i+j]+x*y)%p
    return out
def Bpoly(a):
    v=[sum(a[:i])%p for i in range(m)]
    rho=vand(v)*inv(vand(a))%p
    Q=[1]
    for vi in v: Q=polymul(Q,[(-1-vi)%p,1])   # factor (z-1-v_i), ascending coeffs
    c=((-1)**(m-1)*m*rho)%p
    return [x*c%p for x in Q], v
tot=[0]*(m+1); valid=0; vertsets=[]
for sw in itertools.product((0,1),repeat=4):
    a=a0[:]
    for k,s in enumerate(sw):
        if s: a[2*k],a[2*k+1]=a[2*k+1],a[2*k]
    B,v=Bpoly(a)
    if len(set(v))==m: valid+=1
    vertsets.append(v)
    tot=[(x+y)%p for x,y in zip(tot,B)]
print("orderings:",16,"valid (distinct vertices):",valid)
print("summed polynomial mod 37:",tot)
print("fixed vertices (positions 0,2,4,6,8):",sorted(set.intersection(*[set([v[0],v[2],v[4],v[6],v[8]]) for v in vertsets])))
print("intermediate pairs:",[tuple(sorted(set(v[2*k+1] for v in vertsets))) for k in range(4)])
