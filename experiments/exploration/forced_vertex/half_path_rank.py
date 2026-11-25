"""Certify the balanced half-path rank inequality, exhaustively at small primes.

Run with Python 3.10+:
    python3 half_path_rank.py 2 3 5 7 11 13 17 19
    python3 half_path_rank.py 19 --size 15

Every positive result is a rank certificate. The seeded binary substitutions
give lower bounds, so an inconclusive instance is reported separately.
"""

import argparse
from functools import lru_cache
from itertools import combinations
from math import comb, isqrt
from random import Random


def interior_sets(p, labels, start, end, forbidden):
    """All interior vertex sets of simple half paths with the given endpoints."""
    result = set()

    def visit(remaining, vertex, interior):
        if remaining.bit_count() == 1:
            last = remaining.bit_length() - 1
            assert (vertex + last) % p == end
            result.add(interior)
            return
        choices = remaining
        while choices:
            bit = choices & -choices
            choices ^= bit
            dest = (vertex + bit.bit_length() - 1) % p
            dest_bit = 1 << dest
            if not dest_bit & (forbidden | interior):
                visit(remaining ^ bit, dest, interior | dest_bit)

    visit(labels, start, 0)
    return result


def exterior_masks(d):
    # Bit I of a wedge represents the basis monomial with index subset I.
    # Multiplication by e_j discards terms containing j, then adds j.
    return [
        sum(1 << index for index in range(1 << d) if not index & (1 << j))
        for j in range(d)
    ]


def certified_ranks(left, right, ground, masks, dimension, rng):
    d = len(masks)
    rng.shuffle(ground)
    coordinates = {}
    for i, v in enumerate(ground):
        vector = 0
        if i < d:
            vector = 1 << i
        elif d:
            vector = rng.randrange(1, 1 << d)
        coordinates[v] = tuple(j for j in range(d) if vector & (1 << j))

    @lru_cache(maxsize=None)
    def wedge(vertices):
        if not vertices:
            return 1
        bit = vertices & -vertices
        previous = wedge(vertices ^ bit)
        product = 0
        for j in coordinates[bit.bit_length() - 1]:
            product ^= (previous & masks[j]) << (1 << j)
        return product

    def rank(family, target):
        pivots = {}
        for vertices in family:
            row = wedge(vertices)
            while row:
                pivot = row.bit_length()
                if pivot not in pivots:
                    pivots[pivot] = row
                    break
                row ^= pivots[pivot]
            if len(pivots) >= target:
                break
        return len(pivots)

    left_rank = rank(left, dimension)
    right_rank = rank(right, dimension + 1 - left_rank)
    wedge.cache_clear()
    return left_rank, right_rank


def split_bounds(p, tail, first, middle, x, masks, dimension, rng, trials):
    forbidden = 3 | (1 << middle) | (1 << x)  # 0, 1, middle, x
    left = interior_sets(p, first, 1, middle, forbidden)
    right = interior_sets(p, tail ^ first, middle, 0, forbidden)
    if min(len(left), dimension) + min(len(right), dimension) <= dimension:
        return 0, 0
    ground = [v for v in range(p) if not forbidden & (1 << v)]
    best_left = best_right = 0
    for _ in range(trials):
        a, b = certified_ranks(left, right, ground, masks, dimension, rng)
        # Both bounds hold over the common rational function field, even
        # when the best ranks arise from different binary substitutions.
        best_left, best_right = max(best_left, a), max(best_right, b)
        if best_left + best_right > dimension:
            break
    return best_left, best_right


def certify(p, tail, splits, x, masks, dimension, rng, trials):
    for first, middle in splits:
        if middle in (0, 1, x):
            continue
        a, b = split_bounds(p, tail, first, middle, x, masks, dimension, rng, trials)
        if a + b > dimension:
            return True
    return False


def census(p, n):
    rng = Random(475 * p + n)
    m, k, d = n - 1, (n - 1) // 2, n - 3
    dimension = comb(d, k - 1)
    masks = exterior_masks(d)
    tested = misses = 0
    for elements in combinations(range(2, p), m):
        if (sum(elements) + 1) % p:
            continue
        B = {1, *elements}
        if all(p - b in B for b in B):
            continue
        tail = sum(1 << a for a in elements)
        splits = [
            (sum(1 << a for a in subset), (1 + sum(subset)) % p)
            for subset in combinations(elements, k)
        ]
        rng.shuffle(splits)
        for x in range(2, p):
            if 2 * x % p == 1:
                continue
            tested += 1
            if not any(certify(p, tail, splits, x, masks, dimension, rng, trials)
                       for trials in (3, 64)):
                misses += 1
                print("inconclusive", p, sorted(B), 1, x, flush=True)
    return tested, misses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("primes", nargs="+", type=int)
    parser.add_argument("--size", type=int)
    args = parser.parse_args()
    for p in args.primes:
        if p < 2 or any(p % j == 0 for j in range(2, isqrt(p) + 1)):
            parser.error(f"{p} is not prime")
        if p == 13 and args.size in (None, 9):
            tail = sum(1 << a for a in (2, 3, 5, 6, 7, 8, 9, 11))
            first = sum(1 << a for a in (3, 6, 8, 11))
            a, b = split_bounds(13, tail, first, 3, 4, exterior_masks(6), 20, Random(475), 64)
            assert (a, b) == (12, 9)
            print(f"worked split at p=13: ranks at least ({a}, {b})", flush=True)
        # A nonempty zero-sum complement of fewer than three nonzero labels
        # is an inverse pair. Thus asymmetric B has 3 <= |B| <= p-4.
        sizes = range(3, p - 3)
        if args.size is not None:
            sizes = [args.size] if args.size in sizes else []
        total = misses = 0
        for n in sizes:
            count, inconclusive = census(p, n)
            print(f"p={p} n={n} instances={count} inconclusive={inconclusive}", flush=True)
            total += count
            misses += inconclusive
        print(f"p={p} total={total} certified={total - misses} inconclusive={misses}", flush=True)


if __name__ == "__main__":
    main()
