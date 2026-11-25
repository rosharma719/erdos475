"""Direct witness checks for the symmetric rooted split construction."""
def rooted(p, core, x, y):
    t = (x+y) % p
    m = (p-1)//2
    inv = pow(x, -1, p)
    b = (inv*y + m) % p - m
    scale = inv if b > 0 else -inv
    d = scale*t % p
    mags = sorted({min(z, p-z) for a in core if (z := a*scale % p)})
    pos = mags.index(d)
    path = [s if (i-pos)%2 == 0 else -s for i,s in enumerate(mags)]
    other = path[-1:] + path[:-1]
    word = path + [-z for z in reversed(other)]
    i = word.index(d)
    root = [z*pow(scale, -1, p)%p for z in word[i:]+word[:i]]
    verts = vertices(p,root)
    if x in verts:
        root = root[:1] + root[:0:-1]
    assert root[0] == t and set(root) == core
    assert x not in vertices(p, root)
    assert len(vertices(p, [x,y]+root[1:])) == len(core)+1
    return root

def vertices(p, word):
    s, v = 0, set()
    for a in word:
        assert s not in v
        v.add(s)
        s = (s+a)%p
    assert s == 0
    return v

if __name__ == '__main__':
    for p in (3,5,7,11,13,17,19,23):
        count = 0
        for mask in range(1,1 << ((p-1)//2)):
            core = {z for a in range(1,(p+1)//2) if mask >> (a-1)&1
                    for z in (a,p-a)}
            for x in set(range(1,p))-core:
                for t in core:
                    y = (t-x)%p
                    if y and y != x and y not in core:
                        rooted(p,core,x,y)
                        count += 1
        print(p,count)
