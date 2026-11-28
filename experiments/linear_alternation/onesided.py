import itertools, sys
from fractions import Fraction
from math import factorial, comb
from hole_recurrence import dpow, L, sort_sign
def iota(mono,i):
    if i not in mono: return None,0
    k=mono.index(i); return mono[:k]+mono[k+1:],(-1)**k
def X(F,m):
    out={}
    for (A,B),c in F.items():
        for s in range(1,m+1):
            b2,sb=iota(B,s)
            if not sb: continue
            for a1,ca in dpow(A,s).items():
                a2,sa=iota(a1,0)
                if not sa: continue
                # tensor sign: (P (x) Q)(a(x)b) = (-1)^{|Q||a|} P a (x) Q b ; Q=iota odd, a after P? use Koszul with |a| = len(A) after applying P? apply sign (-1)^{len(a2)}
                key=(a2,b2); out[key]=out.get(key,0)+c*(-1)**s*factorial(s)*ca*sa*sb*(-1)**len(a2)
    return {k:v for k,v in out.items() if v}
def swap(F): return {(B,A):c for (A,B),c in F.items()}
def Y(F,m): return swap(X(swap(F),m))
def add(F,G,s=1):
    out=dict(F)
    for k,v in G.items(): out[k]=out.get(k,0)+s*v
    return {k:v for k,v in out.items() if v}
def prop(F,G):
    keys=set(F)|set(G)
    if not keys: return 'both0'
    k0=next(k for k in keys if G.get(k,0)!=0) if any(G.values()) else None
    if k0 is None: return None
    r=F.get(k0,0)/G[k0]
    return r if all(F.get(k,0)==r*G.get(k,0) for k in keys) else None
for m in (3,4,5,6):
    top=tuple(range(1,m+1)); F0={(top,top):Fraction(1)}
    # genuine F_r via signed recurrence
    Fr=[F0]
    for r in range(1,m):
        Fr.append({k:v*(-1)**(r-1+comb(m+1,2)) for k,v in L(Fr[-1]).items()})
    XF=X(F0,m); YF=Y(F0,m)
    seed={(tuple(x for x in top if x!=s),)*2:Fraction(factorial(s)) for s in top}
    print(f"m={m}: XF0=YF0: {XF==YF};  XF0 / factorial seed = {prop(XF,seed)}")
    cur=F0; res=[]
    for r in range(1,m):
        cur=X(cur,m); res.append(prop(Fr[r],cur))
    print(f"    F_r / X^r F0 for r=1..m-1: {res}")
    # (3),(4) on all balanced positive basis tensors of each size
    ok3=ok4=True; n=0
    for k in range(1,m+1):
        for A in itertools.combinations(top,k):
            for B in itertools.combinations(top,k):
                if sum(A)!=sum(B): continue
                f={(A,B):Fraction(1)}; n+=1
                L2=L(L(f)); XY=X(Y(f,m),m); YX=Y(X(f,m),m)
                if add(L2,XY)!={} or add(L2,YX)!={}:
                    ok3=False
                if add(L(X(f,m)),Y(L(f),m))!={} or add(L(Y(f,m)),X(L(f),m))!={}: ok4=False
    print(f"    (3) L^2=-XY=-YX on {n} balanced positive basis tensors: {ok3};  (4) LX=-YL, LY=-XL: {ok4}")
