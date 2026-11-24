"""R1 core for bridge G=(b,-M,-(M+1),a): shifted V={0}∪([3,n-2]\\{h})∪{n}, n=M+1, start a+1, labels [1,n-2]\\{a,n-a}.
Report which holes h admit a path."""
import sys
from shape_sat import hpath
def r1(M,a,h,timeout=30):
    n=M+1; V={0,n}|set(range(3,n-1)); V.discard(h)
    return hpath(V,set(range(1,n-1))-{a,n-a},a+1,timeout=timeout)
if __name__=="__main__":
    for a,M in [tuple(map(int,x.split(':'))) for x in sys.argv[1:]]:
        good=[];bad=[];to=[]
        for h in range(3,M):
            if h==a+1: continue
            r=r1(M,a,h,20)
            (good if isinstance(r,list) else bad if r=='UNSAT' else to).append(h)
        print(a,M,'good h:',good,'TO:',to,flush=True)
