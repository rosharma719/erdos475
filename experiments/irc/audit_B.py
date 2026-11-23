import sys; sys.path.insert(0,'../../research/data')
from B_certs import C
ok=0
for (M,a),D in C.items():
    b=M+1-a
    S={-1,0,*range(2,M-1),M+1}
    good=len(D)==M and set(D)==S and sorted(abs(y-x) for x,y in zip(D,D[1:]))==list(range(1,M))
    good&=any(D[j:j+3]==[0,a,M+1] for j in range(M-2))
    # lift independently: delta from D shifted to start at 0
    E=[x-D[0] for x in D]; delta=[E[i+1]-E[i] for i in range(M-1)]
    W=delta+[M]+[-x for x in delta[::-1]]+[-M]
    for i in range(len(W)-1):
        if W[i]<0 and W[i+1]<0 and sorted([-W[i],-W[i+1]])==[a,b]: W=W[:i]+[-(M+1)]+W[i+2:];break
    v=0;V=[0]
    for x in W[:-1]: v+=x;V.append(v)
    good&= sorted(x for x in W if x>0)==list(range(1,M+1)) and sorted(-x for x in W if x<0)==sorted(set(range(1,M+2))-{a,b})
    good&= len(set(V))==len(V) and v+W[-1]==0 and max(V)-min(V)<=2*M+2
    ok+=good
print(ok,"/",len(C),"B certificates give valid tight cycles (own lift)")
