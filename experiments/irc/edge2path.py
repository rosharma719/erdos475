import sys
from edgedfs import solve
def topath(E):
    adj={}
    for L,(x,y) in E.items(): adj.setdefault(x,[]).append(y); adj.setdefault(y,[]).append(x)
    ends=[v for v in adj if len(adj[v])==1]; p=[ends[0]];prev=None
    while len(p)<len(adj):
        nx=[w for w in adj[p[-1]] if w!=prev][0]; prev=p[-1]; p.append(nx)
    return p
def rel(v,M): return str(v) if v<M/2 else ("M" if v==M else f"M{v-M:+d}")
a=int(sys.argv[1])
for M in map(int,sys.argv[2].split(',')):
    E=solve(M,a,tl=20)
    if E in (None,'TO'): print(M,E);continue
    p=topath(E)
    if p[0]>p[-1]: p=p[::-1]
    print(M," ".join(rel(v,M) for v in p),flush=True)
