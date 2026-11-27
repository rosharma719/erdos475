import sys, sympy
from two_pattern_v2 import S_apply
for m in range(3,int(sys.argv[1])+1):
    U=list(range(2,m+1))
    v=S_apply(U,U,{0:1}).get(0,0)
    print(f"m={m}: S_m(0) = {v} = {sympy.factorint(v)}  primes > m+1: {[p for p in sympy.factorint(v) if p>m+1]}",flush=True)
