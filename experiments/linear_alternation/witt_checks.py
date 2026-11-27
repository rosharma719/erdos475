"""Witt-differential report: exponent-one insertion, self-adjointness, homotopy, merge recurrence, collision derivative, content of Q_m."""
import itertools, io, contextlib, math, sys, random
from fractions import Fraction
from math import comb, factorial, gcd
from functools import reduce
with contextlib.redirect_stdout(io.StringIO()):
    import pascal_checks as PC
kappa=PC.kappa; parts=PC.parts; Cref=PC.C
def fac(S): return math.prod(factorial(x) for x in S)
# ---- exterior algebra on e_c (c>=1): elements = dict {sorted tuple: coeff}
def sort_sign(seq):
    seq=list(seq)
    if len(set(seq))<len(seq): return 0,None
    s=1
    for i in range(len(seq)):
        for j in range(i+1,len(seq)):
            if seq[i]>seq[j]: s=-s
    return s,tuple(sorted(seq))
def d_basis(J):
    out={}
    for s,c in enumerate(J):
        for a in range(1,c+1):
            b=c+1-a
            if a<b:
                coef=comb(c,a)-comb(c,b)
                if coef==0: continue
                seq=J[:s]+(a,b)+J[s+1:]
                sg,key=sort_sign(seq)
                if sg: out[key]=out.get(key,0)+(-1)**s*coef*sg
    return {k:v for k,v in out.items() if v}
def wedge1(J):
    if 1 in J: return {}
    return {(1,)+J:1}
def contract1(J):
    if J and J[0]==1: return {J[1:]:1}
    return {}
def apply(op,vec):
    out={}
    for J,c in vec.items():
        for K,v in op(J).items(): out[K]=out.get(K,0)+c*v
    return {k:v for k,v in out.items() if v}
def vadd(a,b,s=1):
    out=dict(a)
    for k,v in b.items(): out[k]=out.get(k,0)+s*v
    return {k:v for k,v in out.items() if v}
# (a) exponent-one insertion: kappa({1} u A', I) = sum_J kappa(A',J) [e_I](e_1 ^ e_J - d e_J)
bad=0;n=0
for k in (2,3):
    for Ap in itertools.combinations(range(2,9),k-1):
        sA=sum(Ap)
        for J in parts(sA,k-1):
            pass
        for I in parts(sA+1,k):
            lhs=kappa((1,)+Ap,I)
            rhs=0
            for J in parts(sA,k-1):
                kj=kappa(Ap,J)
                if not kj: continue
                vec=vadd(wedge1(J),d_basis(J),-1)
                rhs+=kj*vec.get(I,0)
            n+=1
            if lhs!=rhs: bad+=1; 
print(f"(a) kappa({{1}} u A',I) = sum_J kappa(A',J)[e_I](e_1^ - d)e_J : {n} cases, k=2,3, mismatches {bad}")
# (b) self-adjointness kappa(A,I) I! = kappa(I,A) A!
bad=0;n=0
for k in (1,2,3,4):
    for I in itertools.combinations(range(1,9),k):
        for A in parts(sum(I),k):
            n+=1
            if kappa(A,I)*fac(I)!=kappa(I,A)*fac(A): bad+=1
print(f"(b) kappa(A,I) prod i! = kappa(I,A) prod a!  (sets incl. exponent 1): {n} pairs, mismatches {bad}")
# (c) homotopy identity: iota_1 D + D iota_1 = (1 - nu) id  on monomials
ok=True
for n_ in range(1,5):
    for J in itertools.combinations(range(1,9),n_):
        w=lambda K: vadd(wedge1(K),d_basis(K),-1)              # D = e_1^ - d
        lhs=vadd(apply(contract1,apply(w,{J:1})),apply(w,apply(contract1,{J:1})))
        nu=sum(c-1 for c in J)
        expected={J:1-nu} if 1-nu else {}
        if lhs!=expected: ok=False
print("(c) iota_1 D + D iota_1 = (1 - nu) id on all e_J, |J|<=4, entries<=8:",ok)
# (d) merge recurrence: kappa({1} u A,{1} u A) = (1-nu(A)) kappa(A,A) - <d*e_A, M d*e_A>/prod a!
def dstar(B):                      # adjoint of d w.r.t. <e_A,e_I> = delta prod a!:  coefficient of e_J in d* e_B = (coef of e_B in d e_J) B!/J!
    out={}
    n=len(B)
    # candidates J: sets of size n-1 obtained by splitting pairs? enumerate J over merge-source: J contains c with a,b in B, a+b=c+1
    for x,a in enumerate(B):
        for y in range(x+1,n):
            b=B[y]; c=a+b-1
            rest=tuple(t for i,t in enumerate(B) if i not in (x,y))
            if c in rest: continue
            J=tuple(sorted(rest+(c,)))
            if J in out: continue
            coef=d_basis(J).get(B,0)
            if coef: out[J]=Fraction(coef*fac(B),fac(J))
    return out
bad=0;n=0
for k in (2,3,4):
    for A in itertools.combinations(range(2,10),k):
        dsA=dstar(A)
        pair=Fraction(0)
        for J,cj in dsA.items():
            for I,ci in dsA.items():
                kk=kappa(J,I)
                if kk: pair+=cj*ci*kk*fac(I)
        nuA=sum(a-1 for a in A)
        lhs=kappa((1,)+A,(1,)+A)
        rhs=(1-nuA)*kappa(A,A)-pair/fac(A)
        n+=1
        if lhs!=rhs: bad+=1; 
        if n<=3: print("    example A=",A,"lhs",lhs,"rhs",rhs)
print(f"(d) merge recurrence: {n} sets A (|A|=2..4, entries 2..9): mismatches {bad}")
print("    kappa({1..m},{1..m}) =",[kappa(tuple(range(1,m+1)),tuple(range(1,m+1))) for m in range(2,8)])
