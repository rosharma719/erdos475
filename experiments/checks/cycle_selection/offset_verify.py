"""Offset paths. Run alongside offset_seeds.json and width12_verify.py."""
from itertools import accumulate, pairwise, combinations
from pathlib import Path
from collections import Counter
import json
from width12_verify import cases, possible

def build(L,A,P,Q,remaining,padding,bins):
    """Every bin is a list of unpaired labels placed before its padding step."""
    assert len(padding)==len(bins) and list(padding)==sorted(set(padding))
    assert min(padding)>L and Counter(sum(bins,[]))==Counter(remaining)
    assert sorted(P+[-x for x in Q]+list(remaining))==sorted(A)
    u,v=P[:],Q[:]
    direction=1
    left=L
    for d,B in zip(padding,bins):
        pu=[a for a in B if a*direction>0]
        qv=[-a for a in B if a*direction<0]
        assert max(abs(sum(pu)),abs(sum(qv))) < d-left
        u.extend(pu);v.extend(qv)
        if d!=padding[-1]:
            u.append(-direction*d);v.append(-direction*d)
        else:
            separator=direction*d if qv and not pu else -direction*d
        direction=-direction
        left=d
    assert sum(u)==sum(v)
    return u+[separator]+[-a for a in v[::-1]]+[-separator]

def check(word,N,labels):
    assert Counter(a%N for a in word)==Counter(a%N for a in labels)
    V=[s%N for s in accumulate(word,initial=0)]
    assert V[-1]==0 and len(set(V[:-1]))==len(word)
    return set(V[:-1])

def test():
    rows=json.loads(Path(__file__).with_name('offset_seeds.json').read_text())
    rows={row[0]:row[1:] for row in rows}
    assert len(rows)==46
    tests=0
    for i,(L,A) in enumerate(cases()):
        if i not in rows:continue
        l,labels,u,v,P,Q=rows.pop(i)
        assert l==L and set(labels)==A and not possible(L,A)
        assert u>0>v and max(u,-v)<=L
        assert sorted(P+[-a for a in Q]+[u,v])==labels
        for path in (P,Q):
            h=list(accumulate(path,initial=L-sum(path)))
            assert len(h)==len(set(h)) and min(h)>=0 and max(h)==h[-1]==L
        a,b=next((a,b) for w in (P,[-t for t in Q[::-1]]) for a,b in pairwise(w)
                 if 0<abs(a+b)<=L and a+b not in A)
        for mask in range(16):
            inner=[L+1+j for j in range(4) if mask>>j&1]
            lo=inner[-1] if inner else L
            first=lo+1+max(u,-v)
            for suffix in ([],[first+1],[first+2,first+6]):
                S=inner+[first]+suffix
                word=build(L,A,P,Q,[u,v],S,[[] for _ in inner]+[[u,v]]+
                           [[] for _ in suffix])
                for N in (2*S[-1]+1,2*S[-1]+9):
                    lab=A|set(S)|{-t for t in S}
                    j=word.index(a);w=word[j:]+word[:j]
                    assert w[:2]==[a,b]
                    check(w,N,lab)
                    assert a%N not in check([a+b]+w[2:],N,(lab-{a,b})|{a+b})
                    tests+=1
    assert not rows and tests==4416
    print(tests,'cycles and contracted witnesses passed; all 46 seeds passed.')

if __name__=='__main__':test()
