"""Constructive protected two-path theorem. Standalone; no third-party dependencies.
Run with no arguments to enumerate all eligible instances through max positive step 12.
Uses exact integer arithmetic; theorem also holds for real step sizes.
"""
from itertools import accumulate, combinations, permutations
from collections import defaultdict
import random, sys

def avoid(C,F):
    C=tuple(C); F={f for f in F if 0<f<sum(C)}
    assert len(F)<len(C)
    if not F:return C
    c=max(C); R=tuple(x for x in C if x!=c)
    if c in F:
        r=avoid(R,{f for f in F if f<c}|{f-c for f in F if f>c})
        return (r[0],c)+r[1:]
    if min(F)<c:return (c,)+avoid(R,{f-c for f in F if f>c})
    f=min(F); w=list((c,)+avoid(R,{g-c for g in F if g!=f})); s=list(accumulate(w))
    if f in s:
        i=s.index(f)+1;w[0],w[i]=w[i],w[0]
    return tuple(w)

def protected(C,E,h):
    C,E=tuple(C),tuple(E);u,v=sum(C),sum(E);Q=u-h;P=v-h;d=v-u
    assert 0<h and P>Q and max(C)<P and max(E)<Q
    if len(C)==1:
        q=avoid(E,{h,u}) if len(E)>=3 else next(w for w in permutations(E) if not {h,u}&set(accumulate(w)))
        return C,q
    A=set(C);B=set(E);p=[];q=[];x=y=0
    def addX(a):
        nonlocal x
        A.remove(a);p.append(a);x+=a
    def addY(b):
        nonlocal y
        B.remove(b);q.append(b);y+=b
    if d==h and d in B:
        if Q in A:
            b=next(b for b in B if b!=h and b+h!=Q)
            addY(b);addX(Q);addY(h)
        else:
            for b in sorted(B-{h}):
                F={h,b,b+h}
                if len(A)>=4:w=avoid(A,F)
                else:w=next((w for w in permutations(A) if not F&set(accumulate(w))),None)
                if w is not None:break
            else:raise AssertionError((C,E,h))
            addY(b)
            for a in w:
                addX(a)
                if x>b:break
            addY(h)
    else:
        if d in B:addY(d)
        if Q in A:
            if h!=Q:addX(Q)
            else:addX(next(a for a in A if a!=Q and a!=y))
    while A or B:
        if not A and x<y:
            for b in sorted(B):addY(b)
            break
        if A and (x<=y or not B):
            a=Q if Q in A and x>0 else next((a for a in sorted(A) if x+a not in {h,y}),None)
            assert a is not None and x+a not in {h,y},(C,E,h,p,q,A,B)
            addX(a)
        else:
            b=next((b for b in sorted(B) if y+b not in {h,u,x}),None)
            assert b is not None,(C,E,h,p,q,A,B)
            addY(b)
    assert sorted(p)==sorted(C) and sorted(q)==sorted(E)
    s=set(accumulate(p));t=set(accumulate(q));assert not s&t and h not in s|t,(C,E,h,p,q)
    return tuple(p),tuple(q)

def equal_extremes(X,Y):
    X,Y=tuple(X),tuple(Y);M=max(X);assert max(Y)==M and sum(X)==sum(Y)>2*M
    b=max(set(Y)-{M});h=sum(X)-M-b;d=M-b
    assert h!=M and d not in set(Y)-{M,b}
    A=set(X)-{M};B=set(Y)-{M,b};u=sum(A);p=[];q=[M];x=0;y=M
    def addX(a):
        nonlocal x
        A.remove(a);p.append(a);x+=a
    if b in A:
        if h==b:addX(next(a for a in A if a!=b and a!=d))
        addX(b)
    while A or B:
        if not A and x<y:
            q.extend(sorted(B));break
        if A and (x<=y or not B):
            a=next(a for a in sorted(A) if x+a not in {h,y});addX(a)
        else:
            a=next(a for a in sorted(B) if y+a not in {h,u,x});B.remove(a);q.append(a);y+=a
    w=tuple(p)+(-b,M)+tuple(-a for a in q[::-1]);s=list(accumulate(w))
    assert sorted(w)==sorted(X+tuple(-a for a in Y)) and len(s)==len(set(s)) and s[-1]==0 and max(s)-min(s)==sum(X)-b
    return w

def audit(M=12):
    D={}
    for P in range(2,M+1):
        d=defaultdict(list)
        for n in range(1,P):
            for a in combinations(range(1,P),n):d[sum(a)].append(a)
        D[P]=d
    count=0;special=0
    for P in range(3,M+1):
        n=0
        for Q in range(2,P):
            for h in range(1,Q+1):
                for C in D[P][Q+h]:
                    for E in D[Q][P+h]:
                        a,b=protected(C,E,h);w=a+(-Q,P)+tuple(-x for x in b[::-1]);s=list(accumulate(w))
                        assert len(s)==len(set(s)) and s[-1]==0 and max(s)-min(s)<=P+Q
                        n+=1;special+=int(P-Q==h and h in E)
        count+=n;print(P,n,flush=True)
    print('TOTAL',count,'special d=h cases',special,flush=True)

def random_audit(trials=50000):
    r=random.Random(475);count=0;special=0
    for _ in range(trials):
        C=r.sample(range(1,61),r.randrange(1,13));E=r.sample(range(1,61),r.randrange(2,13));u,v=sum(C),sum(E)
        if u>=v:continue
        h=r.randrange(1,u//2+1) if u>=2 else 0
        if not h or max(C)>=v-h or max(E)>=u-h:continue
        protected(C,E,h);count+=1;special+=int(v-u==h and h in E)
    print('RANDOM',count,'special',special,flush=True)

def extended_audit():
    r=random.Random(475);count=0
    for _ in range(50000):
        C=r.sample(range(1,80),r.randrange(2,16));E=r.sample(range(1,80),r.randrange(2,16));u,v=sum(C),sum(E)
        if u>=v:continue
        h=r.randrange(u//2+1,u)
        if max(C)>=v-h or max(E)>=u-h:continue
        protected(C,E,h);count+=1
    print('h>Q:',count)
    count=0
    for M in range(3,12):
        D=defaultdict(list)
        for k in range(1,M):
            for a in combinations(range(1,M),k):D[sum(a)].append(a+(M,))
        for t,L in D.items():
            if t<=M:continue
            for x in L:
                for y in L:
                    b=y[-2];h=t-b;d=M-b
                    if h==M or d in y[:-2]:continue
                    equal_extremes(x,y);count+=1
    print('Equal extreme cases:',count)
    from collections import Counter
    w=(-3,-2,-1,2,3,1);c=Counter()
    for i,j in combinations(range(len(w)),2):
        for a in (4,-4):
            t=w[:i]+(a,)+w[i:j]+(-a,)+w[j:];s=list(accumulate(t));z=max(s)-min(s)
            c['collision' if len(set(s))<len(t) else z]+=1
    assert c=={'collision':21,10:8,9:1}
    print('Insertion obstruction:',c)

if __name__=='__main__':
    audit();random_audit();extended_audit()
