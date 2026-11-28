import itertools, sys
from fractions import Fraction
from dual_checks import op, c_coef, to_ext, fadd
from transfer_ops import make
for n in map(int,sys.argv[1:]):
    T=make(n+1); bad=0; tot=0
    for k in range(0,n):
        for A in itertools.combinations(range(1,n+1),k):
            for B in itertools.combinations(range(1,n+1),k):
                if sum(A)!=sum(B): continue
                f={(A,B):Fraction(1)}; tot+=1
                if fadd(to_ext(T(f),n),op(c_coef,to_ext(f,n),n),-1): bad+=1
    print(f"n={n}: corrected insertion form vs true transfer: {tot-bad}/{tot} balanced monomials agree",flush=True)
