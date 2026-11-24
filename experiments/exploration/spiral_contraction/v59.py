p = 59
M = 29
A = {x*x % p for x in range(1, p)}
def centered(x):
    return (x + 29) % p - 29
assert len(A) == 29 and sum(A) % p == 0
imbalances = {sum(centered(s*a) for a in A) for s in range(1, p)}
assert imbalances == {-177, 177}
delta = [27, 21, -10, 8, 18, -25, -15, 4, -24, -22, -9, -1, 13, -7, 12, -6, -17, 16, -2]
assert len(set(map(abs, delta))) == len(delta) and all(0 < abs(d) < M for d in delta)
D = [0]
for d in delta: D.append((D[-1] + d) % p)
assert len(set(D)) == 20 and not set(D) & {(d+M) % p for d in D}
W = delta + [M] + [-d for d in delta[::-1]] + [-M]
V = [0]
for w in W: V.append((V[-1] + w) % p)
assert V[-1] == 0 and len(set(V[:-1])) == 40
cuts = [0,1,2,3,5,7,8,9,11,13,15,17,18,19,20,22,23,25,26,27,28,29,30,32,33,34,35,36,38]
ends = cuts[1:] + [40]
assert all(j-i in (1, 2) for i, j in zip(cuts, ends))
B = [sum(W[i:j]) % p for i, j in zip(cuts, ends)]
assert len(B) == len(set(B)) == 29 and set(B) == A
print("p=59 verified: I(Q59)=3, modular half-walk contraction gives Q59")
# p=101 example
p=101; U=[x for x in range(1,34) if x not in (23,33)]; A=U+[s*x for x in range(34,44) for s in (1,-1)]
assert sum(A)%p==0 and len(A)==51 and len(U)==31
from itertools import combinations
assert not any(sum(t)%p==0 for t in combinations(U,3))
print("p=101 example: zero-sum, q=31, T=0 verified")
