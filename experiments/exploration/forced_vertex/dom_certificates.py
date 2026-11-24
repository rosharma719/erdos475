from itertools import combinations, permutations, product
from math import prod
def vertex(p, w):
    V = [sum(w[:i]) % p for i in range(len(w))]
    if sum(w) % p or len(V) != len(set(V)): return None
    return V
def setup(p, B, x, Pi):
    y = (1-x) % p; used = [a for e in Pi for a in e]; sums = [sum(e) % p for e in Pi]
    assert 1 in B and sum(B) % p == 0 and 0 not in B and x != y and x*y != 0 and x not in B and y not in B
    assert len(set(used)) == len(used) and set(used) <= B-{1} and len(set(sums)) == len(sums)
    assert not set(sums) & (B | {0,x,y})
    return (B-set(used)) | set(sums)
def cycles(p, C):
    for tail in permutations(sorted(C-{1})):
        w = (1,) + tail; V = vertex(p,w)
        if V is not None: yield w,V
def options(p, w, V, Pi): return [tuple((V[w.index(sum(e)%p)]+a)%p for a in e) for e in Pi]
def good(O, F): return [h for h in product(*O) if len(set(h)) == len(h) and not set(h) & F]
def graph_count(O, F):
    R = {a for e in O for a in e}; ans = 1
    while R:
        S = {next(iter(R))}
        while True:
            T = S | {v for e in O if S.intersection(e) for v in e}
            if T == S: break
            S = T
        R -= S; v = len(S); e = sum(a in S for a,b in O); f = len(S & F)
        if e == v-1 and f == 0: ans *= v
        elif e == v-1 and f == 1: pass
        elif e == v and f == 0: ans *= 2
        else: return 0
    return ans
p=13; B={1,2,3,9,11}; x=6; Pi=((2,3),(9,11)); C=setup(p,B,x,Pi)
W=[(w,V) for w,V in cycles(p,C) if x not in V]; assert len(W)==1
w,V=W[0]; O=options(p,w,V,Pi); F=set(V)|{x}
q=[(prod(a-f for a in h for f in F)*prod(a-b for a,b in combinations(h,2)))%p for h in product(*O)]
assert q==[0,1,8,9] and (q[0]-q[1]-q[2]+q[3])%p==0 and len(good(O,F))==3==graph_count(O,F)
p=13; B={1,2,3,4,7,9}; x=6; Pi=((2,9),(3,7)); C=setup(p,B,x,Pi)
w=(1,11,4,10); V=vertex(p,w); O=options(p,w,V,Pi); F=set(V)|{x}
assert [set(e)-F for e in O]==[{10},{10}] and not good(O,F)
for w,V in cycles(p,C):
    if x not in V:
        O=options(p,w,V,Pi); F=set(V)|{x}; assert graph_count(O,F)==len(good(O,F))
p=11; B={1,2,3,5,6,7,9}; x=4; Pi=((3,7),); C=setup(p,B,x,Pi); N=0
for w,V in cycles(p,C):
    if x not in V:
        O=options(p,w,V,Pi); F=set(V)|{x}; N+=len(good(O,F)); assert graph_count(O,F)==len(good(O,F))
assert N==22
p=13; B={1,2,3,5,6,7,8,9,11}; x=4; Pi=((3,9),); C=setup(p,B,x,Pi)
w=(1,11,7,2,8,12,5,6); V=vertex(p,w); assert V is not None and x not in V and set(options(p,w,V,Pi)[0])<=set(V)
for i,j in combinations(range(1,len(w)),2):
    q=list(w); q[i],q[j]=q[j],q[i]; assert vertex(p,q) is None
q=(1,8,2,7,11,12,5,6); V=vertex(p,q); assert V is not None and x not in V and good(options(p,q,V,Pi),set(V)|{x})
p=29; B=set(range(1,p))-{10,20,28}; x=10; Pi=((6,22),); C=setup(p,B,x,Pi)
w=(1,8,22,6,24,4,26,2,15,27,3,25,5,23,7,21,9,19,11,17,13,14,16,12,18)
assert set(w)==B and len(w)==len(B) and x not in vertex(p,w) and any(set(w[i:i+2])=={6,22} for i in range(len(w)-1))
print("all DOM-round analytical certificates verified")
