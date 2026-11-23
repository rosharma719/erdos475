"""LR with invariant: no edge of length <= M//2 crosses the cut c=ceil(M/2) (low=[0,c-1], high=[c,M-1])."""
import sys,time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def solve(M,a,k,timeout=30,extra=None):
    b=M+1-a; V=sorted(set(range(M))-{k+1,k+a}); Vs=set(V); L=set(range(1,M))-{a,b}; c=(M+1)//2
    top=[0]
    def new(): top[0]+=1; return top[0]
    E={}
    for u in V:
        for l in L:
            for w in (u+l,u-l):
                if w in Vs:
                    if l<=M//2 and (min(u,w)<c<=max(u,w)): continue
                    E[(u,w)]=new()
    cl=[]
    def card(l,kk,kind):
        if not l: return False
        f={'eq':CardEnc.equals,'le':CardEnc.atmost}[kind];e=f(lits=l,bound=kk,top_id=top[0],encoding=EncType.seqcounter);top[0]=max(top[0],e.nv);cl.extend(e.clauses);return True
    for l in L:
        if not card([E[e] for e in E if abs(e[1]-e[0])==l],1,'eq'): return 'UNSAT'
    out={u:[] for u in V};inn={u:[] for u in V}
    for (u,w),e in E.items(): out[u].append(e);inn[w].append(e)
    for u in V:
        if u==k: cl.extend([[-e] for e in inn[u]])
        elif not card(inn[u],1,'eq'): return 'UNSAT'
        if out[u]: card(out[u],1,'le')
    S=Cadical153(bootstrap_with=cl);byE={e:kk for kk,e in E.items()};t0=time.time()
    while time.time()-t0<timeout:
        if not S.solve(): return 'UNSAT'
        m=set(l for l in S.get_model() if l>0); succ={byE[e][0]:byE[e][1] for e in byE if e in m}
        p=[k]
        while p[-1] in succ: p.append(succ[p[-1]])
        if len(p)==len(V): return p
        rest=set(succ)-set(p)
        while rest:
            v0=rest.pop();cyc=[v0];w=succ[v0]
            while w!=v0: cyc.append(w);rest.discard(w);w=succ[w]
            S.add_clause([-E[(u,succ[u])] for u in cyc])
    return 'TO'
if __name__=="__main__":
    for M in range(int(sys.argv[1]),int(sys.argv[2])):
        row=[]
        for a in range(2,M//2+1):
            c=(M+1)//2
            ks=[k for k in range(0,M-a) if isinstance(solve(M,a,k,10),list)]
            row.append(f"{a}:{ks}")
        print(M,' '.join(row),flush=True)
