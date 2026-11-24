"""Direct checks for the two-path construction and the centered-lift exceptions."""
from itertools import accumulate, combinations, permutations


def centered(x, p):
    return (x + p // 2) % p - p // 2


def valid(word, residues, p):
    return (sorted(x % p for x in word) == sorted(residues)
            and len({x % p for x in accumulate(word)}) == len(word))


def layer(paths, u, v):
    first, second = paths
    return [u] + [-x for x in second], [v] + [-x for x in first]


def complete(paths):
    first, second = paths
    return first[1:] + first[:1] + [-x for x in reversed(second)]


def family_word(a, padding):
    """Order {-2,-3,4,-a,a+1} and the signed pairs of the supplied magnitudes."""
    padding = set(padding)
    if a < 5 or padding & {2, 3, 4, a, a + 1} or any(b <= 0 for b in padding):
        raise ValueError("overlapping or invalid magnitudes")
    paths = ([4, -1, -2], [3, -1]) if 1 in padding else ([4, -2], [3])
    for b in sorted(padding - {1}):
        if b < a:
            paths = layer(paths, b, b)
    paths = layer(paths, a + 1, a)
    for b in sorted(padding):
        if b > a + 1:
            paths = layer(paths, b, b)
    return complete(paths)


def check_family():
    count = 0
    for modulus in range(13, 32, 2):
        half = modulus // 2
        for a in range(5, half):
            seed = {-2, -3, 4, -a, a + 1}
            free = sorted(set(range(1, half + 1)) - {abs(x) for x in seed})
            for mask in range(1 << len(free)):
                padding = [b for i, b in enumerate(free) if mask >> i & 1]
                word = family_word(a, padding)
                residues = {x % modulus for x in seed}
                residues.update(x % modulus for b in padding for x in (b, -b))
                assert valid(word, residues, modulus)
                count += 1
    print(f"two-path family: {count} orderings verified")


def five_lifts():
    for p in (11, 13, 17, 19, 23):
        exceptions = []
        five_sets = 0
        for u in combinations(range(1, p), 5):
            if sum(u) % p or any(-x % p in u for x in u):
                continue
            five_sets += 1
            if not any(sum(centered(x * a, p) for x in u) == 0 for a in range(1, p)):
                exceptions.append(u)
        if p == 11:
            seed = {1, 3, 4, 5, 9}
            orbit = {tuple(sorted(t * x % p for x in seed)) for t in range(1, p)}
            assert set(exceptions) == orbit
        else:
            assert not exceptions
        print(f"p={p}: {five_sets} inverse-free zero-sum five-sets, {len(exceptions)} unrectified")


def tiny_primes():
    for p in (2, 3, 5, 7):
        for size in range(1, p):
            for subset in combinations(range(1, p), size):
                assert any(valid(word, subset, p) for word in permutations(subset))
    print("all nonempty subsets checked at p=2,3,5,7")


if __name__ == "__main__":
    tiny_primes()
    five_lifts()
    check_family()
