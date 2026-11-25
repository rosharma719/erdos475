"""Five omitted residues in odd cyclic groups. Python 3.10+, standard library."""
from itertools import accumulate, combinations
from collections import Counter

P = (1, 2, 5, -6, 10, -8, 7, -13, 12, -11, 14, -7, -9, 17,
     -18, 19, -20, 21, -22, 23, -24, 25, -26, 27, -28, 29, -30, 31)
Q = (2, 1, 10, -9, 3, -6, 4, 5, -11, 12, -13, 14, -15, 17, -18,
     19, -20, 21, -22, 23, -24, 25, -26, 27, -28, 29, -30, 16, 15)
HOLES = {3, 4, 8, 16, -31}
BASE = set(range(-31, 32)) - {0} - HOLES

def verify_base():
    assert Counter(P) + Counter(-x for x in Q) == Counter(BASE)
    for path in (P, Q):
        vertices = list(accumulate(path, initial=0))
        assert len(set(vertices)) == len(vertices)
        assert (min(vertices), max(vertices), vertices[-1]) == (-10, 21, 21)
    assert P[-1] == 31 and P[:2] == (1, 2)

def witness(modulus, outer):
    outer = sorted(outer)
    assert modulus % 2 == 1 and modulus >= 63
    assert len(outer) == len(set(outer))
    assert all(31 < a <= modulus//2 for a in outer)
    if outer:
        common = [(-a if j % 2 == 0 else a)
                  for j, a in enumerate(outer[:-1])]
        R = outer[-1]
        word = [*P, *common, R] + [-a for a in reversed((*Q,*common))] + [-R]
    else:
        word = [31,*P[:-1]] + [-a for a in reversed(Q)]
        word = word[1:] + word[:1]
    return word

def check_cycle(word, labels, modulus):
    assert Counter(x % modulus for x in word) == Counter(x % modulus for x in labels)
    v = [s % modulus for s in accumulate(word, initial=0)]
    assert v[-1] == 0 and len(set(v[:-1])) == len(word)
    return set(v[:-1])

def audit(modulus, outer):
    word = witness(modulus, outer)
    labels = BASE | set(outer) | {-a for a in outer}
    check_cycle(word, labels, modulus)
    assert word[:2] == [1,2]
    contracted = [3,*word[2:]]
    assert 1 not in check_cycle(contracted,(labels-{1,2})|{3}, modulus)

if __name__ == '__main__':
    verify_base()
    count = 0
    for modulus in range(63,84,2):
        magnitudes = range(32,modulus//2+1)
        for r in range(len(magnitudes)+1):
            for subset in combinations(magnitudes,r):
                audit(modulus,subset)
                count += 1
    for modulus in range(63,1002,2):
        audit(modulus, range(32,modulus//2+1))
    print(count,'exhaustive outer-padding cases; 470 full-padding checks passed.')
