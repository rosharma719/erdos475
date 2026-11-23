"""Structured LR: path = k -> Z (greedy inward zigzag from extreme e on S=[0,M-1]\\{k,k+1,k+a}, stop when next
length <= a) -> Walecki zigzag on the leftover interval I (junction = last vertex of Z)."""
import sys
def wal(lo,hi,start):
    out=[];l,h=lo,hi;low=(start==lo)
    while l<=h:
        if low: out.append(l);l+=1
        else: out.append(h);h-=1
        low=not low
    return out
def try1(M,a,k,e):
    b=M+1-a; S=sorted(set(range(M))-{k,k+1,k+a}); lo,hi=0,len(S)-1
    Z=[];take_hi=(e==M-1)
    while lo<=hi:
        v=S[hi] if take_hi else S[lo]
        if Z and abs(v-Z[-1])<=a: break
        Z.append(v); 
        if take_hi: hi-=1
        else: lo+=1
        take_hi=not take_hi
    rest=S[lo:hi+1]; J=Z[-1]
    I=sorted(rest+[J])
    if I!=list(range(I[0],I[-1]+1)) or len(I)!=a or J not in (I[0],I[-1]): return None
    p=[k]+Z+wal(I[0],I[-1],J)[1:]
    L=sorted(abs(y-x) for x,y in zip(p,p[1:]))
    if L==[x for x in range(1,M) if x not in (a,b)] and len(set(p))==M-2: return p
    return None
if __name__=="__main__":
    for M in range(int(sys.argv[1]),int(sys.argv[2])):
        row=[]
        for a in range(2,M//2+1):
            sols=[(k,e) for k in range(0,M-a) for e in (0,M-1) if try1(M,a,k,e)]
            row.append(f"{a}:{sols[0] if sols else '-'}")
        print(M,' '.join(row))
