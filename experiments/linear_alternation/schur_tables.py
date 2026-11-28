import itertools, io, contextlib, sys, time
from math import gcd, comb
from functools import reduce
with contextlib.redirect_stdout(io.StringIO()):
    import pascal_checks as PC
    import witt_checks as WC
    import merge_matrix_check as MM
    import schur_checks as SC
kappa=PC.kappa
W_basis=MM.W_basis; dstar=WC.dstar
def content(v): return reduce(gcd,[abs(int(x)) for x in v])
for m in range(5,int(sys.argv[1])+1):
    t0=time.time()
    U=tuple(range(2,m+1))
    # merge image gcd
    basis=W_basis(m); ds=dstar(U)
    b={K:ds.get(K,0) for K in basis}
    img=[sum(kappa(J,I)*b[J] for J in basis if b[J]) for I in basis]
    merge_g=content(img)
    # Schur packets via kappa(I_mu, J_d)
    gd1=0; gall=0
    for d in range(1,m+1):
        J=tuple(x for x in range(1,m+1) if x!=d)
        for mu in SC.partitions(m-d,m-1):
            I=SC.Iset(mu,m)
            if sum(I)!=sum(J): continue
            v=kappa(I,J)
            gall=gcd(gall,abs(v))
            if d==1: gd1=gcd(gd1,abs(v))
    print(f"rank {m}: d=1 Schur packet gcd = {gd1};  combined (all d) gcd = {gall};  merge-image gcd = {merge_g};  |W basis|={len(basis)}   ({time.time()-t0:.0f}s)",flush=True)
