# Exact all-cut and individual quadratic saturation contents for the cyclic chord polynomial.
# Usage: python erdos475_exact_quadratic_packets.py 8
# A: linear value content; B and T: (matrix content, diagonal content, four-index rectangular-difference content).
# All arithmetic is integral; Artin normal forms use 0 <= exponent of x_i < i (1-indexed).
from functools import lru_cache
from itertools import combinations
from collections import defaultdict
from math import gcd
import sys

def comps(k,d):
 if d==1: yield (k,);return
 for x in range(k+1):
  for y in comps(k-x,d-1):yield (x,)+y

def calc(n):
 rules=[list(c for c in comps(i+1,n-i) if c[0]!=i+1) for i in range(n)]
 @lru_cache(None)
 def red(a):
  i=next((i for i,k in enumerate(a) if k>i),n)
  if i==n:return {a:1}
  out=defaultdict(int)
  for c in rules[i]:
   b=list(a);b[i]-=i+1
   for j,v in enumerate(c,i):b[j]+=v
   for z,v in red(tuple(b)).items():out[z]-=v
  return {z:v for z,v in out.items() if v}
 def mul(D,L):
  E=defaultdict(int)
  for a,v in D.items():
   for k,s in L:
    b=list(a);b[k]+=1
    for z,w in red(tuple(b)).items():E[z]+=v*w*s
  return {z:v for z,v in E.items() if v}
 def add(*terms):
  E=defaultdict(int)
  for D,c in terms:
   for a,v in D.items(): E[a]+=v*c
  return {a:v for a,v in E.items() if v}
 top=tuple(range(n)); one={(0,)*n:1}
 def M(B):
  BB=[mul(B,[(r,1)]) for r in range(n)]
  return [[mul(BB[r],[(s,1)]).get(top,0) for s in range(n)] for r in range(n)]
 def contents(M):
  return gcd(*(v for r in M for v in r)),gcd(*(M[i][i] for i in range(n))),gcd(*(M[i][j]-M[i][l]-M[k][j]+M[k][l] for i,j,k,l in __import__('itertools').permutations(range(n),4)))
 Acont=0; Bcont=[0,0,0]
 print('rank',n,flush=True)
 for j in range(1,n+1):
  edges=[([(i,1)],-1 if i==0 else 0) for i in range(n)]
  edges.insert(j,([],1))
  A=one; B={}
  for l,r in combinations(range(n),2):
   if l==0 and r==n-1:continue
   L=[v for i in range(l,r+1) for v in edges[i][0]]
   c=sum(edges[i][1] for i in range(l,r+1))
   A,B=mul(A,L),add((mul(B,L),1),(A,c),(mul(B,[(0,1)]),c))
  ac=gcd(*(mul(A,[(r,1)]).get(top,0) for r in range(n)))
  bc=contents(M(B))
  Acont=gcd(Acont,ac); Bcont=[gcd(a,b) for a,b in zip(Bcont,bc)]
  print(' cut',j,'A',ac,'B',bc,flush=True)
 Q=one
 for l,r in combinations(range(n-1),2):
  if l==0 and r==n-2:continue
  Q=mul(Q,[(i,1) for i in range(l,r+1)])
 Tcont=[0,0,0]
 for i,j in combinations(range(n),2):
  T=Q
  for k in range(n):
   if k not in (i,j):T=mul(T,[(k,1)])
  Tcont=[gcd(a,b) for a,b in zip(Tcont,contents(M(T)))]
 print('aggregate A,B,T',Acont,Bcont,Tcont,flush=True)
 red.cache_clear()
for n in range(4,int(sys.argv[1])+1):calc(n)
