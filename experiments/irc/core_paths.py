# Core problem: on [0,n]\{w}, two disjoint paths starting at s1,s2 covering all, labels exactly {1..n}\{a, n+4-a}
import sys
def solve(n,a,w,s1,s2):
    labs=set(range(1,n+1))-{a,n+4-a}
    V=set(range(0,n+1))-{w}
    if s1 not in V or s2 not in V or len(labs)!=len(V)-2: return None
    used=set();vis={s1,s2};paths=[[s1],[s2]]
    def rec():
        if len(vis)==len(V): return [list(p) for p in paths]
        for pi in (0,1):
            x=paths[pi][-1]
            for L in sorted(labs-used,reverse=True):
                for y in (x+L,x-L):
                    if y in V and y not in vis:
                        used.add(L);vis.add(y);paths[pi].append(y)
                        r=rec()
                        if r: return r
                        paths[pi].pop();vis.discard(y);used.discard(L)
            # must extend largest label somewhere: prune: largest remaining label must be placed by some path
        return None
    return rec()
for M in range(9,19):
    n=M-3
    for a in range(4,(M+1)//2+1):
        b=M+1-a
        if a==b: continue
        for w in (a,b):
            r=solve(n,a,w-2,n-1,0)
            if r: print(M,a,"w",w,"optII",r);break
        else: print(M,a,"optII none")
