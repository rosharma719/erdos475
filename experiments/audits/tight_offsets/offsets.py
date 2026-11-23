import itertools
def alpha(c,L):
    q,r=divmod(L,c); return (c-r)*((q+1)//2)+r*((q+2)//2)
def brute(c,L):  # exact max independent set, positions 0..L-1, forbidden difference c (greedy per chain is optimal; brute check small)
    best=0
    for mask in range(1<<L):
        ok=all(not(mask>>i&1 and mask>>(i+c)&1) for i in range(L-c))
        if ok: best=max(best,bin(mask).count('1'))
    return best
# formula vs brute force for small L
for L in range(1,15):
    for c in range(1,L+2):
        assert alpha(c,L)==brute(c,L),(c,L)
print("alpha formula ok (L<=14)")
bad=[]
for M in range(1,3001):
    for c in range(1,M+1):
        feas = alpha(c,2*M+3-c)>=M
        div = any((M+i)%c==0 for i in range(4))
        if feas!=div: bad.append((M,c,feas,div))
print("mismatches M<=3000:",len(bad),bad[:10])
for M in (24,40,100,400):
    print(M,[c for c in range(1,M+1) if alpha(c,2*M+3-c)>=M])
