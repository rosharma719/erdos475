import sys
sys.setrecursionlimit(5000)
# Half-walk form of RS+ for tight family: path with lengths L=[1,M-1]\{b}, vertices distinct in window of M slots,
# step -a lands on global min. Normalize min=0: vertices in [0,M-1]; path contains a->0. Search all, print one.
def solve(M,a,cap=3_000_000):
    n=M-1;b=M+1-a;L=set(range(1,n+1))-{b}
    cnt=[0]
    # build path as a two-ended chain around the edge (a,0): left end grows from a, right end from 0
    def dfs(left,right,used,lens,pl,pr):
        cnt[0]+=1
        if cnt[0]>cap: return None
        if not lens: return pl[::-1]+pr
        for end in (1,0):
            v=right if end else left
            for l in sorted(lens,reverse=True):
                for w in (v+l,v-l):
                    if 0<w<=n and w not in used:   # w>0: 0 is the unique min
                        used.add(w);lens.discard(l)
                        r=dfs(left if end else w, w if end else right, used,lens, pl if end else pl+[w], pr+[w] if end else pr)
                        if r: return r
                        used.discard(w);lens.add(l)
        return None
    return dfs(a,0,{a,0},L-{a},[a],[0])
for a in (2,3,4):
    for M in range(2*a+2,2*a+14):
        r=solve(M,a)
        print(a,M,r)
