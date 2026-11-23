"""Two-cluster lemma test. W=(H1, +c, X, -d), c=maxP>=d=maxN. Vertices of H1 in cluster 0, X in cluster d.
Equivalent: closed walk in a window of length d (d consecutive integers): arc A from 0 (self-avoiding), virtual
step +Delta (Delta=c-d), arc B (self-avoiding, may meet A) ending at 0; uses P\{c} as +, N\{d} as -.
Range of the resulting ordering <= 2d-1 <= maxP+maxN-1."""
import sys, random, time
def solve(P,N,tl=20):
    P=sorted(P);N=sorted(N)
    if max(N)>max(P): P,N=N,P   # negate the whole problem
    c=P[-1];d=N[-1];Delta=c-d
    steps=[x for x in P[:-1]]+[-x for x in N[:-1]]
    n=len(steps);t0=time.time()
    used=[False]*n
    def rec(v,phase,vis,lo,hi,k,path):
        if time.time()-t0>tl: raise TimeoutError
        if k==n:
            if phase==1 and v==0: return path
            if phase==0:
                # switch then must be at 0 already
                w=v+Delta
                if w==0 and max(hi,w)-min(lo,w)<=d-1: return path+['|']
            return None
        if phase==0:
            w=v+Delta
            nlo,nhi=min(lo,w),max(hi,w)
            if nhi-nlo<=d-1:
                r=rec(w,1,{w},nlo,nhi,k,path+['|'])
                if r: return r
        tried=set()
        for i in range(n):
            if used[i] or steps[i] in tried: continue
            tried.add(steps[i])
            w=v+steps[i]
            last=(k==n-1)
            if w in vis and not (phase==1 and last and w==0 and False): 
                if not(phase==1 and last and w==0 and 0 not in vis): continue
            nlo,nhi=min(lo,w),max(hi,w)
            if nhi-nlo>d-1: continue
            used[i]=True
            r=rec(w,phase,vis|{w},nlo,nhi,k+1,path+[steps[i]])
            used[i]=False
            if r: return r
        return None
    try: return rec(0,0,{0},0,0,0,[])
    except TimeoutError: return 'TO'
def build(P,N,path):
    P=sorted(P);N=sorted(N);neg=False
    if max(N)>max(P): P,N=N,P;neg=True
    c=P[-1];d=N[-1];i=path.index('|')
    H1=path[:i];G=path[i+1:]
    W=H1+[c]+G+[-d]
    if neg: W=[-x for x in W]
    return W
def valid(W,P,N):
    if sorted(x for x in W if x>0)!=sorted(P) or sorted(-x for x in W if x<0)!=sorted(N): return False
    v=0;S=[0]
    for x in W[:-1]: v+=x;S.append(v)
    return len(set(S))==len(S) and v+W[-1]==0, max(S)-min(S)
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="tight":
        for M in range(4,int(sys.argv[2])+1):
            row=[]
            for a in range(1,(M+1)//2+1):
                if 2*a==M+1: continue
                P=list(range(1,M+1));N=sorted(set(range(1,M+2))-{a,M+1-a})
                r=solve(P,N)
                if r in (None,'TO'): row.append(f"a{a}:{r}")
                else:
                    W=build(P,N,r);row.append(f"a{a}:{valid(W,P,N)}")
            print("M",M," ".join(row),flush=True)
