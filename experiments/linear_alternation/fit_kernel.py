import itertools, sys
from fractions import Fraction
from math import comb, factorial
from dual_checks import M, c_coef, op, fpow, fadd, fscal, to_ext
from transfer_ops import make
import sympy
n=int(sys.argv[1]); T=make(n+1)
keys=[(h,a,b) for h in range(1,n+1) for a in range(h) for b in range(h)]
bal=[(A,B) for k in range(0,n+1) for A in itertools.combinations(range(1,n+1),k) for B in itertools.combinations(range(1,n+1),k) if sum(A)==sum(B)]
rows={}; cols=[]
data=[]
for A,B in bal:
    f={(A,B):Fraction(1)}; ef=to_ext(f,n)
    tgt=to_ext(T(f),n)
    basis=[]
    for (h,a,b) in keys:
        g=fpow(fpow(M(h-a,h-b,ef,n),n,0,a),n,1,b); basis.append(g)
    data.append((tgt,basis))
# unknowns c_k ; equations per output monomial
eqs=[]
for idx,(tgt,basis) in enumerate(data):
    monos=set(tgt)|set(m for g in basis for m in g)
    for mo in monos:
        eqs.append(([g.get(mo,0) for g in basis],tgt.get(mo,0)))
A=sympy.Matrix([[sympy.Rational(x.numerator,x.denominator) if hasattr(x,'numerator') else x for x in r] for r,_ in eqs])
b=sympy.Matrix([sympy.Rational(t.numerator,t.denominator) if hasattr(t,'numerator') else t for _,t in eqs])
aug=A.row_join(b)
print("unknowns",len(keys),"eqs",len(eqs),"rank A",A.rank(),"rank aug",aug.rank())
sol,params=A.gauss_jordan_solve(b) if A.rank()==aug.rank() else (None,None)
if sol is not None:
    free=params
    for k,s in zip(keys,sol):
        pc=c_coef(*k)
        print(k,"fit:",s,"paste:",pc)
