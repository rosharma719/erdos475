import sys
sys.setrecursionlimit(10000)
def allzig(P,N):
    P=tuple(P);N=tuple(N);res=[]
    def rec(x,y,up,un,seen,steps):
        if len(steps)==len(P)+len(N):
            if x==y: res.append((tuple(steps),sorted(seen)))
            return
        if steps and x==y: return
        if x<=y:
            for i,p in enumerate(P):
                if not up>>i&1:
                    nx=x+p; d=nx-y
                    last=len(steps)+1==len(P)+len(N)
                    if not last and d in seen: continue
                    rec(nx,y,up|1<<i,un,seen|({d} if not last else set()),steps+[p])
        else:
            for j,n in enumerate(N):
                if not un>>j&1:
                    ny=y+n; d=x-ny
                    last=len(steps)+1==len(P)+len(N)
                    if not last and d in seen: continue
                    rec(x,ny,up,un|1<<j,seen|({d} if not last else set()),steps+[-n])
    rec(0,0,0,0,frozenset({0}),[])
    return res
if __name__=="__main__":
 for M in range(3,10):
    P=range(1,M+1);N=list(range(2,M))+[M+1]
    Z=allzig(P,N); bad=0; holes=set()
    for st,V in Z:
        Vs=set(V)
        hn=set(range(-M,1))-Vs; hp=set(range(1,M+1))-Vs
        assert len(hn)==len(hp)==1
        u=-next(iter(hn));v=next(iter(hp)); holes.add((u,v))
        if not ((M-u)**2+(M-v)**2<=u+3*v-2-2*(v==1)<=4*M-2): bad+=1
        # slack identity
        Q=sum(i*i for i in range(1,M+1))
        pos=[(s,d) for s,d in zip([0]+[sum(st[:k]) for k in range(1,len(st))],st)]
        lhs=sum(-s*d for s,d in pos if d>0)+sum(s*-d for s,d in pos if d<0)
        assert lhs==Q+M
    print(M,"zigzags",len(Z),"violations of Thm1",bad,"hole pairs",sorted(holes)[:8],"u+v==M+1 occurs:",any(u+v==M+1 for u,v in holes),flush=True)
