"""How often can a vertex r of a valid rooted cycle be removed by (i) one adjacent swap, (ii) a hole-transport chain of <=L simultaneous
non-consecutive adjacent swaps?  Random zero-sum sets, random valid rooted cycles, every internal vertex r.  Reported by density k/p."""
import random, itertools, sys, collections

def random_valid_cycle(B, p, z, rng, cap=20000):
    k = len(B); n = [0]
    used = {z}; seq = [z]; S = [0, z % p]; seen = {0, z % p}
    def rec():
        n[0] += 1
        if n[0] > cap: return None
        if len(seq) == k: return True
        last = len(seq) == k - 1
        cand = [a for a in B if a not in used]; rng.shuffle(cand)
        for a in cand:
            t = (S[-1] + a) % p
            if last:
                if t == 0: seq.append(a); return True
                continue
            if t in seen: continue
            seen.add(t); S.append(t); seq.append(a); used.add(a)
            r = rec()
            if r: return True
            seq.pop(); used.discard(a); S.pop(); seen.discard(t)
            if r is None: return None
        return False
    return list(seq) if rec() else None

def vertices(a, p):
    s = 0; V = [0]
    for x in a[:-1]: s = (s + x) % p; V.append(s)
    return V

def rates(p, k, nsets, rng, L=3):
    stats = collections.Counter()
    tries = 0
    while stats["cycles"] < nsets and tries < nsets * 50:
        tries += 1
        B = rng.sample(range(1, p), k)
        if sum(B) % p: continue
        z = rng.choice(B)
        a = random_valid_cycle(B, p, z, rng)
        if not a: continue
        V = vertices(a, p); Vs = set(V); holes = set(range(p)) - Vs
        stats["cycles"] += 1
        # T_i (swap of steps i,i+1, 1-indexed steps; vertex index i changes): s_{i-1}+a_{i+1}
        T = {}
        for i in range(2, k):                       # vertex index i in 2..k-1, swaps steps i,i+1 (1-indexed)
            T[i] = (V[i - 1] + a[i]) % p            # a is 0-indexed: a[i] is step i+1
        for i0 in range(2, k):                      # target r = V[i0]
            stats["targets"] += 1
            if T[i0] in holes: stats["swap1"] += 1; stats["chain"] += 1; continue
            # chain: i_1=i0, T_{i_j} = V[i_{j+1}], nonconsecutive indices, end in a hole, length<=L
            found = False
            def dfs(path):
                nonlocal found
                if found or len(path) > L: return
                i = path[-1]; t = T[i]
                if t in holes: found = True; return
                for j in range(2, k):
                    if V[j] == t and all(abs(j - q) > 1 for q in path) and j not in path:
                        dfs(path + [j])
            dfs([i0])
            stats["chain"] += found
    return stats

if __name__ == "__main__":
    rng = random.Random(11)
    for p in map(int, sys.argv[2:]):
        for k in range(5, p - 2, max(1, (p - 8) // 8)):
            st = rates(p, k, int(sys.argv[1]), rng)
            if st["targets"]:
                print(f"p={p} k={k} (density {k/p:.2f}): cycles {st['cycles']}, targets {st['targets']}, "
                      f"one swap {100*st['swap1']/st['targets']:.0f}%, chain<=3 {100*st['chain']/st['targets']:.0f}%", flush=True)
