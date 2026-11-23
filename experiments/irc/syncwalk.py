"""Synchronized-walk form of the overlay half-walk (general pairs).
P,N balanced with a common element c. Split P\{c}=P1+P2, N\{c}=N1+N2. X: walk 0->e with steps +P1,-N1. K: walk 0->e with
steps +N2,-P2. Valid ordering W=(X, +c, -K^rev, -c) iff X self-avoiding, K self-avoiding, V(X) ∩ (V(K)+c) = ∅.
(Any such pair gives a valid cycle; compatibility/common refinement is NOT needed for validity.)
STRUCTURED test: require X and K to be CO-MONOTONE (common refinement), i.e. a genuine mirrored half-walk with merges."""
import itertools, random, sys
def verts(seq):
    v=[0]
    for s in seq: v.append(v[-1]+s)
    return v
def comonotone(xv,kv):
    """Common refinement test: interleave the two vertex sequences into one walk D such that, between consecutive
    X-vertices, D moves monotonically from x_i to x_{i+1}, and likewise for K. State (i,j,p): next targets xv[i+1],
    kv[j+1]; current D point p."""
    from functools import lru_cache
    m,n=len(xv)-1,len(kv)-1
    def between(p,q,end):  # q lies on the monotone segment from p to end (inclusive of end)
        return (p<=q<=end) or (end<=q<=p)
    @lru_cache(None)
    def ok(i,j,p):
        if i==m and j==n: return True
        opts=[]
        if i<m: opts.append((i+1,j,xv[i+1]))
        if j<n: opts.append((i,j+1,kv[j+1]))
        for ii,jj,q in opts:
            if q==p: 
                # both targets coincide at p
                pass
            if i<m and not between(p,q,xv[i+1]): continue
            if j<n and not between(p,q,kv[j+1]): continue
            # if we advance K only but X segment continues, fine; same for X
            if ok(ii,jj,q): return True
        return False
    return ok(0,0,0)
def search(P,N,structured=True,R=None):
    C=set(P)&set(N)
    for c in sorted(C,reverse=True):
        Pr=[x for x in P if x!=c]; Nr=[x for x in N if x!=c]
        for mp in range(1<<len(Pr)):
            P1=[Pr[i] for i in range(len(Pr)) if mp>>i&1]; P2=[Pr[i] for i in range(len(Pr)) if not mp>>i&1]
            for mn in range(1<<len(Nr)):
                N1=[Nr[i] for i in range(len(Nr)) if mn>>i&1]; N2=[Nr[i] for i in range(len(Nr)) if not mn>>i&1]
                e=sum(P1)-sum(N1)
                if sum(N2)-sum(P2)!=e: continue
                Xs=[s for s in itertools.permutations(P1+[-x for x in N1])]
                Ks=[s for s in itertools.permutations(N2+[-x for x in P2])]
                Xg=[(s,verts(s)) for s in Xs if len(set(verts(s)))==len(s)+1]
                Kg=[(s,verts(s)) for s in Ks if len(set(verts(s)))==len(s)+1]
                for xs,xv in Xg:
                    for ks,kv in Kg:
                        if set(xv)&{v+c for v in kv}: continue
                        allv=xv+[v+c for v in kv]
                        if R is not None and max(allv)-min(allv)>R: continue
                        if structured and not comonotone(tuple(xv),tuple(kv)): continue
                        return c,xs,ks
    return None
if __name__=="__main__":
    random.seed(int(sys.argv[1]));H=int(sys.argv[2]);T=int(sys.argv[3])
    st={'yes':0,'no':0,'nocommon':0}
    for _ in range(T):
        while True:
            P=sorted(random.sample(range(1,H+1),random.randint(3,5)));N=sorted(random.sample(range(1,H+1),random.randint(3,5)))
            if sum(P)==sum(N) and P!=N: break
        if not set(P)&set(N): st['nocommon']+=1; continue
        R=max(P)+max(N)+((max(P)+max(N))%2)
        r=search(P,N,True,R)
        if r: st['yes']+=1
        else: st['no']+=1; print("NO",P,N,flush=True)
    print(st)
