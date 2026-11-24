from itertools import combinations
import sys
def path_ok(steps,r,M):
    # delta = steps; need distinct partial sums D (incl 0), span<=M-1, and the step -r lands at global min
    D=[0];s=0;land=None
    for x in steps:
        s+=x; D.append(s)
        if x==-r: land=s
    return len(set(D))==len(D) and max(D)-min(D)<=M-1 and land is not None and land==min(D)
def spiral(ds,first):  # descending alternating, first sign
    return [d*(first if i%2==0 else -first) for i,d in enumerate(ds)]
def templates(S,r):
    M=max(S); R=sorted(set(S)-{M,r},reverse=True)
    # T1: -r then inward spiral up
    yield 'T1',[-r]+spiral(R,1)
    # T2: outward spiral ascending, ending so that -r is last down-step
    asc=sorted(set(S)-{M})
    for first in (1,-1):
        yield 'T2',[a*(first if i%2==0 else -first) for i,a in enumerate(asc)]
        yield 'T2r',[-x for x in reversed([a*(first if i%2==0 else -first) for i,a in enumerate(asc)])]
    # T3: inward spiral of U (first sign f), then -r, then inward spiral of V upward, for all splits by rank
    for k in range(0,len(R)+1):
        for U,V in ((R[k:],R[:k]),(R[:k],R[k:])):
            for f in (1,-1):
                yield 'T3',spiral(U,f)+[-r]+spiral(V,1)
                yield 'T3b',spiral(V,1)+[-r]+spiral(U,f)
def cover(S,r):
    M=max(S)
    if r==M: return 'max'
    for name,st in templates(S,r):
        if path_ok(st,r,M): return name
    return None
V=int(sys.argv[1]); tot=0; miss=[]; from collections import Counter; c=Counter()
for m in range(2,V+1):
    for S in combinations(range(1,V+1),m):
        for r in S:
            tot+=1; t=cover(S,r); c[t]+=1
            if t is None: miss.append((S,r))
print(tot,dict(c)); print(len(miss),miss[:25])
