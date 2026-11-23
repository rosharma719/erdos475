"""Two-cluster with OUTWARD arcs: W=(A,+c,B,-d), c=maxP>=d=maxN; A and B~ (reverse-negated B) are outward walks from 0
(every new vertex is a new max or new min). Require spread(V(A) ∪ V(B)) <= d-1 => valid, range <= 2d-1."""
import sys, random, time
def outward_walks(steps, L, tl):
    """yield (A,B~) partitions; steps: list of signed ints; both outward from 0; union spread <= L."""
    n=len(steps); t0=time.time()
    used=[False]*n
    # build A then Btilde (Btilde uses negated remaining steps)
    def walk(seq_id, v, lo, hi, glo, ghi, A, Bt, k):
        if time.time()-t0>tl: raise TimeoutError
        if k==n: return (A,Bt)
        tried=set()
        for i in range(n):
            if used[i]: continue
            s=steps[i] if seq_id==0 else -steps[i]
            if (s,seq_id) in tried: continue
            tried.add((s,seq_id))
            w=v+s
            if v==hi and v==lo: nlo,nhi=min(lo,w),max(hi,w)
            elif v==hi:
                if s>0: nlo,nhi=lo,w
                elif w<lo: nlo,nhi=w,hi
                else: continue
            else:
                if s<0: nlo,nhi=w,hi
                elif w>hi: nlo,nhi=lo,w
                else: continue
            g1,g2=min(glo,nlo),max(ghi,nhi)
            if g2-g1>L: continue
            used[i]=True
            r=walk(seq_id,w,nlo,nhi,g1,g2,A+[s] if seq_id==0 else A,Bt+[s] if seq_id==1 else Bt,k+1)
            used[i]=False
            if r: return r
        if seq_id==0 and k<n:
            # switch to building Btilde
            return walk(1,0,0,0,glo,ghi,A,Bt,k)
        return None
    return walk(0,0,0,0,0,0,[],[],0)
def solve(P,N,tl=10):
    P=sorted(P);N=sorted(N);neg=False
    if max(N)>max(P): P,N=N,P;neg=True
    c=P[-1];d=N[-1]
    steps=[x for x in P[:-1]]+[-x for x in N[:-1]]
    try: r=outward_walks(steps,d-1,tl)
    except TimeoutError: return 'TO'
    if not r: return None
    A,Bt=r; B=[-x for x in Bt[::-1]]
    W=A+[c]+B+[-d]
    return [-x for x in W] if neg else W
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
        print(st); 
        for x in nones[:5]: print("NONE",x)
