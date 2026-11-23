// IRC search: positive integers P and N (multisets) with sum P == sum N.  Find an ordering of all steps (+p_i, -n_j) with partial sums
// S_0=0,S_1..S_{n-1} pairwise distinct (S_n=0 closes) and max(S)-min(S) <= R (over S_0..S_{n-1}).  stdin: nP nN P.. N.. R ; stdout: 1 found / 0 none (exhausted) / -1 undetermined
#include <cstdio>
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <bitset>
using namespace std;
int n; vector<int> step; int R; long long nodes,cap; mt19937_64 rng(7);
bitset<1024> vis; const int OFF=512;
int dfs(int depth,int s,int lo,int hi,unsigned long long usedLo,unsigned long long usedHi){ // used as two 64-bit words (n<=128)
  if(++nodes>cap) return -1;
  if(depth==n) return s==0?1:0;
  int idx[128]; int m=0; for(int i=0;i<n;i++){ bool u = i<64? (usedLo>>i&1):(usedHi>>(i-64)&1); if(!u) idx[m++]=i; }
  for(int i=m-1;i>0;i--){int j=rng()%(i+1); swap(idx[i],idx[j]);}
  int lastStepSeen=-1;
  for(int t=0;t<m;t++){ int i=idx[t]; int ns=s+step[i];
    if(depth==n-1){ if(ns==0) return 1; continue; }
    if(vis[ns+OFF]) continue; int nlo=min(lo,ns), nhi=max(hi,ns); if(nhi-nlo>R) continue;
    // skip duplicate equal steps at same node
    bool dup=false; for(int u=0;u<t;u++) if(step[idx[u]]==step[i]){dup=true;break;} if(dup) continue;
    vis[ns+OFF]=1; unsigned long long ul=usedLo, uh=usedHi; if(i<64) ul|=1ULL<<i; else uh|=1ULL<<(i-64);
    int r=dfs(depth+1,ns,nlo,nhi,ul,uh);
    if(r==1) return 1; vis[ns+OFF]=0; if(r==-1) return -1; }
  return 0; }
int solve(){ long long caps[]={50000,500000,5000000,50000000};
  for(int c=0;c<4;c++){ cap=caps[c]; nodes=0; vis.reset(); vis[OFF]=1; int r=dfs(0,0,0,0,0,0); if(r==1) return 1; if(r==0) return 0; } return -1; }
int main(){ int nP,nN; while(cin>>nP>>nN){ n=nP+nN; step.assign(n,0); for(int i=0;i<nP;i++) cin>>step[i]; for(int j=0;j<nN;j++){int v; cin>>v; step[nP+j]=-v;} cin>>R; printf("%d\n",solve()); fflush(stdout);} }
