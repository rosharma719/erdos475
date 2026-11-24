// Hamiltonian path on D=[-b,a]\{1,1-b,y}, start 0 -> a, lengths [1,M-1]\{b} each once.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int M,a,b,off,inD[256],usedv[256],usedl[256],path[256],need; long long nodes,cap;
int dfs(int v,int k){
  if(++nodes>cap) return -1;
  if(k==need) return 1;
  for(int l=M-1;l>=1;l--){ if(usedl[l]) continue;
    for(int s=-1;s<=1;s+=2){ int w=v+s*l; if(w+off<0||w+off>=256||!inD[w+off]||usedv[w+off]) continue;
      usedl[l]=1; usedv[w+off]=1; path[k]=w; int r=dfs(w,k+1); if(r) return r; usedl[l]=0; usedv[w+off]=0; } }
  return 0;
}
int main(int argc,char**argv){
  int Mmax=atoi(argv[1]); cap=atoll(argv[2]); int ysel=atoi(argv[3]);
  for(M=5;M<=Mmax;M++){ printf("M=%d:",M);
    for(a=2;2*a<M+1;a++){ b=M+1-a; off=128; memset(inD,0,sizeof inD); memset(usedv,0,sizeof usedv); memset(usedl,0,sizeof usedl);
      int y= ysel? -b : a-1;
      for(int x=-b;x<=a;x++) if(x!=1&&x!=1-b&&x!=y) inD[x+off]=1;
      need=M-1; usedv[0+off]=1; usedv[a+off]=1; usedl[a]=1; usedl[b]=1; path[0]=0; path[1]=a; nodes=0;
      int r= inD[a+off]? dfs(a,2) : 0;
      printf(" a%d:%s",a,r==1?"Y":r==0?"n":"?"); }
    printf("\n"); fflush(stdout); }
}
