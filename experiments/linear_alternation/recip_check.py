import itertools, sympy
from math import gcd, factorial
from functools import reduce
rows={6:(80,70,-12,-6),7:(-280,2950,490),8:(15120,-524104,-46592),9:(-68826240,380773512,120766464,22777020)}
for m,r in rows.items():
    print(f"m={m}: gcd of individual coeffs = {reduce(gcd,[abs(x) for x in r])}")
print("rank-8 Casoratian:", -90*1-3397*2, sympy.factorint(6884))
# reciprocity c_{B,A} prod a! = c_{A,B} prod b!
r=3; t=sympy.symbols('t1:4')
L=[sum(t[:i+1]) for i in range(r)]
def V(A,x): return sympy.Matrix([[xi**a for a in A] for xi in x]).det()
def alt(f):
    out=0
    for p in itertools.permutations(range(r)):
        sg=sympy.combinatorics.Permutation(list(p)).signature()
        out+=sg*f.subs({t[i]:t[p[i]] for i in range(r)},simultaneous=True)
    return sympy.expand(out)
sets=[A for A in itertools.combinations(range(0,7),r)]
def coeffs(B):
    f=alt(V(B,L)); P=sympy.Poly(f,*t); out={}
    for A in sets:
        if sum(A)!=sum(B): continue
        # coefficient of V_A: leading monomial t1^{a3} t2^{a2} t3^{a1}? use monomial t^A sorted descending on t1..t3
        mono=t[0]**A[2]*t[1]**A[1]*t[2]**A[0]
        out[A]=P.coeff_monomial(mono)
    return out
# extract c_{B,A} properly: solve f = sum c_A V_A
def cBA(B):
    f=alt(V(B,L)); cand=[A for A in itertools.combinations(range(0,sum(B)+1),r) if sum(A)==sum(B)]
    cs=sympy.symbols('c0:%d'%len(cand))
    g=sympy.expand(f-sum(c*V(A,t) for c,A in zip(cs,cand)))
    sol=sympy.solve(sympy.Poly(g,*t).coeffs(),cs,dict=True)[0]
    return {A:sol.get(c,0) for c,A in zip(cs,cand)}
import sympy.combinatorics
C={B:cBA(B) for B in sets}
ok=True; n=0
for B in sets:
    for A,v in C[B].items():
        lhs=v*sympy.prod([factorial(a) for a in A]); rhs=(C[A] if A in C else cBA(A)).get(B,0)*sympy.prod([factorial(b) for b in B]); n+=1
        if sympy.simplify(lhs-rhs)!=0: ok=False
print(f"reciprocity (4), r=3, exponent sets in [0,6]: {ok} on {n} pairs")
