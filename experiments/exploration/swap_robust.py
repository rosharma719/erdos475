"""For zero-sum B and root z: over ALL valid rooted cycles, what is the maximum fraction of internal vertices s_2..s_{k-1} removable by a single
valid adjacent (non-root) swap?  Is a fully swap-robust cycle (fraction 1) always available?"""
import itertools, sys, collections

def rooted_cycles(B, p, z):
    rest = [x for x in B if x != z]; out = []
    k = len(B)
    def rec(seq, used, s, seen):
        if len(seq) == k: out.append(tuple(seq)); return
        last = len(seq) == k - 1
        for i, a in enumerate(rest):
            if used >> i & 1: continue
            t = (s + a) % p
            if last:
                if t == 0: out.append(tuple(seq) + (a,))
                continue
            if t in seen: continue
            seen.add(t); seq.append(a)
            rec(seq, used | 1 << i, t, seen)
            seq.pop(); seen.discard(t)
    rec([z], 0, z % p, {0, z % p})
    return out

def verts(a, p):
    s = 0; V = [0]
    for x in a[:-1]: s = (s + x) % p; V.append(s)
    return V

def removable_fraction(a, p):
    k = len(a); V = verts(a, p); good = 0; tot = 0
    for i in range(2, k):                       # vertex index i, swap steps (i, i+1) 1-indexed => a[i-1], a[i]
        tot += 1
        b = list(a); b[i - 1], b[i] = b[i], b[i - 1]
        if len(set(verts(b, p))) == k: good += 1
    return good, tot

def run(p, kmin, kmax):
    for k in range(kmin, kmax + 1):
        hist = collections.Counter(); nosets = 0; fully = 0; total = 0
        for B in itertools.combinations(range(1, p), k):
            if sum(B) % p: continue
            for z in B:
                cyc = rooted_cycles(B, p, z)
                if not cyc: continue
                total += 1
                best = max(removable_fraction(a, p)[0] / max(1, removable_fraction(a, p)[1]) for a in cyc)
                if best == 1.0: fully += 1
                hist[round(best, 2)] += 1
        print(f"p={p} k={k}: (set,root) pairs {total}; some cycle has ALL internal vertices swap-removable: {fully} ({100*fully/max(1,total):.1f}%); lowest best-fraction {min(hist) if hist else None}", flush=True)

if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
