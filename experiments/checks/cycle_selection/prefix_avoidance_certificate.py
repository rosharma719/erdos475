"""Exact integer certificates for modular prefix avoidance. Python 3.10+."""
from math import factorial, gcd, prod

def coefficient(exponents):
    n = len(exponents) + 1
    assert sum(exponents) == n*(n-1)//2
    full = (1 << n) - 1
    alt = [0] * (full + 1)
    sums = [0] * (full + 1)
    alt[0] = 1
    for mask in range(1, full + 1):
        bit = mask & -mask
        sums[mask] = sums[mask ^ bit] + bit.bit_length()
        total = 0
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            inversions = (mask // (2 * bit)).bit_count()
            term = alt[mask ^ bit]
            total += -term if inversions % 2 else term
        rank = mask.bit_count()
        alt[mask] = (total if mask == full else
                     total * sums[mask] ** exponents[rank-1])
    vandermonde = prod(factorial(i) for i in range(n))
    value, remainder = divmod(alt[full], vandermonde)
    assert remainder == 0
    return value

def verify():
    expected = (1, 2, 18, 96, 7500, 194400, 1882384,
                2832334848, 239990252544)
    for h, target in enumerate(expected, 1):
        tight = coefficient([h] * (2*h-1))
        exponents = [h] * (2*h)
        exponents[1] += h
        extended = coefficient(exponents)
        g = gcd(tight, extended)
        assert g == target
        remaining = g
        for d in range(2, 2*h + 2):
            while remaining % d == 0:
                remaining //= d
        assert remaining == 1
        print(h, g)

if __name__ == '__main__':
    verify()
