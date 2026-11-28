import itertools
from fractions import Fraction
from dual_checks import op, c_coef, to_ext, from_ext
def T(f,n): return from_ext(op(c_coef,to_ext(f,n),n),n)
def embed_q(f,n): return {(A+(n,),B+(n,)):-c for (A,B),c in f.items()}
for n in (5,6,7,8):
    bad=[]
    for k in range(0,n-1):
        for A in itertools.combinations(range(1,n),k):
            for B in itertools.combinations(range(1,n),k):
                if sum(A)!=sum(B): continue
                lhs=T({(A+(n,),B+(n,)):Fraction(1)},n)
                rhs=embed_q(T({(A,B):Fraction(1)},n-1),n)
                diff={key:lhs.get(key,0)-rhs.get(key,0) for key in set(lhs)|set(rhs)}
                diff={k_:v for k_,v in diff.items() if v}
                if diff: bad.append(((A,B),list(diff.items())[:2]))
    print("n=",n,"intertwining failures:",len(bad), bad[:3],flush=True)
