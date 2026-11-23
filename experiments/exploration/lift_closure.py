"""Does PURE lift-induction work?  Q(A) := valid cycles of A obtainable by lifting a Q-cycle of some merged set B'=A\\{a1,a2}∪{a1+a2}.
Base: all valid cycles for |A|<=4.  If Q(A) is empty for some zero-sum A (|A|>=5) then induction 'lift any previously built cycle'
cannot prove Graham for A; the invariant must carry more information than 'is a lifted cycle'."""
import sys, itertools, collections
sys.path.insert(0, "experiments/exploration")
from cycle_space import valid_cycles, canon

def lifts(Cp, z, a1, a2, p):
    k = len(Cp); out = []
    i = Cp.index(z)
    S = [0]
    for x in Cp[:-1]: S.append((S[-1] + x) % p)
    pts = set(S); P = S[i]
    for (x, y) in ((a1, a2), (a2, a1)):
        if (P + x) % p not in pts:
            out.append(canon(Cp[:i] + (x, y) + Cp[i + 1:]))
    return out

def run(p, kmax=None):
    Q = {}; bad = []; stats = []
    for k in range(2, p):
        for A in itertools.combinations(range(1, p), k):
            if sum(A) % p: continue
            fs = frozenset(A)
            if k <= 4:
                Q[fs] = set(canon(c) for c in valid_cycles(list(A), p)); continue
            if kmax and k > kmax: continue
            acc = set(); npairs = nok = 0
            for a1, a2 in itertools.combinations(A, 2):
                z = (a1 + a2) % p
                if z == 0 or z in fs: continue
                Bp = (fs - {a1, a2}) | {z}; npairs += 1
                src = Q.get(Bp)
                if src is None: continue
                found = set()
                for Cp in src: found.update(lifts(Cp, z, a1, a2, p))
                if found: nok += 1
                acc |= found
            Q[fs] = acc
            if not acc: bad.append(A)
            stats.append((k, npairs, nok))
    full = {k: sum(1 for _ in [0]) for k in []}
    print(f"p={p}: zero-sum sets size>=5 processed: {len(stats)}, Q empty for {len(bad)} sets")
    for A in bad[:6]: print("  Q empty:", A)
    worst = [(nok / np_, k, np_) for k, np_, nok in stats if np_]
    if worst: print("  min fraction of legal pairs with a lifted cycle:", round(min(worst)[0], 3), "(k, #pairs)=", min(worst)[1:])
    return Q

if __name__ == "__main__":
    for p in map(int, sys.argv[1:]): run(p)
