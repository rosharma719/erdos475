"""Grid test: X bridge + LR core with k=floor((M-a)/2), all 2<=a, 2a<=M-1, M in [lo,hi]. Full walk verified."""
import sys
from lrscan import lr
from xcore import ok
def walkX(M,a,D):
    b=M+1-a; d=[y-x for x,y in zip(D,D[1:])]
    return d+[M]+[-x for x in d[::-1]]+[a,-M,b,-(M+1)]
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for M in range(lo,hi+1):
    bad=[]
    for a in range(2,(M-1)//2+1):
        k=(M-a)//2; r=lr(M,a,k,timeout=60)
        if not (isinstance(r,list) and ok(M,a,walkX(M,a,[v-k for v in r]))): bad.append((a,r if not isinstance(r,list) else 'BADWALK'))
    print(M,'fail:',bad,flush=True)
