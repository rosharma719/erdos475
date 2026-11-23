"""Junction half-walk with c=a: W=(delta,+a,-delta^rev,-a), delta = signed ordering of [1..M]\{a} with delta_1=+b.
The final steps (-b,-a) merge to -(M+1). Need D distinct, D∩(D+a)=∅, range a+spread(D) <= 2M+2."""
import sys,time
def find(M,a,tl=20):
    b=M+1-a; labs=[x for x in range(1,M+1) if x not in (a,b)]
    D=[0,b];S={0,b};used=set();t0=time.time();spr=2*M+2-a
    def ok(y): return y not in S and y-a not in S and y+a not in S
    def rec(lo,hi):
        if time.time()-t0>tl: raise TimeoutError
        if len(used)==len(labs): return list(D)
        x=D[-1]
        for L in sorted(set(labs)-used,reverse=True):
            for s in (1,-1):
                y=x+s*L
                if not ok(y): continue
                nlo,nhi=min(lo,y),max(hi,y)
                if nhi-nlo>spr: continue
                D.append(y);S.add(y);used.add(L)
                r=rec(nlo,nhi)
                if r: return r
                D.pop();S.discard(y);used.discard(L)
        return None
    try: return rec(0,b)
    except TimeoutError: return 'TO'
def check(M,a,D):
    b=M+1-a;d=[D[i+1]-D[i] for i in range(M-1)]
    W=d+[a]+[-x for x in d[::-1]]+[-a]
    assert W[-2:]==[-b,-a]; W=W[:-2]+[-(M+1)]
    v=0;V=[0]
    for x in W[:-1]: v+=x;V.append(v)
    ok=sorted(x for x in W if x>0)==list(range(1,M+1)) and sorted(-x for x in W if x<0)==sorted(set(range(1,M+2))-{a,b}) and len(set(V))==len(V) and v+W[-1]==0
    return ok,max(V)-min(V)
a=int(sys.argv[1])
for M in map(int,sys.argv[2].split(',')):
    D=find(M,a)
    print(M,a,D if D in (None,'TO') else (check(M,a,D),D),flush=True)
