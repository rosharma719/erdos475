"""Cut-and-place induction test. Core walk W_C=(δ, c, −δ^rev, −c) on ±C. Take a valid ordering U of the remainder R
(zero-sum mod p), cut it at t into arc1 (sum σ) and arc2. Walk: δ, arc1, +c, −δ^rev, arc2, −c.
Valid iff all partial sums distinct mod p. Search over orderings U (DFS enumeration, capped), cuts t, and the choice of
which element of C is c (any core element can serve as the pivot if δ is the alternating walk on the rest)."""
import random,sys,itertools,time
def lift(A,p):
    r=sorted(x%p for x in A)
    for T in range(len(r)+1):
        P=r[:len(r)-T]; N=[p-x for x in r[len(r)-T:]]
        if sum(P)==sum(N): return P,N
def orderings(R,p,cap):
    out=[];n=len(R)
    def rec(seq,mask,s,seen):
        if len(out)>=cap: return
        if mask==(1<<n)-1:
            if s%p==0: out.append(list(seq))
            return
        for j in range(n):
            if mask>>j&1: continue
            t=(s+R[j])%p
            last=(mask|1<<j)==(1<<n)-1
            if (last and t!=0) or (not last and (t==0 or t in seen)): continue
            seq.append(R[j]);seen.add(t);rec(seq,mask|1<<j,t,seen);seen.discard(t);seq.pop()
    rec([],0,0,set());return out
def test(C,R,p,cap=300):
    S=sorted(C,reverse=True); c=S[0]; d=[x if i%2==0 else -x for i,x in enumerate(S[1:])]
    for U in orderings(R,p,cap):
        for t in range(0,len(U)+1):
            W=d+U[:t]+[c]+[-x for x in d[::-1]]+U[t:]+[-c]
            v=0;seen=set();ok=True
            for x in W[:-1]:
                if v%p in seen: ok=False;break
                seen.add(v%p); v+=x
            if ok and v%p not in seen and (v+W[-1])%p==0: return True
    return False
p=int(sys.argv[1]);alpha=float(sys.argv[2]);T=int(sys.argv[3]);random.seed(11)
k=int(alpha*(p-1));st={'yes':0,'no':0,'skip':0}
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
    if len(R)>12: st['skip']+=1;continue
    st['yes' if test(C,R,p) else 'no']+=1
print(p,alpha,st)
