from frec import reductions
import sys
N=int(sys.argv[1]);G=int(sys.argv[2])
have={};
for al in range(2,N+1):
    for be in range(2,N+1):
        rs=reductions(al,be,G)
        have[(al,be)]=sorted(set(r[3] for r in rs))
none=[k for k,v in have.items() if not v and k[0]+k[1]>=10]
print("T-instances (al,be) with al+be>=10 and NO bounded reduction:",len(none),"of",sum(1 for k in have if k[0]+k[1]>=10))
from collections import Counter
print("by (al+be) mod 3:",Counter((a+b)%3 for a,b in none))
print("examples with reduction:",[(k,v[:2]) for k,v in have.items() if v][:12])
