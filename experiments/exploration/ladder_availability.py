"""Top-down contraction ladder.  To get a valid cycle of A with x,y adjacent, take A+ = A\\{z} ∪ {a,b} (a,b ∉ A, a+b=z∈A\\{x,y}) and a valid
cycle of A+ with BOTH (a,b) and (x,y) adjacent, then contract (a,b) -> z (vertex subset, no side condition).
Availability = fraction of (A,{x,y}) for which some (z,a,b) satisfies the no-coincidence conditions for the two-pair pattern on A+.
Reports availability by complement size c = p-1-|A|."""
import random, itertools, sys, collections

def available(A, x, y, p):
    Aset = set(A); comp = [u for u in range(1, p) if u not in Aset]; cs = set(comp)
    s2 = (x + y) % p
    for z in A:
        if z in (x, y): continue
        for a in comp:
            b = (z - a) % p
            if b == a or b not in cs or b == 0: continue
            Ap = (Aset - {z}) | {a, b}
            rest = Ap - {a, b, x, y}
            if (z + s2) % p == 0 or z == s2 or s2 in rest or s2 == 0: continue
            return True
    return False

def run(p, trials, seed=1):
    rng = random.Random(seed); stat = collections.defaultdict(lambda: [0, 0])
    for _ in range(trials):
        k = rng.randint(5, p - 2)
        A = rng.sample(range(1, p), k)
        if sum(A) % p:
            # fix zero-sum by swapping one element if possible
            for _try in range(50):
                A = rng.sample(range(1, p), k)
                if sum(A) % p == 0: break
            else: continue
        x, y = rng.sample(A, 2)
        if (x + y) % p == 0: continue
        c = p - 1 - k
        stat[c][0] += 1; stat[c][1] += available(A, x, y, p)
    print(f"p={p}: availability of the ladder step by complement size c (available/total):")
    print("  " + ", ".join(f"c={c}: {v[1]}/{v[0]}" for c, v in sorted(stat.items())))

if __name__ == "__main__":
    for p in map(int, sys.argv[2:]): run(p, int(sys.argv[1]))
