# Standalone reverse-rank core and bounded-expansion audit. Python 3.
from random import Random
from collections import Counter

def make_core(X,Y):
    assert len(X)==len(Y) and sum(X)==sum(Y) and not set(X)&set(Y)
    pairs=list(zip(sorted(X),sorted(Y,reverse=True)))
    rem=[[(x,y,x-y) for x,y in pairs if x>y],[(y,x,y-x) for x,y in pairs if x<y]]
    t=sum(p[2] for p in rem[0]);assert t==sum(p[2] for p in rem[1])
    z=[0,0];last=[None,None];out=[[],[]]; doubles=0
    while rem[0] or rem[1]:
        i=0 if z[0]<=z[1] else 1
        if not rem[i]: i=1-i
        j=1-i
        def endpoint(p):return z[i]+p[2]==z[j] and z[j]!=t
        def double(p):return last[j]==(z[i]-p[1],z[i]+p[0])
        good=[p for p in rem[i] if not endpoint(p) and not double(p)]
        if not good:
            good=[p for p in rem[i] if not endpoint(p)]
            assert good and len(rem[i])==2
        p=good[0];doubles+=double(p)
        last[i]=(z[i]-p[1],z[i]+p[0]);out[i].append((z[i],p));z[i]+=p[2];rem[i].remove(p)
    assert z==[t,t] and doubles<=1
    vs=[{z+p[2] for z,p in o} for o in out]
    assert vs[0]&vs[1]=={t}
    ed=[(z-p[1],z+p[0]) for o in out for z,p in o]
    assert len(ed)-len(set(ed))==doubles
    return t,out,doubles

def expand(X,Y,constant=False):
    t,out,nd=make_core(X,Y)
    edges=[(z-p[1],z+p[0]) for o in out for z,p in o];D=max(X)+max(Y)
    H=max(p[1] for o in out for z,p in o);K=min(p[0] for o in out for z,p in o)
    if constant:
        S=edges[0][1]-edges[0][0]
        assert all(b-a==S for a,b in edges) and 2*t<=S
        mid=[a+b for a,b in edges]; c=next((m for m,k in Counter(mid).items() if k==2),t)
        seen=set();selected=[]
        for (a,b),m in zip(edges,mid):
            w=b if m<=c and b not in seen else a
            assert w not in seen;seen.add(w);selected.append(w)
        assert all(c-S<=2*w<=c+S for w in selected+[0,t])
    else:
        assert t<K and t+2*H<=D
        # assign each edge a distinct endpoint via augmenting path
        match={}
        def aug(i,seen):
            for w in edges[i]:
                if w in seen:continue
                seen.add(w)
                if w not in match or aug(match[w],seen):match[w]=i;return True
            return False
        assert all(aug(i,set()) for i in range(len(edges)))
        selected=[None]*len(edges)
        for w,i in match.items():selected[i]=w
    word=[];ind=0
    for z,(M,m,d) in out[0]:
        word.extend((M,-m) if selected[ind]==z+M else (-m,M));ind+=1
    neg=[]
    for z,(M,m,d) in out[1]:
        neg.extend((M,-m) if selected[ind]==z+M else (-m,M));ind+=1
    word+= [-a for a in neg[::-1]]
    assert set(word)==set(X)|{-y for y in Y} and len(word)==len(X)+len(Y)
    s=0;v=[]
    for a in word:s+=a;v.append(s)
    assert s==0 and len(set(v))==len(v) and max(v)-min(v)<=D
    return nd,max(v)-min(v),word

if __name__=='__main__':
    rng=Random(475);counts=Counter();witness=None
    for _ in range(40000):
        k=rng.randint(3,20)
        ds=rng.sample(range(-100,101),k-1);ds.append(-sum(ds))
        if 0 in ds or len(set(ds))!=k or set(ds)&{-d for d in ds}:continue
        t=sum(d for d in ds if d>0);s=2*t+2*rng.randint(0,100)
        X=[s//2+d for d in ds];Y=[s//2-d for d in ds] # actual contracted 2*d; need S>=2*actual t
        X=[a+t for a in X];Y=[a+t for a in Y]
        nd,w,word=expand(X,Y,True);counts['constant']+=1;counts['double']+=nd
        if nd and witness is None:witness=(X,Y,w,word)
    for _ in range(50000):
        k=rng.randint(3,15);X=rng.sample(range(1,101),k);Y=rng.sample(range(1,101),k-1);Y.append(sum(X)-sum(Y))
        if min(Y)<=0 or len(set(Y))!=k or set(X)&set(Y):continue
        t,out,nd=make_core(X,Y);counts['arbitrary core']+=1;counts['arbitrary double']+=nd
        H=max(p[1] for o in out for z,p in o);K=min(p[0] for o in out for z,p in o)
        if t<K and t+2*H<=max(X)+max(Y):
            expand(X,Y);counts['compact']+=1
    print(counts);print('witness',witness)

from random import Random
from collections import defaultdict,Counter

def interval(X,Y):
 t,out,nd=make_core(X,Y);D=max(X)+max(Y)
 edges=[(z-p[1],z+p[0]) for o in out for z,p in o]
 graph=defaultdict(list)
 for i,(a,b) in enumerate(edges):graph[a].append((b,i));graph[b].append((a,i))
 ints=[(t-D,0)];seen=set()
 for a in graph:
  if a in seen:continue
  todo=[a];nodes=set();es=set()
  while todo:
   z=todo.pop()
   if z in nodes:continue
   nodes.add(z);seen.add(z)
   for w,i in graph[z]:es.add(i);todo.append(w)
  ns=sorted(nodes)
  opts=[(ns[-1]-D,ns[0])] if len(es)==len(nodes) else [(ns[-1]-D,ns[1]),(ns[-2]-D,ns[0])]
  ints=[(max(a,c),min(b,d)) for a,b in ints for c,d in opts if max(a,c)<=min(b,d)]
  if not ints:return False,t,out,edges
 return True,t,out,edges

if __name__=="__main__":
    rng=Random(412);ct=Counter();first=None
    for _ in range(100000):
     k=rng.randint(3,25);X=rng.sample(range(1,101),k);Y=rng.sample(range(1,101),k-1);Y.append(sum(X)-sum(Y))
     if min(Y)<=0 or len(set(Y))!=k or set(X)&set(Y):continue
     X=[x+10000 for x in X];Y=[y+10000 for y in Y]
     ok,t,out,edges=interval(X,Y);ct['tested']+=1
     if not ok:
      ct['failed']+=1
      if first is None:first=(X,Y,t,out,edges)
    print(ct);print(first)
