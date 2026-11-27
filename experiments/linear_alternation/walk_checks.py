"""Checks for the signed-height-walk / Weyl-algebra report."""
import itertools, math, sys, re, io, contextlib
from math import comb, factorial
from fractions import Fraction
from functools import lru_cache
with contextlib.redirect_stdout(io.StringIO()):
    import pascal_checks as PC
kappa=PC.kappa; Cref=PC.C; parts=PC.parts
def Cb(n,k): return comb(n,k) if 0<=k<=n else 0
# (1) triangular flow summation
def tri_tables(I,A):
    k=len(I)
    def rec(r,remcols):
        if r==k:
            if all(c==0 for c in remcols): yield []
            return
        def fill(s,left,cur):
            if s==k:
                if left==0: yield tuple(cur)
                return
            if s<r:
                cur.append(0); yield from fill(s+1,left,cur); cur.pop(); return
            for x in range(min(left,remcols[s])+1):
                if s==r and x==0: continue                     # positive diagonal
                cur.append(x); yield from fill(s+1,left-x,cur); cur.pop()
        for row in fill(0,I[r],[]):
            yield from ((([row]+rest)) for rest in rec(r+1,[c-x for c,x in zip(remcols,row)]))
    yield from rec(0,list(A))
ok1=True;n1=0
for k in (1,2,3):
    for I in itertools.product(range(1,6),repeat=k):
        for A in itertools.product(range(1,6),repeat=k):
            if sum(I)!=sum(A): continue
            tot=Fraction(0)
            for M in tri_tables(I,A):
                w=Fraction(math.prod(factorial(a) for a in A))
                for row in M:
                    for x in row: w/=factorial(x)
                tot+=w
            h=0; prod=1
            for r in range(k):
                hp=h; h+=I[r]-A[r]
                prod*= (Cb(I[r]+hp,I[r])-Cb(h,I[r])) if h>=0 else 0
            n1+=1
            if tot!=prod: ok1=False
print(f"(1) triangular-flow summation = prod[C(i_r+h_(r-1),i_r) - C(h_r,i_r)]: {n1} margin pairs (k<=3): {'OK' if ok1 else 'FAIL'}")
# (2) signed-height walk expansion of kappa (double alternation) and DP recursion
def T(i,a,h):
    hn=h+i-a
    if hn<0: return 0
    return Cb(h+i,i)-Cb(hn,i)
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
bad=0;n2=0
for k in (1,2,3,4):
    for I in itertools.combinations(range(2,8),k):
        for A in parts(sum(I),k):
            if max(A)>sum(I): continue
            tot=0
            for s in itertools.permutations(range(k)):
                for t in itertools.permutations(range(k)):
                    h=0; prod=1
                    for r in range(k):
                        i=I[s[r]]; a=A[t[r]]; prod*=T(i,a,h); h+=i-a
                        if prod==0: break
                    tot+=sgn(s)*sgn(t)*prod
            n2+=1
            if tot!=kappa(A,I): bad+=1
print(f"(2) kappa = sum_(sigma,tau) sgn(sigma tau) prod T_(i,a)(h): {n2} pairs, k<=4: mismatches {bad}")
@lru_cache(None)
def F(A,I):
    k=len(A)
    if k==0: return 1
    h=sum(I)-sum(A)
    if h<0: return 0
    tot=0
    for x,i in enumerate(I):
        for y,a in enumerate(A):
            hp=h-i+a
            if hp<0: continue
            tt=T(i,a,hp)
            if tt: tot+=(-1)**(x+y)*tt*F(A[:y]+A[y+1:],I[:x]+I[x+1:])
    return tot
bad=0;n3=0
for k in (1,2,3,4):
    for I in itertools.combinations(range(2,8),k):
        for A in parts(sum(I),k):
            if max(A)>sum(I): continue
            n3+=1
            if F(A,I)!=kappa(A,I): bad+=1
print(f"    DP recursion F(A,I) (remove last transition) vs Pascal kappa: {n3} pairs, mismatches {bad}")
def contraction(m,r,kap):
    U=tuple(range(2,m+1)); tot=0
    for I in itertools.combinations(U,r):
        Ic=tuple(x for x in U if x not in I)
        for A in itertools.combinations(U,r):
            if sum(A)!=sum(I): continue
            Ac=tuple(x for x in U if x not in A)
            tot+=(-1)**(r+sum(Ic))*kap(A,I)*kap(Ac,Ic)
    return tot
for m in range(3,11):
    got=[contraction(m,r,F) for r in range(0,m)]; ref=Cref[m]
    print(f"    m={m}: boundary vector from walk DP vs stored c_m: {'equal' if got==ref else 'negated' if got==[-x for x in ref] else 'DIFFERENT'}",flush=True)
# (3) Weyl commutator weight
ok=True
for h in range(0,9):
    for i in range(1,6):
        for a in range(1,6):
            # U b_h=(h+1)b_{h+1}, D b_h=b_{h-1}; vectors as dict
            def U_(v): return {h_+1:(h_+1)*c for h_,c in v.items()}
            def D_(v): return {h_-1:c for h_,c in v.items() if h_>0}
            def Upow(v,i):
                for _ in range(i): v=U_(v)
                return {k:c//factorial(i) for k,c in v.items()}
            def Dpow(v,a):
                for _ in range(a): v=D_(v)
                return v
            v={h:1}
            lhs1=Dpow(Upow(v,i),a); lhs2=Upow(Dpow(v,a),i)
            diff={k:lhs1.get(k,0)-lhs2.get(k,0) for k in set(lhs1)|set(lhs2)}
            diff={k:c for k,c in diff.items() if c}
            exp={h+i-a:T(i,a,h)} if h+i-a>=0 and T(i,a,h) else {}
            if diff!=exp: ok=False
print("(3) [D^a,U_i] b_h = T_{i,a}(h) b_{h+i-a}  (with [i]-divided powers): h<=8, i,a<=5:", "OK" if ok else "FAIL")
# (4) modular height truncation: for p prime, h<p, 2<=i,a<=p-2: step to h'>=p has T = 0 mod p
for p in (11,13,17,19):
    bad=0
    for h in range(p):
        for i in range(2,p-1):
            for a in range(2,p-1):
                if h+i-a>=p and T(i,a,h)%p!=0: bad+=1
    print(f"(4) p={p}: steps leaving [0,p-1] with nonzero weight mod p: {bad}")
# (5) counterexamples
print("(5) kappa({a,b},{a,b}) = 2 - C(b,a):", all(kappa((a,b),(a,b))==2-comb(b,a) for a in range(2,7) for b in range(a+1,10)), "; kappa({2,7},{2,7}) =",kappa((2,7),(2,7)))
def Cvec(U):
    n=len(U); out=[]
    for r in range(n+1):
        tot=0
        for I in itertools.combinations(U,r):
            Ic=tuple(x for x in U if x not in I)
            for A in itertools.combinations(U,r):
                if sum(A)!=sum(I): continue
                Ac=tuple(x for x in U if x not in A)
                tot+=(-1)**(r+sum(Ic))*kappa(A,I)*kappa(Ac,Ic)
        out.append(tot)
    return out
print("    contraction polynomial for U={2,7}:",Cvec((2,7)))
v=Cvec((13,14,15,16)); print("    contraction polynomial for U={13,14,15,16}:",v)
print("    gcd of first two coefficients:",math.gcd(abs(v[0]),abs(v[1])),"=",[p for p in (2,5,13,53) if math.gcd(abs(v[0]),abs(v[1]))%p==0])
