import sys,random
sys.path.insert(0,'.')
from sp import kernel
from collections import Counter
rng=random.Random(1)
for p in (23,31,37):
    for n in (6,8,10,12,14,16):
        if n>p-2: continue
        c=Counter()
        for _ in range(40):
            while True:
                A=rng.sample(range(1,p),n-1); b=-sum(A)%p
                if b and b not in A: A.append(b); break
            c[len(kernel(A,p))]+=1
        print(p,n,"dim K distribution:",dict(sorted(c.items())))
