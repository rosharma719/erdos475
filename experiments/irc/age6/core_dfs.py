"""Shifted core for bridge G: vertices {0} ∪ ([3,n-2]\{h}) ∪ {n}, n=M+1, start a+1, labels [1,n-2]\{a,n-a}.
DFS largest-label-first; try all h."""
import sys,time
sys.setrecursionlimit(10000)
def core(n,a,h,tl=5):
    V=set([0,n])|set(range(3,n-1)); V.discard(h)
    L=set(range(1,n-1))-{a,n-a}; s=a+1
    if s not in V: return None
    path=[s]; used=set(); on={s}; t0=time.time()
    def rec():
        if time.time()-t0>tl: raise TimeoutError
        if len(path)==len(V): return True
        x=path[-1]
        for l in sorted(L-used,reverse=True):
            for y in (x+l,x-l):
                if y in V and y not in on:
                    path.append(y);used.add(l);on.add(y)
                    if rec(): return True
                    path.pop();used.discard(l);on.discard(y)
        return False
    try: return list(path) if rec() else None
    except TimeoutError: return 'TO'
if __name__=="__main__":
    a=int(sys.argv[1])
    for M in range(int(sys.argv[2]),int(sys.argv[3])):
        n=M+1;res=None
        for h in range(3,n-1):
            if h==a+1: continue
            r=core(n,a,h,1)
            if isinstance(r,list): res=(h,r);break
        print(M,res,flush=True)
