import random
from collections import Counter
def I(A,p):
    c=lambda x:(x+p//2)%p-p//2
    return min(abs(sum(c(l*a) for a in A))//p for l in range(1,p))
rng=random.Random(3)
for p in (29,41,59,83,101):
    cnt=Counter()
    for _ in range(400):
        n=(p-1)//2
        while True:
            A=rng.sample(range(1,p),n-1); b=-sum(A)%p
            if b and b not in A: A.append(b); break
        cnt[I(A,p)]+=1
    # quadratic residues if zero-sum
    Q=sorted({x*x%p for x in range(1,p)}); iq=I(Q,p) if sum(Q)%p==0 else None
    print(p,"random half-density I distribution",dict(sorted(cnt.items())),"I(QR)=",iq)
