from itertools import combinations, permutations
from random import Random

def vertices(xs,start):
    out=[start]
    for x in xs: out.append(out[-1]-x)
    return out

def score(xs,x0,ys,y0,ignore=frozenset()):
    v=vertices(xs,x0);w=vertices(ys,y0)
    common=(set(v)&set(w))-ignore
    return len(common),-sum(v.index(z)+w.index(z) for z in common)

def separate(xs,x0,ys,y0,ignore=frozenset()):
    xs=list(xs);ys=list(ys)
    while True:
        old=score(xs,x0,ys,y0,ignore)
        if old[0]==0:return xs,ys
        changed=False
        for side in (xs,ys):
            for i in range(len(side)-1):
                side[i],side[i+1]=side[i+1],side[i]
                if score(xs,x0,ys,y0,ignore)<old:
                    changed=True;break
                side[i],side[i+1]=side[i+1],side[i]
            if changed:break
        if not changed:raise AssertionError(('separation failed',xs,x0,ys,y0,ignore,old))

def strict_cross(vals,h):
    assert max(vals)<h and sum(vals)>2*h
    vals=sorted(vals,reverse=True);s=0
    for i,x in enumerate(vals):
        s+=x
        if s>h:
            out=vals[:i+1];assert h<sum(out)<h+min(out)
            return out
        if s==h:
            out=vals[:i]+strict_cross(vals[i+1:],x)
            assert h<sum(out)<h+min(out)
            return out
    raise AssertionError('unreachable')

def solve_two(a,b,qs):
    assert 0<a<b and len(qs)==len(set(qs)) and min(qs)>0 and sum(qs)==a+b
    Q=max(qs)
    if a<=Q:
        X,Y=separate([a,b],a+b,qs,a+b,{0,a+b})
        return tuple(X[::-1]+[-x for x in Y]),'mass'
    X=strict_cross(qs,a);Y=sorted(set(qs)-set(X));e=sum(X)-a
    if sum(X)!=b:
        X,Y=separate(X,a,Y,b-e)
        return tuple([a]+[-x for x in X]+[b]+[-y for y in Y]),'strict'
    q=min(qs)
    Z,W=(X,Y) if q in X else (Y,X)
    u,v=sum(Z),sum(W)
    Z=list(set(Z)-{q})
    Z,W=separate(Z,u,W,v)
    return tuple([u]+[-z for z in Z]+[v,-q]+[-w for w in W]),'bridge'

def verify(w,A,D):
    assert sorted(w)==sorted(A) and sum(w)==0
    V=[0]
    for a in w[:-1]:V.append(V[-1]+a)
    assert len(set(V))==len(V) and max(V)-min(V)<=D,(w,V,D)
    return V

def exhaustive(M):
    count={'mass':0,'strict':0,'bridge':0}
    for k in range(2,M+1):
        for qs in combinations(range(1,M+1),k):
            T=sum(qs)
            for a in range(1,(T+1)//2):
                b=T-a
                w,case=solve_two(a,b,qs)
                verify(w,[a,b]+[-x for x in qs],b+max(qs));count[case]+=1
    return count

def check_examples():
    B=(-1,2,3,1,-3,-2)
    V=verify(B, B, 6)
    assert 4 in V and max(max(V),-5)-min(min(V),-5)==10
    A=(-5,4,-3,-2,3,1,2);verify(A,A,9)
    w=(-4,-3,-2,1,2,4,-1,3);V=verify(w,w,9)
    opts=[]
    for i,x in enumerate(V):
        y=x+w[i]-w[i-1]; W=V.copy();W[i]=y
        opts.append(None if len(set(W))<len(W) else max(W)-min(W))
    assert opts==[None]*7+[10]
    return V,opts

if __name__=='__main__':
    print('exhaustive M=11:',exhaustive(11))
    rng=Random(475);counts={'mass':0,'strict':0,'bridge':0}
    for _ in range(1000):
        M=rng.randint(12,100);qs=rng.sample(range(1,M+1),rng.randint(2,min(15,M)))
        T=sum(qs);a=rng.randint(1,(T-1)//2);b=T-a
        w,case=solve_two(a,b,qs);verify(w,[a,b]+[-x for x in qs],b+max(qs));counts[case]+=1
    print('random:',counts)
    print('obstructions:',check_examples())

