// Rooted valid-cycle search with optional forced prefix and forbidden vertex.
// stdin lines: p k a1..ak  npre b1..bnpre  forbid   ; (forbid=0 -> none).  The prefix steps must be elements of the set, placed first.
// stdout per line: 1 found, 0 exhaustively none (within full search), -1 undetermined (node cap after restarts).
#include <cstdio>
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
using namespace std; typedef unsigned __int128 U;
int p,k; vector<int> A; vector<int> pre; int forb; mt19937_64 rng(12345);
long long nodes, cap; vector<int> order_; U usedS; U vis; int best_len;
bool exhausted_flag;
int dfs(int sum,int depth,vector<int>&perm){ // returns 1 found, 0 fail, -1 cap
  if(++nodes>cap) return -1;
  if(depth==k) return sum==0?1:0;
  int idx[128]; int m=0; for(int i=0;i<k;i++) if(!(usedS>>i&1)) idx[m++]=i;
  for(int i=m-1;i>0;i--){int j=rng()%(i+1); swap(idx[i],idx[j]);}
  for(int t=0;t<m;t++){ int i=idx[t]; int ns=(sum+A[i])%p;
    if(depth==k-1){ if(ns==0){ return 1;} continue; }
    if(vis>>ns&1) continue; if(ns==forb) continue;
    vis|=(U)1<<ns; usedS|=(U)1<<i;
    int r=dfs(ns,depth+1,perm);
    if(r==1) return 1;
    vis&=~((U)1<<ns); usedS&=~((U)1<<i);
    if(r==-1) return -1;
  }
  return 0;
}
int solve(){
  // fix prefix
  long long caps[]={20000,200000,2000000,20000000};
  for(int ci=0; ci<4; ci++){
    cap=caps[ci]; nodes=0; usedS=0; vis=(U)1; int sum=0; bool ok=true;
    for(int b:pre){ int i=-1; for(int j=0;j<k;j++) if(A[j]==b && !(usedS>>j&1)) {i=j;break;} if(i<0){ok=false;break;}
      sum=(sum+b)%p; if((vis>>sum&1)||sum==forb){ if(!(k==(int)pre.size()&&sum==0)){ok=false;break;} } vis|=(U)1<<sum; usedS|=(U)1<<i; }
    if(!ok) return 0;
    int r=dfs(sum,(int)pre.size(),order_);
    if(r==1) return 1;
    if(r==0) return 0;   // complete search finished with no cycle
  }
  return -1;
}
int main(){ while(true){ if(!(cin>>p>>k)) break; A.assign(k,0); for(int i=0;i<k;i++) cin>>A[i]; int np; cin>>np; pre.assign(np,0); for(int i=0;i<np;i++) cin>>pre[i]; cin>>forb; printf("%d\n",solve()); fflush(stdout);} }
