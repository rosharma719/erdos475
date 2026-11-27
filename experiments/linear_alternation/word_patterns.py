"""Balanced coefficient of Z^{m-1} (missing xi_d, eta_d) as eigenvalue on t^h.
Only alternating words survive: S_AB = sum sgn(s)sgn(t) A_t1 B_s1 ... A_tk B_sk ; S_BA = sum sgn sgn B_s1 A_t1 ... B_sk A_tk.
A_a = D^a/a!, B_i = X^i/i!.  Evaluate on t^h exactly at integer h, interpolate."""
import sys, itertools
from fractions import Fraction
from math import factorial
import sympy
def perm_sign(p):
    s=1; p=list(p)
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def ff(x,a):
    r=1
    for j in range(a): r*=(x-j)
    return r
def word_val(word,h):   # word: list of ('A',a)/('B',i), leftmost applied last
    val=Fraction(1); x=h
    for kind,e in reversed(word):
        if kind=='B': val/=factorial(e); x+=e
        else:
            val*=Fraction(ff(x,e),factorial(e)); x-=e
            if val==0: return Fraction(0)
    return val
def patterns(m,d,hs):
    idx=[i for i in range(1,m+1) if i!=d]
    perms=[(p,perm_sign(p)) for p in itertools.permutations(idx)]
    SAB={h:Fraction(0) for h in hs}; SBA={h:Fraction(0) for h in hs}
    for s,ss in perms:
        for t,st in perms:
            sg=ss*st
            wAB=[]; wBA=[]
            for j in range(len(idx)):
                wAB+= [('A',t[j]),('B',s[j])]
                wBA+= [('B',s[j]),('A',t[j])]
            for h in hs:
                SAB[h]+=sg*word_val(wAB,h); SBA[h]+=sg*word_val(wBA,h)
    return SAB,SBA
H=sympy.symbols('h')
def interp(vals):
    pts=sorted(vals)
    return sympy.expand(sympy.interpolate([(x,sympy.Rational(vals[x].numerator,vals[x].denominator)) for x in pts],H))
if __name__=="__main__":
    for m in range(2,int(sys.argv[1])+1):
        for d in range(1,m+1):
            deg=m*(m+1)//2
            hs=list(range(0,deg+3))
            SAB,SBA=patterns(m,d,hs)
            pa=interp(SAB); pb=interp(SBA)
            print(f"m={m} d={d}: deg S_AB={sympy.degree(pa,H) if pa!=0 else '-'}  deg S_BA={sympy.degree(pb,H) if pb!=0 else '-'}")
            print("    S_AB =",sympy.factor(pa)); print("    S_BA =",sympy.factor(pb))
            print("    S_AB - S_BA =",sympy.factor(pa-pb),"   S_AB + S_BA =",sympy.factor(pa+pb))
