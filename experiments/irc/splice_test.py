"""Structured splice test: core = explicit symmetric IRC walk on C=P∩N (fixed step order, any rotation);
insert the remainder steps (+P0, -N0) anywhere, any order. Distinct partial sums mod p required."""
import random,sys,time
def lift(A,p):
    r=sorted(x%p for x in A)
    for T in range(len(r)+1):
        P=r[:len(r)-T]; N=[p-x for x in r[len(r)-T:]]
        if sum(P)==sum(N): return P,N
def core_walk(C):
    S=sorted(C,reverse=True); c=S[0]
    d=[x if i%2==0 else -x for i,x in enumerate(S[1:])]
    return d+[c]+[-x for x in d[::-1]]+[-c]
def splice(core,R,p,tl=10):
    n=len(core);t0=time.time()
    for rot in range(n):
        cw=core[rot:]+core[:rot]
        seen={0}
        def rec(i,mask,s):
            if time.time()-t0>tl: raise TimeoutError
            if i==n and mask==(1<<len(R))-1: return True
            opts=[]
            if i<n: opts.append(('c',cw[i]))
            for j,x in enumerate(R):
                if not mask>>j&1: opts.append((j,x))
            for o,x in opts:
                t=(s+x)%p
                last=(i+(o=='c')==n and (mask|(0 if o=='c' else 1<<o))==(1<<len(R))-1)
                if last:
                    if t==0: return True
                    continue
                if t in seen: continue
                seen.add(t)
                if rec(i+(o=='c'),mask|(0 if o=='c' else 1<<o),t): return True
                seen.discard(t)
            return False
        try:
            if rec(0,0,0): return True
        except TimeoutError: return 'TO'
    return False
p=int(sys.argv[1]);alpha=float(sys.argv[2]);T=int(sys.argv[3]);random.seed(7)
k=int(alpha*(p-1));st={'yes':0,'no':0,'to':0,'skip':0};rs=[]
for _ in range(T):
    while True:
        A=random.sample(range(1,p),k-1);s=(-sum(A))%p
        if s and s not in A: A.append(s);break
    best=None
    for lam in range(1,p):
        L=lift([lam*x for x in A],p)
        P,N=L;C=set(P)&set(N)
        rem=[x for x in P if x not in C]+[-x for x in N if x not in C]
        if C and (best is None or len(rem)<len(best[1])): best=(C,rem)
    C,R=best; rs.append(len(R))
    if len(R)>int(sys.argv[4]) if len(sys.argv)>4 else 14: st['skip']+=1;continue
    r=splice(core_walk(C),R,p)
    st['yes' if r is True else ('to' if r=='TO' else 'no')]+=1
print(f"p={p} alpha={alpha}: remainder sizes {sorted(rs)}  results {st}")
