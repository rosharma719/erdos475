"""Canonical B-path search by descending labels (edge-based), fixed edges 0-a, a-(M+1). Prints label->edge table."""
import sys, time
sys.setrecursionlimit(100000)
def solve(M,a,tl=60):
    b=M+1-a; U=sorted(set([-1,0])|set(range(2,M-1))|{M+1}); Us=set(U)
    deg={v:0 for v in U}; parent={v:v for v in U}
    def find(x):
        while parent[x]!=x: x=parent[x]
        return x
    t0=time.time(); E={}
    def add(x,y):
        rx,ry=find(x),find(y); deg[x]+=1;deg[y]+=1; parent[rx]=ry; return rx,ry
    def undo(x,y,rx,ry):
        deg[x]-=1;deg[y]-=1; parent[rx]=rx
    r1=add(0,a); r2=add(a,M+1); E[a]=(0,a); E[b]=(a,M+1)
    labels=[L for L in range(M-1,0,-1) if L not in (a,b)]
    def rec(i):
        if time.time()-t0>tl: raise TimeoutError
        if i==len(labels): return True
        L=labels[i]
        # pruning: isolated vertices need edges; each remaining label adds 2 endpoint-degrees
        zero=sum(1 for v in U if deg[v]==0)
        if zero>2*(len(labels)-i): return False
        for x in U:
            y=x+L
            if y in Us and deg[x]<2 and deg[y]<2:
                rx,ry=find(x),find(y)
                if rx==ry: continue
                deg[x]+=1;deg[y]+=1;parent[rx]=ry;E[L]=(x,y)
                if rec(i+1): return True
                deg[x]-=1;deg[y]-=1;parent[rx]=rx;del E[L]
        return False
    try:
        ok=rec(0)
    except TimeoutError: return 'TO'
    return E if ok else None
def rel(v,M): return str(v) if v<M/2 else ("M" if v==M else f"M{v-M:+d}")
if __name__=="__main__":
    for M in map(int,sys.argv[2].split(',')):
        a=int(sys.argv[1])
        E=solve(M,a)
        if E in (None,'TO'): print(M,a,E);continue
        print(M,a," ".join(f"{M-L}:{rel(E[L][0],M)}-{rel(E[L][1],M)}" for L in range(M-1,0,-1)),flush=True)
