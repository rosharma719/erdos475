from itertools import combinations, product, accumulate, pairwise
from pathlib import Path
from collections import Counter
import json

def cases():
    for L in range(5,13):
        for mags in combinations(range(1,L),4):
            for signs in product((-1,1),repeat=4):
                U={L,*[a*b for a,b in zip(mags,signs)]}
                if sum(U) or any(a+b in U for a,b in combinations(U,2)):
                    continue
                other=sorted(set(range(1,L))-set(mags))
                for m in range(1<<len(other)):
                    A=set(U)
                    for j,d in enumerate(other):
                        if (m>>j)&1:A.update((d,-d))
                    yield L,A

def possible(L,A):
    labels=sorted(A)
    full=(1<<len(labels))-1
    def masks(sign):
        reached=set()
        def visit(v,used,seen):
            reached.add(used)
            for i,a in enumerate(labels):
                w=v+sign*a
                if (used>>i)&1 or not 0<=w<=L or (seen>>w)&1:continue
                visit(w,used|(1<<i),seen|(1<<w))
        visit(L,0,1<<L)
        return reached
    p,q=masks(-1),masks(1)
    return any((full^s) in q for s in p)

def check_witness(L,A,P,Q):
    assert sorted(P+[-v for v in Q])==sorted(A)
    start=L-sum(P)
    for path in (P,Q):
        v=list(accumulate(path,initial=start))
        assert v[-1]==L and min(v)>=0 and max(v)==L and len(v)==len(set(v))
    assert P[-1]==L
    reverseQ=[-v for v in reversed(Q)]
    pairs=[(a,b) for path in (P[:-1],reverseQ) for a,b in pairwise(path)
           if 0<abs(a+b)<=L and a+b not in A]
    assert pairs
    word=[L,*P[:-1],*reverseQ]
    N=2*L+1
    a,b=pairs[0]; j=word.index(a)
    word=word[j:]+word[:j]
    assert word[1]==b
    for w in (word,[a+b,*word[2:]]):
        v=[s%N for s in accumulate(w,initial=0)]
        assert v[-1]==0 and len(set(v[:-1]))==len(w)
    assert a%N not in v[:-1]

def verify():
    f=Path(__file__).with_name('width12_data.json')
    first,second=json.loads(f.read_text())
    D={i:(P,Q) for i,P,Q in first}
    E={i:(P,Q) for i,P,Q in second}
    assert len(D)==len(first)==5786 and len(E)==len(second)==90720
    bad=dense=0
    for i,(L,A) in enumerate(cases()):
        if i in D:
            check_witness(L,A,*D.pop(i))
            dense+=len(A)>=11
            continue
        assert len(A)<=9 and not possible(L,A)
        bad+=1
        for mask in range(1<<L):
            # At least two of odd magnitudes 3,5,9, or both 7 and 11.
            if (mask&22).bit_count()>1 and (mask&40)!=0:continue
            B={2*a for a in A}
            for j in range(L):
                if not (mask>>j)&1:B.update((2*j+1,-2*j-1))
            check_witness(2*L,B,*E.pop((i<<12)+mask))
    assert not D and not E and (bad,dense)==(46,4307)
    print('5786 direct witnesses, 46 exact obstructions,')
    print('90720 doubled witnesses; all contractions verified.')

if __name__=='__main__':verify()
