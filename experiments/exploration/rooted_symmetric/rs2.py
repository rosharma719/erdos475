from itertools import combinations
def alt_prefix(ds):
    s=0;out=[]
    for i,d in enumerate(ds): s+= d if i%2==0 else -d; out.append(s)
    return out
def rule1(S,r):
    M=max(S); ds=sorted(set(S)-{M,r},reverse=True)
    return r not in alt_prefix(ds)
tot=fail=0; ex=[]
for m in range(2,11):
    for S in combinations(range(1,15),m):
        for r in S:
            if r==max(S): continue
            tot+=1
            if not rule1(S,r):
                fail+=1
                if len(ex)<10: ex.append((S,r,alt_prefix(sorted(set(S)-{max(S),r},reverse=True))))
print(tot,fail,fail/tot); 
for e in ex: print(e)
