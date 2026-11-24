# For balanced (P,N) with values<=V: does an admissible y in N exist for the max-root lift
# (y != p1, t=p1-y; t>0 needs t not in P; t<0 needs -t not in N\{y}), with the reduced instance not exceptional?
from itertools import combinations
import sys
V=int(sys.argv[1])
def exc(r,P,N):
    P=sorted(P);N=sorted(N)
    if len(P)==2 and P==N and r==min(P): return True
    if len(P)==3 and len(N)==3 and max(P)==max(N):
        c=max(P)
        if r!=c and r in P and (c-r) in P and all((c-x) in N for x in N if x!=c):
            b=min(x for x in N if x!=c)
            if r<b or (P==N and r!=c): return True
    if len(P)==5 and P==N and P==[P[0]*i for i in range(1,6)] and r==P[0]: return True
    return False
from collections import defaultdict
bysum=defaultdict(list)
vals=range(1,V+1)
for k in range(1,V+1):
    for S in combinations(vals,k): bysum[sum(S)].append(frozenset(S))
tot=stuck=0; ex=[]
for s,L in bysum.items():
    for P in L:
        for N in L:
            p1=max(P); tot+=1; ok=False
            for y in N:
                if y==p1: continue
                t=p1-y
                if t>0:
                    if t in P: continue
                    P2=(P-{p1})|{t}; N2=N-{y}; r=t
                    # root t positive
                    if not exc(r,P2,N2): ok=True;break
                else:
                    if -t in N-{y}: continue
                    P2=P-{p1}; N2=(N-{y})|{-t}
                    # negative root: by negation this is instance (N2,P2) rooted at +(-t) -- window flips; record separately
                    ok=True;break
            if not ok:
                stuck+=1
                if len(ex)<15: ex.append((sorted(P),sorted(N)))
print(f"V={V} instances={tot} no-admissible-lift={stuck} ({stuck/tot:.3%})")
print(ex)
