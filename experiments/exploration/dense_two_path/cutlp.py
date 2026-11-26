# LP relaxation of "closed walk in [0,M] using each label of S = I_M \ T exactly once" (cut-balance only).
# Infeasible => no closed walk at all => the two-path lemma fails for T.  Feasible => no cut-type obstruction.
import sys, random
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
def feasible(M,T):
    S=[v for v in range(-M,M+1) if v and v not in T]
    var=[]; 
    for i,s in enumerate(S):
        for a in range(0,M+1):
            if 0<=a+s<=M: var.append((i,a,s))
    nv=len(var); A=lil_matrix((len(S)+M,nv)); b=np.zeros(len(S)+M)
    for j,(i,a,s) in enumerate(var):
        A[i,j]=1
        lo,hi=min(a,a+s),max(a,a+s)
        for c in range(lo,hi):  # cut between c and c+1
            A[len(S)+c,j]= 1 if s>0 else -1
    b[:len(S)]=1
    r=linprog(np.zeros(nv),A_eq=A.tocsr(),b_eq=b,bounds=(0,1),method='highs')
    return r.status==0
def rand_T(M,k,rng):
    while True:
        T=rng.sample([v for v in range(-M,M+1) if v],k-1); last=-sum(T)
        if last and abs(last)<=M and last not in T and max(map(abs,T+[last]))==M: return T+[last]
def _main():
  mode=sys.argv[1]
  if mode=='check':  # known counterexample sanity
      print("k=31 cut example feasible?",feasible(31,set(list(range(-18,0))+list(range(5,16))+[30,31])))
      print("11-hole M=8 example feasible?",feasible(8,set(v for v in range(-8,9) if v and v not in {7,8,-4,-5,-6})))
  else:
      M=int(sys.argv[2]); k=int(sys.argv[3]); N=int(sys.argv[4]); rng=random.Random(int(sys.argv[5]))
      bad=0
      for _ in range(N):
          T=rand_T(M,k,rng)
          if not feasible(M,set(T)): bad+=1; print("OBSTRUCTED",M,k,sorted(T)) if bad<=5 else None
      print(f"M={M} k={k} samples={N} LP-obstructed={bad}",flush=True)
if __name__=='__main__': _main()
