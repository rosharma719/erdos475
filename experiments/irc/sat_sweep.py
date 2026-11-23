import sys, time, itertools, collections
sys.path.insert(0, "experiments/irc")
from zigzag_sat import decide, check_steps
def run(name, insts):
    c = collections.Counter(); bad = []
    t = time.time()
    for meta, P, N in insts:
        r, st, it = decide(P, N)
        if r == "FOUND": assert check_steps(st, P, N), ("invalid witness", meta)
        c[r] += 1
        if r != "FOUND": bad.append(meta)
    print(f"{name}: {len(insts)} pairs; found {c['FOUND']}, NONE {c['NONE']}; {time.time()-t:.0f}s", flush=True)
    for m in bad[:10]: print("    NO ZIGZAG:", m, flush=True)
    return bad
if __name__ == "__main__":
    # extra controls
    for h, exp in ((9, "FOUND"), (10, "NONE")):
        r, st, it = decide(list(range(1, h + 1)), list(range(1, h + 1))); print(f"control symmetric [1..{h}]: {r} (ledger: {exp})", "OK" if r == exp else "MISMATCH", flush=True)
    which = sys.argv[1]; lo, hi = int(sys.argv[2]), int(sys.argv[3])
    if which == "tight":
        insts = []
        for M in range(lo, hi + 1):
            for a in range(1, (M + 1) // 2 + 1):
                b = M + 1 - a
                if a < b: insts.append(((M, a, b), list(range(1, M + 1)), sorted(set(range(1, M + 2)) - {a, b})))
        run(f"tight family M={lo}..{hi}", insts)
    elif which == "twoomit":
        for h in range(lo, hi + 1):
            groups = collections.defaultdict(list)
            for a, b in itertools.combinations(range(1, h + 1), 2): groups[a + b].append((a, b))
            insts = [((h, ab, cd), sorted(set(range(1, h + 1)) - set(ab)), sorted(set(range(1, h + 1)) - set(cd))) for g in groups.values() for ab in g for cd in g if ab != cd]
            run(f"two-omission h={h}", insts)
    elif which == "merge":
        for h in range(lo, hi + 1):
            full = list(range(1, h + 1)); insts = []
            for a, b in itertools.combinations(full, 2):
                s = a + b
                if s in full: continue
                N = sorted(set(full) - {a, b} | {s}); insts.append(((h, a, b), full, N)); insts.append(((h, a, b, "rev"), N, full))
            run(f"merge h={h}", insts)
