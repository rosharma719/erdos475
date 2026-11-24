from itertools import combinations
from collections import Counter
exec(open('rs3.py').read().split("V=int")[0])
c=Counter(); miss=[]
for m in range(2,12):
    for S in combinations(range(1,15),m):
        r=min(S)
        t=cover(S,r); c[t]+=1
        if t is None: miss.append(S)
print(dict(c)); print(len(miss), miss[:30])
