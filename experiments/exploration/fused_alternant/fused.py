import sympy as sp, itertools, sys
from sympy.combinatorics import Permutation
n=int(sys.argv[1])
y=sp.symbols('y1:%d'%(n+1)); a=sp.Symbol('a')
def P(ys):
    u=[0]
    for v in ys: u.append(u[-1]+v)
    r=1
    for i in range(n+1):
        for j in range(i+1,n+1): r*=(u[j]-u[i])
    for j in range(1,n): r*=(u[j]+a)
    return r
tot=0
for perm in itertools.permutations(range(n)):
    s=Permutation(list(perm)).signature()
    tot+=s*P([y[i] for i in perm])
tot=sp.expand(tot)
V=sp.prod([y[j]-y[i] for i in range(n) for j in range(i+1,n)])
G=sp.cancel(tot/V)
G=sp.expand(G)
# express in elementary symmetric
from sympy.polys.polyfuncs import symmetrize
sym=symmetrize(G,*y,formal=True)
print(sp.factor(sym[0].subs(dict((s,v) for s,v in []))), sym[1])
print(sym[2])
