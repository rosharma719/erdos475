import sys, time
def ham(D,labs,need,tl=20):
    """Hamiltonian path on D with edge lengths exactly labs (each once), containing consecutive triple need (either direction)."""
    D=sorted(D);Ds=set(D);n=len(D);t0=time.time()
    tri=list(need);tri_r=tri[::-1]
    def contains(p):
        s=','.join(map(str,p)); return (','.join(map(str,tri)) in s) or (','.join(map(str,tri_r)) in s)
    for st in D:
        path=[st];vis={st};used=set()
        def rec():
            if time.time()-t0>tl: raise TimeoutError
            if len(path)==n: return list(path) if contains(path) else None
            x=path[-1]
            # forced continuation through the triple
            cand=[]
            if x==tri[0] and tri[1] not in vis: cand=[tri[1]]
            elif x==tri[1] and len(path)>1 and path[-2]==tri[0]: cand=[tri[2]]
            elif x==tri[2] and tri[1] not in vis: cand=[tri[1]]
            elif x==tri[1] and len(path)>1 and path[-2]==tri[2]: cand=[tri[0]]
            else: cand=[x+L for L in labs-used]+[x-L for L in labs-used]
            for y in cand:
                L=abs(y-x)
                if y in Ds and y not in vis and L in labs and L not in used:
                    # tri vertices must be entered properly
                    if y==tri[1] and x not in (tri[0],tri[2]): continue
                    path.append(y);vis.add(y);used.add(L)
                    r=rec()
                    if r: return r
                    path.pop();vis.discard(y);used.discard(L)
            return None
        r=rec()
        if r: return r
    return None
def shapes(M):
    A=set([0,M+1])|set(range(2,M))
    B=set([-1,0,M+1])|set(range(2,M-1))
    Bm=set([0,M+1,M+2])|set(range(3,M))   # mirror of B
    return {'A':A,'B':B,'Bm':Bm}
for M in range(int(sys.argv[1]),int(sys.argv[2])+1):
    for a in range(2,(M+1)//2+1):
        b=M+1-a
        if a==b: continue
        out=None
        for nm,D in shapes(M).items():
            for w in (a,b):
                if w not in D: continue
                try: r=ham(D,set(range(1,M)),(0,w,M+1),tl=10)
                except TimeoutError: r=None
                if r: out=(nm,w,r);break
            if out: break
        print(M,a,out,flush=True)
