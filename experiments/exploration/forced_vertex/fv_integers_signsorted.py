# FV over Z restricted to sign-sorted tails: after root t, the remaining labels appear as [positives then negatives] or [negatives then positives]
import sys
from itertools import combinations, permutations
K=int(sys.argv[1]); fails=0; tests=0
def ok(t,order,x):
    s=0; seen={0}; s=t
    if s in seen or s==x: return False
    seen.add(s)
    for a in order[:-1]:
        s+=a
        if s in seen or s==x: return False
        seen.add(s)
    return True
for n in range(3,int(sys.argv[2])+1):
    for B in combinations([v for v in range(-K,K+1) if v],n):
        if sum(B): continue
        for t in B:
            R=[b for b in B if b!=t]; P=[b for b in R if b>0]; N=[b for b in R if b<0]
            cands=[list(a)+list(b) for a in permutations(P) for b in permutations(N)]+[list(b)+list(a) for a in permutations(P) for b in permutations(N)]
            lo=-sum(-b for b in N)+min(0,t)-K; hi=sum(P)+max(0,t)+K
            for x in range(lo,hi+1):
                if x in (0,t) or 2*x==t: continue
                tests+=1
                if not any(ok(t,c,x) for c in cands):
                    fails+=1
                    if fails<=8: print("sign-sorted fails:",B,"t=",t,"x=",x)
print("K",K,"tests",tests,"fails",fails)
