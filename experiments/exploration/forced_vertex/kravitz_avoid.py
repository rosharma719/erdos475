from itertools import combinations, permutations, accumulate
import sys
from collections import Counter
K=int(sys.argv[1]); M=int(sys.argv[2])
def pre(o): return list(accumulate(o))
shape=Counter(); ex={}
sets=[frozenset(c) for r in range(0,M+1) for c in combinations(range(1,K+1),r)]
for X in sets:
  oX=[pre(o) for o in permutations(sorted(X))]
  for Y in sets:
    if not X and not Y: continue
    if len(X)+len(Y)!=M or len(X)>len(Y) or (len(X)==len(Y) and sorted(X)>sorted(Y)): continue
    oY=[pre(o) for o in permutations(sorted(Y))]
    for w in range(1,sum(X)+sum(Y)+1):
        ok=False
        for px in oX:
            if w in px[:-1]: continue
            Xs=set(px)
            for py in oY:
                if w in py[:-1]: continue
                inter=Xs&set(py)
                if sum(X)==sum(Y): inter-={sum(X)}
                if not inter: ok=True;break
            if ok:break
        if not ok:
            s=(len(X),len(Y)); shape[s]+=1; ex.setdefault(s,(sorted(X),sorted(Y),w))
print(sorted(shape.items())); 
for s,e in sorted(ex.items()): print(s,e)
