import sys,time
def lrdfs(M,a,k,tl=3):
    V=set(range(M))-{k+1,k+a}; L=set(range(1,M))-{a,M+1-a}; path=[k];used=set();on={k};t0=time.time()
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
    try: return path if rec() else None
    except TimeoutError: return 'TO'
a=int(sys.argv[1])
for M in range(2*a+1,2*a+13):
    k=(M-a)//2; r=lrdfs(M,a,k)
    print(M,k,'holes',k+1,k+a,'b',M+1-a,r if not isinstance(r,list) else ' '.join(str(v) for v in r),flush=True)
