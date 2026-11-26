"""Verify the IT(31) counterexample by enumerating every possible edge placement."""

from itertools import accumulate, permutations


def cut_changes(height, step, cut):
    """All changes of the indicator of vertices strictly above the cut."""
    return {
        int(start + step > cut) - int(start > cut)
        for start in range(height + 1)
        if 0 <= start + step <= height
    }


def main():
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    height = 31
    holes = set(range(-18, 0)) | set(range(5, 16)) | {30, 31}
    full = set(range(-height, height + 1)) - {0}
    steps = full - holes
    assert len(holes) == height == max(map(abs, holes))
    assert len(steps) == 31 and sum(holes) == sum(steps) == 0
    assert steps == set(range(1, 5)) | set(range(16, 30)) | set(range(-31, -18))

    for cut in range(height):
        diameter = max(cut, height - cut - 1)
        possible_totals = {0}
        for step in sorted(steps):
            changes = cut_changes(height, step, cut)
            sign = 1 if step > 0 else -1
            assert changes == ({sign} if abs(step) > diameter else {0, sign})
            possible_totals = {total + change for total in possible_totals for change in changes}

        low = sum(s > diameter for s in steps) - sum(s < 0 for s in steps)
        high = sum(s > 0 for s in steps) - sum(s < -diameter for s in steps)
        assert possible_totals == set(range(low, high + 1))
        if cut == 15:
            assert low == 1 and 0 not in possible_totals
            print(f"M=31 k=31 retained=31 cut=15 net crossing range=[{low},{high}]")
    print("Every edge placement was checked. A closed walk would require net crossing zero.")

    small_steps = {7, 8, -4, -5, -6}
    small_holes = set(range(-8, 9)) - {0} - small_steps
    assert len(small_holes) == 11 and sum(small_holes) == 0 and max(map(abs, small_holes)) == 8
    assert sum(s > 4 for s in small_steps) <= sum(s < 0 for s in small_steps)
    assert sum(s < -4 for s in small_steps) <= sum(s > 0 for s in small_steps)
    widths = []
    for order in permutations(small_steps):
        vertices = list(accumulate(order, initial=0))
        assert vertices[-1] == 0
        widths.append(max(vertices) - min(vertices))
    assert len(widths) == 120 and min(widths) == 9
    left, right = (0, 7), (0, 5, 9, 1, 7)
    for path in (left, right):
        assert len(set(path)) == len(path) and min(path) == 0 and max(path) <= 9
    assert left[0] == right[0] == 0 and left[-1] == right[-1] > 0
    labels = [b - a for a, b in zip(left, left[1:])] + [a - b for a, b in zip(right, right[1:])]
    assert sorted(labels) == sorted(small_steps)
    print(f"M=8 k=11 orders=120 minimum closed-walk width={min(widths)}")


if __name__ == "__main__":
    main()
