"""G_{n,d}: path starting at n-1, n-1 distinct vertices of [1,n], labels [1,n-1]\{d}. Find seeds n=d+1,d+2,d+3 for d=4..16,
preferring zigzag-like structure (DFS with largest label first)."""
import sys,time
def G(n,d,tl=10):
    V=set(range(1,n+1)); L=set(range(1,n))-{d}; path=[n-1]; used=set(); t0=time.time()
    def rec():
        if time.time()-t0>tl: raise TimeoutError
        if len(path)==n-1: return True
        x=path[-1]
        for l in sorted(L-used,reverse=True):
            for y in (x+l,x-l):
                if y in V and y not in path:
                    path.append(y);used.add(l)
                    if rec(): return True
                    path.pop();used.discard(l)
        return False
    try: return list(path) if rec() else None
    except TimeoutError: return 'TO'
for d in range(4,int(sys.argv[1])+1):
    print(d,[G(n,d) for n in (d+1,d+2,d+3)],flush=True)
