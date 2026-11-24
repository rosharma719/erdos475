import itertools,sys
exec(open('rs3.py').read().split("V=int")[0])
def any_halfwalk(S,r):
    M=max(S); R=sorted(set(S)-{M})
    for perm in itertools.permutations(R):
        for eps in itertools.product((1,-1),repeat=len(R)):
            st=[e*x for e,x in zip(eps,perm)]
            if path_ok(st,r,M): return st
    return None
def any_walk(S,r,lo,hi):
    el=[x for x in S if x!=r]+[-x for x in S]
    vis={0,r}
    def dfs(pos,rem):
        if not rem: return pos==0
        for i,x in enumerate(rem):
            w=pos+x
            if len(rem)==1: 
                if w==0: return True
                continue
            if lo<=w<=hi and w not in vis:
                vis.add(w)
                if dfs(w,rem[:i]+rem[i+1:]): return True
                vis.discard(w)
        return False
    return dfs(r,el)
from itertools import combinations
miss=[(S,r) for m in range(2,9) for S in combinations(range(1,10),m) for r in S if cover(S,r) is None]
hw=0; walk=0; neither=[]
for S,r in miss:
    M=max(S)
    if any_halfwalk(S,r): hw+=1
    elif any_walk(S,r,-M,M): walk+=1
    else: neither.append((S,r))
print(len(miss),"halfwalk exists:",hw,"only general walk:",walk,"none:",len(neither),neither[:20])
