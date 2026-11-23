"""Independent audit of GPT doubling-rigidity round (own code, not GPT's)."""
import sys, itertools, math
from sympy import isprime
from zigzag_sat import decide, check_steps
def prim2(M):
    q=2*M+1
    return isprime(q) and len({pow(2,j,q) for j in range(q-1)})==q-1
def valid(steps,P,N):
    if sorted(x for x in steps if x>0)!=sorted(P) or sorted(-x for x in steps if x<0)!=sorted(N): return False
    v=0;seen=set()
    for i,d in enumerate(steps):
        if (i==0 or v<0) and d<0: return False
        if i>0 and v>=0 and d>0 and False: pass
        # sign rule: positive step iff current vertex <=0 ; vertex 0 start positive
        if (v<=0)!=(d>0): return False
        if v in seen: return False
        seen.add(v); v+=d
    return v==0
# 1. doubling walk for M<=100 and equality with criterion
good=[]
for M in range(1,101):
    if prim2(M):
        v=0;st=[]
        for _ in range(2*M):
            w=2*v+M if v<=0 else 2*v-(M+1); st.append(w-v); v=w
        assert v==0 and valid(st,range(1,M+1),range(1,M+1)),M
        good.append(M)
print("T1 constructive M in",good[:12],"... all valid")
# T1 only-if via exact SAT, M<=13 (done before for <=11)
for M in range(12,14):
    r=decide(list(range(1,M+1)),list(range(1,M+1)))[0]; print("SAT sym",M,r,prim2(M))
# 2. Theorem 2 contraction
for M in (5,14,26,29,41,50,53,65):
    assert (M+1)%3==0 and prim2(M)
    v=0;st=[]
    for _ in range(2*M):
        w=2*v+M if v<=0 else 2*v-(M+1); st.append(w-v); v=w
    a=(M+1)//3;b=2*a
    idx=[i for i in range(len(st)-1) if st[i]==-a and st[i+1]==-b]
    assert len(idx)==1
    i=idx[0]; r=st[:i]+[-(M+1)]+st[i+2:]
    N=[x for x in range(1,M+2) if x not in (a,b)]
    assert valid(r,range(1,M+1),N),M
    print("T2 M",M,"ok len",len(r))
# 3. R refutation
P=(1,2,3,4,5,6,7);N=(1,3,4,5,7,8)
asc=lambda s:sum(x<y for x,y in zip(s,s[1:]))
def merge(sig,tau):
    X=Y=i=j=0;seen=set();tot=len(sig)+len(tau)
    for k in range(tot):
        if k and X==Y: return False
        if X<=Y:
            if i>=len(sig):return False
            X+=sig[i];i+=1
        else:
            if j>=len(tau):return False
            Y+=tau[j];j+=1
        if k<tot-1:
            if X-Y in seen or X-Y==0: return False
            seen.add(X-Y)
    return X==Y
pp=[p for p in itertools.permutations(P) if asc(p)<=2];nn=[p for p in itertools.permutations(N) if asc(p)<=2]
print("R: counts",len(pp),len(nn),"valid pairs",sum(merge(p,n) for p in pp for n in nn))
w=[3,-5,6,-7,5,-3,7,-1,-4,-8,2,1,4]; print("R witness valid",valid(w,P,N))
# 4. Theorem 3 and strict alternation on SAT witnesses
for M in range(4,11):
    for a in range(1,(M+1)//2+1):
        b=M+1-a
        if a==b: continue
        Nn=[x for x in range(1,M+2) if x not in (a,b)]
        r,st,_=decide(list(range(1,M+1)),Nn)
        if r!="FOUND": print("tight NONE",M,a); continue
        v=0;T=0
        for d in st:
            v+=d
            if d<0 and v>0: T+=1
        bd=max(0,math.ceil(M-(1+math.sqrt(2*M*M+6*M-3))/2))
        alt=all((st[i]>0)!=(st[i+1]>0) for i in range(len(st)-1))
        assert T>=bd and not alt,(M,a,T,bd)
print("T3 holds on SAT witnesses M=4..10; no alternating")
