import itertools, math
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def F_interval(w):                          # Q_m as polynomial F_{m-1}(w_0..w_{m-2})
    mm=len(w)-1; f=1
    for i in range(mm):
        s=w[i]
        for j in range(i+1,mm):
            s+=w[j]
            if i==0 and j==mm-1: continue
            f*=s
    return f
def content(m):
    pt=list(range(1,m+1)); d=1
    for i in range(m):
        for j in range(i+1,m): d*=pt[j]-pt[i]
    gm=[mm for mm in itertools.product(range(3),repeat=m) if sum(mm)==2]
    tot=[0]*len(gm)
    for p in itertools.permutations(range(m)):
        w=[pt[k] for k in p]; s=sgn(p)
        y=0; A0=1
        for j in range(m):
            y+=w[j-1] if j>0 else 0
            if j>=2: A0*=y
        v=s*F_interval(w)*A0
        for idx,mm in enumerate(gm):
            t=v
            for e,x_ in zip(mm,w): t*=x_**e
            tot[idx]+=t
    vals=[t//d for t in tot]; assert all(t%d==0 for t in tot)
    g=0
    for x_ in vals: g=math.gcd(g,abs(x_))
    return g,vals
