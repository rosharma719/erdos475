import sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
from template5 import check_fixed
def all_gadgets(t,A):
    M,pre,post=check_fixed(t,A)
    labels=set(range(1,M+1))-{2}
    used=[abs(pre[i+1]-pre[i]) for i in range(len(pre)-1)]+[abs(post[i+1]-post[i]) for i in range(len(post)-1)]
    if len(set(used))<len(used): return None
    remL=labels-set(used)
    u=(M-1)//4;tt=u//2;v=4*((u-1)//2)+1
    E=set(range(-4*u,4*u,4));O=set(range(-4*u-1,4*u,4))
    deleted=set(range(v-2,v+4*tt-1,4));shifted=set(range(v,v+4*tt,4))
    U=E|((O-deleted)|shifted)|{4*u}
    free=U-set(pre+post)
    def key(x):
        if x==M-5: return 'P'
        if x==-M+4*t+1: return 'Q'
        if x%4==0 and x>0: return ('L',(x-4*A)//4)
        return ('H',(M-9-x-4*A)//4)
    sols=[];path=[pre[-1]];used2=set()
    def rec():
        x=path[-1]
        if len(path)==len(free)+1:
            L=abs(post[0]-x)
            if L in remL and L not in used2: sols.append(tuple(key(y) for y in path[1:]))
            return
        for y in free:
            if y in path: continue
            L=abs(y-x)
            if L in remL and L not in used2:
                path.append(y);used2.add(L);rec();path.pop();used2.discard(L)
    rec();return sols,sorted((str(key(x)) for x in free))
common=None
for t in range(int(sys.argv[1]),int(sys.argv[2])+1):
    r=all_gadgets(t,t-5)
    if not r: print(t,"clash");continue
    sols,fk=r
    s=set(sols)
    common=s if common is None else common&s
    print(t,"gadgets",len(s),"free keys",fk if t==int(sys.argv[1]) else "", "common so far",len(common),flush=True)
print("COMMON:",list(common)[:3])
