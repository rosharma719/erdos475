import sys,time
def search_c1(M,a,tl=30):
    b=M+1-a; rem=[k for k in range(2,M+1) if k not in (a,b)]
    path=[0,a,M+1]; t0=time.time(); used=set()
    def rec(s,lo,hi):
        if time.time()-t0>tl: raise TimeoutError
        if len(used)==len(rem): return list(path)
        for k in sorted(set(rem)-used,reverse=True):
            for e in (1,-1):
                t=s+e*k
                if any(abs(t-u)<=1 for u in path): continue
                nlo,nhi=min(lo,t),max(hi,t)
                if nhi-nlo+1>2*M+2: continue
                path.append(t);used.add(k)
                r=rec(t,nlo,nhi)
                if r: return r
                path.pop();used.discard(k)
        return None
    try: return rec(M+1,0,M+1)
    except TimeoutError: return 'TO'
def lift(M,a,D):
    delta=[D[i+1]-D[i] for i in range(M-1)];b=M+1-a
    W=delta+[1]+[-x for x in delta[::-1]]+[-1]
    for i in range(len(W)-1):
        if W[i]<0 and W[i+1]<0 and sorted([-W[i],-W[i+1]])==[a,b]: W=W[:i]+[-(M+1)]+W[i+2:];break
    v=0;S=[0]
    for x in W[:-1]: v+=x;S.append(v)
    ok=sorted(x for x in W if x>0)==list(range(1,M+1)) and sorted(-x for x in W if x<0)==sorted(set(range(1,M+2))-{a,b}) and len(set(S))==len(S) and v+W[-1]==0
    return ok,max(S)-min(S)
for M in map(int,sys.argv[1].split(',')):
    for a in map(int,sys.argv[2].split(',')):
        D=search_c1(M,a)
        print(M,a, D if D in (None,'TO') else lift(M,a,D),flush=True)
