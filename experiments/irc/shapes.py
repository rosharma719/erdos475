# search structured ruler orders (shapes) that give a zigzag for every M (a=1 tight family)
import itertools, sys
def merge_ok(sig,tau):
    X=Y=i=j=0;seen={0};T=len(sig)+len(tau)
    for k in range(T):
        if k and X==Y: return False
        if X<=Y:
            if i>=len(sig): return False
            X+=sig[i];i+=1
        else:
            if j>=len(tau): return False
            Y+=tau[j];j+=1
        if k<T-1:
            d=X-Y
            if d in seen: return False
            seen.add(d)
    return X==Y
def shapes(S):
    S=sorted(S);out={}
    n=len(S)
    out['inc']=S; out['dec']=S[::-1]
    od=[x for x in S if x%2]; ev=[x for x in S if x%2==0]
    for a_,A in (('o',od),('e',ev)):
        for b_,B in (('o',od),('e',ev)):
            if a_==b_: continue
            for da in (1,-1):
                for db in (1,-1):
                    out[f'{a_}{"+" if da>0 else "-"}{b_}{"+" if db>0 else "-"}']=A[::da]+B[::db]
    # interleave big/small: alternate from ends
    lo,hi=0,n-1;z=[];t=0
    while lo<=hi:
        if t%2==0: z.append(S[hi]);hi-=1
        else: z.append(S[lo]);lo+=1
        t+=1
    out['hilo']=z; out['lohi']=[S[i] for i in range(0)] or z[::-1]
    return out
res={}
Ms=range(4,41)
for M in Ms:
    P=list(range(1,M+1));N=list(range(2,M))+[M+1]
    sp=shapes(P);sn=shapes(N)
    for a,s in sp.items():
        for b,t in sn.items():
            # also try rotations of tau by 1 and moving max to front/back
            for tv,tn in ((t,'') ,(t[1:]+t[:1],'rot'),(t[-1:]+t[:-1],'rotb')):
                key=(a,b+tn)
                res.setdefault(key,[]).append(M if merge_ok(s,tv) else None)
best=sorted(res.items(),key=lambda kv:-sum(x is not None for x in kv[1]))[:12]
for k,v in best: print(k,[m for m in v if m])
