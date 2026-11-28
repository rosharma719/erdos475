import sys, time, pickle, os
from fractions import Fraction
from math import factorial, gcd
from functools import reduce
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
import sympy
cache='kappa_cache.pkl'
K=pickle.load(open(cache,'rb')) if os.path.exists(cache) else {}
M=int(sys.argv[1])
for m in range(3,M+1):
    if m not in K:
        t0=time.time()
        K[m]=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
        pickle.dump(K,open(cache,'wb')); print(f"kappa m={m} ({time.time()-t0:.0f}s)",flush=True)
def big(x,b):
    x=abs(x)
    if x==0: return 0
    for p in sympy.primerange(2,b+1):
        while x%p==0: x//=p
    return x
def kap(m,d): return K[m][d-1] if 1<=d<=m else 0
# (1) identification with corrected v_n coordinates (parse ph2_fixed.txt)
v={}; cur=None
for line in open('ph2_fixed.txt'):
    if line.startswith('n='): cur=int(line.split('=')[1]); v[cur]={}
    elif line.strip().startswith('e_') and cur:
        d=int(line.split(':')[0].strip()[2:]); v[cur][d]=Fraction(line.split(':')[1].split()[0])
for n in sorted(v):
    if n+1>M: continue
    ratios=set()
    for j in range(1,n+1):
        val=v[n].get(j,Fraction(0)); ref=factorial(j+1)*kap(n+1,j+1)
        if ref==0: ratios.add('ok0' if val==0 else 'BAD')
        else: ratios.add(val/ref)
    print(f"(1) n={n}: v_n[j] / ((j+1)! kappa_(n+1,j+1)) over j: {ratios}")
print("kappa_{m,m}=0 for all m:",all(K[m][m-1]==0 for m in K if m<=M))
print("alternating sum zero:",all(sum((-1)**(d-1)*K[m][d-1] for d in range(1,m+1))==0 for m in K if m<=M))
# (2)-(3) minor table
print(" n | full 2x2 gcd | first-3-rows gcd | big part (>n+1) full / first3 | I_{n+1}*I_n content (odd n check)")
for n in range(4,M):
    rows=[(kap(n+1,d),kap(n,d)) for d in range(2,n+2)]
    def mg(rs):
        return reduce(gcd,[abs(rs[i][0]*rs[j][1]-rs[j][0]*rs[i][1]) for i in range(len(rs)) for j in range(i+1,len(rs))],0)
    gf=mg(rows); g3=mg(rows[:3])
    I1=reduce(gcd,[abs(x) for x in K[n+1]]); I0=reduce(gcd,[abs(x) for x in K[n]])
    print(f" {n} | {gf} | {g3} | {big(gf,n+1)} / {big(g3,n+1)} | {I1*I0}  {'(odd: D=I*I up to units: '+str(big(gf,n+2)==big(I1*I0,n+2))+')' if n%2 else ''}")
# (4) three-coefficient gcd
for m in range(4,M+1):
    g=reduce(gcd,[abs(kap(m,d)) for d in (2,3,4)])
    print(f"(4) m={m}: gcd(k2,k3,k4) = {sympy.factorint(g)}  primes>m+1: {[p for p in sympy.factorint(g) if p>m+1]}")
