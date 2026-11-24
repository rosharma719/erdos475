#!/usr/bin/env python3
"""Standalone exact checks for the imbalance-carrying and compact-core results.
No external dependencies. Finite tests do not prove the unrestricted conjecture.
"""
from collections import Counter
from itertools import accumulate
from random import Random


def vertices(w):
    return [0]+list(accumulate(w))[:-1]


def span(w):
    v=vertices(w);return max(v)-min(v)


def valid(w, A=None, D=None):
    if A is None:A=w
    if D is None:D=max(A)-min(A)
    return (len(set(A))==len(A) and 0 not in A and sorted(w)==sorted(A)
            and sum(w)==0 and len(set(vertices(w)))==len(w) and span(w)<=D)


def insert_at_edge(w,M,i,sign=1):
    z=w[:i]+[sign*M,w[i],-sign*M]+w[i+1:]
    assert valid(z,w+[M,-M],2*M)
    assert [a for a in z if abs(a)!=M]==w
    return z


def word_from_records(records):
    paths=[]
    for rr in records:
        p=[]
        for x,u,y,a,b,down in rr:
            assert y==x+a-b and u==(x-b if down else x+a)
            p.extend([-b,a] if down else [a,-b])
        paths.append(p)
    return paths[0]+[-a for a in paths[1][::-1]]


def greedy_certificate(records):
    # Verify that the records are an allowed execution of the original flexible-pair algorithm.
    t=records[0][-1][2];assert records[1][-1][2]==t
    hi=[{r[3] for r in rr} for rr in records]
    lo=[{r[4] for r in rr} for rr in records]
    H=max(lo[0]|lo[1]);K=min(hi[0]|hi[1]);assert 0<t<K and H<K
    z=[0,0];last=[None,None];indices=[0,0]
    for _ in range(sum(map(len,records))):
        i=min((i for i in range(2) if hi[i]),key=lambda i:z[i]);j=1-i
        x,u,y,a,b,down=records[i][indices[i]]
        assert x==z[i] and x<=z[j] and a in hi[i] and b in lo[i]
        assert y!=z[j] or y==t
        if len(hi[i])>1: assert not down and x+a!=last[j]
        else:assert y==t and down==(x+a==last[j])
        hi[i].remove(a);lo[i].remove(b);z[i]=y;last[i]=None if down else u;indices[i]+=1
    assert z==[t,t]
    return t,H,K


def all_insertions(w,M):
    out=Counter()
    for i in range(len(w)):
        for j in range(len(w)):
            if i==j:continue
            z=[]
            for k,a in enumerate(w):
                if k==i:z.append(M)
                if k==j:z.append(-M)
                z.append(a)
            if len(set(vertices(z)))<len(z):out['collision']+=1
            else:out[span(z)]+=1
    return out


def obstruction():
    R=[[(0,77,20,77,57,False),(20,-6,61,67,26,True)],
       [(0,68,4,68,64,False),(4,83,18,79,65,False),
        (18,87,30,69,57,False),(30,103,37,73,66,False),
        (37,113,53,76,60,False),(53,120,61,67,59,False)]]
    W=word_from_records(R);M=83
    assert greedy_certificate(R)==(61,66,67) and valid(W) and span(W)==126
    assert sum(a for a in W if a>0)==515
    out=all_insertions(W,M)
    assert out==Counter({'collision':215,209:18,203:2,176:2,202:1,172:1,199:1})
    assert min(k for k in out if isinstance(k,int))>2*M
    for mask in (1,2,3):
        S=[list(rr) for rr in R]
        for i in (0,1):
            if mask&(1<<i):
                x,u,y,a,b,down=S[i][-1]
                S[i][-1]=(x,x+a if down else x-b,y,a,b,not down)
        assert not valid(word_from_records(S),W)
    RR=[[(0,67,41,67,26,False),(41,118,61,77,57,False)],
        [(0,68,11,68,57,False),(11,78,19,67,59,False),
         (19,88,28,69,60,False),(28,101,37,73,64,False),
         (37,113,48,76,65,False),(48,127,61,79,66,False)]]
    assert greedy_certificate(RR)==(61,66,67)
    W2=word_from_records(RR);assert valid(W2,W) and span(W2)==127
    Z=insert_at_edge(W2,M,0);assert span(Z)==150
    return out


def singleton_group(a,b,highs,lows,M):
    # One high-low group consists of a single edge 0 -> a-b.
    t=a-b;assert t==sum(highs)-sum(lows)>0
    H=max([b]+lows);K=min([a]+highs);assert H<K and t<K
    assert M>max([a,b]+highs+lows)
    A=[a]+lows+[-b]+[-q for q in highs]
    if len(highs)==1 and highs[0]==a:
        assert lows==[b]
        w=[b,a,-b,-a]
        z=insert_at_edge(w,M,1 if M==a+b else 0)
        return w,z
    # Reserve a low step different from b for the final edge.
    l=list(lows);h=list(highs)
    final=next(q for q in l if q!=b);l.remove(final);l.append(final)
    x=0;Q=[]
    for q in l:
        Ahi=next(v for v in h if x+v!=a)
        h.remove(Ahi);Q.extend([Ahi,-q]);x+=Ahi-q
    assert x==t
    w=[a,-b]+[-q for q in Q[::-1]]
    assert valid(w,A)
    z=insert_at_edge(w,M,1,-1)
    assert span(z)<=M+H
    return w,z


def block_path(blocks):
    """Monochromatic alternating blocks; largest step jumps over previous span."""
    prev=0;sgn=0;p=[]
    for block in blocks:
        assert block and all((a>0)==(block[0]>0) for a in block)
        sign=1 if block[0]>0 else -1;assert sign!=sgn
        b=sorted(block,key=abs,reverse=True);assert abs(b[0])>prev
        prev=sum(map(abs,b));sgn=sign;p+=b
        V=[0]+list(accumulate(p));assert len(V)==len(set(V)) and max(V)-min(V)==prev
    return p


def block_cycle(P,Q):
    assert len(P[-1])==len(Q[-1])==1 and P[-1][0]*Q[-1][0]>0
    p=block_path(P);q=block_path(Q);assert sum(p)==sum(q)
    A=p+[-x for x in q]
    q=[q[-1]]+q[:-1];w=p+[-x for x in q[::-1]]
    assert valid(w,A,abs(p[-1])+abs(q[0]))
    assert valid(w,A)
    return w


def dense_block_family(m):
    assert m>=2
    p=[2,-3];q=[1,-4]
    for j in range(1,m-1):
        p += [4*j+1,-(4*j+3)];q += [4*j+2,-(4*j+4)]
    p += [4*m-3,-4*m];q += [4*m-2,-(4*m-1)]
    P=[[1,2,5]]+[[4*a] for a in p[1:]];Q=[[4*a] for a in q]
    # block_path sorts the first block descending, so its two new vertices are 5,7.
    w=block_cycle(P,Q);assert len(w)==4*m+2 and max(w)-min(w)==32*m-4
    assert sum(a>0 for a in w)-sum(a<0 for a in w)==2
    a=sorted(w,key=abs);assert len(set(map(abs,a)))==len(a)
    assert all(s!=0 for s in list(accumulate(a))[:-1])
    cnt=[0]+list(accumulate(1 if x>0 else -1 for x in a));assert max(cnt)-min(cnt)>=3
    assert w[-2:]==[-4,4*(4*m-1)]
    b=w[:-2]+[4*(4*m-2)];assert valid(b)
    M=16*m+1;i=w.index(-16*m)
    z=insert_at_edge(w,M,i,-1);assert span(z)==32*m+1
    return w,b,z


def dense_lift(core):
    """Constant-modulus triple expansion, preserving a marked contraction and all larger inverse-pair insertions."""
    assert len(core)>=2 and valid(core) and all(a%3==0 for a in core)
    V=vertices(core);i=V.index(min(V));core=core[i:]+core[:i];V=vertices(core)
    W=span(core);k=len(core);assert min(V)==0 and core[-1]<0
    L=3*((max(2*W,12*k+6)+2)//3)
    xs=set();zs=set();u=set();v=set();out=[]
    for i,d in enumerate(core[:-1],1):
        y=2*L+3*i+1;s=V[i-1]
        for x in range(L+1,L+12*k+2,3):
            z=x+y-d
            if x in xs or z in zs or s+x in u or s+x+y in v:continue
            break
        else:raise AssertionError('greedy pool exhausted')
        xs.add(x);zs.add(z);u.add(s+x);v.add(s+x+y);out.extend([x,y,-z])
    x=3*L+1;y=6*L+1;z=x+y-core[-1]
    out.extend([x,y,-z]);assert valid(out) and len(out)==3*k
    assert min(vertices(out))==0 and max(vertices(out))==z==max(map(abs,out))
    small=out[:-2]+[y-z];assert valid(small)
    assert y-z not in out and y==max(out) and -z==min(out)
    for M in (z+1,z+2,2*z):
        expanded=insert_at_edge(out,M,0);assert valid(expanded,out+[M,-M],2*M)
    return out,small,z,L


def symmetric_core(r):
    p=[3*((-1)**(r-i))*i for i in range(1,r+1)]
    w=p+[-a for a in p[-2::-1]]+[-p[-1]];assert valid(w)
    return w


def main():
    print('Fixed-core obstruction:',obstruction())
    rng=Random(4752026);counts=Counter()
    for _ in range(3000):
        n=rng.randrange(1,20);lo=rng.sample(range(1,50),n);hi=rng.sample(range(51,120),n)
        t=sum(hi)-sum(lo);b=rng.randrange(1,50);a=b+t
        if a<=max([b]+lo):continue
        shift=max(0,t-min([a]+hi)+1)+rng.randrange(0,10)
        a+=shift;b+=shift;lo=[x+shift for x in lo];hi=[x+shift for x in hi]
        for M in (max([a]+hi)+1,max([a]+hi)+rng.randrange(2,40)):
            singleton_group(a,b,hi,lo,M);counts['singleton-group insertions']+=1
    for a in range(2,25):
        for b in range(1,a):
            for M in (a+1,a+b,a+b+1):
                singleton_group(a,b,[a],[b],M);counts['symmetric two-pair insertions']+=1
    for m in range(2,301):
        dense_block_family(m);counts['dense grouped families, both compatibility operations']+=1
    for r in range(1,301):
        A,B,z,L=dense_lift(symmetric_core(r));counts['dense triple lifts, both compatibility operations']+=1
        if r in (1,10,100,300):print('triple lift r,n,D,span:',r,len(A),max(A)-min(A),span(A))
    # Additional nonmonotone asymmetric cores from the grouped family, scaled by 3.
    for m in range(2,61):
        w,_,_=dense_block_family(m);dense_lift([3*a for a in w]);counts['asymmetric nonmonotone triple lifts']+=1
    print(dict(counts))
    print('All checks passed.')

if __name__=='__main__':main()
