// Exact count of valid cyclic orders for every zero-sum k-set up to dilation; report min/mean and minimizers.
#include <cstdio>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std; typedef unsigned long long U;
int p,K; vector<int> A; long long cnt;
void dfs(int depth,int sum,U used,U vis){
  if(depth==K-1){ for(int i=1;i<K;i++) if(!(used>>i&1)) if((sum+A[i])%p==0) cnt++; return; }
  for(int i=1;i<K;i++) if(!(used>>i&1)){ int ns=(sum+A[i])%p; if(vis>>ns&1) continue; dfs(depth+1,ns,used|(1ULL<<i),vis|(1ULL<<ns)); }
}
bool canonical(const vector<int>&s){ for(int a=2;a<p;a++){ vector<int> t; t.reserve(s.size()); for(int x:s) t.push_back(x*a%p); sort(t.begin(),t.end()); if(t<s) return false; } return true; }
int main(int argc,char**argv){ p=atoi(argv[1]); int kmin=atoi(argv[2]), kmax=atoi(argv[3]);
  for(int k=kmin;k<=kmax;k++){ K=k; long long best=-1, tot=0, n=0, zeros=0; vector<vector<int>> mins; 
    vector<int> idx(k); for(int i=0;i<k;i++) idx[i]=i+1;
    while(true){ int s=0; for(int x:idx) s+=x;
      if(s%p==0){ vector<int> v(idx.begin(),idx.end()); if(canonical(v)){ A=v; cnt=0; int r0=A[0]%p; dfs(1,r0,1ULL,(1ULL<<0)|(1ULL<<r0)); n++; tot+=cnt; if(cnt==0) zeros++;
          if(best<0||cnt<best){best=cnt; mins.clear(); mins.push_back(v);} else if(cnt==best && mins.size()<4) mins.push_back(v); } }
      int i=k-1; while(i>=0 && idx[i]==p-1-(k-1-i)) i--; if(i<0) break; idx[i]++; for(int j=i+1;j<k;j++) idx[j]=idx[j-1]+1; }
    double fact=1; for(int i=2;i<k;i++) fact*=i;
    printf("p=%d k=%d: orbits %lld, sets with NO valid cycle %lld, min #cycles %lld (=%.2e of (k-1)!), mean %.1f; minimizers:",p,k,n,zeros,best,best/fact,(double)tot/n);
    for(auto&v:mins){printf(" {"); for(size_t j=0;j<v.size();j++) printf("%d%s",v[j],j+1<v.size()?",":""); printf("}");} printf("\n"); fflush(stdout); }
}
