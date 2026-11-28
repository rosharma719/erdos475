import itertools, sympy
from fractions import Fraction
from math import factorial, comb
from onesided import X, Y, L
from hole_recurrence import C
def basis2(m):
    top=range(1,m+1)
    return [(A,B) for A in itertools.combinations(top,2) for B in itertools.combinations(top,2) if sum(A)==sum(B)]
def onehole(F,m): return [sympy.Rational(F.get(((d,),(d,)),0)) for d in range(1,m+1)]
for m in range(4,9):
    bas=basis2(m)
    cols=[]; xs=[]; ys=[]; Ys=[]; pis=[]
    for b in bas:
        f={b:Fraction(1)}
        x=onehole(X(f,m),m); y=onehole(L(f),m); yy=onehole(Y(f,m),m)
        pi=C(f,m); piv=[sympy.Rational(pi.get(((d,),(d,)),0)) for d in range(1,m)]
        xs.append(x); ys.append(y); Ys.append(yy); pis.append(piv)
    Mxy=sympy.Matrix([x+y for x,y in zip(xs,ys)]).T
    # diagonal-only inputs
    diag=[i for i,(A,B) in enumerate(bas) if A==B]
    Md=Mxy[:,diag]
    # formula (2),(3) check on diagonal E_ab
    ok2=ok3=True
    for i in diag:
        a,b=bas[i][0]
        pred2=[0]*m; pred2[a-1]+=(-1)**(b+1)*factorial(b)*(comb(b,a)-1); pred2[b-1]+=(-1)**a*factorial(a)
        pred3=[(-1)**(a+b)*(factorial(a+b-d) if a+b-d>=0 else 0)*(comb(b,d)-comb(a,d))**2 for d in range(1,m+1)]
        if [abs(v) for v in xs[i]]!=[abs(v) for v in pred2] : ok2=False
        if [abs(v) for v in ys[i]]!=[abs(v) for v in pred3]: ok3=False
    print(f"m={m}: |(2)| matches X E_ab (up to sign): {ok2}; |(3)| matches L E_ab: {ok3}; rank Psi (all two-hole) = {Mxy.rank()}, (diagonal only) = {Md.rank()}, 2m-2 = {2*m-2}",flush=True)
    # Theorem 3: kernel of (X, Y, L) on SYMMETRIC tensors with prescribed pi_m projection
    if m in (5,6,7):
        # symmetric basis: E_{A,B}+E_{B,A}
        sym=[]; seen=set()
        for i,(A,B) in enumerate(bas):
            if (B,A) in seen: continue
            seen.add((A,B)); j=bas.index((B,A)); sym.append((i,j))
        def vec(lst,i,j): return [lst[i][k]+(lst[j][k] if j!=i else 0) for k in range(len(lst[i]))]
        K=sympy.Matrix([vec(xs,i,j)+vec(Ys,i,j)+vec(ys,i,j) for i,j in sym]).T
        P=sympy.Matrix([vec(pis,i,j) for i,j in sym]).T
        ker=K.nullspace()
        img=sympy.Matrix.hstack(*[P*v for v in ker]) if ker else sympy.zeros(m-1,1)
        w=sympy.Matrix([(-1)**d*factorial(d) for d in range(1,m)]).T
        print(f"     symmetric kernel dim {len(ker)}; pi_m(kernel) rank {img.rank()} (claim: = hyperplane sum (-1)^d d! g_d = 0, dim {m-2}); image inside hyperplane: {(w*img).is_zero_matrix}")
