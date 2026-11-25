"""Erdos #475 — nonlocal defect-barrier obstruction, November 24, 2026.

Exact certificate, standard library only. Not a counterexample to Graham.

The SDE assertion from the previous research round is false: a one-defect
ordering obtained by expanding an admissible contraction can belong to a
closed component under arbitrary transpositions preserving defect <= 1.
The p=53 example below has exactly 10 states modulo cyclic rotation,
10 undirected edges, and no zero-defect neighbor. Its barrier is exactly 2,
and the same admissible contraction also has a successful expansion.

The p=61 example illustrates a different trap: no state in its closed
14-state component admits a legal contraction at a repeated vertex.

Additional analytical result (not established by this finite certificate):
Let A be zero-sum, |A|=n, S a dissociated k-element subset of A, k>=5,
t=sum(S) outside A union {0}. Suppose (A\\S) union {t} has a valid cycle.
If 9*k >= 4*n+1, then A has a valid cycle. Proof:
Root the contracted cycle at t and let V be its vertex set. If every
expansion fails, forbidden proper subsets whose sums are in V hit all
maximal chains of the Boolean lattice. Their number is <= n-k-1.
The uniform-chain bound implies there are at least k such subsets, hence
r=n-2*k-1>=0. The assumed inequality gives k>=4*r+5.

Separator rigidity: write a,b,c for the counts of forbidden singletons,
co-singletons, and all other subsets. The chain union bound gives
k<=a+b+2*c/(k-1), so c<=r*(k-1)/(k-3). If neither extreme layer is
complete, conditioning on a missing singleton as the first element yields
b+c>=k-1 (each remaining eligible subset has conditional probability at
most 1/(k-1)). Conditioning on a missing co-singleton as the penultimate
subset yields a+c>=k-1. Adding forces r>=(k-3)/2, a contradiction.
Thus V contains S or t-S. Tail reversal lets us assume it contains S.

There are r other vertices strictly between t and the return to 0. The
vertices of S form at most r+1 runs. Select alternate interior vertices
of each run; if M are selected then k<=2*M+2*(r+1), so M>=r+2. At a
selected vertex s with neighbors u,v in S, swap the incident labels to
replace s by w=u+v-s. Dissociation and distinct edge labels imply
w is outside S union {0}. The w's are distinct: nonadjacent centers
ensure that the equality of two such expressions is an equality of sums
of distinct subsets of S (cancel a shared neighbor if necessary), which
is forbidden. There are only r+1 occupied vertices outside S union {0},
so some replacement is unoccupied. The resulting rooted cycle is valid,
misses one element of S, and has at most r+1<k members of t-S because
S and t-S are disjoint. Neither extreme layer is now complete. Separator
rigidity implies an expansion succeeds. QED.

This strengthens the earlier n>=2k+1 necessary condition, but dissociation
implies k<=log2(p), so the theorem does not settle dense cases. It is not
claimed to be independently referee-audited or novel in the literature.
"""
from collections import Counter, deque
from itertools import combinations

P53 = (1,8,11,15,24,22,29,52,34,18,40,23,10,26,21,51,50,48,46,27,
       17,33,4,20,35,49,6,30,38,14,31,25,39,43,5,45,47,28,13,32,
       16,2,19,7,44,42,3,9,37,36)
P61 = (2,21,19,9,56,32,26,11,20,17,34,30,55,37,50,42,7,4,13,10,
       24,29,27,23,22,59,12,52,28,41,5,31,53,36,16,39,43,6,8,40,
       38,15,35,44,47,45,54,25,48,3,57,46,49,58,51,18,14,33)


def canon(a):
    a = tuple(a)
    i = a.index(min(a))
    return a[i:] + a[:i]


def vertices(a, p):
    assert len(set(a)) == len(a) and all(0 < x < p for x in a)
    assert sum(a) % p == 0
    v, s = [], 0
    for x in a:
        v.append(s)
        s = (s+x) % p
    return v


def defect(a, p):
    return len(a)-len(set(vertices(a,p)))


def swap(a,i,j):
    b = list(a)
    b[i],b[j] = b[j],b[i]
    return canon(b)


def legal_merges(a,p):
    v = vertices(a,p)
    c = Counter(v)
    return [(a[i-1],a[i],(a[i-1]+a[i])%p) for i in range(len(a))
            if c[v[i]]==2 and (a[i-1]+a[i])%p not in set(a)|{0}]


def merge(a,p,x,y):
    i = a.index(x)
    a = a[i:]+a[:i]
    assert a[1]==y
    t = (x+y)%p
    assert t not in set(a)|{0}
    b = (t,)+a[2:]
    assert defect(b,p)==0
    return b


def closed_component(a,p):
    assert defect(a,p)==1
    a=canon(a)
    q=deque([a]); seen={a}; edges=set(); merges=[]
    while q:
        u=q.popleft()
        merges.extend(legal_merges(u,p))
        for i,j in combinations(range(len(u)),2):
            w=swap(u,i,j)
            d=defect(w,p)
            assert d != 0, ('escape',u,w)
            if d==1:
                edges.add(tuple(sorted((u,w))))
                if w not in seen:
                    seen.add(w);q.append(w)
    return seen,edges,merges


def verify():
    assert set(range(1,53))-set(P53)=={12,41}
    assert (48,46,41) in legal_merges(P53,53)
    b=merge(P53,53,48,46)
    s,e,m=closed_component(P53,53)
    assert (len(s),len(e))==(10,10)
    assert Counter(m)==Counter({(48,46,41):2,(46,48,41):2})
    print('p=53: 10 states, 10 edges, 0 exits; 4 admissibly contractible states.')
    print('Verified contracted cycle:',b)
    # The exact energy barrier is 2, with a four-swap witness.
    a=P53
    path=((1,8),(29,37),(11,24),(49,6))
    for (x,y),d in zip(path,(2,2,1,0)):
        a=swap(a,a.index(x),a.index(y))
        assert defect(a,53)==d
    print('Barrier 2 witness:',path)
    print('Valid ordering:',a)
    b2=merge(a,53,48,46)
    assert set(b)==set(b2)
    print('Same contraction, successful alternative rooted cycle:',b2)
    # A separate p=61 obstruction to the all-one-defect version.
    s,e,m=closed_component(P61,61)
    assert len(s)==14 and not m
    print('p=61: 14 states,',len(e),'edges, no exits and no legal merges.')
    print('All assertions passed.')

if __name__=='__main__':
    verify()
