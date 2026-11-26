"""Find and verify affine extensions of the nested IT5 construction."""

import argparse
import json
import time
from collections import Counter, defaultdict
from itertools import accumulate
from pathlib import Path

from it5_nested import band_intervals, bands, construct, normalized_sets
from verify_interval_lift import check_pair


def sign_order(T):
    return tuple(x > 0 for x in sorted(T, key=abs))


def prefix_codes(T, prefixes):
    return [
        [(T.index(s), 1) if s in T else (T.index(-s), -1)
         for s in (b - a for a, b in zip(path, path[1:]))]
        for path in prefixes
    ]


def profile(T, codes, sign):
    M = -T[0]
    P, Q = (tuple(accumulate((T[i] * mul for i, mul in path), initial=0))
            for path in codes)
    assert P[-1] == Q[-1]
    tests = [P[-1]]
    for path in (P, Q):
        for i, x in enumerate(path):
            tests.extend((x, M - x))
            tests.extend(x - y for y in path[:i])
    z = P[-1]
    for high, low in bands(M, map(abs, T)):
        spans, z, sign = band_intervals(z, sign, high, low)
        for lo, hi in spans:
            tests.extend((lo, M - hi))
            for path in (P, Q):
                for x in path[:-1]:
                    tests.extend((lo - x, hi - x))
    return tests, P, Q


def stable(base, next_values):
    assert len(base) == len(next_values)
    return all((v >= u if u > 0 else v <= u if u < 0 else v == 0)
               for u, v in zip(base, next_values))


def check_ray(row):
    T, direction = tuple(row["T"]), tuple(row["D"])
    codes = prefix_codes(T, row["prefixes"])
    sign = row["first_sign"]
    for v in (T, direction):
        assert len(v) == len(set(map(abs, v))) == 5 and min(map(abs, v)) > 0
        assert tuple(sorted(v)) == v and sum(v) == 0 and -v[0] == max(map(abs, v))
    assert sorted(range(5), key=lambda i: abs(T[i])) == sorted(range(5), key=lambda i: abs(direction[i]))
    assert tuple(x > 0 for x in T) == tuple(x > 0 for x in direction)
    g = sorted(map(abs, T))
    assert min(g[0], *(b-a for a,b in zip(g,g[1:]))) >= 2
    old, _, _ = profile(T, codes, sign)
    for t in (0, 1, 17):
        new = tuple(x + 2*t*y for x, y in zip(T, direction))
        values, P, Q = profile(new, codes, sign)
        if t == 1:
            assert stable(old, values)
        M = -new[0]
        plan = (M, M, tuple(bands(M, map(abs, new))), P, Q, sign)
        check_pair(M + 1, new, construct(plan))


def read_manifest(path):
    rows = {}
    if path.exists():
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
                if row["D"]:
                    check_ray(row)
                rows[tuple(row["T"])] = row
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--census", type=Path)
    parser.add_argument("--seconds", type=int, default=45)
    args = parser.parse_args()
    if not __debug__ or args.seconds <= 0:
        parser.error("positive time cap and assertions required")
    rows = read_manifest(args.manifest)
    if args.census:
        deadline = time.monotonic() + args.seconds
        directions = defaultdict(list)
        for m in range(5, 25):
            for d in normalized_sets(m):
                if len(set(map(abs, d))) == 5:
                    directions[sign_order(d)].append(d)
        with args.manifest.open("a") as out:
            for m in range(15, 31):
                with (args.census / f"height-{m}.jsonl").open() as data:
                    for line in data:
                        if time.monotonic() >= deadline:
                            print("Time cap. Rerun to resume.")
                            return
                        record = json.loads(line)
                        T = tuple(record["T"])
                        g = sorted(map(abs, T))
                        if (not record["hit"] or T in rows or
                                min(g[0], *(b-a for a,b in zip(g,g[1:]))) < 2):
                            continue
                        codes = prefix_codes(T, record["prefixes"])
                        sign = record["first_sign"]
                        base, _, _ = profile(T, codes, sign)
                        direction = None
                        for d in directions[sign_order(T)]:
                            values, _, _ = profile(tuple(x + 2*y for x,y in zip(T,d)), codes, sign)
                            if stable(base, values):
                                direction = d
                                break
                        row = dict(T=T, D=direction, first_sign=sign, prefixes=record["prefixes"])
                        if direction:
                            check_ray(row)
                        out.write(json.dumps(row, separators=(",", ":")) + "\n")
                        out.flush()
                        rows[T] = row
    hits = Counter(sum(x < 0 for x in T) for T,r in rows.items() if r["D"])
    print(f"bases={len(rows)} certified rays={sum(hits.values())} by negative count={dict(hits)}")


if __name__ == "__main__":
    main()
