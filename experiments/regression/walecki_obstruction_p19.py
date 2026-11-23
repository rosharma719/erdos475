# Regression case (from GPT, re-run by Claude): fixed-Walecki-contraction strategy fails for p=19, C={7,8,10,14,18} although a valid ordering exists.
from itertools import combinations
p = 19; C = {7, 8, 10, 14, 18}; A = set(range(1, p)) - C
r = 9; lo, hi, al, tl = 1, r, [], True
while lo <= hi:
    if tl: al.append(lo); lo += 1
    else: al.append(hi); hi -= 1
    tl = not tl
D = [(al[i + 1] - al[i]) % p for i in range(r - 1)]
B = D + [r] + [(-x) % p for x in D[::-1]] + [(-r) % p]
V = [0]
for x in B[:-1]: V.append((V[-1] + x) % p)
found = 0; tried = 0
for ids in combinations(range(18), 13):
    steps = [(V[ids[(i + 1) % 13]] - V[ids[i]]) % p for i in range(13)]
    if len(set(steps)) < 13: continue
    tried += 1
    S = set(steps)
    if any({(lam * x) % p for x in S} == A for lam in range(1, p)): found += 1
print("distinct-label contractions", tried, "matching A under some dilation:", found)
valid = [3, 5, 6, 4, 17, 16, 2, 15, 1, 11, 13, 9, 12]; s = 0; seen = {0}
for i, x in enumerate(valid):
    s = (s + x) % p
    if i < 12: assert s not in seen
    seen.add(s)
print("explicit valid cycle of A ok:", set(valid) == A and s == 0)
