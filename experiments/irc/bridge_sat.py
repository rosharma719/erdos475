"""Core-plus-bridge for the tight pair with general a: W = (delta, +M, -delta^rev, bridge), where the bridge is a
permutation of {+a,+b,-M,-(M+1)} (sum 0, starting from vertex M). delta = directed path from 0 with labels [1,M-1]\{a,b}.
Constraints: D distinct, D ∩ (D+M) = ∅, bridge vertices avoid D ∪ (M+D), total range <= 2M+2. Exact SAT."""
import sys,itertools,time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def solve(M,a,bridge,timeout=30):
    b=M+1-a; labels=[L for L in range(1,M) if L not in (a,b)]
    Bv=[];v=M
    for x in bridge[:-1]: v+=x;Bv.append(v)
    if v+bridge[-1]!=0 or len(set(Bv))<len(Bv) or 0 in Bv or M in Bv: return None
    R=2*M+2; lo=max(Bv+[M])-R; hi=min(Bv+[0])+R-M
    V=list(range(lo,hi+1)); nv=0;top=0
    def new():
        nonlocal nv,top; nv=max(nv,top)+1; top=nv; return nv
    x={u:new() for u in V}; E={}
    for u in V:
        for L in labels:
            for w in (u+L,u-L):
                if w in x: E[(u,w)]=new()
    cl=[]
    def card(l,k,kind):
        nonlocal top
        f={'eq':CardEnc.equals,'le':CardEnc.atmost}[kind];e=f(lits=l,bound=k,top_id=top,encoding=EncType.seqcounter);top=max(top,e.nv);cl.extend(e.clauses)
    for L in labels: card([E[e] for e in E if abs(e[1]-e[0])==L],1,'eq')
    out={u:[] for u in V};inn={u:[] for u in V}
    for (u,w),e in E.items(): out[u].append(e);inn[w].append(e);cl.append([-e,x[u]]);cl.append([-e,x[w]])
    en={u:new() for u in V}
    for u in V:
        if len(out[u])>1: card(out[u],1,'le')
        if len(inn[u])>1: card(inn[u],1,'le')
        if u==0:
            for e in inn[u]: cl.append([-e])
            cl.append([x[0]])
        else: cl.append([-x[u]]+inn[u])
        cl.append([-x[u],en[u]]+out[u])
        for e in out[u]: cl.append([-en[u],-e])
        cl.append([-en[u],x[u]])
    card([en[u] for u in V],1,'eq')
    for u in V:
        if u+M in x: cl.append([-x[u],-x[u+M]])
        if u in Bv or (u+M) in Bv: cl.append([-x[u]])
    for u in V:
        for w in V:
            if w-u>M+2: cl.append([-x[u],-x[w]])
    S=Cadical153(bootstrap_with=cl);byE={e:k for k,e in E.items()};t0=time.time()
    while time.time()-t0<timeout:
        if not S.solve(): return 'UNSAT'
        m=set(l for l in S.get_model() if l>0)
        succ={byE[e][0]:byE[e][1] for e in byE if e in m}
        path=[0]
        while path[-1] in succ: path.append(succ[path[-1]])
        if len(path)==len(labels)+1: return path
        rest=set(succ)-set(path)
        while rest:
            v0=rest.pop();cyc=[v0];w=succ[v0]
            while w!=v0: cyc.append(w);rest.discard(w);w=succ[w]
            S.add_clause([-E[(u,succ[u])] for u in cyc])
    return 'TO'
def verify(M,a,path,bridge):
    b=M+1-a;d=[path[i+1]-path[i] for i in range(len(path)-1)]
    W=d+[M]+[-x for x in d[::-1]]+list(bridge)
    v=0;S=[0]
    for y in W[:-1]: v+=y;S.append(v)
    return (sorted(y for y in W if y>0)==list(range(1,M+1)) and sorted(-y for y in W if y<0)==sorted(set(range(1,M+2))-{a,b})
            and len(set(S))==len(S) and v+W[-1]==0 and max(S)-min(S)<=2*M+2)
if __name__=="__main__":
    for a in map(int,sys.argv[1].split(',')):
        for M in map(int,sys.argv[2].split(',')):
            b=M+1-a; found=[]
            for br in set(itertools.permutations((a,b,-M,-(M+1)))):
                r=solve(M,a,br,timeout=20)
                if isinstance(r,list) and verify(M,a,r,br): found.append(br)
            print("a",a,"M",M,"working bridges:",sorted(found),flush=True)
