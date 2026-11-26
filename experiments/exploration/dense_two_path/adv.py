import sys, itertools, random
from cutlp import feasible
M=int(sys.argv[1]); kmax_frac=float(sys.argv[2]); budget=int(sys.argv[3]); rng=random.Random(5)
runs=[]  # signed intervals
for s in (1,-1):
    for a in range(1,M+1):
        for b in range(a,M+1): runs.append(frozenset(s*v for v in range(a,b+1)))
cands=set()
tries=0
while len(cands)<budget and tries<budget*200:
    tries+=1
    r=rng.choice([1,2,2,3,3])
    T=set()
    for _ in range(r): T|=rng.choice(runs)
    if any(-t in T for t in []): pass
    # fix sum with up to 2 singletons
    s=sum(T); extra=[]
    if s!=0:
        if abs(s)<=M and -s not in T and -s!=0: extra=[-s]
        else:
            x=rng.randint(1,M)*(-1 if s>0 else 1); y=-(s+x)
            if y and abs(y)<=M and x!=y and x not in T and y not in T: extra=[x,y]
            else: continue
    T|=set(extra)
    if sum(T)!=0 or 0 in T or max(map(abs,T))!=M: continue
    if len(T)>kmax_frac*M or len(T)<2: continue
    cands.add(frozenset(T))
bad=0
for T in cands:
    if not feasible(M,T):
        bad+=1
        if bad<=5: print("OBSTRUCTED k=%d"%len(T),sorted(T))
print(f"M={M} k<= {kmax_frac}M structured candidates={len(cands)} obstructed={bad}")
