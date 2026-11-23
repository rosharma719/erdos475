// Exact zigzag decision for ONE instance with a huge node budget and a bounded direct-mapped failure cache.  usage: zigzag_big capBillions  then stdin: nP nN P.. N..
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
using namespace std; typedef unsigned long long U;
int nP,nN,n; vector<int> P,N; int Umax,Dmax; long long nodes,cap; 
const int BITS=26; vector<U> table; 
static inline U mix(U a,U b,U c){ U h=a*0x9E3779B97F4A7C15ULL; h^=(b+0x7F4A7C15ULL)*0xC2B2AE3D27D4EB4FULL; h^=(c+0x165667B19E3779F9ULL)*0x94D049BB133111EBULL; h^=h>>29; return h|1ULL; }
bool dfs(U pm,U nm,int cur,U seen,int rem){
  if(++nodes>cap) return false;
  if(rem==0) return cur==0;
  U h=mix(pm,nm,seen); U slot=h>>(64-BITS); if(table[slot]==h) return false;
  bool ok=false;
  if(cur>=0 && !(cur==0 && rem!=n)){
    if(cur==0){ for(int i=nP-1;i>=0&&!ok;i--) if(!(pm>>i&1)){ int x=P[i]; if(seen>>(x+Dmax-1)&1) continue; ok=dfs(pm|(1ULL<<i),nm,x,seen|(1ULL<<(x+Dmax-1)),rem-1); } }
    else { for(int i=nN-1;i>=0&&!ok;i--) if(!(nm>>i&1)){ int x=cur-N[i]; if(x==0){ if(rem==1) return true; continue;} if(x<1-Dmax||x>Umax||(seen>>(x+Dmax-1)&1)) continue; ok=dfs(pm,nm|(1ULL<<i),x,seen|(1ULL<<(x+Dmax-1)),rem-1); } }
  } else { for(int i=nP-1;i>=0&&!ok;i--) if(!(pm>>i&1)){ int x=cur+P[i]; if(x==0){ if(rem==1) return true; continue;} if(x<1-Dmax||x>Umax||(seen>>(x+Dmax-1)&1)) continue; ok=dfs(pm|(1ULL<<i),nm,x,seen|(1ULL<<(x+Dmax-1)),rem-1); } }
  if(!ok && nodes<=cap) table[slot]=h; return ok; }
int main(int argc,char**argv){ cap=(long long)(atof(argv[1])*1e9); table.assign(1ULL<<BITS,0);
  cin>>nP>>nN; P.assign(nP,0); N.assign(nN,0); for(auto&x:P)cin>>x; for(auto&x:N)cin>>x; sort(P.begin(),P.end()); sort(N.begin(),N.end()); n=nP+nN; Umax=P.back(); Dmax=N.back();
  bool r=dfs(0,0,0,1ULL<<(Dmax-1),n); printf("%s nodes=%lld\n", r?"FOUND":(nodes>cap?"UNDETERMINED(cap)":"NONE (exhaustive)"), nodes); }
