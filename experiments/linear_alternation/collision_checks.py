import itertools, io, contextlib, math, sys
from math import comb
with contextlib.redirect_stdout(io.StringIO()):
    import pascal_checks as PC
kappa=PC.kappa; C=PC.C
def shuffle_sign(S,Sc):
    seq=list(S)+list(Sc); s=1
    for i in range(len(seq)):
        for j in range(i+1,len(seq)):
            if seq[i]>seq[j]: s=-s
    return s
def Fpoly(m,r):
    S=tuple(range(1,m+1)); poly={}
    for I in itertools.combinations(S,r):
        Ic=tuple(x for x in S if x not in I)
        for A in itertools.combinations(S,r):
            if sum(A)!=sum(I): continue
            Ac=tuple(x for x in S if x not in A)
            kk=kappa(A,I)*kappa(Ac,Ic)
            if not kk: continue
            t=shuffle_sign(A,Ac)*shuffle_sign(I,Ic)*(-1)**sum(Ic)*kk
            poly[sum(I)]=poly.get(sum(I),0)+t
    return poly
def ev(poly,q): return sum(c*q**e for e,c in poly.items())
def dev(poly): return sum(c*e for e,c in poly.items())
for m in range(3,8):
    res=[]
    for r in range(1,m):
        P=Fpoly(m,r); F1=ev(P,1); d1=dev(P)
        res.append((r,F1,d1))
    print(f"m={m}: (r, F_(m,r)(1), F'_(m,r)(1)) =",res)
    # compare derivative vector with partial sums of boundary vectors of rank m and m+1 (global sign allowed)
    for rank in (m,m+1):
        if rank in C:
            c=C[rank]
            for r,F1,d1 in res:
                ps=sum(c[:max(0,rank-r)])
                pass
    d=[x[2] for x in res]
    for rank in (m,m+1):
        c=C[rank]
        cand=[(-1)**r*sum(c[:j]) for r in range(1,m) for j in [m-r]]
        cand2=[(-1)**r*sum(c[:j]) for r in range(1,m) for j in [rank-r]]
        print(f"     derivative vector {d}   vs (-1)^r*partial sums (first m-r coefficients) of c_{rank}: {cand}   (first rank-r): {cand2}")
