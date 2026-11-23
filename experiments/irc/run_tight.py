"""Exact zigzag tests on (a) GPT's tight family P=[1,M], N=[1,M+1]\\{a,b}, a+b=M+1 and (b) P=[1,h]\\{1,4}, N=[1,h]\\{2,3} (annealing failed at h>=20) and other 2-omission pairs, h=11..16."""
import sys, collections, itertools
sys.path.insert(0, "experiments/irc")
from run_zigzag import run
def tight(Mmax):
    out = []
    for M in range(3, Mmax + 1):
        for a in range(1, (M + 1) // 2 + 1):
            b = M + 1 - a
            if a >= b: continue
            out.append(((M, a, b), (list(range(1, M + 1)), sorted(set(range(1, M + 2)) - {a, b}))))
    return out
def two_omission(h, limit=None):
    out = []; groups = collections.defaultdict(list)
    for a, b in itertools.combinations(range(1, h + 1), 2): groups[a + b].append((a, b))
    for pairs in groups.values():
        for ab in pairs:
            for cd in pairs:
                if ab != cd:
                    out.append(((h, ab, cd), (sorted(set(range(1, h + 1)) - set(ab)), sorted(set(range(1, h + 1)) - set(cd)))))
    return out
if __name__ == "__main__":
    which = sys.argv[1]
    if which == "tight":
        T = tight(int(sys.argv[2])); res = run([i for _, i in T]); c = collections.Counter(res)
        print(f"tight family M<={sys.argv[2]}: {len(T)} pairs; found {c[1]}, NONE {c[0]}, undet {c[-1]}", flush=True)
        for (meta, _), v in zip(T, res):
            if v != 1: print("   ", "NONE" if v == 0 else "UNDET", meta, flush=True)
    else:
        for h in map(int, sys.argv[2:]):
            T = two_omission(h); res = run([i for _, i in T]); c = collections.Counter(res)
            print(f"two-omission h={h}: {len(T)} pairs; found {c[1]}, NONE {c[0]}, undet {c[-1]}", flush=True)
            for (meta, _), v in zip(T, res):
                if v != 1: print("   ", "NONE" if v == 0 else "UNDET", meta, flush=True)
