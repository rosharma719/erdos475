import sys
from junction_shape import path_on
def test(M,L=1,shift=2):
    b=M-1;labels=set(range(1,M+1))-{2};u=4*L+shift
    base=[4*i+r for i in range(L) for r in (0,1)];rest=M-len(base);U=rest//2
    upper=[u+4*j+r for j in range(U) for r in (0,1)]
    opts=[base+upper] if rest%2==0 else [base+upper+[upper[-1]+3],base+upper+[base[0]-3]]
    for D in opts:
        S=set(D)
        if any(x+2 in S for x in S) or max(D)-min(D)>2*M: continue
        for st in sorted(S):
            if st+b in S:
                p=path_on({x-st for x in S},labels,0,b)
                if p: return st,(len(D)-len(base)-len(upper)),[x+st for x in p]
    return None
if __name__=="__main__":
 for M in range(int(sys.argv[1]),int(sys.argv[2])+1):
    r=test(M)
    print(M, r[:2] if r else None, flush=True)
