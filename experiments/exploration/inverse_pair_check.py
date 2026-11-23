"""Free local sanity check of the inverse-pair proposition (C={u,-u,v}, v≠±u).
Construction: graceful permutation alpha of [1..r] whose LAST |difference| is d  ->  rotational sequencing
b=(δ1..δ_{r-1}, r, -δ_{r-1}..-δ1, -r); block (δ_{r-1}, r, -δ_{r-1}) has underlying set {±d, r};
delete it -> arc of a valid cyclic sequencing of Z_p^*.  We verify every step for each (p,d) and report where
a graceful permutation with last |difference| d was found (Lemma 4.5 itself is NOT proved here)."""
import random, sys, itertools

def graceful_with_last(r, d, tries=300, rng=random.Random(1)):
    # DFS over permutations of 1..r with distinct |differences| = {1..r-1}, last |difference| == d
    sys.setrecursionlimit(10000)
    for _ in range(tries):
        start = rng.randint(1, r)
        used = {start}; diffs = set(); path = [start]
        order = list(range(1, r + 1))
        def rec():
            if len(path) == r:
                return abs(path[-1] - path[-2]) == d
            cand = [x for x in order if x not in used and abs(x - path[-1]) not in diffs]
            rng.shuffle(cand)
            if len(path) == r - 1:                       # force last difference d
                cand = [x for x in cand if abs(x - path[-1]) == d]
            for x in cand:
                used.add(x); diffs.add(abs(x - path[-1])); path.append(x)
                if rec(): return True
                path.pop(); used.discard(x); diffs.discard(abs(x - path[-1]) if False else abs(x - path[-1]))
            return False
        # simple restart-based search with node cap
        budget = [20000]
        def rec2(depth_limit=[0]):
            budget[0] -= 1
            if budget[0] < 0: return None
            if len(path) == r:
                return abs(path[-1] - path[-2]) == d
            cand = [x for x in order if x not in used and abs(x - path[-1]) not in diffs]
            rng.shuffle(cand)
            if len(path) == r - 1:
                cand = [x for x in cand if abs(x - path[-1]) == d]
            for x in cand:
                dd = abs(x - path[-1]); used.add(x); diffs.add(dd); path.append(x)
                res = rec2()
                if res: return True
                path.pop(); used.discard(x); diffs.discard(dd)
                if res is None: return None
            return False
        if rec2(): return list(path)
    return None

def check(p, d):
    r = (p - 1) // 2
    al = graceful_with_last(r, d)
    if al is None: return "nofind"
    delta = [al[i + 1] - al[i] for i in range(r - 1)]
    b = [x % p for x in delta] + [r] + [(-x) % p for x in reversed(delta)] + [(-r) % p]
    S = list(itertools.accumulate(b, lambda s, x: (s + x) % p))
    if sorted(b) != list(range(1, p)): return "not-all-of-Zp*"
    if len(set(S)) != len(S): return "not-a-sequencing"
    blk = b[r - 2:r + 1]                                   # positions r-1,r,r+1 (1-indexed)
    if sorted(blk) != sorted([d, p - d, r]): return f"block-set-wrong {blk}"
    arc = b[r + 1:] + b[:r - 2]                           # cyclic arc after the block
    ps = list(itertools.accumulate(arc, lambda s, x: (s + x) % p))
    return "ok" if len(set(ps)) == len(ps) and len(arc) == p - 4 else "arc-invalid"

if __name__ == "__main__":
    for p in (19, 23, 29):
        r = (p - 1) // 2
        res = {d: check(p, d) for d in range(1, r)}
        bad = {d: v for d, v in res.items() if v != "ok"}
        print(f"p={p} r={r}: ok for {len(res)-len(bad)}/{len(res)} values of d; non-ok: {bad}", flush=True)
