import sympy, itertools
from itertools import combinations_with_replacement
def nf(poly,vars_):
    """integral normal form modulo (e_1..e_n) in vars_ (lex x1>...>xn) using h_k(x_k..x_n)"""
    n=len(vars_)
    G=[sympy.expand(sum(sympy.prod(c) for c in combinations_with_replacement(vars_[k:],k+1))) for k in range(n)]
    return sympy.reduced(sympy.expand(poly),G,*vars_,order='lex')[1]
def fres(xs):
    m=len(xs); r=1
    for i in range(2,m+1):
        for j in range(i+1,m+1):
            if (i,j)==(2,m): continue
            r*=sum(xs[k-1] for k in range(i,j+1))
    return sympy.expand(r)
x=sympy.symbols('x1:6'); y=sympy.symbols('y1:5')
f5=fres(list(x)); f4=fres(list(y))
def dd(F,i):  # i 1-based
    a,b=x[i-1],x[i]
    sw=F.subs({a:b,b:a},simultaneous=True)
    return sympy.cancel((F-sw)/(a-b))
def word(F,w):   # apply rightmost first
    for i in reversed(w): F=sympy.expand(dd(F,i))
    return F
words=[(1,2,1),(2,3,2),(4,3,2)]
target=nf(f4,list(y))
for zero in (1,5):
    rest=[v for k,v in enumerate(x,1) if k!=zero]
    tot=0
    for w in words: tot+=word(f5,w)
    D=sympy.expand(tot.subs(x[zero-1],0).subs(dict(zip(rest,y)),simultaneous=True))
    for order_note in ("as stated",):
        print(f"restrict x{zero}=0: nf(-sum D) == nf(f_4): {sympy.expand(nf(-D,list(y))-target)==0};  nf(sum D)==nf(f4): {sympy.expand(nf(D,list(y))-target)==0}")
# also reversed reading (leftmost first)
for zero in (1,5):
    rest=[v for k,v in enumerate(x,1) if k!=zero]
    tot=sum(word(f5,tuple(reversed(w))) for w in words)
    D=sympy.expand(tot.subs(x[zero-1],0).subs(dict(zip(rest,y)),simultaneous=True))
    print(f"[left-to-right] restrict x{zero}=0: -sum == f4: {sympy.expand(nf(-D,list(y))-target)==0}; +sum: {sympy.expand(nf(D,list(y))-target)==0}")
