"""Exact SAT decision for tight half-walks with offset c.
delta = directed path, M vertices, labels {1..M}\{c} each once (|step| = label), D ∩ (D+c) = ∅, spread(D) <= 2M+2-c.
mode 'junction': requires c in {a,b} and first step +other (merge at seam).  mode 'internal': consecutive 0->a->M+1 or
M+1->a->0 somewhere (merge internal pair). Lazy elimination of cycles. UNSAT = no such half-walk."""
import sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def solve(M,a,c,mode,timeout=60):
    b=M+1-a; s=2*M+2-c; labels=[L for L in range(1,M+1) if L!=c]
    V=list(range(-s,s+1)); nv=0; top=0
    def new():
        nonlocal nv,top; nv=max(nv,top)+1; top=nv; return nv
    x={v:new() for v in V}
    E={}
    for v in V:
        for L in labels:
            for w in (v+L,v-L):
                if w in x: E[(v,w)]=new()
    top=nv; cl=[]
    def card(lits,k,kind):
        nonlocal top
        f={'eq':CardEnc.equals,'le':CardEnc.atmost,'ge':CardEnc.atleast}[kind]
        enc=f(lits=lits,bound=k,top_id=top,encoding=EncType.seqcounter); top=max(top,enc.nv); cl.extend(enc.clauses)
    for L in labels: card([E[e] for e in E if abs(e[1]-e[0])==L],1,'eq')
    out={v:[] for v in V}; inn={v:[] for v in V}
    for (v,w),e in E.items(): out[v].append(e); inn[w].append(e); cl.append([-e,x[v]]); cl.append([-e,x[w]])
    st={v:new() for v in V}; en={v:new() for v in V}; top=max(top,nv)
    for v in V:
        if len(out[v])>1: card(out[v],1,'le')
        if len(inn[v])>1: card(inn[v],1,'le')
        # x[v] -> (in or start) and (out or end)
        cl.append([-x[v],st[v]]+inn[v]); cl.append([-x[v],en[v]]+out[v])
        for e in inn[v]: cl.append([-st[v],-e])
        for e in out[v]: cl.append([-en[v],-e])
        cl.append([-st[v],x[v]]); cl.append([-en[v],x[v]])
    card([st[v] for v in V],1,'eq'); card([en[v] for v in V],1,'eq')
    card([x[v] for v in V],M,'eq')
    cl.append([st[0]])
    for v in V:
        if v+c in x: cl.append([-x[v],-x[v+c]])
    for u in V:
        for v in V:
            if v-u>s: cl.append([-x[u],-x[v]])
    if mode=='junction':
        other=b if c==a else a
        cl.append([E[(0,other)]])
    else:
        t1=[E.get((0,a)),E.get((a,M+1))]; t2=[E.get((M+1,a)),E.get((a,0))]
        # triple appears in either direction (after translation we fix 0 in the triple; start vertex free -> use st anywhere)
        y=new(); top=max(top,nv)
        cl.append([-y,t1[0]]);cl.append([-y,t1[1]])
        z=new(); top=max(top,nv)
        cl.append([-z,t2[0]]);cl.append([-z,t2[1]]); cl.append([y,z])
        # in internal mode the start need not be 0: drop st[0]
        cl.remove([st[0]])
    S=Cadical153(bootstrap_with=cl); byE={e:k for k,e in E.items()}; t0=time.time(); it=0
    while True:
        if time.time()-t0>timeout: return 'TO',None
        it+=1
        if not S.solve(): return 'UNSAT',None
        m=set(l for l in S.get_model() if l>0)
        succ={byE[e][0]:byE[e][1] for e in byE if e in m}
        start=[v for v in V if st[v] in m][0]
        path=[start]
        while path[-1] in succ: path.append(succ[path[-1]])
        if len(path)==M: return 'FOUND',path
        # block every cycle
        rest=set(succ)-set(path)
        while rest:
            v0=rest.pop(); cyc=[v0]; w=succ[v0]
            while w!=v0: cyc.append(w); rest.discard(w); w=succ[w]
            S.add_clause([-E[(u,succ[u])] for u in cyc])
def lift(M,a,c,mode,path):
    b=M+1-a; D=[v-path[0] for v in path]; d=[D[i+1]-D[i] for i in range(M-1)]
    W=d+[c]+[-x for x in d[::-1]]+[-c]
    done=False
    for i in range(len(W)-1):
        if W[i]<0 and W[i+1]<0 and sorted([-W[i],-W[i+1]])==[a,b]: W=W[:i]+[-(M+1)]+W[i+2:];done=True;break
        if W[i]>0 and W[i+1]>0 and sorted([W[i],W[i+1]])==[a,b]: W=[-y for y in W[:i]+[M+1]+W[i+2:]];done=True;break
    if not done: return False,0
    v=0;S=[0]
    for y in W[:-1]: v+=y;S.append(v)
    ok=sorted(y for y in W if y>0)==list(range(1,M+1)) and sorted(-y for y in W if y<0)==sorted(set(range(1,M+2))-{a,b}) and len(set(S))==len(S) and v+W[-1]==0 and max(S)-min(S)<=2*M+2
    return ok,max(S)-min(S)
if __name__=="__main__":
    mode=sys.argv[1]; Ms=list(map(int,sys.argv[2].split(','))); As=list(map(int,sys.argv[3].split(','))); cs=sys.argv[4]
    for M in Ms:
        for a in As:
            if not 2*a<M+1: continue
            c=a if cs=='a' else int(cs)
            t=time.time(); r,p=solve(M,a,c,mode,timeout=float(sys.argv[5]) if len(sys.argv)>5 else 60)
            print(M,a,"c",c,mode,r, lift(M,a,c,mode,p) if p else "", f"{time.time()-t:.0f}s",flush=True)
