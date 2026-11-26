"""Arithmetic test and construction for IT5 with a common descending tail."""

import argparse
import json
import time
from itertools import accumulate, combinations, permutations
from pathlib import Path

from verify_interval_lift import check_pair, lift_once


def bands(height, absent):
    previous = height + 1
    for gap in sorted(set(absent) | {0}, reverse=True):
        if gap > height:
            continue
        if previous - 1 > gap:
            yield previous - 1, gap + 1
        previous = gap


def band_intervals(z, sign, high, low):
    count = high - low + 1
    even = z + sign * (count // 2)
    odd_first = z + sign * high
    odd_last = odd_first - sign * ((count - 1) // 2)
    intervals = (tuple(sorted((z, even))), tuple(sorted((odd_first, odd_last))))
    return intervals, odd_last if count % 2 else even, -sign if count % 2 else sign


def choose_prefixes(holes):
    M = max(map(abs, holes))
    singles = tuple(sorted(-h for h in holes if -h not in holes))
    height = max(map(abs, singles))
    absent = {abs(h) for h in holes if abs(h) <= height}
    runs = tuple(bands(height, absent))
    for ordered in permutations(singles):
        for cut in range(1, len(ordered)):
            P = tuple(accumulate(ordered[:cut], initial=0))
            Q = tuple(accumulate((-a for a in ordered[cut:]), initial=0))
            y = P[-1]
            if not 0 < y <= height or any(
                min(path) < 0 or max(path) > height or len(path) != len(set(path))
                for path in (P, Q)
            ):
                continue
            forbidden = set(P[:-1]) | set(Q[:-1])
            for first_sign in (-1, 1):
                z, sign = y, first_sign
                for high, low in runs:
                    spans, z, sign = band_intervals(z, sign, high, low)
                    if any(lo < 0 or hi > height or any(lo <= x <= hi for x in forbidden)
                           for lo, hi in spans):
                        break
                else:
                    return M, height, runs, P, Q, first_sign
    return None


def construct(plan):
    M, height, runs, P, Q, sign = plan
    tail = []
    z = P[-1]
    for high, low in runs:
        for magnitude in range(high, low - 1, -1):
            z += sign * magnitude
            tail.append(z)
            sign *= -1
    pair = (P + tuple(tail), Q + tuple(tail))
    for q in range(height + 1, M):
        pair = lift_once(q, pair)
    return pair


def normalized_sets(M):
    for a, b, c in combinations((v for v in range(1 - M, M + 1) if v), 3):
        d = M - a - b - c
        if not c < d <= M or not d:
            continue
        T = (-M, a, b, c, d)
        if d != M or T <= tuple(-x for x in reversed(T)):
            yield T


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lo", type=int, default=15)
    parser.add_argument("--hi", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=60)
    args = parser.parse_args()
    if not __debug__ or not 3 <= args.lo <= args.hi <= 40 or args.seconds <= 0:
        parser.error("use assertions, 3 <= lo <= hi <= 40 and a positive time cap")
    args.output.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + args.seconds
    count = hits = 0
    for M in range(args.lo, args.hi + 1):
        file = args.output / f"height-{M}.jsonl"
        done = set()
        if file.exists():
            with file.open("rb+") as source:
                while True:
                    offset = source.tell()
                    line = source.readline()
                    if not line:
                        break
                    if not line.endswith(b"\n"):
                        source.truncate(offset)
                        break
                    row = json.loads(line)
                    done.add(tuple(row["T"]))
        with file.open("a") as output:
            for T in normalized_sets(M):
                if time.monotonic() >= deadline:
                    print(f"time cap; added {count} rows, {hits} certificates")
                    return
                if T in done:
                    continue
                plan = choose_prefixes(T)
                row = {"T": T, "hit": plan is not None}
                if plan is not None:
                    pair = construct(plan)
                    check_pair(M + 1, T, pair)
                    row.update(prefixes=plan[3:5], first_sign=plan[5])
                    hits += 1
                output.write(json.dumps(row, separators=(",", ":")) + "\n")
                output.flush()
                count += 1
    print(f"completed; added {count} rows, {hits} certificates")


if __name__ == "__main__":
    main()
