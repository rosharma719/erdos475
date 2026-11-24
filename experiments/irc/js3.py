import sys
from js2 import test
for M in range(int(sys.argv[1]),int(sys.argv[2])+1):
    res=None
    for L in (1,2,3):
        r=test(M,L,2)
        if r: res=(L,r[0],r[1]);break
    print(M,res,flush=True)
