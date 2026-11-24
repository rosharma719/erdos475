"""Junction c=2 (a=2) restricted to TWO-PHASE PAIR shapes: D = {4i,4i+1 : i<L} ∪ {u+4j,u+4j+1 : j<U} (+ one singleton
if needed), u = 4L+1 or 4L+2 (phase shift 1 or 2), translated so the start vertex is 0. Exact SAT on the fixed vertex set."""
import sys
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def path_on(Dset,labels,start,first,timeout_iters=5000):
    V=sorted(Dset); nv=0
    def new():
        nonlocal nv; nv+=1; return nv
    E={}
    for v in V:
        for w in V:
            if v!=w and abs(w-v) in labels: E[(v,w)]=new()
    top=nv; cl=[]
    def card(l,k,kind):
        nonlocal top
        f={'eq':CardEnc.equals,'le':CardEnc.atmost}[kind]; e=f(lits=l,bound=k,top_id=top,encoding=EncType.seqcounter); top=max(top,e.nv); cl.extend(e.clauses)
    for L in labels:
        lits=[E[e] for e in E if abs(e[1]-e[0])==L]
        if not lits: return None
        card(lits,1,'eq')
    out={v:[E[e] for e in E if e[0]==v] for v in V}; inn={v:[E[e] for e in E if e[1]==v] for v in V}
    for v in V:
        if len(out[v])>1: card(out[v],1,'le')
        if len(inn[v])>1: card(inn[v],1,'le')
        if v!=start: cl.append(inn[v])          # every non-start vertex entered
        else:
            for e in inn[v]: cl.append([-e])
    # exactly one end (no out): count vertices with out=0 must be 1 -> enforce via #edges = |V|-1 (labels count) automatically
    if (start,first) not in E: return None
    cl.append([E[(start,first)]])
    S=Cadical153(bootstrap_with=cl); byE={e:k for k,e in E.items()}
    for _ in range(timeout_iters):
        if not S.solve(): return None
        m=set(l for l in S.get_model() if l>0)
        succ={byE[e][0]:byE[e][1] for e in byE if e in m}
        path=[start]
        while path[-1] in succ and len(path)<=len(V): path.append(succ[path[-1]])
        if len(path)==len(V): return path
        seen=set(path); rest=set(succ)-seen
        while rest:
            v0=rest.pop();cyc=[v0];w=succ[v0]
            while w!=v0 and w in succ: cyc.append(w);rest.discard(w);w=succ[w]
            S.add_clause([-E[(u,succ[u])] for u in cyc if u in succ])
    return None
def shapes(M):
    for L in range(1,M):
        for shift in (1,2):
            u=4*L+shift-1+1  # u=4L+shift
            u=4*L+shift
            base=[4*i+r for i in range(L) for r in (0,1)]
            rest=M-len(base)
            if rest<0: continue
            U=rest//2; upper=[u+4*j+r for j in range(U) for r in (0,1)]
            D=base+upper
            if rest%2: 
                for extra in (upper[-1]+3 if upper else u, base[0]-3):
                    yield L,shift,D+[extra]
            else: yield L,shift,D
