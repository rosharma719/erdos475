"""Half-walk construction for the tight pair P=[1,M], N=[1,M+1]\{a,b} (a+b=M+1):
W=(delta, M, -delta^rev, -M), delta a signed ordering of [1..M-1] with partial sums D (D_0=0) distinct,
D ∩ (D+M) = ∅, containing consecutive (+a,+b) or (+b,+a); contract the mirrored (-b,-a) to -(M+1).
Find delta with spread(D) <= W (W=M+1 -> range 2M+1; W=M+2 -> range 2M+2)."""
import sys
def find(M,a,spread):
    b=M+1-a; labels=list(range(1,M))
    sys.setrecursionlimit(10000)
    best=None
    def rec(D,used,pairdone,lo,hi):
        k=len(D)
        if k==M:
            return D if pairdone else None
        x=D[-1]
        for L in sorted(set(labels)-used,reverse=True):
            for sgn in (1,-1):
                y=x+sgn*L
                if y in Dset or (y-M) in Dset or (y+M) in Dset: continue
                nlo,nhi=min(lo,y),max(hi,y)
                if nhi-nlo>spread: continue
                # pair condition: consecutive ascending a,b
                pd=pairdone
                if sgn>0 and len(D)>=2 and D[-1]-D[-2] in (a,b) and L==(a+b)-(D[-1]-D[-2]): pd=True
                Dset.add(y);used.add(L);D.append(y)
                r=rec(D,used,pd,nlo,nhi)
                if r: return r
                D.pop();used.discard(L);Dset.discard(y)
        return None
    Dset={0}
    return rec([0],set(),False,0,0)
def check(M,a,D):
    b=M+1-a
    delta=[D[i+1]-D[i] for i in range(len(D)-1)]
    W=delta+[M]+[-x for x in delta[::-1]]+[-M]
    # contract consecutive (-b,-a) or (-a,-b)
    for i in range(len(W)-1):
        if sorted([-W[i],-W[i+1]])==sorted([a,b]) and W[i]<0 and W[i+1]<0:
            W=W[:i]+[-(M+1)]+W[i+2:];break
    else: return None
    P=sorted(x for x in W if x>0);N=sorted(-x for x in W if x<0)
    assert P==list(range(1,M+1)) and N==sorted(set(range(1,M+2))-{a,b}),(P,N)
    v=0;seen=[0]
    for x in W[:-1]: v+=x;seen.append(v)
    assert len(set(seen))==len(seen) and v+W[-1]==0
    return max(seen)-min(seen)
for spread in (int(sys.argv[1]),):
  for M in range(4,int(sys.argv[2])+1):
    row=[]
    for a in range(1,(M+1)//2+1):
        b=M+1-a
        if a>=b: continue
        D=find(M,a,M+spread)
        row.append(f"a={a}:{check(M,a,D) if D else '-'}")
    print("M",M," ".join(row),flush=True)
