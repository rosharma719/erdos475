// SIA multiplicity: zero-sum B (t=1 after dilation), external x,y (x+y=1, x,y notin B, x!=y, x<y canonical),
// for each admissible inner pair {u,v} (u,v in B\{t}, s=u+v notin B∪{0,x,y}), does a t-rooted valid cycle of B exist
// avoiding x that contains u,v adjacent?  Count working pairs per instance.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,n,B[32],X,U,Vv; char vis[64];
int dfs(int pos,int cnt,unsigned used,int last,int ok){
  if(cnt==n) return pos==0 && ok;
  for(int i=0;i<n;i++){ if(used>>i&1) continue; int a=B[i]; int w=(pos+a)%p;
    int nok = ok || (last>=0 && ((last==U&&a==Vv)||(last==Vv&&a==U)));
    if(cnt==n-1){ if(w==0 && nok) return 1; continue; }
    if(w==0||w==X||vis[w]) continue; vis[w]=1; int r=dfs(w,cnt+1,used|1u<<i,a,nok); vis[w]=0; if(r) return 1; }
  return 0;}
int main(int argc,char**argv){ p=atoi(argv[1]); int kmin=atoi(argv[2]);
  long long inst=0,totpairs=0,totwork=0,failinst=0; long long hist[64]={0}; int minw=999; long long minfrac_num=1,minfrac_den=1;
  for(unsigned m=0;m<(1u<<(p-2));m++){ // B = {1} ∪ subset of {2..p-1}
    unsigned M=(m<<1)|1; int k=__builtin_popcount(M); if(k<kmin||k>p-3) continue;
    int s=0; n=0; for(int i=0;i<p-1;i++) if(M>>i&1){ B[n++]=i+1; s+=i+1; } if(s%p) continue;
    int inB[64]={0}; for(int i=0;i<n;i++) inB[B[i]]=1;
    // put t=1 first
    for(X=2;X<p;X++){ int Y=(1-X+p)%p; if(Y<=X||inB[X]||inB[Y]) continue;
      int pairs=0,work=0;
      for(int i=1;i<n;i++) for(int j=i+1;j<n;j++){ int sm=(B[i]+B[j])%p; if(!sm||inB[sm]||sm==X||sm==Y) continue;
        pairs++; U=B[i]; Vv=B[j]; memset(vis,0,sizeof vis); vis[1]=1;
        if(dfs(1,1,1u,1,0)) work++; }
      inst++; totpairs+=pairs; totwork+=work; if(work<pairs){failinst++; if(failinst<=5){printf("PAIR FAIL B={"); for(int q=0;q<n;q++) printf("%d,",B[q]); printf("} x=%d\n",X);}} if(pairs==0) continue;
      if(work<64) hist[work]++; if(work<minw) minw=work;
      if((long long)work*minfrac_den < minfrac_num*pairs){ minfrac_num=work; minfrac_den=pairs; }
    } }
  printf("p=%d |B|>=%d pairs=%lld working=%lld instances-with-a-failing-pair=%lld instances=%lld ",p,kmin,totpairs,totwork,failinst,inst); printf(" min #working inner pairs=%d  min fraction=%lld/%lld\n",p,kmin,inst,minw,minfrac_num,minfrac_den);
  printf("  distribution of #working pairs (first values):"); for(int w=0;w<12;w++) if(hist[w]) printf(" %d:%lld",w,hist[w]); printf("\n");
}
