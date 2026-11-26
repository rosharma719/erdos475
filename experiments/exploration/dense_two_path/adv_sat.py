import sys, random
from twopath_sat import solve, verify
M=int(sys.argv[1]); N=int(sys.argv[2]); rng=random.Random(9)
runs=[frozenset(s*v for v in range(a,b+1)) for s in (1,-1) for a in range(1,M+1) for b in range(a,M+1)]
done=0; ok=0; bad=0
while done<N:
    T=set()
    for _ in range(rng.choice([2,3])): T|=rng.choice(runs)
    s=sum(T)
    if s and abs(s)<=M and -s not in T: T.add(-s)
    if sum(T)!=0 or max(map(abs,T))!=M or len(T)>M//2 or len(T)<2: continue
    done+=1; r=solve(M,T,True)
    if r and verify(M,T,*r): ok+=1
    else: bad+=1; print("NO PATHS" if not r else "VERIFY-ERR",M,sorted(T),flush=True)
print(f"adversarial M={M} k<=M/2 samples={N} ok={ok} fail={bad}",flush=True)
