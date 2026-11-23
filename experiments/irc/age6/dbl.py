"""LR via cyclic double steps in Z_{M+1}: from u, do u->u+s->u+2s (s=±d), linear lengths must be {d, M+1-d}.
Singles: length 1, and for odd M the self-paired (M+1)/2. Vertices in [0,M-1] minus holes."""
import sys,time
def run(M,a,k,tl=3):
    N=M+1;b=M+1-a;V=set(range(M))-{k+1,k+a}
    pairs=[d for d in range(2,M//2+1) if d!=a and 2*d!=N]
    singles=[1]+([N//2] if N%2==0 else [])
    path=[k];on={k};t0=time.time()
    def rec(usedp,useds):
        if time.time()-t0>tl: raise TimeoutError
        if len(path)==len(V): return True
        u=path[-1]
        for d in pairs:
            if d in usedp: continue
            for s in (d,-d):
                v=(u+s)%N;w=(v+s)%N
                if v in V and w in V and v not in on and w not in on and v!=w and {abs(v-u),abs(w-v)}=={d,N-d}:
                    path.extend([v,w]);on.update([v,w])
                    if rec(usedp|{d},useds): return True
                    path.pop();path.pop();on.difference_update([v,w])
        for L in singles:
            if L in useds: continue
            for v in (u+L,u-L):
                if v in V and v not in on:
                    path.append(v);on.add(v)
                    if rec(usedp,useds|{L}): return True
                    path.pop();on.discard(v)
        return False
    try: return list(path) if rec(frozenset(),frozenset()) else None
    except TimeoutError: return 'TO'
for M in range(int(sys.argv[1]),int(sys.argv[2])):
    row=[]
    for a in range(2,M//2+1):
        r=None
        for k in sorted(range(0,M-a),key=lambda k:abs(k-(M-a)//2)):
            r=run(M,a,k,0.5)
            if isinstance(r,list): break
        row.append(f"{a}:{'Y' if isinstance(r,list) else '-'}")
    print(M,' '.join(row),flush=True)
