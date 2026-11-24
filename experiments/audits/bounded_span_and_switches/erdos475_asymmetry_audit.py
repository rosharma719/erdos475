"""Erdos #475: five-unpaired-element contraction audit.
Standard library only. Default verifies two template failures and a successful
symmetric-core expansion. --exhaustive also checks every symmetric completion
of each multiplicative orbit of weakly sum-free five-element zero-sum remainders
for p=23,29,31. This is not a proof or counterexample to Graham's conjecture.
"""
from itertools import combinations,product

def valid(w,p):
 s=0; v=set()
 for a in w:
  s=(s+a)%p
  if s in v:return False
  v.add(s)
 return True

def four(A,p):
 U=sorted(a for a in A if -a%p not in A)
 assert len(U)==4
 M=p//2
 for b in U[1:]:
  l=pow((U[0]+b)%p,-1,p); il=pow(l,-1,p)
  B={a*l%p for a in A};
  # descending scan, choose path for each unpaired
  def rec(i,P,Q,e,f):
   if i==0:
    if not P or not Q:return
    P=P[::-1]; Q=Q[::-1]
    for X,Y,sgn in [(P,Q,1),(Q,P,-1)]:
     w=X+[-a for a in Y[-2::-1]]+[-Y[-1]]
     yield tuple(a*il*sgn%p for a in w)
    return
   a=i in B; b=p-i in B
   if a and b:
    if e==f:yield from rec(i-1,P+[e*i],Q+[f*i],-e,-f)
   elif a or b:
    x=i if a else -i
    if x==e*i:yield from rec(i-1,P+[x],Q,-e,f)
    if -x==f*i:yield from rec(i-1,P,Q+[-x],e,-f)
   else:yield from rec(i-1,P,Q,e,f)
  yield from rec(M,[],[],1,1)

def solve(A,p,U):
 for a,b in combinations(sorted(U),2):
  c=(a+b)%p
  if c not in A:
   opts=[(a,b,c)]
  else:opts=[(a,-c%p,-b%p),(b,-c%p,-a%p)]
  for x,y,z in opts:
   B=(A-{x,y})|{z}
   assert len(B)==len(A)-1 and z not in A
   for w in four(B,p):
    assert valid(w,p),(w,B,p)
    j=w.index(z)
    for u,v in [(x,y),(y,x)]:
     w2=w[:j]+(u,v)+w[j+1:]
     if valid(w2,p):return w2
 return None

def reps(p):
 seen=set()
 for U in combinations(range(1,p),5):
  if sum(U)%p or any(-x%p in U for x in U) or any((x+y)%p in U for x,y in combinations(U,2)):continue
  U=frozenset(U)
  if U in seen:continue
  seen.update(frozenset(x*l%p for x in U) for l in range(1,p))
  yield U

from itertools import permutations

def sym(B,p,l):
 il=pow(l,-1,p)
 mags=sorted(min(a*l%p,-a*l%p) for a in B if a<(-a%p))
 X=[a if i%2==0 else -a for i,a in enumerate(mags)]
 return tuple(a*il%p for a in X+[-a for a in X[-2::-1]]+[-X[-1]])

def double(A,p,U):
 for pair in combinations(sorted(U),2):
  X=set(pair);Y=U-X;c=sum(X)%p
  if c not in A:
   opts=[(X,Y,c,-c%p)]
  else:
   opts=[((X-{x})|{-c%p},(Y-{y})|{c},-x%p,-y%p) for x in X for y in Y]
  for D,E,d,e in opts:
   B=A-(D|E)|{d,e}
   assert B=={-x%p for x in B} and len(B)==len(A)-3
   for l in range(1,p//2+1):
    w=sym(B,p,l); assert valid(w,p)
    # use both global orientations of x_i signs? B symmetric, negation gives alternative order, not same original expansion. try both signs (reverse not needed)
    for w in [w,tuple(-x%p for x in w)]:
     s=0;V=set();u=v=None
     for a in w:
      V.add(s)
      if a==d:u=s
      if a==e:v=s
      s=(s+a)%p
     for dd in permutations(D):
      s=u;H=set()
      for a in dd[:-1]:s=(s+a)%p;H.add(s)
      if H&V or len(H)!=len(dd)-1:continue
      for ee in permutations(E):
       s=v;J=set()
       for a in ee[:-1]:s=(s+a)%p;J.add(s)
       if J&(V|H) or len(J)!=len(ee)-1:continue
       w2=tuple(a for b in w for a in (dd if b==d else ee if b==e else (b,)))
       assert valid(w2,p) and set(w2)==A
       return (pair,d,e,l,dd,ee,w2)
 return None


def maximal_completion(p,U):
    assert len(U)==5 and sum(U)%p==0
    assert all(-a%p not in U for a in U)
    assert all((a+b)%p not in U for a,b in combinations(U,2))
    return set(range(1,p))-{-a%p for a in U}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    p=211; U={31,87,133,179,203}; A=maximal_completion(p,U)
    assert solve(A,p,U) is None
    ans=double(A,p,U)
    assert ans is not None and valid(ans[-1],p) and set(ans[-1])==A
    print('p=211: one-contraction template fails; two-block template succeeds:',ans[:-1])
    p=503; U={112,168,388,406,435}; A=maximal_completion(p,U)
    assert solve(A,p,U) is None
    assert double(A,p,U) is None
    print('p=503: both stated canonical templates fail.')
    if args.exhaustive:
        for p in (23,29,31):
            count=0
            for U in reps(p):
                av=[a for a in range(1,p//2+1) if a not in U and p-a not in U]
                for mask in range(1<<len(av)):
                    A=set(U)|{v for i,a in enumerate(av) if mask>>i&1 for v in (a,p-a)}
                    w=solve(A,p,U)
                    assert w is not None and valid(w,p) and set(w)==A and len(w)==len(A)
                    count+=1
            print(f'p={p}: {count} completions checked; no failures')
