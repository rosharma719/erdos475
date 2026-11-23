"""Independent audit of the cycle-flexibility note.
EC: zero-sum B, root z∈B, r∉B∪{0}: some valid cycle with first step z avoids vertex r.
MC (|B|>=5): same for EVERY r∉{0,z} (including r∈B).  Also: rotation-boundary count, hole-transport example, k=4 inverse-pair claim."""
import itertools, sys, random

def find(B, p, z, r, rng, cap):
    """valid cycle (steps) with first step z whose vertex set avoids r; None=undetermined, False=none exists, list=found."""
    k = len(B); B = list(B); n = [0]
    first = [z]; used = {z}; S = [0, z % p]
    if r == z % p or r == 0: return False
    seen = {0, z % p}
    seq = [z]
    def rec():
        n[0] += 1
        if n[0] > cap: return None
        if len(seq) == k: return True
        last_step = (len(seq) == k - 1)
        cand = [a for a in B if a not in used]; rng.shuffle(cand)
        for a in cand:
            t = (S[-1] + a) % p
            if last_step:
                if t == 0: seq.append(a); return True
                continue
            if t in seen or t == r: continue
            seen.add(t); S.append(t); seq.append(a); used.add(a)
            res = rec()
            if res: return True
            seq.pop(); used.discard(a); S.pop(); seen.discard(t)
            if res is None: return None
        return False
    res = rec()
    return list(seq) if res else (None if res is None else False)

def run(p, kmin, kmax, sample=None, seed=1, cap=200000):
    rng = random.Random(seed); ec_fail = mc_fail = und = tot_ec = tot_mc = 0; nocycle = 0
    for k in range(kmin, kmax + 1):
        sets = [B for B in itertools.combinations(range(1, p), k) if sum(B) % p == 0]
        if sample and len(sets) > sample: sets = rng.sample(sets, sample)
        for B in sets:
            Bs = set(B)
            for z in B:
                if find(B, p, z, p + 5, rng, cap) is False and False: pass
                anycyc = find(B, p, z, (z + 1) % p if (z + 1) % p not in (0, z) else (z + 2) % p, rng, cap)   # probe existence quickly below
                for r in range(1, p):
                    if r == z: continue
                    res = find(B, p, z, r, rng, cap)
                    if res is None:
                        res = find(B, p, z, r, rng, cap * 20)
                    if res is None: und += 1; continue
                    ext = r not in Bs
                    if ext: tot_ec += 1
                    if k >= 5: tot_mc += 1
                    if res is False:
                        if ext: ec_fail += 1; print("  EC FAIL", p, B, z, r, flush=True)
                        elif k >= 5: mc_fail += 1; print("  MC-only fail", p, B, z, r, flush=True)
                        elif k <= 4: pass
    print(f"p={p} sizes {kmin}..{kmax}{' sampled '+str(sample) if sample else ''}: EC checks {tot_ec} fail {ec_fail}; MC (k>=5, r in B too) checks {tot_mc} extra failures {mc_fail}; undetermined {und}", flush=True)

if __name__ == "__main__":
    p, lo, hi = map(int, sys.argv[1:4]); samp = int(sys.argv[4]) if len(sys.argv) > 4 else None
    run(p, lo, hi, samp)
