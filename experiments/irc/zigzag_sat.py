"""Exact zigzag decision by SAT with lazy sub-cycle elimination (complete: UNSAT is a proof of non-existence).
Graph: positions w in [1-D, U]; nonpositive v has edges v -> v+p (label p in P), positive v has edges v -> v-q (label q in N).  A zigzag ordering is a single closed
walk from 0 using every label exactly once, visiting distinct positions (in-degree/out-degree <= 1), returning to 0 only at the end."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def decide(P, N, want_witness=True, timeout=None):
    P, N = sorted(P), sorted(N); U, D = P[-1], N[-1]
    var = {}; nv = 0; edges = []          # (v, label, sign, target)
    def newvar():
        nonlocal nv; nv += 1; return nv
    for v in range(1 - D, U + 1):
        if v <= 0:
            for p in P:
                w = v + p
                if w <= U: var[(v, p, 1)] = newvar(); edges.append((v, p, 1, w))
        else:
            for q in N:
                w = v - q
                if w >= 1 - D: var[(v, q, -1)] = newvar(); edges.append((v, q, -1, w))
    clauses = []
    top = nv
    def exactly_one(lits):
        nonlocal top
        enc = CardEnc.equals(lits=lits, bound=1, top_id=top, encoding=EncType.seqcounter)
        top = max(top, enc.nv); clauses.extend(enc.clauses)
    def at_most_one(lits):
        nonlocal top
        if len(lits) > 1:
            enc = CardEnc.atmost(lits=lits, bound=1, top_id=top, encoding=EncType.seqcounter)
            top = max(top, enc.nv); clauses.extend(enc.clauses)
    for p in P: exactly_one([var[(v, p, 1)] for (v, l, s, w) in edges if l == p and s == 1])
    for q in N: exactly_one([var[(v, q, -1)] for (v, l, s, w) in edges if l == q and s == -1])
    out = {}; inn = {}
    for (v, l, s, w) in edges:
        out.setdefault(v, []).append(var[(v, l, s)]); inn.setdefault(w, []).append(var[(v, l, s)])
    for v in range(1 - D, U + 1):
        o = out.get(v, []); i = inn.get(v, [])
        at_most_one(o); at_most_one(i)
        # flow conservation: out(v) == in(v): for each lit a in o: (a -> OR i); for each b in i: (b -> OR o)
        for a in o: clauses.append([-a] + i)
        for b in i: clauses.append([-b] + o)
    clauses.append(list(out.get(0, [])))          # 0 must have an outgoing edge
    # the walk must START with a positive step from 0: edges from 0 are positive-labelled by construction (v<=0)
    S = Cadical153(bootstrap_with=clauses)
    byvar = {var[(v, l, s)]: (v, l, s, w) for (v, l, s, w) in edges}
    iters = 0
    while True:
        iters += 1
        if not S.solve(): return ("NONE", None, iters)
        model = set(x for x in S.get_model() if x > 0 and x in byvar)
        succ = {}
        for x in model: v, l, s, w = byvar[x]; succ[v] = (x, w, s * l)
        # cycle through 0
        seen = []; cur = 0; steps = []
        while True:
            x, w, d = succ[cur]; seen.append(x); steps.append(d); cur = w
            if cur == 0: break
        if len(seen) == len(model): return ("FOUND", steps, iters)
        # other cycles: block each
        covered = set(seen); rest = {v for v in succ if succ[v][0] not in covered}
        done = set()
        for v0 in rest:
            if v0 in done: continue
            cyc = []; cur = v0
            while cur not in done:
                done.add(cur); x, w, d = succ[cur]; cyc.append(x); cur = w
            S.add_clause([-x for x in cyc])

def check_steps(steps, P, N):
    s = 0; seen = {0}
    if sorted(x for x in steps if x > 0) != sorted(P) or sorted(-x for x in steps if x < 0) != sorted(N): return False
    for i, d in enumerate(steps):
        if (d > 0) != (i == 0 or s < 0): return False
        s += d
        if i < len(steps) - 1:
            if s in seen or s == 0: return False
            seen.add(s)
    return s == 0

if __name__ == "__main__":
    # controls
    for name, P, N, exp in (("[1..7]=[1..7]", range(1, 8), range(1, 8), "NONE"), ("{1,2,3}", [1, 2, 3], [1, 2, 3], "NONE"), ("[1..5]", range(1, 6), range(1, 6), "FOUND"), ("[1..6]", range(1, 7), range(1, 7), "FOUND"),
                            ("{1,2,3,4}/{2,3,5}", [1, 2, 3, 4], [2, 3, 5], "FOUND"), ("[1..8]/[1..9]\\{4,5}", range(1, 9), [1, 2, 3, 6, 7, 8, 9], "FOUND"), ("[1..8]=[1..8]", range(1, 9), range(1, 9), "NONE")):
        t = time.time(); r, st, it = decide(list(P), list(N)); ok = (r == exp) and (r != "FOUND" or check_steps(st, list(P), list(N)))
        print(f"control {name}: {r} (expected {exp}) {'OK' if ok else 'MISMATCH'} [{it} iters, {time.time()-t:.2f}s]")
