import sys, time
from math import gcd
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
import sympy
for m in map(int,sys.argv[1:]):
    t0=time.time(); vals=[]
    for d in (1,2):
        J=tuple(c for c in range(1,m+1) if c!=d); vals.append(kappa(J,J))
    g=gcd(abs(vals[0]),abs(vals[1]))
    print(f"m={m}: gcd(kappa_1,kappa_2) = {g} = {sympy.factorint(g)}  primes>m+1: {[p for p in sympy.factorint(g) if p>m+1]}  ({time.time()-t0:.0f}s)",flush=True)
