"""X bridge W=(δ,+M,−δ^rev,+a,−M,+b,−(M+1)). Window family: D=[−j,M+2−j]\\{1,a} minus one point from each
distance-M pair (−j+i, M−j+i), i=0,1,2 (pattern bits: 0=drop low,1=drop high). Path from 0, labels [1,M−1]\\{a,b}."""
import sys,itertools
from shape_sat import hpath
from xcore import ok
def xshape(M,a,j,pat):
    D=set(range(-j,M+3-j))-{1,a}
    for i,bit in enumerate(pat): D.discard((-j+i) if bit==0 else (M-j+i))
    return D
def walk(M,a,path):
    b=M+1-a; d=[y-x for x,y in zip(path,path[1:])]
    return d+[M]+[-x for x in d[::-1]]+[a,-M,b,-(M+1)]
def test(M,a,j,pat,timeout=20):
    D=xshape(M,a,j,pat)
    if 0 not in D or len(D)!=M-2 or a-M in D or (M+1) in D: return None
    r=hpath(D,set(range(1,M))-{a,M+1-a},0,timeout=timeout)
    if isinstance(r,list): return 'Y' if ok(M,a,walk(M,a,r)) else 'BAD'
    return r
if __name__=="__main__":
    a,M=int(sys.argv[1]),int(sys.argv[2])
    for j in range(0,M):
        row=[]
        for pat in itertools.product((0,1),repeat=3):
            t=test(M,a,j,pat)
            if t is not None: row.append(''.join(map(str,pat))+':'+t[0])
        if row: print('j',j,' '.join(row),flush=True)
