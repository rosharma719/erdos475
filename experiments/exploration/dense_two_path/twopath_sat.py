# Exact SAT check of the two-path lemma for one hole set T.
# Closed walk x_0=0,...,x_L=0 in [0,M] using each label of S = I_M \ T exactly once;
# split index u (1<=u<=L-1): x_0..x_u distinct (P), x_u..x_{L-1} distinct (Q reversed), x_t != 0 for 0<t<L.
import sys, random
from itertools import combinations
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
def solve(M,T,return_paths=False):
    S=[v for v in range(-M,M+1) if v and v not in T]; L=len(S); V=range(M+1)
    pool=IDPool(); X=lambda t,v: pool.id(('x',t,v)); Y=lambda t,i: pool.id(('y',t,i)); I1=lambda t: pool.id(('p1',t))
    cl=[]
    def exactly_one(lits):
        cl.extend(CardEnc.equals(lits=lits,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    for t in range(L+1): exactly_one([X(t,v) for v in V])
    cl.append([X(0,0)]); cl.append([X(L,0)])
    for t in range(1,L): cl.append([-X(t,0)])
    for t in range(1,L+1): exactly_one([Y(t,i) for i in range(L)])
    for i in range(L): exactly_one([Y(t,i) for t in range(1,L+1)])
    for t in range(1,L+1):
        for i,s in enumerate(S):
            for a in V:
                b=a+s
                if 0<=b<=M: cl.append([-X(t-1,a),-Y(t,i),X(t,b)])
                else: cl.append([-X(t-1,a),-Y(t,i)])
    # phase indicator: I1(t) <=> t<=u ; I1(0)=I1(1)=1 ; monotone ; I1(L)=0
    cl.append([I1(0)]); cl.append([I1(1)]); cl.append([-I1(L)])
    for t in range(1,L+1): cl.append([-I1(t),I1(t-1)])
    for t in range(L+1):
        for t2 in range(t+1,L+1):
            for v in V:
                if v==0: continue
                # both in phase 1: t2<=u  <=> I1(t2)
                cl.append([-I1(t2),-X(t,v),-X(t2,v)])
                # both in phase 2: t>=u <=> not I1(t+1) ; t2<=L-1
                if t2<=L-1: cl.append([I1(t+1),-X(t,v),-X(t2,v)])
    s=Cadical153(bootstrap_with=cl); r=s.solve()
    if r and return_paths:
        m=set(l for l in s.get_model() if l>0)
        walk=[next(v for v in V if X(t,v) in m) for t in range(L+1)]
        u=max(t for t in range(L+1) if I1(t) in m)
        return walk,u
    return r
def verify(M,T,walk,u):
    S=sorted(v for v in range(-M,M+1) if v and v not in T)
    steps=sorted(b-a for a,b in zip(walk,walk[1:]))
    P=walk[:u+1]; Qr=walk[u:]
    return steps==S and len(set(P))==len(P) and len(set(Qr[:-1]))==len(Qr)-1 and min(walk)>=0 and max(walk)<=M and walk[u]>0
if __name__=='__main__':
    M=int(sys.argv[1]);k=int(sys.argv[2]);N=int(sys.argv[3]);rng=random.Random(int(sys.argv[4]))
    ok=fail=0
    for _ in range(N):
        while True:
            T=rng.sample([v for v in range(-M,M+1) if v],k-1); last=-sum(T)
            if last and abs(last)<=M and last not in T and max(map(abs,T+[last]))==M: T=set(T+[last]); break
        res=solve(M,T,True)
        if res and verify(M,T,*res): ok+=1
        else: fail+=1; print("NO PATHS (SAT-proved)" if not res else "VERIFY-ERR",M,sorted(T),flush=True)
    print(f"M={M} k={k} samples={N} ok={ok} fail={fail}",flush=True)
