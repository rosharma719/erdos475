import itertools
from fractions import Fraction
from math import comb, factorial
def weyl_mul(A,B):
    out={}
    for (a,b),c1 in A.items():
        for (c,d),c2 in B.items():
            for s in range(min(b,c)+1):
                co=c1*c2*factorial(s)*comb(b,s)*comb(c,s)
                key=(a+c-s,b+d-s); out[key]=out.get(key,0)+co
    return {k:v for k,v in out.items() if v}
def wadd(A,B,s=1):
    out=dict(A)
    for k,v in B.items(): out[k]=out.get(k,0)+s*v
    return {k:v for k,v in out.items() if v}
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def D(a): return {(0,a):1}
def X(b): return {(b,0):1}
def pattern(A,B,first='D'):
    r=len(A); tot={}
    for s in itertools.permutations(range(r)):
        for t in itertools.permutations(range(r)):
            prod={(0,0):1}
            for j in range(r):
                f1=D(A[s[j]]); f2=X(B[t[j]])
                prod=weyl_mul(prod,f1); prod=weyl_mul(prod,f2) if first=='D' else prod
                if first=='X':
                    prod={(0,0):1} if False else prod
            tot=wadd(tot,{k:v*sgn(s)*sgn(t) for k,v in prod.items()})
    return tot
def pattern2(A,B,first):
    r=len(A); tot={}
    for s in itertools.permutations(range(r)):
        for t in itertools.permutations(range(r)):
            prod={(0,0):1}
            for j in range(r):
                if first=='D': facs=[D(A[s[j]]),X(B[t[j]])]
                else: facs=[X(B[t[j]]),D(A[s[j]])]
                for f in facs: prod=weyl_mul(prod,f)
            tot=wadd(tot,{k:v*sgn(s)*sgn(t) for k,v in prod.items()})
    return tot
def S(A,B):
    r=len(A); P=pattern2(A,B,'D'); Q=pattern2(A,B,'X')
    return wadd(P,{k:v*(-1)**r for k,v in Q.items()})
# (13): P_r({0} u A, {0} u B) = S_{r-1}(A,B)
for A,B in [((1,2),(3,4)),((2,3),(1,5)),((1,2,3),(2,3,4))]:
    r=len(A)+1
    lhs=pattern2((0,)+A,(0,)+B,'D'); rhs=S(A,B)
    print(f"(13) r={r}, A={A}, B={B}: P_r({{0}} u A, {{0}} u B) == S_(r-1)(A,B): {lhs==rhs}")
# (14)/(15): C={1..m-1};  T_{m-1} = S on {2..m-1}.  Compare normal-ordered coefficients.
for m in (4,5):
    C=tuple(range(1,m)); Up=tuple(range(2,m))
    P=pattern2(C,C,'D'); Sg=S(Up,Up)
    print(f"m={m}: S_(m-2)({{2..m-1}}) = {dict(sorted(Sg.items()))}")
    print(f"      P_(m-1)({{1..m-1}}) = {dict(sorted(P.items()))}")
    ratios=[]
    for (i,j),a in sorted(Sg.items()):
        if i==j and i>=0:
            k=i
            c=P.get((k+1,k+1),0)
            ratios.append((k,Fraction(c)/Fraction(a)*(k+1)**2 if a else None))
    print(f"      P_(k+1,k+1) / (a_k/(k+1)^2) over k with a_k != 0: {[(k,str(r)) for k,r in ratios]}")
