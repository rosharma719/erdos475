import sys, itertools, time
def graceful_from(n,k):
    if n<=1: return k==0
    for perm in itertools.permutations([x for x in range(n) if x!=k]):
        p=(k,)+perm
        if sorted(abs(p[i+1]-p[i]) for i in range(n-1))==list(range(1,n)): return list(p)
    return None
def search(M,a,n,tl=20):
    b=M+1-a; D=set([-1,0])|set(range(2,M-1))|{M+1}
    labs=set(range(n+1,M))   # frame labels incl a,b ; connection label n ; core 1..n-1
    t0=time.time()
    for s in range(2,M-1-n+1):
        core=set(range(s,s+n))
        if a in core: continue
        F=D-core
        for st in sorted(F):
            path=[st];vis={st};used=set()
            def rec():
                if time.time()-t0>tl: raise TimeoutError
                v=path[-1]
                if len(vis)==len(F):
                    if used!=labs: return None
                    if not any(path[j:j+3] in ([0,a,M+1],[M+1,a,0]) for j in range(len(path)-2)): return None
                    for c0 in (v+n,v-n):
                        if c0 in core:
                            g=graceful_from(n,c0-s)
                            if g is not None: return list(path)+[s+x for x in g]
                    return None
                # triple forcing
                if v==a and len(path)>=2 and path[-2] in (0,M+1):
                    cand=[M+1 if path[-2]==0 else 0]
                else:
                    cand=[v+L for L in labs-used]+[v-L for L in labs-used]
                for w in cand:
                    if w in F and w not in vis and abs(w-v) in labs and abs(w-v) not in used:
                        if w==a and v not in (0,M+1): continue
                        if v==a and w not in (0,M+1): continue
                        path.append(w);vis.add(w);used.add(abs(w-v))
                        r=rec()
                        if r: return r
                        path.pop();vis.discard(w);used.discard(abs(w-v))
                return None
            r=rec()
            if r: return s,r
    return None
for M in range(int(sys.argv[1]),int(sys.argv[2])+1):
    for a in range(3,(M+1)//2+1):
        if 2*a==M+1: continue
        n=a-1
        try: r=search(M,a,n,tl=15)
        except TimeoutError: r='TO'
        print(M,a,"n",n,r,flush=True)
