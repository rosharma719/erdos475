from itertools import combinations
from functools import lru_cache

def solve(A,W):
 n=len(A);F=(1<<n)-1
 @lru_cache(None)
 def f(m,s,v):
  if m==F:return ()
  for i,a in enumerate(A):
   if m>>i&1:continue
   t=s+a
   if not 0<=t<=W:continue
   if m|1<<i==F:
    if t==0:return (a,)
   elif not v>>t&1:
    w=f(m|1<<i,t,v|1<<t)
    if w is not None:return (a,)+w
  return None
 return f(0,0,1)
for M in range(1,12):
 A0=list(range(-M,0))+list(range(1,M+1));count=0
 for k in range(2,2*M+1):
  for A in combinations(A0,k):
   if sum(A) or max(map(abs,A))!=M:continue
   count+=1
   W=max(A)-min(A)
   if solve(A,W) is None:print('FAIL',M,A,W,flush=True);raise SystemExit
 print(M,count,flush=True)
