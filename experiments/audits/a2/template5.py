"""a=2, M=8t+5 template (from GPT certificates M=69,77,85): fixed formula segments + a free middle gadget G1a found by DFS.
Path = H + Z1 + G1a + T + Z2 + Z3 + G2 + Z4, where
 H  = 0, M-1, M-2, M-9
 Z1 = 4i, M-9-4i  (i=1..A)   [A chosen]
 G1a = free (DFS)
 T  = -M+4t+4, -M+4t-7, -M+4t+8, -M+4t-11
 Z2 = -(4J+5), then (-M+4j+1, -(4j+5)) for j=J-1..0   with J=t-3
 Z3 = (M-8-4i, 4i-1) for i=0..t-2, then M-8-4(t-1)
 G2 = M-(4t+10), -M+(4t-3), -M+4t, -M+(4t+5), -M+(4t-4), -M+(4t+9), -M+(4t-8)
 Z4 = (-4j... ) : -4(t-2)?? then (-M+4j, -4j) j=t-3..1, then -M
"""
import sys,time
def segs(t,A):
    M=8*t+5;J=t-3
    H=[0,M-1,M-2,M-9]
    Z1=[]
    for i in range(1,A+1): Z1+=[4*i,M-9-4*i]
    T=[-M+4*t+4,-M+4*t-7,-M+4*t+8,-M+4*t-11]
    Z2=[-(4*J+5)]
    for j in range(J-1,-1,-1): Z2+=[-M+4*j+1,-(4*j+5)]
    Z3=[]
    for i in range(0,t-1): Z3+=[M-8-4*i,4*i-1]
    Z3+=[M-8-4*(t-1)]
    G2=[M-(4*t+10),-M+(4*t-3),-M+4*t,-M+(4*t+5),-M+(4*t-4),-M+(4*t+9),-M+(4*t-8)]
    Z4=[]
    for j in range(t-2,0,-1): Z4+=[-4*j,-M+4*(j-1)] if False else []
    # from data: after G2 ends at -M+4t-8: then -(4t-8), -M+4(t-3), -(4(t-3)), ..., -M+4, -4, -M
    Z4=[-(4*t-8)]
    for j in range(t-3,0,-1): Z4+=[-M+4*j,-4*j]
    Z4+=[-M]
    return M,H,Z1,T,Z2,Z3,G2,Z4
def check_fixed(t,A):
    M,H,Z1,T,Z2,Z3,G2,Z4=segs(t,A)
    pre=H+Z1; post=T+Z2+Z3+G2+Z4
    allv=pre+post
    return M,pre,post
def solve(t,A,tl=20):
    M,pre,post=check_fixed(t,A)
    labels=set(range(1,M+1))-{2}
    fixed=pre+post
    if len(set(fixed))<len(fixed): return 'dup'
    used=[abs(pre[i+1]-pre[i]) for i in range(len(pre)-1)]+[abs(post[i+1]-post[i]) for i in range(len(post)-1)]
    if len(set(used))<len(used) or not set(used)<=labels: return ('labelclash',sorted(x for x in used if used.count(x)>1))
    remL=labels-set(used)
    # vertex universe: GPT scaffold G_u^(1) for M=4u+1
    u=(M-1)//4
    tt=u//2;v=4*((u-1)//2)+1
    E=set(range(-4*u,4*u,4));O=set(range(-4*u-1,4*u,4))
    deleted=set(range(v-2,v+4*tt-1,4));shifted=set(range(v,v+4*tt,4))
    U=E|((O-deleted)|shifted)|{4*u}
    if not set(fixed)<=U: return ('notinU',sorted(set(fixed)-U)[:5])
    free=U-set(fixed)
    # gadget: path from pre[-1] through all free vertices to post[0], labels exactly remL
    if len(remL)!=len(free)+1: return ('count',len(remL),len(free))
    t0=time.time();path=[pre[-1]];used2=set()
    def rec():
        if time.time()-t0>tl: raise TimeoutError
        x=path[-1]
        if len(path)==len(free)+1:
            L=abs(post[0]-x)
            return L in remL and L not in used2 and len(used2)+1==len(remL)
        for y in free:
            if y in path: continue
            L=abs(y-x)
            if L in remL and L not in used2:
                path.append(y);used2.add(L)
                if rec(): return True
                path.pop();used2.discard(L)
        return False
    try:
        if rec(): return ('OK',path[1:])
    except TimeoutError: return 'TO'
    return 'NONE'
if __name__=="__main__":
    for t in range(int(sys.argv[1]),int(sys.argv[2])+1):
        res=None
        for A in range(t+2,0,-1):
            r=solve(t,A)
            if isinstance(r,tuple) and r[0]=='OK': res=(A,r[1]);break
            last=r
        M=8*t+5
        rel=lambda x: str(x) if abs(x)<M/2-6 else (f"M{x-M:+d}" if x>0 else f"-M{x+M:+d}")
        print(t,M, (res[0],[rel(x) for x in res[1]]) if res else last,flush=True)
