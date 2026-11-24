import sys
def zig(n,lowskip,highskip):
    sk=set(lowskip)|set(highskip); tot=n+1-len(sk)
    lows=[x for x in range(n+1) if x not in sk]; highs=[x for x in range(n,-1,-1) if x not in sk]
    path=[];used=set();i=j=0;turn=0
    while True:
        if turn==0:
            while i<len(lows) and lows[i] in used: i+=1
            if i==len(lows): break
            v=lows[i]; i+=1
        else:
            while j<len(highs) and highs[j] in used: j+=1
            if j==len(highs): break
            v=highs[j]; j+=1
        if v in used: break
        path.append(v);used.add(v);turn^=1
        if len(path)==tot: break
    return path
def valid(P,M,a):
    n=M-1;b=M+1-a
    if len(set(P))!=len(P) or min(P)!=0 or max(P)>n or len(P)!=M-1: return False
    L=sorted(abs(P[i+1]-P[i]) for i in range(len(P)-1))
    return L==sorted(set(range(1,n+1))-{b}) and P[0]==a and P[1]==0
def family(M,a):
    n=M-1;out=[]
    for h in range(1,n):
        if h in (a,n-1): continue
        for D in ([n-1],):
            Z=zig(n,{a,h},{h}|set(D))
            if set(Z)|{a}|set(D)!=set(range(n+1))-{h}: continue
            for k in range(1,len(Z)+1):
                P=[a]+Z[:k]+D+Z[k:]
                if valid(P,M,a): out.append((h,k))
    return out
res={}
for a in range(3,9):
    for M in range(2*a+2,2*a+40):
        f=family(M,a); res[(M,a)]=f
miss=[k for k,v in res.items() if not v]
print("missing:",miss[:30],len(miss),"of",len(res))
for a in range(3,6):
    print(a,[(M,res[(M,a)][:2]) for M in range(2*a+2,2*a+22)])
