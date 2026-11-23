import itertools, collections, sys
def pairs(m):
    g=collections.defaultdict(list)
    for mask in range(1,1<<m):
        s=[i+1 for i in range(m) if mask>>i&1]; g[sum(s)].append(tuple(s))
    for S,l in g.items():
        for P in l:
            for N in l:
                if P!=N and max(P)+max(N)>=3: yield P,N
def run(P,N,rule):
    P=set(P);N=set(N);v=0;seen={0};n=len(P)+len(N)
    for k in range(n):
        side=P if v<=0 else N; sg=1 if v<=0 else -1
        last=(k==n-1)
        cand=[x for x in side if (v+sg*x==0 if last else (v+sg*x) not in seen)]
        if not cand: return False
        if last: x=cand[0]
        else: x=rule(cand,v,sg,seen,P,N)
        side.remove(x); v+=sg*x; seen.add(v)
    return v==0
rules={
 'max':lambda c,v,s,seen,P,N:max(c),
 'min':lambda c,v,s,seen,P,N:min(c),
 'toward0':lambda c,v,s,seen,P,N:min(c,key=lambda x:(abs(v+s*x),x)),
 'away0':lambda c,v,s,seen,P,N:max(c,key=lambda x:(abs(v+s*x),x)),
 'mid':lambda c,v,s,seen,P,N:sorted(c)[len(c)//2],
}
m=int(sys.argv[1]); allp=list(pairs(m)); print(len(allp),"pairs")
for name,r in rules.items():
    ok=sum(run(P,N,r) for P,N in allp); print(name,ok,"/",len(allp),flush=True)
