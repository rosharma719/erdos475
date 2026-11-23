"""Exact SAT: Hamiltonian path on a fixed vertex set V starting at s, using each label in L exactly once."""
import sys,time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def hpath(V,L,s,timeout=60,end=None):
    V=sorted(V);Vs=set(V);top=[0]
    def new(): top[0]+=1; return top[0]
    E={}
    for u in V:
        for l in L:
            for w in (u+l,u-l):
                if w in Vs: E[(u,w)]=new()
    cl=[]
    def card(l,k,kind):
        f={'eq':CardEnc.equals,'le':CardEnc.atmost}[kind];e=f(lits=l,bound=k,top_id=top[0],encoding=EncType.seqcounter);top[0]=max(top[0],e.nv);cl.extend(e.clauses)
    for l in L:
        if not any(abs(e[1]-e[0])==l for e in E): return 'UNSAT'
    for l in L: card([E[e] for e in E if abs(e[1]-e[0])==l],1,'eq')
    out={u:[] for u in V};inn={u:[] for u in V}
    for (u,w),e in E.items(): out[u].append(e);inn[w].append(e)
    for u in V:
        if u==s:
            for e in inn[u]: cl.append([-e])
        elif not inn[u]: return 'UNSAT'
        else: card(inn[u],1,'eq')
        if out[u]: card(out[u],1,'le')
    if end is not None:
        for e in out[end]: cl.append([-e])
    S=Cadical153(bootstrap_with=cl);byE={e:k for k,e in E.items()};t0=time.time()
    while time.time()-t0<timeout:
        if not S.solve(): return 'UNSAT'
        m=set(l for l in S.get_model() if l>0)
        succ={byE[e][0]:byE[e][1] for e in byE if e in m}
        path=[s]
        while path[-1] in succ: path.append(succ[path[-1]])
        if len(path)==len(V): return path
        rest=set(succ)-set(path)
        while rest:
            v0=rest.pop();cyc=[v0];w=succ[v0]
            while w!=v0: cyc.append(w);rest.discard(w);w=succ[w]
            S.add_clause([-E[(u,succ[u])] for u in cyc])
    return 'TO'
