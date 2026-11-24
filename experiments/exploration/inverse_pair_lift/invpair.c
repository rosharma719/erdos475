// For balanced (P,N) and common x in P∩N with x != maxP, x != maxN (window unchanged):
// enumerate ALL G-walks (root +maxP, window (-q1,p1]) of reduced (P\{x},N\{x}); for each, test whether
// inserting +x after vertex index i and -x after index j (or -x first then +x), 1<=i, i<j, keeps validity+window.
// Report reduced walks that admit NO insertion (robust-lift failures).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int el[40],ne,lo,hi,X; int path[40],vtx[41]; long long walks,badwalks,inst,badinst; int curbad;
char vis[512];
int ins_ok(int n){ // vtx[0..n-1] vertices (vtx[0]=0), steps path[0..n-1], vtx[n]=0
  for(int sgn=1;sgn>=-1;sgn-=2) for(int i=1;i<n;i++) for(int j=i+1;j<=n;j++){
    // first insertion after arriving at vertex i (before step i), second after vertex j (before step j), j<=n means before return
    // new vertices: vtx[0..i], vtx[i..j]+s*X, vtx[j..n-1] (vtx[j] if j<n)
    static char seen[512]; memset(seen,0,sizeof seen); int ok=1;
    for(int k=0;k<=i&&ok;k++){ int v=vtx[k]; if(seen[v+256]) ok=0; else seen[v+256]=1; }
    for(int k=i;k<=j&&ok;k++){ int v=(k==n?0:vtx[k])+sgn*X; if(v<lo||v>hi||seen[v+256]) ok=0; else seen[v+256]=1; }
    for(int k=j;k<n&&ok;k++){ if(k==i) continue; int v=vtx[k]; if(k==j && j>i){ if(seen[v+256]) ok=0; else seen[v+256]=1; } else if(k>j){ if(seen[v+256]) ok=0; else seen[v+256]=1;} }
    if(ok) return 1;
  }
  return 0;
}
void dfs(int pos,int cnt,unsigned long long used){
  if(cnt==ne){ if(pos==0){ walks++; vtx[ne]=0; if(!ins_ok(ne)){badwalks++; curbad=1;} } return; }
  for(int i=0;i<ne;i++){ if(used>>i&1) continue; int w=pos+el[i];
    if(cnt==ne-1){ if(w==0){ path[cnt]=el[i]; dfs(0,cnt+1,used|1ULL<<i);} continue; }
    if(w<lo||w>hi||vis[w+256]) continue; vis[w+256]=1; path[cnt]=el[i]; vtx[cnt+1]=w; dfs(w,cnt+1,used|1ULL<<i); vis[w+256]=0; }
}
int main(int argc,char**argv){ int V=atoi(argv[1]),MAXE=atoi(argv[2]); int shown=0;
  for(int P=1;P<(1<<V);P++) for(int N=1;N<(1<<V);N++){
    int sp=0,sn=0,p1=0,q1=0,c=0; for(int x=1;x<=V;x++){ if(P>>(x-1)&1){sp+=x;c++;p1=x;} if(N>>(x-1)&1){sn+=x;c++;q1=x;} }
    if(sp!=sn||c>MAXE) continue;
    for(X=1;X<=V;X++){ if(!((P&N)>>(X-1)&1)||X==p1||X==q1) continue;
      int P2=P&~(1<<(X-1)),N2=N&~(1<<(X-1));
      ne=0; el[ne++]=p1; for(int x=1;x<=V;x++){ if((P2>>(x-1)&1)&&x!=p1) el[ne++]=x; if(N2>>(x-1)&1) el[ne++]=-x; }
      lo=-q1+1; hi=p1; memset(vis,0,sizeof vis); vis[256]=1; vis[p1+256]=1; path[0]=p1; vtx[0]=0; vtx[1]=p1;
      long long w0=walks,b0=badwalks; curbad=0; dfs(p1,1,1ULL); inst++;
      if(walks-w0>0 && badwalks-b0==walks-w0){ badinst++; if(shown<8){shown++; printf("ALL reduced walks fail: x=%d P=",X); for(int x=1;x<=V;x++) if(P>>(x-1)&1) printf("%d,",x); printf(" N="); for(int x=1;x<=V;x++) if(N>>(x-1)&1) printf("%d,",x); printf(" (%lld walks)\n",walks-w0);} }
    }
  }
  printf("V=%d (instance,x)=%lld walks=%lld non-extendable walks=%lld instances-with-no-extendable-walk=%lld\n",V,inst,walks,badwalks,badinst);
}
