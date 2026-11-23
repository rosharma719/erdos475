"""Full recursive GO construction: GO(R,F) = ordering of zero-sum R (mod p) whose nonzero partial sums avoid F.
Step: pick dilation λ (try several), core C of λR (best lift), core walk W_C (rotations), require V_C ∩ λF = ∅ (V_C
includes 0 = start), then U = GO(λR', λF ∪ V_C) whose first step x1 also satisfies top+x1 ∉ λF∪V_C∪V(U).
Base: empty core -> brute-force DFS avoiding F. Then Graham(A) = GO(A, ∅)."""
import random,sys,time
sys.setrecursionlimit(10000)
def lift(A,p):
    r=sorted(x%p for x in A)
    for T in range(len(r)+1):
        P=r[:len(r)-T]; N=[p-x for x in r[len(r)-T:]]
        if sum(P)==sum(N): return P,N
def core_walk(C):
    S=sorted(C,reverse=True); c=S[0]; d=[x if i%2==0 else -x for i,x in enumerate(S[1:])]
    return d+[c]+[-x for x in d[::-1]]+[-c]
def brute(R,F,p,first_ok=None,tl=3):
    n=len(R);t0=time.time()
    def rec(mask,s,seen,seq):
        if time.time()-t0>tl: raise TimeoutError
        if mask==(1<<n)-1: return list(seq)
        for j in range(n):
            if mask>>j&1: continue
            if not seq and first_ok and not first_ok(R[j]): continue
            t=(s+R[j])%p; last=(mask|1<<j)==(1<<n)-1
            if last:
                if t==0: return seq+[R[j]]
                continue
            if t==0 or t in F or t in seen: continue
            seen.add(t);seq.append(R[j])
            r=rec(mask|1<<j,t,seen,seq)
            if r: return r
            seq.pop();seen.discard(t)
        return None
    try: return rec(0,0,set(),[])
    except TimeoutError: return None
def GO(R,F,p,depth=0,first_ok=None):
    if not R: return []
    if len(R)<=8: return brute(R,F,p,first_ok)
    cands=[]
    for lam in range(1,p):
        P,N=lift([lam*x for x in R],p);C=set(P)&set(N)
        rem=[x for x in P if x not in C]+[-x for x in N if x not in C]
        if C: cands.append((len(rem),lam,C,rem))
    cands.sort()
    for _,lam,C,rem in cands[:6]:
        inv=pow(lam,p-2,p); lF={(lam*f)%p for f in F}
        core=core_walk(C); n=len(core)
        for rot in range(n):
            cw=core[rot:]+core[:rot]
            V=[0]
            for x in cw[:-1]: V.append((V[-1]+x)%p)
            VC=set(V)
            if VC & lF: continue
            top=V[-1]
            F2=lF|VC
            if not rem:
                if first_ok is None or first_ok(cw[0]*inv%p): return [x*inv%p for x in cw]
                continue
            fo=lambda x1,top=top,F2=F2: ((top+x1)%p not in F2) and (x1%p not in F2)
            U=GO(rem,F2-{0},p,depth+1,fo)
            if U is None: continue
            # bridging point top+x1 must also avoid U's vertices
            Uv=set();s=0
            for x in U[:-1]: s=(s+x)%p;Uv.add(s)
            if (top+U[0])%p in Uv: continue
            W=cw[:-1]+[U[0]]+[cw[-1]]+U[1:]
            W=[x*inv%p for x in W]
            if first_ok is not None and not first_ok(W[0]): continue
            return W
    STATS['fallback']+=1
    return None
STATS={'fallback':0}
def valid(W,A,p,F=set()):
    if sorted(x%p for x in W)!=sorted(x%p for x in A): return False
    s=0;seen=set()
    for x in W[:-1]:
        s=(s+x)%p
        if s==0 or s in seen or s in F: return False
        seen.add(s)
    return (s+W[-1])%p==0
p=int(sys.argv[1]);random.seed(int(sys.argv[3]) if len(sys.argv)>3 else 1)
for alpha in map(float,sys.argv[2].split(',')):
    k=int(alpha*(p-1));ok=0;T=8
    for _ in range(T):
        while True:
            A=random.sample(range(1,p),k-1);s=(-sum(A))%p
            if s and s not in A: A.append(s);break
        W=GO(A,set(),p)
        ok+= bool(W) and valid(W,A,p)
    print("  fallbacks (no structured step found at some level, |R|>8):",STATS["fallback"]); STATS["fallback"]=0
    print(f"p={p} alpha={alpha}: recursive GO succeeded {ok}/{T}",flush=True)
