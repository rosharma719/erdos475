import sys
def build(M):
    V=set(range(-M+1,M+1))-{M-1}
    f={}
    for s in V:
        f[s]=2*s+M if s<=0 else (2*s-M-3 if s%2==0 else 2*s-M+1)
    return V,f
def cycles(M):
    V,f=build(M)
    assert set(f.values())==V
    P=sorted(f[s]-s for s in V if f[s]>s);N=sorted(s-f[s] for s in V if f[s]<s)
    assert P==list(range(1,M+1)) and N==list(range(2,M))+[M+1],M
    assert all((s<=0)==(f[s]>s) for s in V)
    seen=set();L=[]
    for s in sorted(V):
        if s in seen: continue
        c=0;x=s
        while x not in seen: seen.add(x);x=f[x];c+=1
        L.append(c)
    return sorted(L)
one=[];multi=[]
for M in range(4,601,2):
    L=cycles(M)
    (one if len(L)==1 else multi).append((M,L))
print("permutation+steps+sign OK for all even M<=600")
print("one-cycle M:",[m for m,_ in one])
print("multi:",[(m,l[:6]) for m,l in multi][:40],"count multi",len(multi),"of",len(one)+len(multi))
# M=20 certificate
V,f=build(20);x=0;st=[]
for _ in range(39): st.append(f[x]-x);x=f[x]
print(x==0,st)
