import random
from itertools import accumulate
def vs(w,start=0):
    out=[start]
    for x in w: out.append(out[-1]+x)
    return out
# Thm 1: reverse-rank contraction
rng=random.Random(1); n=0
while n<20000:
    k=rng.randint(2,8); X=sorted(rng.sample(range(1,60),k)); Y=sorted(rng.sample(range(1,60),k))
    if sum(X)!=sum(Y) or set(X)&set(Y): continue
    d=[X[i]-Y[k-1-i] for i in range(k)]
    assert len(set(d))==k and 0 not in d and sum(d)==0
    assert max(d)-min(d)==(X[-1]+Y[-1])-X[0]-Y[0]; n+=1
print("Thm1 ok on",n)
# obstruction example
B=(18,-12,6,-4,2,-10); V=vs(B,-9); print("B vertices",V)
x={d:(100+d)//2 for d in B}; y={d:(100-d)//2 for d in B}
cands=[{V[i]+x[B[i]],V[i]-y[B[i]]} for i in range(6)]; print("expansion pairs",cands)
X=sorted(x.values()); Y=sorted(y.values()); print(X,Y,sum(X),sum(Y),"D=",max(X)+max(Y))
w=(53,-47,51,-49,44,-56,59,-41,48,-52,-55,45)
assert sorted(a for a in w if a>0)==X and sorted(-a for a in w if a<0)==Y
s=list(accumulate(w)); print(s, len(set(s))==len(s), s[-1]==0, max(s+[0])-min(s+[0]))
