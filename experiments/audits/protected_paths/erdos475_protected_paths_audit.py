"""Single-file audit of protected monotone paths (Erdos #475).
Run: python erdos475_protected_paths_audit.py
Use --random for the seeded broader 50,000-trial experiment.
'REMAINING' denotes instances outside the proved sufficient tests, not failures.
The theorem proofs are in the accompanying chat response.
"""
from itertools import combinations, permutations, accumulate
from collections import defaultdict, Counter

def avoid(A,F):
    A=tuple(A); T=sum(A); F={f for f in F if 0<f<T}
    assert len(F)<len(A), (A,F)
    if not F:return A
    if len(A)==2:return next(p for p in permutations(A) if not set(accumulate(p))&F)
    c=max(A); R=tuple(x for x in A if x!=c)
    if c in F:
        G={f for f in F if f<c}|{f-c for f in F if f>c}
        r=avoid(R,G); w=(r[0],c)+r[1:]
    elif min(F)<c:
        w=(c,)+avoid(R,{f-c for f in F if f>c})
    else:
        f=min(F); w=list((c,)+avoid(R,{g-c for g in F if g!=f})); s=list(accumulate(w))
        if f in s:
            i=s.index(f)+1; w[0],w[i]=w[i],w[0]
        w=tuple(w)
    assert not set(accumulate(w))&F and sorted(w)==sorted(A),(A,F,w)
    return w

def separate(a,b):
    a,b=sorted(a),sorted(b)
    while True:
        p=list(accumulate(a));q=list(accumulate(b));I=set(p)&set(q)
        if not I:return tuple(a),tuple(b)
        old=(len(I),sum(I));ok=False
        for t in sorted(I):
            for w,other,vals in ((a,q,p),(b,p,q)):
                i=vals.index(t)
                if i+1==len(w):continue
                J=(I-{t})|({t+w[i+1]-w[i]}&set(other))
                if (len(J),sum(J))<old:
                    w[i],w[i+1]=w[i+1],w[i];ok=True;break
            if ok:break
        assert ok,(a,b,I)

def solve(a,b,h,P,Q):
    m,n=len(a),len(b);u,v=sum(a),sum(b)
    if n>=m+2:
        p=avoid(a,{h});q=avoid(b,set(accumulate(p))|{h});return 'cardinality',p,q
    r=max(0,n-m+1)
    if r<=n-1 and sum(b[:r])<v-u:
        R=b[:r];B=b[r:]
        F={h,u};F={f for f in F if 0<f<sum(B)}
        if len(B)==2:
            q=next(q for q in permutations(B) if not set(accumulate(q))&F)+R
        else:q=avoid(B,F)+R
        p=avoid(a,{f for f in set(accumulate(q))|{h} if f<u})
        return ('cardinality' if r==0 else 'tail'),p,q
    c=max(b); k=m-n+2
    if k>=1 and h<c and m-k>=3:
        for e in combinations(a,k):
            if sum(e)>=c:continue
            w=next((w for w in permutations(e) if h not in set(accumulate(w))),None)
            if w is None:continue
            p=w+avoid(tuple(x for x in a if x not in e),{h-sum(e),c-sum(e)})
            q=(c,)+avoid(tuple(x for x in b if x!=c),{f-c for f in set(accumulate(p))|{h} if f>c})
            return 'head',p,q
    def sums(a):
        s=1
        for x in a:s|=s<<x
        return s
    if not ((sums(a)|sums(b))>>h&1):
        p,q=separate(a,b);return 'subset',p,q
    return 'remaining',None,None

# Compare reserve-prefix tests in both orientations of the long path.

def reverse_head(a,b,h,P,Q):
    m,n=len(a),len(b);u,v=sum(a),sum(b);c=max(b);d=v-u;k=m-n+2
    # reverse the short path; reserve k trailing original steps whose sum < c-d.
    if k<1 or d>=c or m-k<3:return None
    for e in combinations(a,k):
        if sum(e)>=c-d:continue
        # reverse path must avoid u-h and c-d
        w=next((w for w in permutations(e) if u-h not in set(accumulate(w))),None)
        if w is None:continue
        pp=w+avoid(tuple(x for x in a if x not in e),{u-h-sum(e),c-d-sum(e)})
        p=pp[::-1]
        F={v-f for f in set(accumulate(p))|{h}}
        # first step c in reversed Y-path. Excludes d and k more forbidden vertices.
        assert c not in F
        qq=(c,)+avoid(tuple(x for x in b if x!=c),{f-c for f in F if f>c})
        return p,qq[::-1]


def exhaustive(M=12):
    D={}
    for P in range(2,M+1):
        d=defaultdict(list)
        for m in range(2,P):
            for a in combinations(range(1,P),m):d[sum(a)].append(a)
        D[P]=d
    total=Counter()
    for P in range(3,M+1):
        c=Counter()
        for Q in range(2,P):
            for h in range(1,Q+1):
                for a in D[P].get(Q+h,[]):
                    for b in D[Q].get(P+h,[]):
                        z,p,q=solve(a,b,h,P,Q)
                        if p is None:
                            pq=reverse_head(a,b,h,P,Q)
                            if pq is not None:z='reverse-head';p,q=pq
                        c[z]+=1
                        if p is not None:
                            assert sorted(p)==list(a) and sorted(q)==list(b)
                            v=set(accumulate(p));w=set(accumulate(q));assert not v&w and h not in v|w
                            A=tuple(a)+(P,)+tuple(-x for x in b)+(-Q,)
                            W=p+(-Q,P)+tuple(-x for x in q[::-1]);s=list(accumulate(W));assert sorted(A)==sorted(W) and len(s)==len(set(s)) and s[-1]==0 and max(s)-min(s)<=P+Q
        total+=c;print(P,dict(c))
    print('TOTAL',dict(total),sum(total.values()))
import random,itertools
from functools import lru_cache
from itertools import accumulate
rng=random.Random(475)

def masks(a,h):
 for q in itertools.permutations(a):
  s=0;v=0
  for x in q:
   s+=x
   if s==h:break
   v|=1<<s
  else:yield v

def works(a,b,h):
 # fast randomized check first
 for _ in range(20):
  aa=rng.sample(a,len(a));bb=rng.sample(b,len(b));s=set(accumulate(aa));t=set(accumulate(bb))
  if h not in s and h not in t and not s&t:return True
 aa=list(set(masks(a,h)));bb=list(set(masks(b,h)))
 return any(not x&y for x in aa for y in bb)

def randomized():
    n=0
    for t in range(50000):
     a=rng.sample(range(1,31),rng.randrange(2,7));b=rng.sample(range(1,31),rng.randrange(2,7));u,v=sum(a),sum(b)
     if u>v:a,b=b,a;u,v=v,u
     if u==v:continue
     h=rng.randrange(1,u//2+1)
     if max(b)>=u-h:continue
     n+=1
     if not works(a,b,h):print('FAIL',a,b,h,u,v,flush=True);break
    else:print('PASS',n,flush=True)

if __name__=='__main__':
    import sys
    if '--random' in sys.argv:randomized()
    else:exhaustive()
