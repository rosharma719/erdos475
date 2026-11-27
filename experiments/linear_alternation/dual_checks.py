import itertools, sys
from fractions import Fraction
from math import comb, factorial
from transfer_ops import *
from transfer_checks import *
import sympy
def M(i,j,f,n):
    return lmul(i,lmul(n+j,f)) if (1<=i<=n and 1<=j<=n) else {}
def c_coef(h,a,b):
    if a==0:
        return Fraction(comb(h,b),factorial(h+1))-Fraction(h-b,factorial(h-b+1)*factorial(b))
    return -Fraction((h-a)*comb(h-a,b),factorial(h-a+1)*factorial(a+1))
def d_coef(h,A,B):
    if B==0: return Fraction(0)
    if A>=1: return Fraction((-1)**(h+1)*B*comb(h-B,A),factorial(B+1)*factorial(h-B+1))
    return Fraction((-1)**(h+1)*B*(h-B),(h+1)*factorial(B+1)*factorial(h-B+1))
def op(coef,f,n,maxh=None):
    tot={}
    for h in range(1,2*n):
        for a in range(max(0,h-n),h):
            for b in range(max(0,h-n),h):
                c=coef(h,a,b)
                if c==0: continue
                g=fpow(fpow(f,n,0,a),n,1,b)
                g=M(h-a,h-b,g,n)
                tot=fadd(tot,fscal(g,c))
    return tot
if __name__=="__main__":
    # (1) vs T
    if __name__=="__main__":
      for n in (3,4,5):
        T=make(n+1); ok=True
        for k in range(0,n+1):
            for A in itertools.combinations(range(1,n+1),k):
                for B in itertools.combinations(range(1,n+1),k):
                    if sum(A)!=sum(B): continue
                    f={(A,B):Fraction(1)}
                    lhs=to_ext(T(f),n); rhs=op(c_coef,to_ext(f,n),n)
                    if fadd(lhs,rhs,-1): ok=False
        print("n=",n,"insertion form (1) matches T on all balanced monomials:",ok,flush=True)
    # (7),(8): polynomial check D_h(x,y)=C_h(-1-x,-1-y) vs (5),(6)
    x,y=sympy.symbols('x y')
    for h in range(1,9):
        C=sum(sympy.Rational(c_coef(h,a,b).numerator,c_coef(h,a,b).denominator)*x**a*y**b for a in range(h) for b in range(h))
        D=sympy.expand(C.subs({x:-1-x,y:-1-y},simultaneous=True))
        P=sympy.Poly(D,x,y)
        D2=sum(sympy.Rational(d_coef(h,a,b).numerator,d_coef(h,a,b).denominator)*x**a*y**b for a in range(h) for b in range(h))
        diff=sympy.expand(D-D2)
        print("h=",h,"D_h = C_h(-1-x,-1-y) agrees with (4)-(6) on a,b<=h-1:",diff==0, "" if diff==0 else str(sympy.Poly(diff,x,y).terms()[:3]))
    # pairing adjointness numerically with the explicit d's
    def top(f,n):
        return f.get(tuple(range(1,2*n+1)),0)
    def pair(f,g,n):
        tot=Fraction(0)
        for m1,c1 in f.items():
            for m2,c2 in g.items():
                if set(m1)&set(m2): continue
                new=m1+m2; inv=sum(1 for i in range(len(new)) for j in range(i+1,len(new)) if new[i]>new[j])
                tot+=c1*c2*(-1)**inv
        return tot
    for n in (3,4):
        allm=[tuple(s) for k in range(2*n+1) for s in itertools.combinations(range(1,2*n+1),k)]
        ok=True; bad=0
        import random; random.seed(1)
        for m1 in allm:
            for m2 in allm:
                if len(m1)+len(m2)!=2*n: continue
                if random.random()>0.15: continue
                lhs=pair(op(c_coef,{m1:Fraction(1)},n),{m2:Fraction(1)},n)
                rhs=pair({m1:Fraction(1)},op(d_coef,{m2:Fraction(1)},n),n)
                if lhs!=rhs: ok=False; bad+=1
        print("n=",n,"<T f,g> = <f, T^dagger g> with d from (5),(6) (sampled complementary pairs):",ok,bad,flush=True)
