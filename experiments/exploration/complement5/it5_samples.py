"""Bounded, resumable, stratified IT5 witness search. Run with --help."""

import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

from it5_nested import normalized_sets
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
    for T in normalized_sets(M):
        rank = hashlib.blake2s(str(T).encode(), digest_size=8).digest()
        group = groups[stratum(T)]
        group.append((rank, T))
        group.sort()
        if len(group) > per_stratum:
            group.pop()
    return sorted(T for group in groups.values() for _, T in group)


def patterns(T):
    magnitudes = [v for v in range(1, -T[0] + 1) if v not in T and -v not in T]
    for name, base in (("rank", [v if i % 2 == 0 else -v for i, v in enumerate(magnitudes)]),
                       ("parity", [v if v % 2 == 0 else -v for v in magnitudes])):
        yield name + "+", tuple(base)
        yield name + "-", tuple(-v for v in base)


def flipped_patterns(T):
    seen = {seq for _, seq in patterns(T)}
    for name, seq in patterns(T):
        for i, v in enumerate(seq):
            altered = seq[:i] + (-v,) + seq[i + 1:]
            if altered not in seen:
                seen.add(altered)
                yield f"{name}/flip{abs(v)}", altered


def signature(T, P):
    signed = set(steps(P))
    for choices in (patterns(T), flipped_patterns(T)):
        for name, seq in choices:
            if all(v in signed for v in seq):
                return name
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
    parser.add_argument("--all", action="store_true", help="enumerate every normalized input")
    parser.add_argument("--flip-one", action="store_true", help="also try flipping one common sign")
    parser.add_argument("--seconds", type=int, default=90)
    args = parser.parse_args()
    if not __debug__ or not (15 <= args.lo <= args.hi <= 30 and
            1 <= args.per_stratum <= 100 and 1 <= args.budget <= 10000 and args.seconds > 0):
        parser.error("run with assertions, heights 15..30, sample size 1..100 and budget 1..10000")
    until = time.monotonic() + args.seconds
    rows = load_rows(args.output)
    with args.output.open("a") as out:
        for M in range(args.lo, args.hi + 1):
            inputs = normalized_sets(M) if args.all else sample(M, args.per_stratum)
            for T in inputs:
                if time.monotonic() >= until:
                    print("Time cap reached. Rerun the same command to resume.")
                    return
                old = rows.get(T)
                if old and (old["status"] == "witness" or
                            (old["budget"] >= args.budget and
                             (old.get("flip", False) or not args.flip_one))):
                    continue
                pair = seed(T, M, args.budget)
                if pair is None and args.flip_one:
                    pair = seed(T, M, args.budget,
                                common_choices=(s for _, s in flipped_patterns(T)))
                row = dict(T=T, case=stratum(T), budget=args.budget,
                           flip=args.flip_one, status="inconclusive")
                if pair is not None:
                    check_pair(M + 1, T, pair)
                    row.update(status="witness", paths=pair, signature=signature(T, pair[0]))
                out.write(json.dumps(row, separators=(",", ":")) + "\n")
                out.flush()
                rows[T] = row
    print(dict(Counter(row["status"] for row in rows.values())))


if __name__ == "__main__":
    main()
