"""Induction test: from a B-path for (M,a), build (M+1,a) by shifting all vertices >= t up by 1 and inserting the new
vertex t at an end of the path (or at both-end variants). Chain as far as possible (DFS over t and end choices)."""
import sys; sys.path.insert(0,'../../research/data')
from B_certs import C
def isB(M,a,D):
    S={-1,0,*range(2,M-1),M+1}
    return len(D)==M and set(D)==S and sorted(abs(y-x) for x,y in zip(D,D[1:]))==list(range(1,M)) and any(D[j:j+3] in ([0,a,M+1],[M+1,a,0]) for j in range(M-2))
def grow(M,a,D):
    outs=[]
    for t in range(a+1,M):           # new vertex value t in [2,M-1] for D_B(M+1)
        E=[x+1 if x>=t else x for x in D]
        for cand in ([t]+E, E+[t]):
            if isB(M+1,a,cand): outs.append((t,cand))
    return outs
def chain(M,a,D,depth,limit):
    if depth==limit: return [D]
    for t,E in grow(M,a,D):
        r=chain(M+1,a,E,depth+1,limit)
        if r: return [D]+r
    return None
for a in range(2,7):
    best=None
    for (M,aa),D in sorted(C.items()):
        if aa!=a: continue
        for L in (40,):
            r=chain(M,a,D,0,L)
            if r: best=(M,len(r)); break
        if best: break
    # also report max chain length from each cert with smaller limit
    lens=[]
    for (M,aa),D in sorted(C.items()):
        if aa!=a: continue
        # greedy longest
        cur=[(M,D)];m=M;d=D
        while True:
            g=grow(m,a,d)
            if not g: break
            d=g[0][1];m+=1
            if m>m+0 and m>200: break
            if m-M>60: break
        lens.append((M,m))
    print("a",a,"full chain of 40 from",best,"greedy reach",lens[:8],flush=True)
