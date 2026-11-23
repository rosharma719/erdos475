"""AVOID form: W = core[:n-1] + [x1] + [core[n-1]] + rest, where (x1, rest) is a valid ordering U of the remainder from 0.
Equivalently: U's nonzero partial sums avoid V_C = vertex set of the core walk (mod p), and b1+x1 avoids V_C ∪ V(U).
Search: rotations of the core walk (which vertex plays 0), and orderings U (DFS with the avoidance constraint)."""
import random,sys,time
from splice_test import lift, core_walk
def avoid(core,R,p,tl=20):
    n=len(core);t0=time.time()
    for rot in range(n):
        cw=core[rot:]+core[:rot]
        V=[0]
        for x in cw[:-1]: V.append((V[-1]+x)%p)
        VC=set(V)
        top=V[-1]   # vertex before the last core step
        # U: x1 first; vertices: top+x1, then x1, x1+x2, ... ; must avoid VC and each other, end at 0
        n2=len(R)
        def rec(mask,s,seen):
            if time.time()-t0>tl: raise TimeoutError
            if mask==(1<<n2)-1: return s%p==0
            for j in range(n2):
                if mask>>j&1: continue
                t=(s+R[j])%p; last=(mask|1<<j)==(1<<n2)-1
                if last:
                    if t==0: return True
                    continue
                if t in VC or t in seen: continue
                seen.add(t)
                if rec(mask|1<<j,t,seen): return True
                seen.discard(t)
            return False
        for j in range(n2):
            x1=R[j]; b=(top+x1)%p; v1=x1%p
            if b in VC or v1 in VC or b==v1: continue
            try:
                if rec(1<<j,x1,{b,v1}): return True
            except TimeoutError: return 'TO'
    return False
p=int(sys.argv[1]);alpha=float(sys.argv[2]);T=int(sys.argv[3]);random.seed(int(sys.argv[4]) if len(sys.argv)>4 else 3)
k=int(alpha*(p-1));st={'yes':0,'no':0,'to':0}
for _ in range(T):
    while True:
        A=random.sample(range(1,p),k-1);s=(-sum(A))%p
        if s and s not in A: A.append(s);break
    best=None
    for lam in range(1,p):
        P,N=lift([lam*x for x in A],p);C=set(P)&set(N)
        rem=[x for x in P if x not in C]+[-x for x in N if x not in C]
        if C and (best is None or len(rem)<len(best[1])): best=(C,rem)
    C,R=best
    r=avoid(core_walk(C),R,p)
    st['yes' if r is True else ('to' if r=='TO' else 'no')]+=1
print(p,alpha,st)
