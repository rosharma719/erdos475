import sys, itertools, time
from fractions import Fraction
from math import factorial, comb
from transfer_ops import *
from transfer_checks import *
import sympy
def balanced(n,k):
    out=[]
    for A in itertools.combinations(range(1,n+1),k):
        for B in itertools.combinations(range(1,n+1),k):
            if sum(A)==sum(B): out.append((A,B))
    return out
def run(n):
    m=n+1; T=make(m); t0=time.time()
    bases={k:balanced(n,k) for k in range(0,n+1)}
    Tm={}   # Tm[k][(A,B)] = image dict
    for k in range(1,n):
        Tm[k]={}
        for mono in bases[k]:
            Tm[k][mono]=T({mono:Fraction(1)})
    print(f"n={n}: dims",{k:len(bases[k]) for k in bases}, "time",round(time.time()-t0,1),flush=True)
    # grading
    graded=all(set((len(A)) for (A,B) in im)<= {k+1} and all(sum(A)==sum(B) for (A,B) in im) for k in Tm for im in Tm[k].values())
    print("  T maps B_k -> B_{k+1}:",graded)
    # terminal vanishing (6)
    term=all(not Tm[n-1][mono] for mono in bases[n-1]) if n-1 in Tm else None
    print("  T(B_{n,n-1})=0:",term)
    # matrices
    def mat(k):
        rows=bases[k+1]; cols=bases[k]; idx={r:i for i,r in enumerate(rows)}
        M=sympy.zeros(len(rows),len(cols))
        for j,c in enumerate(cols):
            for r,v in Tm[k][c].items(): M[idx[r],j]=sympy.Rational(v.numerator,v.denominator)
        return M
    Ms={k:mat(k) for k in range(1,n)}
    # surjectivity (5): T(B_{n,n-2}) = M_n = span e_1..e_{n-1}
    if n>=3:
        M=Ms[n-2]; rows=bases[n-1]
        print("  rank T:B_{n-2}->B_{n-1} =",M.rank(),"(M_n dim",n-1,"; B_{n,n-1} dim",len(rows),")")
        # image contained in span e_d, d<n  : e_d = U_{n\d}V_{n\d}
        edix=[i for i,(A,Bm) in enumerate(rows) if A==Bm]
        # columns of image in terms of e_d: row (A,B) A=B=n\d
        miss=[ [x for x in range(1,n+1) if x not in A][0] for (A,Bm) in rows]
        print("  image rows (missing index d):",miss)
        print("  image row d=n zero:", all(M[i,:].is_zero_matrix for i,d in enumerate(miss) if d==n))
    # P_n = T^{n-2} on B_{n,1}
    if n>=3:
        P=sympy.eye(len(bases[1]))
        for k in range(1,n-1): P=Ms[k]*P
        print("  P_n shape",P.shape,"rank",P.rank())
        # seed vectors
        b1=bases[1]; Hseed=sympy.Matrix([sympy.Rational(1-i,factorial(i+1)) for (A,Bm) in b1 for i in [A[0]]])
        qn=sympy.Matrix([1 if A[0]==n else 0 for (A,Bm) in b1])
        PH=P*Hseed; Pq=P*qn
        print("  P_n(H_2) nonzero:",not PH.is_zero_matrix,"  P_n(q_n) nonzero:",not Pq.is_zero_matrix)
        two=sympy.Matrix.hstack(PH,Pq); print("  rank{P(H2),P(qn)} =",two.rank())
        # smith-style: gcd of maximal minors of P restricted to span{H2,q_n}: use integer content of 2-col matrix
        # primes where rank drops
        den=sympy.ilcm(*[sympy.fraction(x)[1] for x in two]) if two.rows else 1
        Zm=(two*den).applyfunc(sympy.Integer)
        from sympy.matrices.normalforms import smith_normal_form
        snf=smith_normal_form(Zm,domain=sympy.ZZ)
        d=[abs(snf[i,i]) for i in range(min(snf.shape)) if snf[i,i]!=0]
        print("  Smith invariants of [P(H2)|P(q_n)] (scaled by",den,"):",d, " prime support:",sorted(set(sympy.primefactors(sympy.prod(d)))) if d else None)
        # unscaled content on P(H2) alone
        v=PH*den; g=sympy.igcd(*[int(x) for x in v]) if any(v) else 0
        print("  P_n(H_2) scaled integer content:",g, sorted(sympy.primefactors(g)) if g else None)
    # pivot (8)
    if n>=3:
        a=((tuple(range(1,n-1)),tuple(range(1,n-1))))
        im=Tm[n-2].get(a)
        if im is not None:
            key=(tuple(x for x in range(1,n+1) if x!=n-1),)*2
            print("  a_n in basis:",a in Tm[n-2]," coeff of e_{n-1} in T(a_n):",im.get(key),"  predicted",-Fraction(comb(n,2),factorial(n+1)))
for n in map(int,sys.argv[1:]): run(n)
