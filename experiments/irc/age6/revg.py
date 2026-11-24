"""Does LR(M,a,k) have a solution whose REVERSE starts with the G-step header (M-2, 0, M-1, 2)?
Equivalently: path from 2 to k on [0,M-1]\\{k+1,k+a,M-2,0,M-1}, lengths [1,M-1]\\{a,b,M-1,M-2,M-3}."""
import sys
from shape_sat import hpath
for M in range(int(sys.argv[1]),int(sys.argv[2])):
    row=[]
    for a in range(5,M//2+1):
        b=M+1-a; ks=[]
        for k in range(0,M-a):
            V=set(range(M))-{k+1,k+a}
            if not {M-2,0,M-1,2}<=V or k in (M-2,0,M-1,2): continue
            L=set(range(1,M))-{a,b}
            if not {M-1,M-2,M-3}<=L: continue
            r=hpath(V-{M-2,0,M-1},L-{M-1,M-2,M-3},2,timeout=10,end=k)
            if isinstance(r,list): ks.append(k)
        row.append(f"{a}:{ks}")
    print(M,' '.join(row),flush=True)
