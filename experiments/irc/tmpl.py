# Template (A): D={0}∪[2,M-1]∪{M+1}; delta starts 0 -> w -> M+1 (w in {b,a}); Hamiltonian path on D, labels {1..M-1} once.
import sys, time
def find(M,a,w,tl=5):
    b=M+1-a; D=set([0,M+1])|set(range(2,M))
    labs=set(range(1,M))-{a,b}
    path=[0,w,M+1]; vis=set(path); t0=time.time()
    def rec():
        if time.time()-t0>tl: raise TimeoutError
        if len(vis)==len(D): return list(path)
        x=path[-1]
        big=max(labs-used) if labs-used else 0
        for L in sorted(labs-used,reverse=True):
            for y in (x+L,x-L):
                if y in D and y not in vis:
                    used.add(L);vis.add(y);path.append(y)
                    r=rec()
                    if r: return r
                    path.pop();vis.discard(y);used.discard(L)
        return None
    used=set()
    try: return rec()
    except TimeoutError: return 'TO'
for M in range(7,int(sys.argv[1])+1):
    for a in range(2,(M+1)//2+1):
        b=M+1-a
        if a==b: continue
        r=find(M,a,b)
        if r in (None,'TO'): r2=find(M,a,a); 
        else: r2=None
        res=r if r not in (None,'TO') else r2
        print(M,a,res if res else (r,r2),flush=True)
