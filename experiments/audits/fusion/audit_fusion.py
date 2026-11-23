"""Independent audit of GPT atom-fusion: (1) two disjoint minimal zero-sum triples always fuse in the word
(b1,c1,b2,b3,c2,c3) with the explicit positional matching; (2) general theorem: if the only proper zero-sum
subsets of B∪C are B, C, cross inverse pairs and their complements, the matched four-block word is valid."""
from itertools import combinations, permutations
def valid(w,p):
    s=0;seen={0}
    for i,x in enumerate(w):
        s=(s+x)%p
        if i<len(w)-1:
            if s in seen: return False
            seen.add(s)
    return s==0
def minimal(B,p): return sum(B)%p==0 and all(sum(T)%p for r in range(1,len(B)) for T in combinations(B,r))
def zs_subsets(A,p): return [set(T) for r in range(1,len(A)) for T in combinations(A,r) if sum(T)%p==0]
def word(B,C,p):
    # build per the theorem: slots b1,c1,b2..bm,c2..cn ; avoid cross inverse pairs at the 4 cross adjacencies
    m,n=len(B),len(C)
    for pb in permutations(B):
        for pc in permutations(C):
            w=[pb[0],pc[0]]+list(pb[1:])+list(pc[1:])
            N=len(w); ok=True
            for i in range(N):
                x,y=w[i],w[(i+1)%N]
                if ((x in B)!=(y in B)) and (x+y)%p==0: ok=False;break
            if ok: return w
    return None
tri=0;gen=0;bad=[]
for p in (7,11,13,17,19,23):
    atoms=[T for r in (3,4,5) for T in combinations(range(1,p),r) if minimal(T,p)] if p<=13 else [T for T in combinations(range(1,p),3) if minimal(T,p)]
    for B,C in combinations(atoms,2):
        if set(B)&set(C): continue
        A=set(B)|set(C)
        allowed=[set(B),set(C)]+[{x,y} for x in B for y in C if (x+y)%p==0]
        allowed+= [A-s for s in allowed[2:]]
        hyp=all(s in allowed for s in zs_subsets(sorted(A),p))
        if len(B)==3 and len(C)==3 and not hyp: bad.append(('triple-hyp-fails',p,B,C))
        if hyp:
            w=word(B,C,p)
            if w is None or not valid(w,p): bad.append(('fusion-fails',p,B,C,w))
            if len(B)==len(C)==3: tri+=1
            else: gen+=1
print("triple pairs:",tri,"general (sizes 3..5, p<=13):",gen,"problems:",bad[:5])
print("example p=19 (3,2,4,5,7,8,9):",valid((3,2,4,5,7,8,9),19), " triple ex (16,11,1,2,3,5):",valid((16,11,1,2,3,5),19))
