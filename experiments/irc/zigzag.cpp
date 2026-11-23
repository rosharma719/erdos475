// Zigzag existence: P,N sets of positive ints with equal sums. Ordering starts with a positive step; then a negative step whenever the current sum >0, a positive step when <0;
// partial sums S_0=0,S_1..S_{n-1} pairwise distinct (S_n=0). stdin: nP nN P.. N..; stdout 1 found / 0 none (exhausted) / -1 undetermined (node cap)
#include <cstdio>
#include <iostream>
#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std; typedef unsigned long long U;
int nP,nN,n; vector<int> P,N; int Umax,Dmax; long long nodes,cap; unordered_set<unsigned long long> failed;
struct Key{U a,b,c;};
bool dfs(U pm,U nm,int cur,U seen,int rem){ // seen: bit (cur+Dmax-1) for vertex cur... window [1-D,U]
  if(++nodes>cap) return false;
  if(rem==0) return cur==0;
  unsigned long long h=pm*1000003ULL ^ (nm*998244353ULL) ^ (seen*1469598103934665603ULL); 
  if(failed.count(h)) return false;
  bool ok=false;
  if(cur>=0 && !(cur==0 && rem!=n)){ // cur==0 only at the start
    if(cur==0){ for(int i=nP-1;i>=0&&!ok;i--) if(!(pm>>i&1)){ int x=P[i]; if(seen>>(x+Dmax-1)&1) continue; ok=dfs(pm|(1ULL<<i),nm,x,seen|(1ULL<<(x+Dmax-1)),rem-1); } }
    else { for(int i=nN-1;i>=0&&!ok;i--) if(!(nm>>i&1)){ int x=cur-N[i]; if(x==0){ if(rem==1) return true; continue;} if(x<1-Dmax||x>Umax||(seen>>(x+Dmax-1)&1)) continue; ok=dfs(pm,nm|(1ULL<<i),x,seen|(1ULL<<(x+Dmax-1)),rem-1); } }
  } else { for(int i=nP-1;i>=0&&!ok;i--) if(!(pm>>i&1)){ int x=cur+P[i]; if(x==0){ if(rem==1) return true; continue;} if(x<1-Dmax||x>Umax||(seen>>(x+Dmax-1)&1)) continue; ok=dfs(pm|(1ULL<<i),nm,x,seen|(1ULL<<(x+Dmax-1)),rem-1); } }
  if(!ok && nodes<=cap) failed.insert(h); return ok; }
int main(){ while(cin>>nP>>nN){ P.assign(nP,0); N.assign(nN,0); for(auto&x:P)cin>>x; for(auto&x:N)cin>>x; sort(P.begin(),P.end()); sort(N.begin(),N.end()); n=nP+nN; Umax=P.back(); Dmax=N.back(); failed.clear(); nodes=0; cap=60000000;
   bool r=dfs(0,0,0,1ULL<<(Dmax-1),n); printf("%d\n", r?1:(nodes>cap?-1:0)); fflush(stdout);} }
