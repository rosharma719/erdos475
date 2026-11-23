"""BR_m (block-realizability): an ordered tuple t=(x_1..x_m) of distinct elements of zero-sum A (m<k) with every contiguous
sub-sum nonzero (the necessary condition inside the block) is consecutive in SOME valid cycle of A?  Test all tuples for each m."""
import sys, itertools, collections
sys.path.insert(0, "experiments/exploration")
from pattern_realizability import all_cycles

def admissible(t, p):
    m = len(t)
    return all(sum(t[i:j]) % p for i in range(m) for j in range(i + 1, m + 1))

def run(p, ms, kmin, kmax, show=5):
    for m in ms:
        tot = fail = 0; ex = []; byk = collections.defaultdict(lambda: [0, 0])
        for k in range(max(kmin, m + 1), kmax + 1):
            for A in itertools.combinations(range(1, p), k):
                if sum(A) % p: continue
                cyc = all_cycles(A, p); n = k
                seen = set()
                for c in cyc:
                    for i in range(n):
                        seen.add(tuple(c[(i + j) % n] for j in range(m)))
                for t in itertools.permutations(A, m):
                    if not admissible(t, p): continue
                    tot += 1; byk[k][0] += 1
                    if t not in seen:
                        fail += 1; byk[k][1] += 1
                        if len(ex) < show: ex.append((A, t))
        print(f"p={p} m={m} sizes {max(kmin,m+1)}..{kmax}: admissible tuples {tot}, NOT realised {fail}", flush=True)
        print("   by |A|: " + ", ".join(f"k={k}: {v[1]}/{v[0]}" for k, v in sorted(byk.items())), flush=True)

if __name__ == "__main__":
    p = int(sys.argv[1]); ms = list(map(int, sys.argv[2].split(","))); run(p, ms, int(sys.argv[3]), int(sys.argv[4]))
