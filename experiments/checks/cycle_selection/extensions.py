"""Inductive extensions of the seed in five_hole_certificate.py."""
from itertools import accumulate
from collections import Counter
from five_hole_certificate import P,Q,HOLES

def check(P,Q,H,L):
    a=list(accumulate(P,initial=0)); b=list(accumulate(Q,initial=0))
    assert len(a)==len(set(a)) and len(b)==len(set(b))
    assert a[-1]==b[-1] and max(a+b)-min(a+b)==L
    assert a[-1] in (min(a+b),max(a+b)) and P[:2]==(1,2)
    assert -L in H and L not in H
    assert Counter(P+tuple(-z for z in Q))==Counter(set(range(-L,L+1))-{0}-H)
    assert L>len(P) and L>len(Q)

def extensions(P,Q,H,L):
    check(P,Q,H,L)
    x=list(accumulate(P,initial=0)); y=list(accumulate(Q,initial=0))
    T=x[-1]
    sign=-1 if T==max(x+y) else 1
    used=set(x if sign==-1 else y)
    for j in range(1,L):
        if T+sign*j in used:continue
        if j<=(L+1)//2: q,first=L+1-j,L
        else: q,first=j-1,None
        a=2*q
        first=a if first is None else first
        common=tuple(sign*(-1)**i*d for i,d in
                     enumerate(d for d in range(L+1,L+a) if d!=a))
        two=(sign*first,sign*(L+a-first))
        one=(sign*(L+a),)
        u=P+common+(two if sign==-1 else one)
        v=Q+common+(one if sign==-1 else two)
        newH=(H-{-L})|{a,-(L+a)}
        check(u,v,newH,L+a)
        yield u,v,newH,L+a

def check_modular(P,Q,H,L):
    from five_hole_certificate import check_cycle
    for extra in (0,1,4):
        N=2*(L+extra)+1
        if extra:
            T=sum(P); lo=min(accumulate(P,initial=0))
            sign=1 if T==lo else -1
            common=tuple(sign*(-1)**i*(L+1+i) for i in range(extra-1))
            R=L+extra
            w=P+common+(R,)+tuple(-v for v in reversed(Q+common))+(-R,)
        else:
            u,v=P,Q
            if abs(P[-1])==L: u=P[-1:]+P[:-1]
            else: v=Q[-1:]+Q[:-1]
            w=u+tuple(-z for z in reversed(v))
        i=w.index(1);w=w[i:]+w[:i]
        assert w[:2]==(1,2)
        A=set(range(-N//2+1,N//2+1))-{0}-H
        check_cycle(w,A,N)
        assert 1 not in check_cycle((3,)+w[2:],(A-{1,2})|{3},N)

if __name__=='__main__':
    seed=(P,Q,HOLES,31)
    frontier=[seed]
    for depth in range(1,5):
        frontier=[new for state in frontier for new in extensions(*state)]
        for state in frontier: check_modular(*state)
        assert frontier
        print(depth,len(frontier),min(s[3] for s in frontier),max(s[3] for s in frontier))
