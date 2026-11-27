import itertools, sys
from fractions import Fraction
from math import factorial
from two_pattern_v2 import S_apply
# exterior tensors: dict {(A,B): coef}, A,B sorted tuples of indices in 0..m
def vac(A,B): return S_apply(list(A),list(B),{0:1}).get(0,0)
def F_direct(m,r):
    base=list(range(1,m+1)); out={}
    for holesA in itertools.combinations(base,m-r):
        for holesB in itertools.combinations(base,m-r):
            A=[x for x in base if x not in holesA]; B=[x for x in base if x not in holesB]
            if sum(A)!=sum(B): continue
            v=vac(A,B)
            if v: out[(holesA,holesB)]=Fraction(v)
    return out
def sort_sign(lst):
    s=1; a=list(lst)
    for i in range(len(a)):
        for j in range(len(a)-1-i):
            if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]; s=-s
    return tuple(a),s
def dpow(mono,s):   # divided power partial^(s) = partial^s/s! applied to exterior monomial -> dict
    cur={tuple(mono):Fraction(1)}
    for _ in range(s):
        new={}
        for mo,c in cur.items():
            for idx,x in enumerate(mo):
                if x==0: continue
                y=x-1
                if y in mo: continue
                l=list(mo); l[idx]=y; t,sg=sort_sign(l)
                new[t]=new.get(t,0)+sg*c*x
        cur={k:v for k,v in new.items() if v}
    return {k:v/factorial(s) for k,v in cur.items()}
def Rop(F):
    out={}
    for (A,B),c in F.items():
        sign=(-1)**sum(A)
        smax=max(sum(A),1)
        for s in range(0,sum(A)+1):
            da=dpow(A,s)
            if not da: continue
            db=dpow(B,s)
            for a2,ca in da.items():
                for b2,cb in db.items():
                    key=(a2,b2); out[key]=out.get(key,0)+c*sign*factorial(s)*ca*cb
    return {k:v for k,v in out.items() if v}
def C(F,j):
    out={}
    for (A,B),c in F.items():
        if j in A and j in B:
            ia=A.index(j); ib=B.index(j)
            out[(A[:ia]+A[ia+1:],B[:ib]+B[ib+1:])]=out.get((A[:ia]+A[ia+1:],B[:ib]+B[ib+1:]),0)+c*(-1)**(ia+ib)
    return {k:v for k,v in out.items() if v}
def L(F): return C(Rop(F),0)
def prop(F,G):
    keys=set(F)|set(G)
    if not keys: return 'both0'
    k0=next(iter(keys)); 
    if G.get(k0,0)==0: return None
    r=F.get(k0,0)/G[k0]
    return r if all(F.get(k,0)==r*G.get(k,0) for k in keys) else None
if __name__=="__main__":
    for m in (3,4,5):
        Fs={r:F_direct(m,r) for r in range(0,m)}
        Fs[0]={(tuple(range(1,m+1)),tuple(range(1,m+1))):Fraction(1)}
        for r in range(1,m):
            print(f"m={m} r={r}: F_r = c * C_0 R F_(r-1) with c =",prop(Fs[r],L(Fs[r-1])),flush=True)
        if m==5:
            print(" genuine F_1 (holes -> coef):",{k[0]:v for k,v in Fs[1].items()})
            # modified seed: change coefficient of highest surviving exponent 5 (hole set = {1,2,3,4})
            Fmod=dict(Fs[1]); key=((1,2,3,4),(1,2,3,4)); Fmod[key]=Fraction(-360)
            cur={1:Fmod}
            signs={r:prop(Fs[r],L(Fs[r-1])) for r in range(1,m)}
            for r in range(2,m): cur[r]={k:v*signs[r] for k,v in L(cur[r-1]).items()}
            print(" modified seed: upper packet F_4 =",cur[4])
            g=C(Fs[3],5); mo=C(cur[3],5)
            print(" genuine C_5 F_3:",g); print(" modified C_5 F_3:",mo, " ratio:",prop(mo,g))
            print(" genuine F_4:",Fs[4])
