import itertools, sympy
from sympy.combinatorics import Permutation
for r in (3,4):
    x=sympy.symbols('x1:%d'%(r+1)); s=[sum(x[:i+1]) for i in range(r)]
    W=sum((r-i)*x[i-1] for i in range(1,r)); e1=sum(x); W0=W-sympy.Rational(r-1,2)*e1
    def alt(f):
        out=0
        for p in itertools.permutations(range(r)):
            out+=Permutation(list(p)).signature()*f.subs({x[i]:x[p[i]] for i in range(r)},simultaneous=True)
        return sympy.expand(out)
    def V(I,y): return sympy.Matrix([[yi**a for a in I] for yi in y]).det()
    zero=0; tot=0; examples=[]
    for I in itertools.combinations(range(1,r+4),r):
        f=alt(W0*V(I,s)); tot+=1
        if f==0: zero+=1
        elif len(examples)<2: examples.append(I)
    print(f"r={r}: Alt(W0 * V_I(Lx)) == 0 for {zero}/{tot} exponent sets I subset [1,{r+3}]; nonzero e.g. {examples}")
