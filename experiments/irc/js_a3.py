"""a=3 junction (c=3): shapes = blocks 'xxx...' (period 6) followed by an alternating run 'x.x.x' (or the reverse),
with a gap g between; exact SAT on the vertex set."""
import sys
from junction_shape import path_on
def shapes(M,a=3):
    for m in range(0,M//a+1):
        t=M-a*m
        if t<0: continue
        for g in range(a, a+4):
            for order in ('BA','AB'):
                if order=='BA':
                    B=[2*a*j+r for j in range(m) for r in range(a)]
                    s=(B[-1]+g) if B else 0
                    A=[s+2*i for i in range(t)]
                else:
                    A=[2*i for i in range(t)]
                    s=(A[-1]+g) if A else 0
                    B=[s+2*a*j+r for j in range(m) for r in range(a)]
                yield (m,t,g,order),A+B
def test(M,a=3):
    b=M+1-a;labels=set(range(1,M+1))-{a}
    for key,D in shapes(M,a):
        S=set(D)
        if len(S)<M or any(x+a in S for x in S) or max(D)-min(D)>2*M+2-a: continue
        for st in sorted(S):
            if st+b in S:
                p=path_on({x-st for x in S},labels,0,b)
                if p: return key,st
    return None
for M in range(int(sys.argv[1]),int(sys.argv[2])+1):
    print(M,test(M),flush=True)
