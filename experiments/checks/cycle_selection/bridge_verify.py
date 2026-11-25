"""Run alongside width12_verify.py and the two embedded JSON datasets."""
import json
from collections import Counter
from pathlib import Path
from itertools import accumulate,pairwise,combinations
from width12_verify import cases,check_witness

def validate():
    here=Path(__file__).parent
    data=json.loads((here/'bridge_data.json').read_text())
    raw=json.loads((here/'width12_data.json').read_text())
    direct={i for i,_,_ in raw[0]}
    lows={i:(L,A) for i,(L,A) in enumerate(cases()) if i not in direct}
    def paths(L,A,r,P,Q):
        assert sorted(P+[-v for v in Q]+list(r))==sorted(A)
        for w in (P,Q):
            vert=list(accumulate(w,initial=0))
            assert max(vert)==vert[-1] and max(vert)-min(vert)<=L and len(vert)==len(set(vert))
        assert any(0<abs(a+b)<=L and a+b not in A for w in (P,[-v for v in Q[::-1]]) for a,b in pairwise(w))
    small={}
    for i,V,w in data['small']:
        L,A=lows[i]; D=max([L]+V); B=A|{s*x for x in V for s in (-1,1)}
        sums=list(accumulate(w,initial=0))
        assert sorted(w)==sorted(B) and sums[-1]==0 and len(set(sums[:-1]))==len(w)
        assert max(sums)-min(sums)<=2*D
        assert any(0<abs(a+b)<=D and a+b not in B for a,b in zip(w,w[1:]+w[:1]))
        small[i,tuple(V)]=True
    seeds=set()
    for i,L,A,s,u,v,P,Q in data['seeds']:
        assert lows[i]==(L,set(A)) and s in (-1,1)
        paths(L,set(A),[u,v],P,Q)
        if s<0:u,v=-v,-u
        c=u+v
        assert u>0>v and c in (1,2)
        for k in range(c+1):
            for V in combinations(range(L+1,2*L+c),k):
                if V and (V[0]>2*L or V[-1]-V[0]>=c):continue
                assert small.pop((i,V))
        seeds.add(i)
    assert seeds==lows.keys() and not small
    for key,options in data['options'].items():
        L,A=lows[int(key)]
        for r,P,Q in options:paths(L,A,r,P,Q)
    coverage={}
    def add(i,m,t):
        assert (i,m) not in coverage
        coverage[i,m]=t
    for i,m,k,s,q,*word in data['cap']:
        L,A=lows[i]; r=data['options'][str(i)][k][0]
        assert s in (-1,1)
        H={d*(128-j) for j in range(L) if not(m>>j)&1 for d in (-1,1)}
        assert q in H and sorted(word+[-q])==sorted(list(H)+[s*x for x in r])
        h=s*sum(r)+(q-128 if q>0 else q+129)
        assert 1-L<=h<=L
        e=b=0; visited=set()
        for idx,x in enumerate(word):
            if x in H:
                d=1 if x>0 else -1
                e+=d; b+=x-d*128
            else:b+=x
            b-=e//2; e%=2
            if idx+1==len(word):assert (e,b)==(1,h)
            else:
                assert ((e==0 and 1<=b<L+h) or (e==1 and h<b<=L)) and (e,b) not in visited
                visited.add((e,b))
        add(i,m,'bridge')
    for i,m,k,*w in data['double']:
        L,A=lows[i]
        B={2*a for a in A}|{s*(2*j+1) for j in range(L) if not(m>>j)&1 for s in (-1,1)}
        check_witness(2*L,B,w[:k],w[k:]);add(i,m,'new double')
    missing=[];summary=Counter()
    for i,(L,A) in lows.items():
        for m in range(1<<L):
            if (m&22).bit_count()<=1 or m&40==0:t='old double'
            elif m&63==63:t='terminal'
            else:t=coverage.pop((i,m),'open')
            summary[t]+=1
            if t=='open':missing.append((i,m))
    assert not coverage
    print(summary,'missing',len(missing),'profiles',sorted({i for i,m in missing}))
    return missing
if __name__=='__main__':assert not validate()

def check_small_moduli():
    base=Path(__file__).parent
    low={i:(L,set(A)) for i,L,A,*_ in json.loads((base/'bridge_data.json').read_text())['seeds']}
    expected={(i,M,m) for i,(L,A) in low.items() for M in range(L,2*L) for m in range(1<<(M-L))}
    n=len(expected)
    for line in (base/'bridge_small_moduli.txt').open():
        i,M,m,*w=map(int,line.split())
        expected.remove((i,M,m))
        L,A=low[i]; N=2*M+1
        B={x%N for x in A}|{(s*j)%N for j in range(L+1,M+1) if m>>(j-L-1)&1 for s in (-1,1)}
        assert sorted(w)==sorted(B)
        t=(w[0]+w[1])%N
        assert t and t not in B
        for path in (w,[t,*w[2:]]):
            v=[x%N for x in accumulate(path,initial=0)]
            assert v[-1]==0 and len(set(v[:-1]))==len(path)
        assert w[0] not in v[:-1]
    assert not expected
    print(n,'small-modulus cycles and contractions verified')
if __name__=='__main__':check_small_moduli()
