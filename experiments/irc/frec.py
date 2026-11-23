"""Generalized problem F(al,be,side): Hamiltonian path on [-al,be] minus {0,1}, labels {2..al+be-1} once each,
starting at the top be (side='T') or the bottom -al (side='B'). H_k = F(k+1,k+1,'T').
Reflection x->1-x maps F(al,be,B) to F(be-1,al+1,T), so only T matters.
Reduction search: zigzag from the top (be, -(al-1), be-1, ...) of length Lz, then a gadget of <=G extra vertices,
then the remaining vertex set must be exactly [-al',be'] minus {0,1} with remaining labels exactly {2..al'+be'-1}, and the
path must enter it at its top or bottom. Report the rule (al,be)->(al',be',side')."""
import sys, itertools
def zig(al,be,Lz):
    seq=[be];p=be;n=-(al-1)
    while len(seq)<Lz:
        seq.append(n);n+=1
        if len(seq)<Lz: p-=1;seq.append(p)
    return seq
def reductions(al,be,G=4):
    V=set(range(-al,be+1))-{0,1}; out=[]
    for Lz in range(2,al+be):
        Z=zig(al,be,Lz)
        if not set(Z)<=V or len(set(Z))<len(Z): break
        labs=[abs(Z[i+1]-Z[i]) for i in range(len(Z)-1)]
        if len(set(labs))<len(labs) or not set(labs)<=set(range(2,al+be)): break
        rem=V-set(Z); reml=set(range(2,al+be))-set(labs)
        # gadget: sequence g of length 0..G from rem, starting adjacent to Z[-1]
        def rec(path,used,g):
            x=path[-1]
            R=rem-set(path); L=reml-used
            # check if R is an F-instance entered at top or bottom from x with next label
            if R:
                lo,hi=min(R),max(R)
                if lo<=-1 and hi>=2 and R==set(range(lo,hi+1))-{0,1} and L==set(range(2,(-lo)+hi)):
                    # remaining labels must also include the connecting edge -> so connecting label must be used already; here we require next vertex = top or bottom via a label NOT in L... instead require connection within gadget: last gadget vertex IS the instance's start (included in R?) 
                    pass
            if g==G: return
            for L2 in sorted(L,reverse=True):
                for y in (x+L2,x-L2):
                    if y in R:
                        # option: y is the start of the inner instance
                        R2=R-{y}
                        Rin=R  # inner instance includes y
                        lo,hi=min(Rin),max(Rin)
                        Lrest=L-{L2}
                        if lo<=-1 and hi>=2 and Rin==set(range(lo,hi+1))-{0,1} and Lrest==set(range(2,(-lo)+hi)) and y in (lo,hi):
                            out.append((Lz,tuple(path[len(Z):]),y,(-lo,hi,'T' if y==hi else 'B')))
                        rec(path+[y],used|{L2},g+1)
        rec(list(Z),set(),0)
    return out
if __name__=="__main__":
    for s in range(int(sys.argv[1]),int(sys.argv[2])+1):
        al=be=s
        rs=reductions(al,be,int(sys.argv[3]))
        best=sorted(set((r[3],r[1],r[0]) for r in rs),key=lambda t:t[0][0]+t[0][1],reverse=True)[:3]
        print("H_k k=",s-1,"F(",al,be,") ->",best,flush=True)
