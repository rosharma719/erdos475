"""Construct modular words from the symbolic proofs at two boundary/interior scales."""
from itertools import accumulate
from pathlib import Path
import json
db=json.loads((Path(__file__).parent/'bridge_data.json').read_text())
seeds={i:(L,A,s,u,v,P,Q) for i,L,A,s,u,v,P,Q in db['seeds']}
def extend(P,Q,ds):
    P=list(P);Q=list(Q)
    for j,d in enumerate(ds):
        a=d if j%2 else -d
        P.append(a);Q.append(a)
    if len(ds)%2:return [-x for x in Q],[-x for x in P]
    return P,Q
def test(N,B,P,Q,word,q):
    w=P+word+[-x for x in reversed(Q)]+[-q]
    assert sorted(x%N for x in w)==sorted(x%N for x in B)
    labels={x%N for x in B}
    j=next(j for j in range(len(w)) if (w[j]+w[(j+1)%len(w)])%N not in labels|{0})
    w=w[j:]+w[:j]; f=w[0]%N
    for path in (w,[w[0]+w[1],*w[2:]]):
        v=[x%N for x in accumulate(path,initial=0)]
        assert v[-1]==0 and len(set(v[:-1]))==len(path)
    assert f not in v[:-1]
def both(D):return {s*d for d in D for s in (-1,1)}
count=0
for i,m,k,s,refq,*word in db['cap']:
    L,A,*_=seeds[i];r,P,Q=db['options'][str(i)][k]
    if s<0:P,Q=Q,P
    for M in (2*L,3*L+7):
        H=[M-j for j in range(L) if not(m>>j)&1]
        ds=[d for d in range(L+1,M-L+1) if (d+m+i)%3]
        def transform(v):
            return v if abs(v)<=L else (1 if v>0 else -1)*(abs(v)-128+M)
        X,Y=extend(P,Q,ds)
        test(2*M+1,{s*x for x in A}|both(ds+H),X,Y,list(map(transform,word)),transform(refq))
        count+=1
for i,(L,A,s,u,v,P,Q) in seeds.items():
    if s<0:P,Q=Q,P;u,v=-v,-u
    c=u+v
    for D in (L+5,3*L+3):
        M=D+6
        for q in (L+1,D-c):
            for ds in ([],list(range(L+1,q)),list(range(L+1,q,2))):
                for H in ([[]] if c==1 else [[],[D-1]]):
                    X,Y=extend(P,Q,ds)
                    w=[-D,v,u,*H,D,*[-x for x in reversed(H)],q]
                    test(2*M+1,{s*x for x in A}|both(ds+[q,D]+H),X,Y,w,q)
                    count+=1
print(count,'complete bridge cycles and their contractions checked')

# Recheck the separate repository example and its least centered radius.

from itertools import accumulate
p = 503
U = {112, 168, 388, 406, 435}
A = set(range(1, p)) - {(-u) % p for u in U}
D, E = (388, 3), (500, 168, 406)
d, e = 391, 68
B = (A - set(D) - set(E)) | {d, e}
assert B == {(-b) % p for b in B}
assert len(B) == 494
lam = 51
il = pow(lam, -1, p)
mags = sorted({min(b*lam % p, -b*lam % p) for b in B})
x = [a * (-1)**i for i, a in enumerate(mags)]
w = [b*il % p for b in x + [-a for a in x[-2::-1]] + [-x[-1]]]
assert w[213:215] == [479, 241]
assert len({s % p for s in accumulate(w)}) == len(B)
w[213], w[214] = w[214], w[213]
assert len({s % p for s in accumulate(w)}) == len(B)
out = [a for b in w for a in (D if b == d else E if b == e else (b,))]
assert len(out) == len(A) == len(set(out)) == 497
assert set(out) == A and sum(out) % p == 0
V = {s % p for s in accumulate(out)}
assert len(V) == 497
assert set(range(p)) - V == {84, 110, 157, 166, 300, 309}

assert min(max(abs((t*x+251)%503-251) for x in U) for t in range(1,503))==59
assert [(171*x+251)%503-251 for x in sorted(U)]==[38,57,-48,12,-59]
