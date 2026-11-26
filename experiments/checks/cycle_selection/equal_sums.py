"""Verify the repeated-pair-sum theorem. Python 3.10+, no dependencies."""
from itertools import accumulate, combinations, pairwise
from random import Random
from collections import Counter

def check(N,A,w,mark):
    assert sorted(x%N for x in w)==sorted({x%N for x in A})
    def vertices(s):
        v=[x%N for x in accumulate(s,initial=0)]
        assert v[-1]==0 and len(set(v[:-1]))==len(s)
        return v[:-1]
    vertices(w)
    if mark:
        a,b=mark; j=w.index(a); w=w[j:]+w[:j]; assert w[1]==b
        assert (a+b)%N not in {x%N for x in A}|{0}
        assert a%N not in vertices([a+b]+w[2:])

def boundary(N,A):
    if N==13:
        w=[-5,-3,-2]+([-1,4,1] if 1 in A else [4])+[6]
        return w,(-5,-3)
    M=N//2; center=lambda x:(x+M)%N-M
    B={center(2*x) for x in A}
    X,Y=[
        ([7],[4,-3,1,5]),
        ([7],[4,2,-3,-2,1,5]),
        ([-6,7],[-6,4,-3,1,5]),
        ([2,-6,7],[-3,4,1,-6,2,5])
    ][int(2 in B)+2*int(6 in B)]
    Q=[-x for x in reversed(Y)]
    assert set(X+Q)=={x for x in B if abs(x)<=7}
    u=list(accumulate(X,initial=0));v=list(accumulate(Y,initial=0))
    assert u[-1]==v[-1]==max(u)==max(v)
    assert all(len(set(s))==len(s) and max(s)-min(s)<=7 for s in (u,v))
    mark=next((a,b) for w in (X[:-1],Q) for a,b in pairwise(w)
              if 0<abs(a+b)<=7 and a+b not in B)
    ds=sorted(x for x in B if x>7)
    if ds:
        for j,x in enumerate(ds[:-1]):
            z=x if j%2 else -x
            X.append(z);Y.append(z)
        w=X+[ds[-1]]+[-a for a in Y[::-1]]+[-ds[-1]]
    else:w=[7]+X[:-1]+Q
    back=lambda a:center(pow(2,-1,N)*a)
    return list(map(back,w)),tuple(map(back,mark))

def build(N,groups,D,marked_five=True):
    M=N//2;U={-2}
    for j,e in groups.items():U.update((-e*j,e*(j+1)))
    assert len({abs(x) for x in U})==len(U)==1+2*len(groups)
    assert sum(U)==0 and max(map(abs,U))<=M
    assert not {abs(x) for x in U}&D
    A=U|{s*d for d in D for s in (-1,1)}
    k=next((j for j in sorted(groups,reverse=True) if groups[j]==1 and j+2<=M and j+2 not in groups),None)
    touch=k is None
    if touch and len(groups)==2 and marked_five:
        w,m=boundary(N,A);check(N,A,w,m);return 'boundary'
    if touch:k=next(j for j in groups if groups[j]==groups.get(j+2)==1)
    occ=not touch and k+2 in D
    core=set(D)
    if occ:core.remove(k+2);core.add(k)
    others={j:e for j,e in groups.items() if j!=k and (not touch or j!=k+2)}
    s=(1 if occ else -1)*(-1)**sum(d<k for d in core)
    X=[];Y=[]
    for d in sorted(core|set(others)|{k if touch else k+1}):
        if d in core:X.append(s*d);Y.append(s*d);s=-s
        elif d in others:
            (X if s==-others[d] else Y).extend([s*d,-s*(d+1)])
        elif touch:
            assert s==-1
            X.extend([-k,-2,k+3]);Y.extend([-(k+1),k+2])
        else:
            assert s==-1
            if occ:Y.extend([-(k+1),k+2])
            else:X.append(-(k+2));Y.append(-(k+1));s=1
    mark=None
    if not touch:
        mark=(-2,k+2) if occ else (-k,-2)
        j=X.index(sum(mark));X[j:j+1]=mark
    assert sum(X)==sum(Y)
    w=X+[-z for z in reversed(Y[-1:]+Y[:-1])]
    check(N,A,w,mark)
    return 'touching' if touch else ('occupied' if occ else 'vacant')

def run():
    count=Counter(); more=Counter()
    for M in range(6,18):
        for t in range(2,((M-2)//2 if M<=13 else 2)+1,2):
            for ks in combinations(range(3,M),t):
                if any(y==x+1 for x,y in pairwise(ks)):continue
                free=sorted(set(range(1,M+1))-{2}-set(ks)-{k+1 for k in ks})
                for neg in combinations(ks,(t-2)//2):
                    groups={k:(-1 if k in neg else 1) for k in ks}
                    for mask in range(1<<len(free)):
                        D={x for j,x in enumerate(free) if mask>>j&1}
                        case=build(2*M+1,groups,D)
                        if t==2:count[case]+=1
                        else:more[case]+=1
    print('all five-label inputs through modulus 35:',count)
    print('all higher-asymmetry inputs through modulus 27:',more)
    rng=Random(475)
    for M in (25,80,260):
        for _ in range(100):
            t=2*rng.randint(1,(M-2)//4)
            ks=[a+j for j,a in enumerate(sorted(rng.sample(range(3,M-t+1),t)))]
            neg=set(rng.sample(ks,(t-2)//2))
            g={k:(-1 if k in neg else 1) for k in ks}
            f=set(range(1,M+1))-{2}-set(ks)-{k+1 for k in ks}
            for D in (set(),f,{x for x in sorted(f) if rng.getrandbits(1)}):
                build(2*M+1,g,D,False)
    for p,U in [(211,(31,87,133,179,203)),(503,(112,168,388,406,435))]:
        assert len({(a+b)%p for a,b in combinations(U,2)})==10
    print('900 additional variable-size cycles and both obstruction checks passed')
if __name__=='__main__':run()
