"""Structured search: half-walk path on D=(A) {0}∪[2,M-1]∪{M+1} = header + inward zigzag on a core [s,t] minus {w}.
The jump 0-w-(M+1) lies in the header (w is in the core interval but visited by the header)."""
import sys, itertools
def zig(s,t,w,start_low=True):
    lo=[x for x in range(s,t+1) if x!=w]; seq=[]
    i,j=0,len(lo)-1; turn=start_low
    while i<=j:
        if turn: seq.append(lo[i]);i+=1
        else: seq.append(lo[j]);j-=1
        turn=not turn
    return seq
def header(Hv,labels,end,M,w):
    """Hamiltonian path on Hv (set) + jump through w, last vertex adjacent to `end` (zigzag start); labels exact."""
    Hv=set(Hv); need=len(Hv)+1  # vertices in header incl. w
    for st in sorted(Hv):
        path=[st];vis={st};used=set()
        def rec():
            if len(path)==need:
                L=abs(end-path[-1])
                if L in labels and L not in used and len(used)+1==len(labels): return list(path)
                return None
            x=path[-1]
            if x==0 and w not in vis: cand=[w]
            elif x==M+1 and w not in vis: cand=[w]
            elif x==w: cand=[M+1] if path[-2]==0 else ([0] if path[-2]==M+1 else [])
            else: cand=[y for y in (Hv|{w}) if y not in vis]
            for y in cand:
                if y in vis: continue
                if y==w and x not in (0,M+1): continue
                L=abs(y-x)
                if L in labels and L not in used:
                    path.append(y);vis.add(y);used.add(L)
                    r=rec()
                    if r: return r
                    path.pop();vis.discard(y);used.discard(L)
            return None
        r=rec()
        if r: return r
    return None
def solve(M,a):
    b=M+1-a; D=set([0,M+1])|set(range(2,M))
    best=None
    for w in (a,b):
        for s in range(2,M):
            for t in range(M-1,s,-1):
                if not (s<=w<=t): continue
                for sl in (True,False):
                    Z=zig(s,t,w,sl)
                    zl=[abs(Z[i+1]-Z[i]) for i in range(len(Z)-1)]
                    if len(set(zl))<len(zl): continue
                    rest=set(range(1,M))-set(zl)
                    if not {a,b}<=rest: continue
                    Hv=(D-set(range(s,t+1)))
                    if len(Hv)>9: continue
                    h=header(Hv,rest,Z[0],M,w)
                    if h: return (w,s,t,sl,h,Z)
    return None
for M in range(int(sys.argv[1]),int(sys.argv[2])+1):
    for a in range(2,(M+1)//2+1):
        if 2*a==M+1: continue
        r=solve(M,a)
        print(M,a,r if r else "NONE",flush=True)
