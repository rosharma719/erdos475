import sys
def paths(M,limit):
    a=2;b=M-1; D=set(range(-b,a+1))-{1,1-b}
    L=set(range(1,M))-{b,a}; out=[]
    def dfs(p,used,L):
        if len(out)>=limit: return
        if len(p)==M-1: out.append(list(p)); return
        v=p[-1]
        for l in sorted(L,reverse=True):
            for w in (v-l,v+l):
                if w in D and w not in used:
                    used.add(w);L.discard(l);p.append(w);dfs(p,used,L);p.pop();L.add(l);used.discard(w)
    dfs([0,2],{0,2},L); return out
for M in range(6,19):
    ps=paths(M,1); print(M, ps[0] if ps else None)
