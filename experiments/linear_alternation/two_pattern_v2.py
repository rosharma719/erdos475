"""Unnormalised alternating patterns: P(A,B)=sum sgn D^{a}X^{b}...D^{a}X^{b} (X applied first), Q(A,B)=sum sgn X^{b}D^{a}...X^{b}D^{a}.
S=P+(-1)^r Q, r=|A|=|B|. Operators act on Z[t]."""
import itertools, sys
from math import prod
import sympy
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def apply_word(word,poly):   # word list of ('D',a)/('X',b) leftmost applied last; poly dict deg->coef
    for kind,e in reversed(word):
        new={}
        for d,c in poly.items():
            if kind=='X': new[d+e]=new.get(d+e,0)+c
            else:
                if d>=e:
                    f=prod(range(d-e+1,d+1)) if e>0 else 1
                    new[d-e]=new.get(d-e,0)+c*f
        poly={k:v for k,v in new.items() if v}
        if not poly: return {}
    return poly
def pattern_apply(A,B,kind,poly):
    A=list(A); B=list(B); r=len(A); out={}
    for s in itertools.permutations(range(r)):
        for t in itertools.permutations(range(r)):
            sg=sgn(s)*sgn(t); w=[]
            for j in range(r):
                if kind=='P': w+=[('D',A[s[j]]),('X',B[t[j]])]
                else: w+=[('X',B[t[j]]),('D',A[s[j]])]
            res=apply_word(w,poly)
            for k,v in res.items(): out[k]=out.get(k,0)+sg*v
    return {k:v for k,v in out.items() if v}
def S_apply(A,B,poly):
    r=len(A); P=pattern_apply(A,B,'P',poly); Q=pattern_apply(A,B,'Q',poly)
    out=dict(P)
    for k,v in Q.items(): out[k]=out.get(k,0)+(-1)**r*v
    return {k:v for k,v in out.items() if v}
H=sympy.symbols('h')
def eig_poly(A,kind,npts):
    vals=[]
    for h in range(npts):
        if kind=='S': res=S_apply(A,A,{h:1})
        else: res=pattern_apply(A,A,kind,{h:1})
        vals.append((h,res.get(h,0)))
    return sympy.expand(sympy.interpolate(vals,H)) if any(v for _,v in vals) else sympy.Integer(0)
if __name__=="__main__":
    M=int(sys.argv[1])
    for m in range(3,M+1):
        U=list(range(2,m+1)); r=m-1; npts=2*m+2
        P=eig_poly(U,'P',npts); Q=eig_poly(U,'Q',npts); S=eig_poly(U,'S',npts)
        print(f"m={m}: deg P={sympy.degree(P,H)}, deg Q={sympy.degree(Q,H)}, deg S={sympy.degree(S,H) if S!=0 else '-'} (bounds 2m-2={2*m-2}, m-1={m-1})")
        if m==3: print("   P_3 =",P,"\n   Q_3 =",Q,"\n   S_3 =",S, "\n   Q_3(0),Q_3(1),Q_3(2) =",[Q.subs(H,x) for x in (0,1,2)])
        sU=sum(U)
        print("   reflection P(-h-1) = (-1)^{sum U} Q(h):",sympy.expand(P.subs(H,-H-1)-(-1)**sU*Q)==0)
        # descent identity (1): P({0}uA,{0}uB) = S(A,B) as operators, test on t^h, h=0..6, A=B=U minus last, also unbalanced pairs
        ok=True; tests=0
        base=list(range(1,m+1))
        for A in itertools.combinations(base,r-1):
            for B in itertools.combinations(base,r-1):
                if sum(A)!=sum(B): continue
                for h in range(0,5):
                    lhs=pattern_apply((0,)+A,(0,)+B,'P',{h:1}); rhs=S_apply(A,B,{h:1}); tests+=1
                    if lhs!=rhs:
                        neg={k:-v for k,v in rhs.items()}
                        if lhs!=neg: ok=False
                if not ok: break
            if not ok: break
        print(f"   descent P(0+A,0+B) = +-S(A,B) on t^h ({tests} tests, A,B subsets of 1..m of size r-1): {ok}")
        # moment theorem (3)
        def vac(A,B):
            res=S_apply(A,B,{0:1}); return res.get(0,0)
        moms={}
        for k in range(2,2*m-1):
            tot=0
            for i in range(1,m+1):
                for j in range(i+1,m+1):
                    if i+j!=k+1: continue
                    Aij=[x for x in base if x not in (i,j)]
                    for a in range(1,m+1):
                        for b in range(a+1,m+1):
                            if a+b!=k+1: continue
                            Aab=[x for x in base if x not in (a,b)]
                            tot+=(j-i)*(b-a)*vac(Aij,Aab)
            moms[k]=tot
        pred=sympy.expand((-1)**(m-2)*sum(moms[k]*sympy.ff(H,k) for k in moms))
        print("   moments M_{m,k}:",moms)
        print("   Q_m = (-1)^(m-2) sum M_k h^(k) :",sympy.expand(pred-Q)==0, "  (with opposite sign:",sympy.expand(pred+Q)==0,")")
        if sympy.expand(pred-Q)!=0 and sympy.expand(pred+Q)!=0:
            print("     Q_m in falling-factorial basis:", [ (k, sympy.Poly(sympy.expand(Q),H)) for k in []], )
