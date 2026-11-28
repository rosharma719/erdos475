import itertools, sympy
from fractions import Fraction
def sort_sign(l):
    s=1; a=list(l)
    for i in range(len(a)):
        for j in range(len(a)-1-i):
            if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]; s=-s
    return tuple(a),s
def deriv(f,op):   # op: exponent -> new exponent or None
    out={}
    for mono,c in f.items():
        for idx,x in enumerate(mono):
            y=op(x)
            if y is None or (y in mono and y!=x): continue
            l=list(mono); l[idx]=y; t,s=sort_sign(l)
            if len(set(t))<len(t): continue
            out[t]=out.get(t,0)+s*c
    return {k:v for k,v in out.items() if v}
def add(f,g,s=1):
    o=dict(f)
    for k,v in g.items(): o[k]=o.get(k,0)+s*v
    return {k:v for k,v in o.items() if v}
def iota(f,k):
    out={}
    for mono,c in f.items():
        if k in mono:
            i=mono.index(k); out[mono[:i]+mono[i+1:]]=out.get(mono[:i]+mono[i+1:],0)+c*(-1)**i
    return out
def wedge1(f):
    out={}
    for mono,c in f.items():
        if 1 in mono: continue
        t=(1,)+mono; out[t]=out.get(t,0)+c
    return out
ok=True; n=0
for k in (2,3,4):
    R=lambda x:x+1; T=lambda x:(x-k if x>k else None)
    for size in (1,2,3):
        for mono in itertools.combinations(range(1,10),size):
            f={mono:1}; n+=1
            lhs=add(deriv(deriv(f,R),T),deriv(deriv(f,T),R),-1)
            rhs=wedge1(iota(f,k))
            if add(lhs,rhs,-1): ok=False
print(f"[T_k,R] = e_1 wedge iota_k on {n} exterior monomials (k=2,3,4; sizes 1-3): {ok}")
r=4; x=sympy.symbols('x1:5'); X,Y=sympy.symbols('X Y'); S=sum(x); s=[sum(x[:i+1]) for i in range(r)]
V=[0]+s+[X,Y]; W0=sum((sympy.Rational(r+1,2)-i)*x[i-1] for i in range(1,r+1))
print("(11) W0 = e1(V - S/2) - (X+Y-S):", sympy.expand(sum(v-S/2 for v in V)-(X+Y-S)-W0)==0)
