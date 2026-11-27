import sys, sympy, time
from fractions import Fraction
from math import comb
from hole_recurrence import L
def run(m):
    t0=time.time(); base=tuple(range(1,m+1))
    def iterate(F):
        for r in range(2,m):
            F={k:v*(-1)**(r-1+comb(m+1,2)) for k,v in L(F).items()}
        return F
    vecs=[]
    for a in range(1,m+1):
        h=tuple(x for x in base if x!=a)
        vecs.append(iterate({(h,h):Fraction((-1)**comb(m+1,2))}))
    keys=sorted(set(k for v in vecs for k in v))
    N=sympy.Matrix([[sympy.Rational(v.get(k,0)) for k in keys] for v in vecs])
    d=N.det() if N.shape[0]==N.shape[1] else None
    print(f"m={m}: N_m shape {N.shape}, rank {N.rank()}, det = {sympy.factorint(d) if d else d}, primes > m+1: {[p for p in sympy.factorint(d) if p>m+1] if d else '-'}  ({time.time()-t0:.0f}s)",flush=True)
for m in range(4,int(sys.argv[1])+1): run(m)
