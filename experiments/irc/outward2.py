"""Two-cluster, arcs are outward walks from EITHER end. W=(A,+c,B,-d); arcs A: 0->e1, B: e1+Delta->0.
Valid if V(A), V(B) self-avoiding, V(A) ∩ (V(B)+d) = ∅, total range <= R (Graham: c+d, +1 if odd)."""
import sys, random, time, itertools
def outward_seqs(pool, maxspread, t0, tl):
    """generate (seq, vertices) outward walks from 0 using a sub-multiset of pool (list of signed ints),
    each walk maximal? no: all walks; yields (used_mask, seq, vertexlist)."""
    n=len(pool)
    def rec(mask,v,lo,hi,seq,verts):
        if time.time()-t0>tl: raise TimeoutError
        yield mask,seq,verts
        tried=set()
        for i in range(n):
            if mask>>i&1 or pool[i] in tried: continue
            tried.add(pool[i]);s=pool[i];w=v+s
            if lo==hi: nlo,nhi=min(lo,w),max(hi,w)
            elif v==hi:
                if s>0: nlo,nhi=lo,w
                elif w<lo: nlo,nhi=w,hi
                else: continue
            else:
                if s<0: nlo,nhi=w,hi
                elif w>hi: nlo,nhi=lo,w
                else: continue
            if nhi-nlo>maxspread: continue
            yield from rec(mask|1<<i,w,nlo,nhi,seq+[s],verts+[w])
    yield from rec(0,0,0,0,[],[0])
def solve(P,N,tl=20):
    P=sorted(P);N=sorted(N);neg=False
    if max(N)>max(P): P,N=N,P;neg=True
    c=P[-1];d=N[-1];Delta=c-d;R=c+d+((c+d)%2)
    T=[x for x in P[:-1]]+[-x for x in N[:-1]];n=len(T);full=(1<<n)-1
    t0=time.time()
    # arc candidates: for A from 0 outward (orientation 0) uses steps T; outward-from-end uses -T (reversed)
    try:
        for oa in (0,1):
            poolA=T if oa==0 else [-x for x in T]
            for maskA,seqA,vA in outward_seqs(poolA,R,t0,tl):
                if maskA==0 or maskA==full: continue
                if oa==0: A=seqA; VA=vA; e1=sum(A)
                else:
                    e1=-sum(seqA); A=[-x for x in seqA[::-1]]; VA=[e1+x for x in vA]
                rest=[T[i] for i in range(n) if not maskA>>i&1]
                for ob in (0,1):
                    # B: from e1+Delta to 0. ob=0: outward from its end 0: Btilde = rev-neg(B) outward from 0 using -rest
                    poolB=[-x for x in rest] if ob==0 else rest
                    m=len(poolB);fullB=(1<<m)-1
                    for maskB,seqB,vB in outward_seqs(poolB,R,t0,tl):
                        if maskB!=fullB: continue
                        if ob==0:
                            B=[-x for x in seqB[::-1]]; VB=vB
                            if -sum(seqB)!=e1+Delta: continue   # Btilde ends at start of B
                        else:
                            B=seqB; s0=e1+Delta
                            if s0+sum(B)!=0: continue
                            VB=[s0+x for x in vB]
                        SA=set(VA);SB=set(VB)
                        if len(SA)<len(VA) or len(SB)<len(VB): continue
                        if 0 in SB and VB[-1]!=0: pass
                        if any((x+d) in SA for x in SB): continue
                        allv=VA+[x+d for x in VB]
                        if max(allv)-min(allv)>R: continue
                        W=A+[c]+B+[-d]
                        return [-x for x in W] if neg else W
    except TimeoutError: return 'TO'
    return None
def valid(W,P,N):
    if sorted(x for x in W if x>0)!=sorted(P) or sorted(-x for x in W if x<0)!=sorted(N): return (False,0)
    v=0;S=[0]
    for x in W[:-1]: v+=x;S.append(v)
    return (len(set(S))==len(S) and v+W[-1]==0, max(S)-min(S))
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="tight":
        for M in range(4,int(sys.argv[2])+1):
            row=[]
            for a in range(1,(M+1)//2+1):
                if 2*a==M+1: continue
                P=list(range(1,M+1));N=sorted(set(range(1,M+2))-{a,M+1-a})
                r=solve(P,N)
                row.append(f"a{a}:"+(str(r) if r in (None,'TO') else str(valid(r,P,N))))
            print("M",M," ".join(row),flush=True)
    else:
        random.seed(int(sys.argv[3]));H=int(sys.argv[2]);st={'ok':0,'none':0,'to':0,'bad':0};nones=[]
        for _ in range(int(sys.argv[4])):
            while True:
                P=sorted(random.sample(range(1,H+1),random.randint(H//2,H)))
                N=sorted(random.sample(range(1,H+1),random.randint(H//2,H)))
                if sum(P)==sum(N) and P!=N: break
            r=solve(P,N)
            if r=='TO': st['to']+=1
            elif r is None: st['none']+=1; nones.append((P,N))
            else: st['ok' if valid(r,P,N)[0] else 'bad']+=1
        print(st)
        for x in nones[:5]: print("NONE",x)
