# Prepended to every check script. Pure stdlib.
import itertools, sys
sys.setrecursionlimit(10000)

def partial_sums(seq, p):
    s, out = 0, []
    for a in seq:
        s = (s + a) % p
        out.append(s)
    return out

def valid_ordering(seq, p, nonzero=False):
    """MODE: partial sums s_1..s_k distinct mod p. nonzero=True additionally forbids s_i == 0.
    (problem.md must say which variant Erdős #475 uses; verify before trusting results.)"""
    ps = partial_sums(seq, p)
    if len(set(ps)) != len(ps):
        return False
    return not (nonzero and 0 in ps)

def find_ordering(A, p, nonzero=False):
    """Backtracking search for a valid ordering of A (subset of 1..p-1). Returns list or None."""
    A = list(A)
    used = [False] * len(A)
    seen, seq = set(), []
    if nonzero:
        seen.add(0)
    def rec(s):
        if len(seq) == len(A):
            return True
        tried = set()
        for i, a in enumerate(A):
            if used[i] or a in tried:
                continue
            tried.add(a)
            t = (s + a) % p
            if t in seen:
                continue
            used[i] = True; seen.add(t); seq.append(a)
            if rec(t):
                return True
            used[i] = False; seen.discard(t); seq.pop()
        return False
    return list(seq) if rec(0) else None

def fixed_complement_check(p, c, nonzero=False):
    """For every c-subset C of F_p^*, does A = F_p^* \\ C have a valid ordering?
    Returns list of failing C (empty = all good)."""
    full = range(1, p)
    bad = []
    for C in itertools.combinations(full, c):
        A = [x for x in full if x not in C]
        if find_ordering(A, p, nonzero) is None:
            bad.append(C)
    return bad

def primes_upto(n):
    return [q for q in range(2, n + 1) if all(q % r for r in range(2, int(q ** .5) + 1))]
