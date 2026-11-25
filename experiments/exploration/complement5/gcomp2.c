// Graceful completion from a prescribed prefix: given 6 signed differences W (distinct magnitudes in [1,r-1]),
// does some ordering of W and start a give a prefix alpha_1..alpha_7 in [1,r] (distinct) that extends to a graceful perm of [1..r]?
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int FR; int r,alpha[200],used[200],dused[200]; long long nodes,cap;
int ext(int i){ if(i==r) return 1; if(++nodes>cap) return 0;
  // heuristic: try largest unused difference first both directions
  int last=alpha[i-1];
  for(int d=r-1;d>=1;d--) if(!dused[d]) for(int sg=-1;sg<=1;sg+=2){int v=last+sg*d; if(v<1||v>r||used[v]) continue;
     used[v]=dused[d]=1; alpha[i]=v; if(ext(i+1)) return 1; used[v]=dused[d]=0;}
  return 0;}
int W[6],perm[6];
int tryall(){ // all orders of W and starts
  int idx[6]={0,1,2,3,4,5};
  // iterate permutations via Heap's algorithm simple: use next_permutation-like
  int c[6]={0}; int k=0;
  #define TRY { for(int a=1;a<=r;a++){ memset(used,0,sizeof used); memset(dused,0,sizeof dused); int ok=1; alpha[0]=a; used[a]=1; \
      for(int j=0;j<6;j++){int v=alpha[j]+W[idx[j]]; int d=abs(W[idx[j]]); if(v<1||v>r||used[v]||dused[d]){ok=0;break;} used[v]=dused[d]=1; alpha[j+1]=v;} \
      if(ok){ nodes=0; if(ext(7)) return 1; } } }
  TRY
  while(k<6){ if(c[k]<k){ if(k%2==0){int t=idx[0];idx[0]=idx[k];idx[k]=t;} else {int t=idx[c[k]];idx[c[k]]=idx[k];idx[k]=t;} TRY c[k]++; k=0;} else {c[k]=0;k++;} }
  return 0;}
int main(int argc,char**argv){ r=atoi(argv[1]); int trials=atoi(argv[2]); cap=atoll(argv[3]); srand(atoi(argv[4])); FR=atoi(argv[5]); int succ=0;
  for(int t=0;t<trials;t++){ int mags[200]={0}; for(int j=0;j<6;j++){int m; do m=1+rand()%(r/FR); while(mags[m]); mags[m]=1; W[j]=(rand()&1)?m:-m;}
    if(tryall()) succ++; else { printf("no completion found: r=%d W=",r); for(int j=0;j<6;j++)printf("%d ",W[j]); puts(""); } }
  printf("r=%d trials=%d completed=%d\n",r,trials,succ);}
