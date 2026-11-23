# independent audit: scaled escape family + scaffold uniqueness at M=16
import itertools
def valid(steps,P,N):
    if sorted(x for x in steps if x>0)!=sorted(P) or sorted(-x for x in steps if x<0)!=sorted(N): return None
    v=0;seen=set();V=[]
    for d in steps:
        if (v<=0)!=(d>0) or v in seen: return None
        seen.add(v);V.append(v);v+=d
    return V if v==0 else None
bad=0
for L in range(4,400):
    P=[3]+[L*j for j in range(1,8)];N=[1,2]+[L*j for j in range(1,8)]
    c=[2,-3,5,-1,-7,0,3,7,-2,-4,-6,1,6,0,-5,4,0];o=[0,0,0,0,0,3,0,0,0,0,0,0,0,-1,0,0,-2]
    st=[L*a+b for a,b in zip(c,o)]
    V=valid(st,P,N)
    if V is None or max(V)-min(V)>max(P)+max(N)-1: bad+=1
print("scaled family L=4..399 failures:",bad)
for L in (1,2,3):
    P=[3]+[L*j for j in range(1,8)];N=[1,2]+[L*j for j in range(1,8)]
    print("L",L,"sets distinct?",len(set(P))==len(P) and len(set(N))==len(N))
# scaffold: positive map fixed f(s)=2s+M on s<=0 (s>=-M+1), holes -M and M-1; count bijections of positive sources
M=16;N=list(range(2,M))+[M+1]
src=[s for s in range(1,M+1) if s!=M-1]
tg=set(range(-M+1,M+1))-{M-1}-{2*s+M for s in range(-M+1,1)}
sols=[]
def rec(i,used,assign):
    if i==len(src): sols.append(dict(assign));return
    s=src[i]
    for n in N:
        if n in used: continue
        t=s-n
        if t in tg and t not in assign.values():
            assign[s]=t;used.add(n);rec(i+1,used,assign);used.discard(n);del assign[s]
rec(0,set(),{})
print("scaffold M=16 bijections:",len(sols))
