"""Bounded, resumable, stratified IT5 witness search. Run with --help."""

import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from verify_interval_lift import check_pair, seed, steps


def stratum(T):
    M = -T[0]
    magnitudes = sorted({abs(x) for x in T})
    if M in T:
        family = "paired-maximum"
    elif len(magnitudes) == 4:
        family = "paired-interior"
    else:
        negatives = sum(x < 0 for x in T)
        family = {1: "one-four", 2: "two-three-max-on-two",
                  3: "two-three-max-on-three"}[negatives]
    gap = min(b - a for a, b in zip(magnitudes, magnitudes[1:]))
    return family + ("/separated" if gap >= 3 else "/close")


def sample(M, per_stratum):
    groups = defaultdict(list)
    for a, b, c in combinations((v for v in range(1 - M, M + 1) if v), 3):
        d = M - a - b - c
        if not c < d <= M or d == 0:
            continue
        T = (-M, a, b, c, d)
        if d == M and T > tuple(-x for x in reversed(T)):
            continue
        rank = hashlib.blake2s(str(T).encode(), digest_size=8).digest()
        group = groups[stratum(T)]
        group.append((rank, T))
        group.sort()
        if len(group) > per_stratum:
            group.pop()
    return sorted(T for group in groups.values() for _, T in group)


def signature(T, P):
    magnitudes = [v for v in range(1, -T[0] + 1) if v not in T and -v not in T]
    positive = set(steps(P))
    pattern = tuple(v in positive for v in magnitudes)
    for name, test in (("rank", tuple(i % 2 == 0 for i in range(len(pattern)))),
                       ("parity", tuple(v % 2 == 0 for v in magnitudes))):
        if pattern == test:
            return name + "+"
        if pattern == tuple(not value for value in test):
            return name + "-"
    raise AssertionError("unexpected signature")


def load_rows(path):
    rows = {}
    if path.exists():
        # Drop an interrupted final append so the same instance is retried.
        with path.open("rb+") as stream:
            while True:
                offset = stream.tell()
                line = stream.readline()
                if not line:
                    break
                if not line.endswith(b"\n"):
                    stream.truncate(offset)
                    break
                row = json.loads(line)
                T = tuple(row["T"])
                if row["status"] == "witness":
                    pair = tuple(tuple(p) for p in row["paths"])
                    check_pair(1 - T[0], T, pair)
                    assert signature(T, pair[0]) == row["signature"]
                rows[T] = row
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--lo", type=int, default=15)
    parser.add_argument("--hi", type=int, default=30)
    parser.add_argument("--per-stratum", type=int, default=4)
    parser.add_argument("--budget", type=int, default=120)
    parser.add_argument("--seconds", type=int, default=90)
    args = parser.parse_args()
    if not __debug__ or not (15 <= args.lo <= args.hi <= 30 and
            1 <= args.per_stratum <= 100 and 1 <= args.budget <= 10000 and args.seconds > 0):
        parser.error("run with assertions, heights 15..30, sample size 1..100 and budget 1..10000")
    until = time.monotonic() + args.seconds
    rows = load_rows(args.output)
    with args.output.open("a") as out:
        for M in range(args.lo, args.hi + 1):
            for T in sample(M, args.per_stratum):
                if time.monotonic() >= until:
                    print("Time cap reached. Rerun the same command to resume.")
                    return
                old = rows.get(T)
                if old and (old["status"] == "witness" or old["budget"] >= args.budget):
                    continue
                pair = seed(T, M, args.budget)
                row = dict(T=T, case=stratum(T), budget=args.budget, status="inconclusive")
                if pair is not None:
                    check_pair(M + 1, T, pair)
                    row.update(status="witness", paths=pair, signature=signature(T, pair[0]))
                out.write(json.dumps(row, separators=(",", ":")) + "\n")
                out.flush()
                rows[T] = row
    print(dict(Counter(row["status"] for row in rows.values())))


if __name__ == "__main__":
    main()
