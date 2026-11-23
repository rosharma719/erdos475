"""Recursive GO with FLEXIBLE core walks: at each level, the core half-walk (δ, c, −δ^rev, −c) is searched (any pivot c,
any signed order δ of C\{c}) so that D, c+D are distinct and avoid the obstacles; then AVOID insertion of the remainder.
Brute force only for |R| <= 8. No fallback."""
import random,sys,time
sys.setrecursionlimit(10000)
from go_recursive import lift, brute, valid
STATS={'fail':0}
def core_search(C,F,p,tl=2,want=20):
    """yield core walks (as step lists) whose vertices avoid F."""
    C=sorted(C,reverse=True); t0=time.time(); found=0
    for c in C[:4]:
        rest=[x for x in C if x!=c]; n=len(rest)
        D=[0]; Ds={0}; used=[False]*n
        def ok(v): return v not in Ds and v not in F and (v+c)%p not in F and (v+c)%p not in Ds and (v-c)%p not in Ds and (v+c)%p!=0
        def rec(seq):
            nonlocal found
            if time.time()-t0>tl or found>=want: return
            if len(seq)==n:
                found+=1; yield seq+[c]+[-x for x in seq[::-1]]+[-c]; return
            idx=list(range(n)); random.shuffle(idx)
            for i in idx:
                if used[i]: continue
                for sg in (1,-1):
                    v=(D[-1]+sg*rest[i])%p
                    if ok(v):
                        used[i]=True;D.append(v);Ds.add(v)
                        yield from rec(seq+[sg*rest[i]])
                        used[i]=False;D.pop();Ds.discard(v)
        if 0 in F or c%p in F: continue
        yield from rec([])
def GO(R,F,p,first_ok=None):
    if not R: return []
    if len(R)<=8: return brute(R,F,p,first_ok)
    cands=[]
    for lam in range(1,p):
        P,N=lift([lam*x for x in R],p);C=set(P)&set(N)
        rem=[x for x in P if x not in C]+[-x for x in N if x not in C]
        if C: cands.append((len(rem),lam,C,rem))
    cands.sort()
    for _,lam,C,rem in cands[:4]:
        inv=pow(lam,p-2,p); lF={(lam*f)%p for f in F}
        for cw in core_search(C,lF,p):
            V=[0]
            for x in cw[:-1]: V.append((V[-1]+x)%p)
            VC=set(V); top=V[-1]; F2=lF|VC
            if not rem:
                W=[x*inv%p for x in cw]
                if first_ok is None or first_ok(W[0]): return W
                continue
            fo=lambda x1,top=top,F2=F2: ((top+x1)%p not in F2) and (x1%p not in F2)
            U=GO(rem,F2-{0},p,fo)
            if U is None: continue
            Uv=set();s=0
            for x in U[:-1]: s=(s+x)%p;Uv.add(s)
            if (top+U[0])%p in Uv: continue
            W=[x*inv%p for x in cw[:-1]+[U[0]]+[cw[-1]]+U[1:]]
            if first_ok is not None and not first_ok(W[0]): continue
            return W
    STATS['fail']+=1
    return None
if __name__=="__main__":
    p=int(sys.argv[1]);random.seed(2)
    for alpha in map(float,sys.argv[2].split(',')):
        k=int(alpha*(p-1));ok=0;T=int(sys.argv[3]) if len(sys.argv)>3 else 6
        for _ in range(T):
            while True:
                A=random.sample(range(1,p),k-1);s=(-sum(A))%p
                if s and s not in A: A.append(s);break
            W=GO(A,set(),p); ok+= bool(W) and valid(W,A,p)
        print(f"p={p} alpha={alpha}: flexible recursive GO {ok}/{T} (level failures {STATS['fail']})",flush=True); STATS['fail']=0
