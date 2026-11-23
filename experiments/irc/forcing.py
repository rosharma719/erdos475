"""Propagate forced edges in the B-shape from the core H=(M-2,0,a,M+1,2), labels from the top down.
At each label L (descending), list candidate edges {x,x+L} with both endpoints in U, degree<2, not closing a cycle.
If exactly one, force it. Stop when ambiguous."""
import sys
def run(M,a,verbose=False):
    b=M+1-a; U=set([-1,0])|set(range(2,M-1))|{M+1}
    deg={v:0 for v in U}; parent={v:v for v in U}
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    edges=[]
    def add(x,y):
        deg[x]+=1;deg[y]+=1;parent[find(x)]=find(y);edges.append((x,y))
    H=[M-2,0,a,M+1,2]
    for i in range(4): add(H[i],H[i+1])
    used={abs(H[i+1]-H[i]) for i in range(4)}
    forced=[]
    for L in range(M-1,0,-1):
        if L in used: continue
        cands=[(x,x+L) for x in U if x+L in U and deg[x]<2 and deg[x+L]<2 and find(x)!=find(x+L)]
        if len(cands)==1:
            add(*cands[0]);used.add(L);forced.append((L,cands[0]))
        else:
            return forced,L,cands
    return forced,None,None
for M,a in [(30,8),(31,8),(32,8),(40,10),(41,10),(40,15),(60,12),(61,20)]:
    f,L,c=run(M,a)
    print(f"M={M} a={a}: forced {len(f)} labels; stuck at L={L} (M-L={M-L if L else None}) with {len(c) if c else 0} options")
    print("   ",[(M-l,(x if x<M//2 else f'M{ x-M:+d}'),(y if y<M//2 else f'M{y-M:+d}')) for l,(x,y) in f][:14])
