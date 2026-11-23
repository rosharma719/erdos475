"""INDEPENDENT audit of the NC3Z construction (written from the proof text, not from GPT's script).
For every prime 11<=p<=LIMIT and every zero-sum 3-subset C of F_p^*:
  1. find nu and t with nu*C = C_t = {-1, t, 1-t}, 3<=t<=r-1 (trying the proof's normalisation: send each element to -1, and the x2 fix for t=r);
  2. build the Walecki rotational sequencing, check its vertices are 2r distinct nonzero residues (every proper cyclic interval nonzero);
  3. contract P=(delta_i,delta_{i+1}) (i=r-t) and Q=(delta_{r-1},r,-delta_{r-1}) simultaneously;
  4. check labels == F_p^* minus eps*C_t, then scale and check the result is a valid ordering of F_p^* \\ C (all partial sums distinct)."""
import itertools, sys

def walecki(r):
    a, lo, hi, take_lo = [], 1, r, True
    while lo <= hi:
        if take_lo: a.append(lo); lo += 1
        else: a.append(hi); hi -= 1
        take_lo = not take_lo
    return a

def normalise(C, p):
    r = (p - 1) // 2
    for x in C:                                   # send x -> -1
        nu = (-pow(x, -1, p)) % p
        N = {(nu * c) % p for c in C}
        signed = sorted(((c if c <= r else c - p) for c in N))
        others = [s for s in signed if s != -1]
        pos = [s for s in others if s > 0]
        if len(pos) == 1 and -1 in {s for s in signed}:
            t = pos[0]
            if t == r:                            # proof: multiply by 2 -> {-2,-1,3}
                nu = 2 * nu % p; N = {(nu * c) % p for c in C}; t = 3
                if N != {p - 1, 3, (1 - 3) % p}: continue
            if 3 <= t <= r - 1 and N == {p - 1, t % p, (1 - t) % p}:
                return nu, t
    return None

def construct(p, C):
    r = (p - 1) // 2
    nm = normalise(C, p)
    if nm is None: return "no-normalisation"
    nu, t = nm
    al = walecki(r)
    d = [al[i + 1] - al[i] for i in range(r - 1)]
    assert all(d[i - 1] == (-1) ** (i + 1) * (r - i) for i in range(1, r))     # proof's formula for delta_i
    B = d + [r] + [-x for x in reversed(d)] + [-r]
    Bm = [x % p for x in B]
    # B is a rotational sequencing: all residues once, partial sums distinct (vertices 2r distinct)
    if sorted(Bm) != list(range(1, p)): return "B-labels"
    S = list(itertools.accumulate(Bm, lambda s, x: (s + x) % p))
    if len(set(S)) != len(S): return "B-not-simple"
    i = r - t                                      # 1-indexed position of delta_i
    eps = (-1) ** (i + 1)
    if (B[i - 1] + B[i]) != eps or B[i - 1] != eps * t: return "P-block"
    eta = B[r - 2]                                 # delta_{r-1}, position r-1
    if abs(eta) != 1 or B[r - 1] != r or B[r] != -eta: return "Q-block"
    if not (i + 1 < r - 1): return "overlap"
    out, k = [], 1
    while k <= len(B):
        if k == i: out.append(eps % p); k += 2
        elif k == r - 1: out.append(r % p); k += 3
        else: out.append(B[k - 1] % p); k += 1
    exp = set(range(1, p)) - {(eps * c) % p for c in {(nu * x) % p for x in C}}
    if sorted(out) != sorted(exp) or len(out) != p - 4: return "labels"
    scale = (eps * pow(nu, -1, p)) % p
    # eps*C_t = eps*nu*C, so multiply labels by eps*nu^{-1}... verify directly
    for sc in (scale, pow(eps * nu, -1, p) if False else scale):
        res = [(sc * x) % p for x in out]
        if set(res) == set(range(1, p)) - set(C):
            ps = list(itertools.accumulate(res, lambda s, x: (s + x) % p))
            return "ok" if len(set(ps)) == len(ps) else "partial-sum-collision"
    return "rescale-mismatch"

def primes(a, b): return [q for q in range(a, b + 1) if all(q % d for d in range(2, int(q ** .5) + 1))]

if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 61
    tot = 0; bad = {}
    for p in primes(11, lim):
        n = 0
        for C in itertools.combinations(range(1, p), 3):
            if sum(C) % p: continue
            res = construct(p, C); n += 1; tot += 1
            if res != "ok": bad.setdefault(res, []).append((p, C))
        print(f"p={p}: zero-sum triples {n}", flush=True)
    print("TOTAL", tot, "failures:", {k: (len(v), v[:3]) for k, v in bad.items()})
