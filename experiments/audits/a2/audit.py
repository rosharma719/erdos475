import json
C={int(k):v for k,v in json.load(open('a2/certs.json')).items()}
bad=[]
for M,path in sorted(C.items()):
    a=2;b=M-1
    ok=len(path)==M and len(set(path))==M and path[:2]==[0,b]
    d=[path[i+1]-path[i] for i in range(M-1)]
    ok&= sorted(abs(x) for x in d)==[x for x in range(1,M+1) if x!=2]
    S=set(path); ok&= not any(x+2 in S for x in S) and max(S)-min(S)<=2*M
    W=d+[2]+[-x for x in d[::-1]]+[-2]
    assert W[-2:]==[-b,-2]; W=W[:-2]+[-(M+1)]
    v=0;V=[0]
    for x in W[:-1]: v+=x;V.append(v)
    ok&= sorted(x for x in W if x>0)==list(range(1,M+1)) and sorted(-x for x in W if x<0)==sorted(set(range(1,M+2))-{2,b})
    ok&= len(set(V))==len(V) and v+W[-1]==0 and max(V)-min(V)<=2*M+2
    if not ok: bad.append(M)
print("certificates:",len(C),"invalid:",bad, "Ms:",sorted(C)[:5],"...",sorted(C)[-5:])
