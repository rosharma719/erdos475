"""Independent audit of GPT's H_k proof (own implementation from the stated formulas)."""
def B(s): return set(range(-s,0))|set(range(2,s+2))
def L(p): return sorted(abs(p[i+1]-p[i]) for i in range(len(p)-1))
seedF={3:[2,-1,3,-2,4,-3],4:[3,-2,2,-1,5,-4,4,-3],5:[4,-4,3,-2,2,-1,5,-5,6,-3]}
seedT={4:[-4,-1,4,2,-2,5,-3,3],5:[-5,-2,2,4,-1,5,-3,6,-4,3],6:[-6,-2,3,-5,7,-4,6,-3,4,2,-1,5]}
seedC={3:[-2,3,-1,2,4,-3],4:[-3,-1,4,-2,2,5,-4,3],5:[-4,5,-3,-1,4,-2,2,-5,6,3]}
seedD={4:[-2,4,-4,5,2,-3,-1,3],5:[-3,4,-1,-4,2,-2,6,-5,5,3],6:[-4,5,-5,-3,4,-2,6,-6,7,2,-1,3]}
def Q_ok(s,d,e,p): return p[0]==e and len(p)==2*s and set(p)==B(s) and L(p)==[x for x in range(2,2*s+2) if x!=d]
def F(s): return seedF[s] if s in seedF else [s-1,-s+2,s,-s+1,s+1,-s]+F(s-3)
def T(s): return seedT[s] if s in seedT else [-s,s,-s+3,s-2,-s+2,s+1,s-1,-s+1]+F(s-4)
def Cc(s): return seedC[s] if s in seedC else [-s+1,s,-s+2,s-1,s+1,-s]+F(s-3)
def Dd(s): return seedD[s] if s in seedD else [-s+2,s-2,-s+3,s,-s,s+1,s-1,-s+1]+F(s-4)
bad=0
for s in range(3,1500):
    bad+= not Q_ok(s,2,s-1,F(s)); bad+= not Q_ok(s,2*s,-s+1,Cc(s))
    if s>=4: bad+= not Q_ok(s,2*s+1,-s,T(s)); bad+= not Q_ok(s,2*s-1,-s+2,Dd(s))
print("generalized states F,T,C,D for s<=1499: failures",bad)
base={2:[3,-2,2,-1,-3],3:[4,-3,-1,-4,2,-2,3],4:[5,-4,4,-2,3,-1,2,-5,-3],5:[6,-5,5,-4,-6,2,-1,3,-2,4,-3],
6:[7,-6,6,-5,5,-3,-7,2,-1,4,-2,-4,3],7:[8,-7,7,-6,6,-5,4,-4,-8,2,-1,-3,3,-2,5],8:[9,-8,8,-7,7,-6,6,-5,5,-4,4,2,-1,3,-2,-9,-3],
9:[10,-9,9,-8,8,-7,7,-6,6,-5,5,-4,-10,-2,3,-1,2,4,-3],10:[11,-10,10,-9,9,-8,8,-7,7,-6,6,-5,5,-3,4,2,-4,-1,3,-2,-11]}
def H(k):
    if k in base: return base[k]
    if k%3==0: s=k//3; Q=Cc(s)
    elif k%3==1: s=(k-1)//3; Q=T(s)
    else: s=(k+1)//3; Q=Dd(s)
    Z=[]
    for t in range(k+1,s+1,-1): Z+=[t,-(t-1)]
    return Z+[-k-1]+Q
def H_ok(k,p): return p[0]==k+1 and len(p)==2*k+1 and set(p)==set(range(-k-1,0))|set(range(2,k+2)) and L(p)==list(range(2,2*k+2))
print("H_k failures k=2..3000:",sum(not H_ok(k,H(k)) for k in range(2,3001)))
# end-to-end: tight pair M=4k+2, a=2, c=1 half-walk (aligned ladder), own lift
def tight(k):
    M=4*k+2; q=M+1; D=[0,2,q]
    for i in range(k):
        D.append(M-2-2*i)
        if i+1<k: D.append(q+2*(i+1))
    D+= [2*x for x in H(k)[1:]]
    d=[D[i+1]-D[i] for i in range(M-1)]
    W=d+[1]+[-x for x in d[::-1]]+[-1]
    i=next(i for i in range(len(W)-1) if W[i]<0 and W[i+1]<0 and sorted([-W[i],-W[i+1]])==[2,M-1])
    W=W[:i]+[-(M+1)]+W[i+2:]
    v=0;S=[0]
    for x in W[:-1]: v+=x;S.append(v)
    return (sorted(x for x in W if x>0)==list(range(1,M+1)) and sorted(-x for x in W if x<0)==sorted(set(range(1,M+2))-{2,M-1})
            and len(set(S))==len(S) and v+W[-1]==0 and max(S)-min(S)<=2*M+2)
print("tight (M=4k+2, a=2) end-to-end failures k=2..400:",sum(not tight(k) for k in range(2,401)))
