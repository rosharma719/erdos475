import sys
from audit_skew import allzig
M=int(sys.argv[1]); a=int(sys.argv[2]); b=M+1-a
P=range(1,M+1); N=sorted(set(range(1,M+2))-{a,b})
Z=allzig(P,N)
print(len(Z),"zigzags")
for st,V in Z[:int(sys.argv[3])]:
    sig=[x for x in st if x>0]; tau=[-x for x in st if x<0]
    Vs=set(V); u=[x for x in range(-M,1) if x not in Vs]; v=[x for x in range(1,M+1) if x not in Vs]
    runs=[];cur=[st[0]]
    for x in st[1:]:
        if (x>0)==(cur[-1]>0): cur.append(x)
        else: runs.append(cur);cur=[x]
    runs.append(cur)
    print("holes",u,v,"sig",sig,"tau",tau)
