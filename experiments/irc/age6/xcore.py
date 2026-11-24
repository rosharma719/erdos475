"""X-bridge core: W=(delta,+M,-delta^rev,+a,-M,+b,-(M+1)). D = {0} ∪ ([3,M-1]\\{a}) ∪ {M+2}, path from 0,
labels [1,M-1]\\{a,b}, b=M+1-a. (All bridge/range/D∩(D+M) constraints hold automatically for this D.)"""
import sys,time
sys.setrecursionlimit(10000)
def xcore(M,a,tl=5):
    b=M+1-a; V=set([0,M+2])|set(range(3,M)); V.discard(a)
    L=set(range(1,M))-{a,b}; path=[0]; used=set(); on={0}; t0=time.time()
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
def walk(M,a,path):
    b=M+1-a; d=[y-x for x,y in zip(path,path[1:])]
    return d+[M]+[-x for x in d[::-1]]+[a,-M,b,-(M+1)]
def ok(M,a,w):
    b=M+1-a
    if sorted(x for x in w if x>0)!=list(range(1,M+1)): return False
    if sorted(-x for x in w if x<0)!=sorted(set(range(1,M+2))-{a,b}): return False
    v=0;S=[0]
    for x in w[:-1]: v+=x;S.append(v)
    return len(set(S))==len(S) and v+w[-1]==0 and max(S)-min(S)<=2*M+2
if __name__=="__main__":
    for a in map(int,sys.argv[1].split(',')):
        for M in range(max(2*a,int(sys.argv[2])),int(sys.argv[3])):
            r=xcore(M,a,2)
            print(a,M,r if not isinstance(r,list) else (ok(M,a,walk(M,a,r)),r),flush=True)
