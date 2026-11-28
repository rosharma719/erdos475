from functools import lru_cache
from itertools import combinations
from collections import defaultdict

def comps(k,d):
 if d==1: yield (k,);return
 for x in range(k+1):
  for y in comps(k-x,d-1):yield (x,)+y

def test(n,p):
 rules=[list(c for c in comps(i+1,n-i) if c[0]!=i+1) for i in range(n)]
 @lru_cache(None)
 def red(a):
  i=next((i for i,k in enumerate(a) if k>i),n)
  if i==n:return {a:1}
  out=defaultdict(int)
  for c in rules[i]:
   b=list(a);b[i]-=i+1
   for j,v in enumerate(c,i):b[j]+=v
   for z,v in red(tuple(b)).items():out[z]=(out[z]-v)%p
  return {z:v for z,v in out.items() if v}
 def mul(D,L):
  E=defaultdict(int)
  for a,v in D.items():
   for k,s in L:
    b=list(a);b[k]+=1
    for z,w in red(tuple(b)).items():E[z]=(E[z]+v*w*s)%p
  return {z:v for z,v in E.items() if v}

 def add(*terms):
  E=defaultdict(int)
  for D,c in terms:
   for a,v in D.items(): E[a]=(E[a]+v*c)%p
  return {a:v for a,v in E.items() if v}
 # split u_1 into u_1-t and t, insert t after j original labels.
 # all labels represented by (linear combination of u, coefficient of t)
 for j in range(1,n+1):
  edges=[([(i,1)],-1 if i==0 else 0) for i in range(n)]
  edges.insert(j,([],1))
  A={(0,)*n:1}; B={}
  for l,r in combinations(range(n),2):
   if l==0 and r==n-1:continue
   L=[v for i in range(l,r+1) for v in edges[i][0]]
   c=sum(edges[i][1] for i in range(l,r+1))
   A,B=mul(A,L),add((mul(B,L),1),(A,c),(mul(B,[(0,1)]),c))
  print('m,p,cut',n,p,j,'value',len(A),'jet',len(B),next(iter(B.items()),None),flush=True)
test(7,3)
