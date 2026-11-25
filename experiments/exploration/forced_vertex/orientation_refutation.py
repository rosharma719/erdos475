"""Python 3. Exhaust all directed block orders for the counterexample."""
from itertools import permutations, accumulate, product
p,t,x=13,1,2
blocks=((3,5),(7,4),(9,10))
B={t}|{a for pair in blocks for a in pair}
sums={(a+b)%p for a,b in blocks}
assert len(B)==7 and sum(B)%p==0 and 2*x%p!=t
assert not {x,(t-x)%p}&B
assert len(sums)==3 and not sums & (B|{0,x,(t-x)%p})
def witnesses(bits):
    oriented=[pair[::-1] if flip else pair for pair,flip in zip(blocks,bits)]
    for perm in permutations(oriented):
        w=(t,)+sum(perm,())
        v=tuple(s%p for s in accumulate(w,initial=0))
        assert v[-1]==0
        if x not in v[:-1] and len(set(v[:-1]))==len(B):
            yield w,v[:-1]
for bits in product(range(2),repeat=3):
    hits=list(witnesses(bits))
    print(bits,len(hits),hits[:1])
assert not list(witnesses((0,0,0))) and not list(witnesses((1,1,1)))
assert any(list(witnesses(bits)) for bits in product(range(2),repeat=3))
