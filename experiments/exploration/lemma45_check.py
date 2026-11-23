"""Free local check of HOS Lemma 4.5 as used by the inverse-pair proof: for r>=9, every d in 1..r-1 admits a graceful
permutation of [1..r] whose FIRST absolute difference is d (reverse for last). Fast DFS, most-constrained difference first."""
import sys
sys.setrecursionlimit(10000)

def find(r, d, node_cap=3_000_000):
    cnt = [0]
    for x in range(1, r + 1):
        for y in (x - d, x + d):
            if not 1 <= y <= r: continue
            used = 1 << x | 1 << y; diffs = 1 << d; path = [x, y]
            def rec():
                cnt[0] += 1
                if cnt[0] > node_cap: return None
                if len(path) == r: return True
                last = path[-1]
                cands = []
                for z in range(1, r + 1):
                    if used >> z & 1: continue
                    dd = abs(z - last)
                    if diffs >> dd & 1: continue
                    cands.append((-dd, z))        # try big differences first
                cands.sort()
                for _, z in cands:
                    dd = abs(z - last); used_bit = 1 << z; diff_bit = 1 << dd
                    globals_ = None
                    nonlocal_used[0] |= used_bit; nonlocal_diffs[0] |= diff_bit
                    path.append(z)
                    res = rec()
                    if res: return True
                    path.pop(); nonlocal_used[0] &= ~used_bit; nonlocal_diffs[0] &= ~diff_bit
                    if res is None: return None
                return False
            nonlocal_used = [used]; nonlocal_diffs = [diffs]
            # rebind closures to mutable cells
            def rec2():
                cnt[0] += 1
                if cnt[0] > node_cap: return None
                if len(path) == r: return True
                last = path[-1]
                cands = sorted(((-abs(z - last), z) for z in range(1, r + 1)
                                if not (nonlocal_used[0] >> z & 1) and not (nonlocal_diffs[0] >> abs(z - last) & 1)))
                for _, z in cands:
                    dd = abs(z - last)
                    nonlocal_used[0] |= 1 << z; nonlocal_diffs[0] |= 1 << dd; path.append(z)
                    res = rec2()
                    if res: return True
                    path.pop(); nonlocal_used[0] &= ~(1 << z); nonlocal_diffs[0] &= ~(1 << dd)
                    if res is None: return None
                return False
            res = rec2()
            if res: return list(path)
            if res is None: return None
    return False

if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for r in range(lo, hi + 1):
        fails = {d: find(r, d) for d in range(1, r)}
        bad = [d for d, v in fails.items() if not v]
        print(f"r={r} (p={2*r+1}): missing d = {bad}", flush=True)
