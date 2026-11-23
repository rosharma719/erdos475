"""Check the exact equivalence: symmetric A={±a_i} has a half-cycle (s_1..s_m,-s_1..-s_m) valid  <=>  there are signs eps_j and DISTINCT classes
x_0..x_{m-1} in [1..r] with Q_j=eps_j x_j, Q_m=-Q_0, steps Q_j-Q_{j-1} having classes exactly {a_i}  (T=2Q_m... : P_j=Q_j+T/2).  Test both directions on solutions."""
import itertools, random, sys
sys.path.insert(0, "experiments/exploration")
from symmetric_half_cycle import half_cycle

def vp(seq, p):
    s = 0; seen = set()
    for x in seq:
        s = (s + x) % p
        if s in seen: return False
        seen.add(s)
    return s == 0

def cls(x, p): return min(x % p, (-x) % p)

def half_to_folded(steps, p):
    m = len(steps); P = [0]
    for s in steps: P.append((P[-1] + s) % p)
    T = P[-1]; half = pow(2, -1, p)
    Q = [(P[j] - T * half) % p for j in range(m + 1)]
    ok = Q[m] == (-Q[0]) % p and len({cls(q, p) for q in Q[:m]}) == m and all(cls(q, p) != 0 for q in Q[:m])
    steps2 = [(Q[j] - Q[j - 1]) % p for j in range(1, m + 1)]
    return ok and steps2 == [s % p for s in steps]

def folded_to_cycle(Q, p):
    m = len(Q) - 1
    steps = [(Q[j] - Q[j - 1]) % p for j in range(1, m + 1)]
    return vp(steps + [(-s) % p for s in steps], p), steps

if __name__ == "__main__":
    rng = random.Random(3); n = bad1 = bad2 = 0
    for p in (11, 13, 17, 19):
        r = (p - 1) // 2
        for m in range(2, r + 1):
            for classes in itertools.combinations(range(1, r + 1), m):
                steps = half_cycle(classes, p, rng)
                if not steps: continue
                n += 1
                if not half_to_folded(steps, p): bad1 += 1
                # reverse direction: rebuild Q from the folded data and confirm the cycle is valid and has the right set
                P = [0]
                for s in steps: P.append((P[-1] + s) % p)
                T = P[-1]; half = pow(2, -1, p); Q = [(P[j] - T * half) % p for j in range(m + 1)]
                ok, st = folded_to_cycle(Q, p)
                if not ok or sorted(cls(s, p) for s in st) != sorted(classes): bad2 += 1
    print(f"solutions tested {n}; half->folded violations {bad1}; folded->cycle violations {bad2}")
