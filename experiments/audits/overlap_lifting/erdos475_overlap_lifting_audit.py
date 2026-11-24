"""Standalone verifier for overlapping quotient blocks, Erdős #475.
Tests stated families and counterexamples; does not prove general sequencing.
Python 3. No third-party dependencies.
"""
from itertools import accumulate, product


def verify(word, original):
    assert sorted(word) == sorted(original)
    assert len(original) == len(set(original)) and sum(word) == 0
    vertices = [0, *accumulate(word)][:-1]
    assert len(set(vertices)) == len(word)
    span = max(vertices) - min(vertices)
    assert span <= max(original) - min(original)
    return span


def symmetric_core(k, g):
    x = [(-1)**i * (i+1)*g for i in range(k)]
    return x + [-a for a in x[:-1][::-1]] + [-x[-1]]


def overlapping_family(k):
    assert k >= 4
    g = 2*k + 1
    blocks = {}
    for i in range(1, k+1):
        blocks[i*g] = [i, i*g-i]
        blocks[-i*g] = ([-i, -(i*g-i)] if i in (1,2,k)
                        else [-(g+i), -((i-1)*g-i)])
    A = [a for c in blocks.values() for a in c]
    assert len(A) == 4*k and len(set(A)) == len(A) and sum(A) == 0
    for i in range(1, k+1):
        for d in (i*g,-i*g):
            assert sum(blocks[d]) == d
            assert {a%g for a in blocks[d]} == {i,g-i}
    core = symmetric_core(k,g)
    V = {0,*accumulate(core)}
    assert len(V) == len(core)
    assert max(V)-min(V) == (2*k-1)*g
    start = {}; z = 0
    for d in core:
        start[d] = z; z += d
    seen = set(V); choices = {}
    for i in range(1,k+1):
        for d in (i*g,-i*g):
            p = next(a for a in blocks[d] if start[d]+a not in seen)
            seen.add(start[d]+p); choices[d] = [p,d-p]
    word = [a for d in core for a in choices[d]]
    assert set([1,-1]) <= set(A)
    assert max(A)-min(A) == 4*k*k
    return verify(word,A), word


def incompatible_core():
    # Two increasing contracted paths, recorded as (start, high, low, residue).
    paths = [[(0,355,340,1),(15,376,321,2),(70,388,310,3),(148,400,301,4)],
             [(0,391,305,2),(86,384,311,5),(159,379,312,4),(226,359,338,6)]]
    g = 13; X=[]; Y=[]; ds=[[],[]]; choices=[]; residues=[]
    for j,path in enumerate(paths):
        for z,M,m,r in path:
            M,m=M*g+r,m*g+r
            (X if j==0 else Y).append(M)
            (Y if j==0 else X).append(m)
            ds[j].append(M-m)
            choices.append((z*g-m,z*g+M))
            residues.append({r,g-r})
    A=X+[-y for y in Y]
    assert len(A)==len(set(A)) and sum(A)==0
    D=max(X)+max(Y)
    core=ds[0]+[-d for d in ds[1][::-1]]
    V={0,*accumulate(core)}
    assert sum(core)==0 and len(V)==len(core)==len(set(core))
    assert all(d%g==0 for d in core) and max(V)-min(V)<=D
    overlaps=[(i,j) for i in range(8) for j in range(i) if residues[i]&residues[j]]
    assert overlaps==[(4,1),(6,3)]
    spans=[]
    for c in product(*choices):
        if len(set(c))!=len(c) or set(c)&V: continue
        spans.append(max(V|set(c))-min(V|set(c)))
    assert min(spans)==10965 and D==10289
    return D,min(spans),choices


def admissible_quotient(A,g):
    """Exact search: minimal residue-zero blocks, distinct nonzero sums,
    diameter <= original D, at least one proper contraction."""
    n=len(A); N=1<<n; D=max(A)-min(A)
    su=[0]*N
    for s in range(1,N):
        i=(s&-s).bit_length()-1
        su[s]=su[s^(1<<i)]+A[i]
    mins=[]; by=[[] for _ in A]
    for s in sorted(range(1,N),key=int.bit_count):
        if su[s]%g or any(t&s==t for t in mins): continue
        mins.append(s)
        if not su[s] or abs(su[s])>=D: continue
        for i in range(n):
            if s>>i&1: by[i].append(s)
    def search(mask,ds):
        if not mask: return len(ds)<n
        i=(mask&-mask).bit_length()-1
        for s in by[i]:
            if mask&s!=s or su[s] in ds: continue
            d=ds+[su[s]]
            if max(d)-min(d)<=D and search(mask^s,d): return True
        return False
    return search(N-1,[])


def quotient_obstruction():
    A=(-7,-6,-5,-4,2,3,4,6,7)
    D=max(A)-min(A)
    assert sum(a for a in A if a>0)==22 and D==14
    # A zero-sum nonzero core needs both signs, hence 2g <= D.
    assert not any(admissible_quotient(A,g) for g in range(2,D//2+1))
    w=(-7,-6,2,3,-4,6,7,-5,4)
    return verify(w,A),w


if __name__=='__main__':
    for k in range(4,101): overlapping_family(k)
    print('97 overlapping-block family instances passed (k=4,...,100).')
    for k in (4,10,100):
        print(f'k={k}: n={4*k}, diameter={4*k*k}, span={overlapping_family(k)[0]}')
    print('Incompatible fixed core:',incompatible_core())
    print('No admissible quotient partition:',quotient_obstruction())
