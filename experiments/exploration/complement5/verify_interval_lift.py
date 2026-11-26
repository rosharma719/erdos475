"""Verify the boundary-seed lift and enumerate integer five-hole instances.

Run: python3 verify_interval_lift.py --height 12
"""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import chain, combinations
from math import comb, isqrt


def steps(path):
    return tuple(b - a for a, b in zip(path, path[1:]))


def lift_once(q, pair):
    """Extend a boundary seed on [0,q-1] to [0,q]."""
    left, right = pair
    assert left[0] == right[0] == 0
    return tuple((0,) + tuple(q - v for v in path) for path in (right, left))


def find_path(M, start, labels, budget=None):
    target = start + sum(labels)
    if not 0 <= target <= M or (labels and target == start):
        return None
    labels = tuple(sorted(labels, key=abs, reverse=True))

    @lru_cache(None)
    def search(v, free, remaining):
        nonlocal budget
        if not remaining:
            return (v,) if v == target else None
        if budget is not None:
            if budget <= 0:
                return None
            budget -= 1
        # Every remaining step needs an available source and target.
        sources = free | (1 << v)
        for d in remaining:
            possible = sources << d if d > 0 else sources >> -d
            if not possible & free:
                return None
        for i, d in enumerate(remaining):
            u = v + d
            if not 0 <= u <= M or not (free & (1 << u)):
                continue
            if (u == target) != (len(remaining) == 1):
                continue
            tail = search(u, free ^ (1 << u), remaining[:i] + remaining[i + 1:])
            if tail is not None:
                return (v,) + tail
        return None

    path = search(start, ((1 << (M + 1)) - 1) ^ (1 << start), labels)
    search.cache_clear()
    return path


def seed(H, M, budget=None, *, common_choices=None):
    paired = [j for j in range(1, M + 1) if j not in H and -j not in H]
    singles = [-h for h in sorted(H) if -h not in H]
    alternating = tuple(v if i % 2 == 0 else -v for i, v in enumerate(paired))
    parity = tuple(v if v % 2 == 0 else -v for v in paired)
    preferred = (alternating, tuple(-v for v in alternating),
                 parity, tuple(-v for v in parity))
    all_signs = (tuple(v if bits & (1 << i) else -v for i, v in enumerate(paired))
                 for bits in range(1 << len(paired)))
    choices = preferred if budget is not None else chain(preferred, all_signs)
    if common_choices is not None:
        choices = common_choices
    for common in choices:
        for bits in range(1 << len(singles)):
            first = common + tuple(a for i, a in enumerate(singles) if bits & (1 << i))
            second = common + tuple(-a for i, a in enumerate(singles) if not bits & (1 << i))
            if max(len(first), len(second)) > M or not 0 < sum(first) <= M:
                continue
            if -M in first or -M in second:
                continue
            left = find_path(M, 0, first, budget)
            if left is not None:
                right = find_path(M, 0, second, budget)
                if right is not None:
                    return left, right
    return None


def check_pair(q, H, pair):
    P, Q = pair
    for path in pair:
        assert len(set(path)) == len(path) and min(path) >= 0 and max(path) < q
    assert P[0] == Q[0] == 0 and P[-1] == Q[-1] and P[-1] != 0
    wanted = {v for v in range(1 - q, q) if v and v not in H}
    assert Counter(steps(P) + tuple(-v for v in steps(Q))) == Counter(wanted)
    vertices = P + tuple(q + v for v in reversed(Q))
    modulus = 2 * q + 1
    assert len(set(vertices)) == len(vertices)
    colors = Counter(v % modulus for v in steps(vertices + vertices[:1]))
    omitted = {h % modulus for h in H}
    assert colors == Counter(v for v in range(1, modulus) if v not in omitted)
    return vertices


def prime_orbits(p):
    # Each orbit contains a set with 1. Its representatives containing 1
    # are found by normalizing each of its five entries in turn.
    seen = set()
    for a, b, c in combinations(range(2, p), 3):
        d = -(1 + a + b + c) % p
        if d <= c:
            continue
        H = (1, a, b, c, d)
        if H in seen:
            continue
        for h in H:
            inv = pow(h, -1, p)
            seen.add(tuple(sorted(inv * v % p for v in H)))
        yield H


def check_prime_seed(p, H, unit, pair):
    r = p // 2
    T = {(unit * h + r) % p - r for h in H}
    q = 1 + max(map(abs, T))
    assert sum(T) == 0 and q <= r
    check_pair(q, T, pair)
    while q < r:
        pair = lift_once(q, pair)
        q += 1
    vertices = check_pair(r, T, pair)
    inv = pow(unit, -1, p)
    vertices = tuple(v * inv % p for v in vertices)
    assert len(vertices) == len(set(vertices)) == p - 6
    colors = Counter(v % p for v in steps(vertices + vertices[:1]))
    assert colors == Counter(set(range(1, p)) - set(H))


def prime_census(p):
    r = p // 2
    total = missed = 0
    for H in prime_orbits(p):
        total += 1
        lifts = []
        for unit in range(1, p):
            T = tuple(sorted((unit * h + r) % p - r for h in H))
            M = max(map(abs, T))
            if sum(T) == 0 and M < r:
                lifts.append((M, T, unit))
        lifts.sort()
        found = False
        for budget in (300, 3000, 30000):
            for M, T, unit in lifts:
                pair = seed(T, M, budget)
                if pair is not None:
                    check_prime_seed(p, H, unit, pair)
                    found = True
                    break
            if found:
                break
        if not found:
            missed += 1
            print("prime search inconclusive", p, H, flush=True)
    sets = 0
    if p > 5:
        sets = 1
        for j in range(1, 6):
            sets = comb(p, j) // p - sets
    short_orbit = (p - 1) // 5 if p % 5 == 1 else 0
    assert total * (p - 1) == sets + 4 * short_orbit
    print(f"p={p} orbits={total} certified={total - missed} five-sets={sets}", flush=True)
    if missed:
        raise SystemExit("Some orbits have no certificate in this search.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--height", type=int)
    parser.add_argument("--primes", nargs="+", type=int, default=[])
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("Run with assertions enabled to verify the constructions.")
    for p in args.primes:
        if p < 3 or any(p % j == 0 for j in range(2, isqrt(p) + 1)):
            parser.error(f"{p} must be an odd prime")
        prime_census(p)
    height = args.height if args.height is not None else (0 if args.primes else 14)
    for M in range(3, height + 1):
        passed = total = 0
        for four in combinations([v for v in range(-M, M + 1) if v], 4):
            last = -sum(four)
            if not four[-1] < last <= M or last == 0 or max(-four[0], last) != M:
                continue
            H = frozenset((*four, last))
            total += 1
            pair = seed(H, M)
            if pair is None:
                print("seed search inconclusive", sorted(H), flush=True)
                continue
            q = M + 1
            check_pair(q, H, pair)
            for _ in range(4):
                pair = lift_once(q, pair)
                q += 1
                check_pair(q, H, pair)
            passed += 1
        print(f"height={M} integer five-sets={total} certified seeds={passed}", flush=True)
        if passed != total:
            raise SystemExit("Some integer five-sets have no certificate in this search.")


if __name__ == "__main__":
    main()
