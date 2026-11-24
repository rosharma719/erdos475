"""Junction c=a two-phase BLOCK shape: lower blocks [2a i, 2a i + a-1] (i<L), upper blocks
[2aL+a+2a j, 2aL+2a-1+2a j]; leftover (M mod a) points form a partial block at the top end or bottom end."""
import sys
from junction_shape import path_on
def shape(M,a,L,where):
    low=[2*a*i+r for i in range(L) for r in range(a)]
    rest=M-len(low)
    if rest<0: return None
    U,ex=divmod(rest,a); base=2*a*L+a
    up=[base+2*a*j+r for j in range(U) for r in range(a)]
    D=low+up
    if ex:
        if where=='top': D+= [base+2*a*U+r for r in range(ex)]
        else: D+= [-2*a+a+r for r in range(ex)][:ex]  # partial block below: [-a, -a+ex-1]
    return D
def test(M,a,Ls=(1,2,3,4)):
    b=M+1-a; labels=set(range(1,M+1))-{a}
    for L in Ls:
        for where in ('top','bottom'):
            D=shape(M,a,L,where)
            if not D: continue
            S=set(D)
            if len(S)<M or any(x+a in S for x in S) or max(D)-min(D)>2*M+2-a: continue
            for st in sorted(S):
                if st+b in S:
                    p=path_on({x-st for x in S},labels,0,b)
                    if p: return (L,where,st)
    return None
if __name__=="__main__":
    a=int(sys.argv[1])
    for M in range(int(sys.argv[2]),int(sys.argv[3])+1):
        if 2*a>=M+1: continue
        print(a,M,test(M,a),flush=True)
