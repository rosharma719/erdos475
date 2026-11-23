"""Two-cluster lemma, relaxed: W=(H1,+c,X,-d) with c=maxP>=d=maxN; arcs A (cluster 0) and B=X-d (cluster d).
Need: A self-avoiding, B self-avoiding, V(A) ∩ (V(B)+d) = ∅, overall range <= R, R = maxP+maxN (+1 if odd)  [Graham-sufficient]."""
import sys, random, time
def solve(P,N,tl=10):
    P=sorted(P);N=sorted(N)
    if max(N)>max(P): P,N=N,P
    c=P[-1];d=N[-1];Delta=c-d
    R=c+d+(1 if (c+d)%2 else 0)
    steps=sorted([x for x in P[:-1]]+[-x for x in N[:-1]],key=lambda x:-abs(x))
    n=len(steps);t0=time.time();used=[False]*n
    A=set();B=set()
    def span(lo,hi): return hi-lo
    def rec(v,phase,k,lo,hi,path):
        # lo,hi = bounds of actual vertices: A-vertices as is, B-vertices +d
        if time.time()-t0>tl: raise TimeoutError
        if k==n:
            if phase==0:
                w=v+Delta
                if w==0 and (w+d) not in A and w not in B: return path+['|']
                return None
            return path if v==0 else None
        if phase==0:
            w=v+Delta
            if (w+d) not in A and w!=0 and max(hi,w+d)-min(lo,w+d)<=R:
                B.add(w);r=rec(w,1,k,min(lo,w+d),max(hi,w+d),path+['|']);B.discard(w)
                if r: return r
        tried=set()
        for i in range(n):
            if used[i] or steps[i] in tried: continue
            tried.add(steps[i]);w=v+steps[i]
            if phase==0:
                if w in A or (w-d) in B: continue
                nlo,nhi=min(lo,w),max(hi,w)
            else:
                last=(k==n-1)
                if w in B or (w==0 and not last) or (w+d) in A: continue
                if last and w!=0: continue
                nlo,nhi=min(lo,w+d),max(hi,w+d)
            if nhi-nlo>R: continue
            used[i]=True
            (A if phase==0 else B).add(w)
            r=rec(w,phase,k+1,nlo,nhi,path+[steps[i]])
            (A if phase==0 else B).discard(w)
            used[i]=False
            if r: return r
        return None
    A.add(0)
    try: return rec(0,0,0,0,0,[])
    except TimeoutError: return 'TO'
def build(P,N,path):
    P=sorted(P);N=sorted(N);neg=False
    if max(N)>max(P): P,N=N,P;neg=True
    c=P[-1];d=N[-1];i=path.index('|')
    W=path[:i]+[c]+path[i+1:]+[-d]
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
                row.append(f"a{a}:"+(str(r) if r in (None,'TO') else str(valid(build(P,N,r),P,N))))
            print("M",M," ".join(row),flush=True)
    else:
        random.seed(int(sys.argv[3]))
        H=int(sys.argv[2]);stats={'ok':0,'none':0,'to':0,'bad':0}
        for trial in range(int(sys.argv[4])):
            while True:
                k=random.randint(H//2,H)
                P=sorted(random.sample(range(1,H+1),k));
                # random N with same sum: sample then adjust via retries
                N=sorted(random.sample(range(1,H+1),random.randint(H//2,H)))
                if sum(P)==sum(N) and P!=N: break
            r=solve(P,N)
            if r=='TO': stats['to']+=1
            elif r is None: stats['none']+=1; print("NONE",P,N,flush=True)
            else:
                ok,rg=valid(build(P,N,r),P,N); stats['ok' if ok else 'bad']+=1
        print(stats)
