"""Junction variant: W=(delta, b, -delta^rev, -b), delta = signed ordering of [1..M]\{b} with delta_1=+a.
Last two steps (-a,-b) are consecutive negatives -> contract to -(M+1): tight pair P=[1,M], N=[1,M+1]\{a,b}.
Valid iff D distinct and D ∩ (D+b) = ∅. Range = b + spread(D); Graham needs range <= 2M+2 (IRC: <= 2M)."""
import sys
def find(M,a,maxrange):
    b=M+1-a; labs=[x for x in range(1,M+1) if x!=b]; spread=maxrange-b
    D=[0,a]; Ds={0,a}
    if a-0==b: return None
    def ok(y): return y not in Ds and (y-b) not in Ds and (y+b) not in Ds
    if not ok(a) and False: pass
    used={a}
    def rec(lo,hi):
        if len(D)==M: return list(D)
        x=D[-1]
        for L in sorted(set(labs)-used,reverse=True):
            for s in (1,-1):
                y=x+s*L
                if not ok(y): continue
                nlo,nhi=min(lo,y),max(hi,y)
                if nhi-nlo>spread: continue
                D.append(y);Ds.add(y);used.add(L)
                r=rec(nlo,nhi)
                if r: return r
                D.pop();Ds.discard(y);used.discard(L)
        return None
    if a==b or (a in (b,-b)): return None
    return rec(0,a)
def verify(M,a,D):
    b=M+1-a; delta=[D[i+1]-D[i] for i in range(len(D)-1)]
    W=delta+[b]+[-x for x in delta[::-1]]+[-b]
    assert W[-2:]==[-a,-b]
    W=W[:-2]+[-(M+1)]
    P=sorted(x for x in W if x>0);N=sorted(-x for x in W if x<0)
    assert P==list(range(1,M+1)) and N==sorted(set(range(1,M+2))-{a,b}),(M,a,P,N)
    v=0;S=[0]
    for x in W[:-1]: v+=x;S.append(v)
    assert len(set(S))==len(S) and v+W[-1]==0
    return max(S)-min(S)
mr=sys.argv[1]
for M in range(4,int(sys.argv[2])+1):
    row=[]
    for a in range(1,(M+1)//2+1):
        if 2*a==M+1: continue
        lim=2*M+2 if mr=='g' else 2*M
        D=find(M,a,lim)
        row.append(f"a={a}:{verify(M,a,D) if D else '-'}")
    print("M",M," ".join(row),flush=True)
