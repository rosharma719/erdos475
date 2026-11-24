# k decreasing paths: path i from top t_i using step set S_i (any order) to bottom t_i - sum S_i.
# Hypotheses: tops distinct; no bottom can lie on another path (for any orders, i.e. bottom not in reachable vertex set).
# Question: do orders exist making all vertex sets pairwise disjoint?
import random, itertools
def verts(t,order):
    v=[t]
    for x in order: v.append(v[-1]-x)
    return v
def reach(t,S):  # all vertices any order could visit = t - subset sums
    sums={0}
    for x in S: sums|={s+x for s in sums}
    return {t-s for s in sums}
rng=random.Random(1); found=0; tested=0
for trial in range(200000):
    k=3
    allv=rng.sample(range(1,13),rng.randint(5,8))
    # split into k nonempty step sets
    rng.shuffle(allv); cuts=sorted(rng.sample(range(1,len(allv)),k-1))
    S=[allv[i:j] for i,j in zip([0]+cuts,cuts+[len(allv)])]
    tops=rng.sample(range(-5,25),k)
    bots=[t-sum(s) for t,s in zip(tops,S)]
    R=[reach(t,s) for t,s in zip(tops,S)]
    if any(bots[i] in R[j] for i in range(k) for j in range(k) if i!=j): continue
    if any(tops[i] in R[j] for i in range(k) for j in range(k) if i!=j): pass  # tops allowed on other paths per lemma (distinct tops only)
    tested+=1
    ok=False
    for o in itertools.product(*[list(itertools.permutations(s)) for s in S]):
        V=[set(verts(t,oo)) for t,oo in zip(tops,o)]
        if all(not(V[i]&V[j]) for i in range(k) for j in range(i+1,k)): ok=True;break
    if not ok:
        found+=1
        if found<=3: print("NO SEPARATION:",list(zip(tops,S)))
    if tested>=3000: break
print("tested",tested,"failures",found)
