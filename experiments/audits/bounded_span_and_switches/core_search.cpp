// Exhaustive canonical-core search with independent, non-root switches.
// Input: p and five unpaired residues. Maximal symmetric completion only.
// Output: first witness, or failure for the specified switch budget.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <vector>
#include <set>
using namespace std;
int p;
int mod(long long x){int r=x%p;return r<0?r+p:r;}
struct Opt {vector<int>D,E;int d,e;};
int main(int argc,char**argv){
 int cap=argc>1?stoi(argv[1]):1;
 vector<int>U(5);if(!(cin>>p))return 0;for(int&u:U)cin>>u;sort(U.begin(),U.end());
 vector<int>A(p,1);A[0]=0;for(int u:U)A[p-u]=0;
 vector<Opt>opts;
 for(int i=0;i<5;i++)for(int j=i+1;j<5;j++){
  vector<int>X{U[i],U[j]},Y;for(int k=0;k<5;k++)if(k!=i&&k!=j)Y.push_back(U[k]);int c=mod(U[i]+U[j]);
  if(!A[c])opts.push_back({X,Y,c,p-c});
  else for(int x:X)for(int y:Y){vector<int>D{X[0]==x?X[1]:X[0],p-c},E{c};for(int z:Y)if(z!=y)E.push_back(z);opts.push_back({D,E,p-x,p-y});}
 }
 vector<int>V,ix(p),where(p),alt,step;
 long long candidates=0;
 for(auto opt:opts){
  auto [D,E,d,e]=opt;sort(D.begin(),D.end());sort(E.begin(),E.end());vector<int>B=A;for(int a:D)B[a]=0;for(int a:E)B[a]=0;B[d]=B[e]=1;for(int a=1;a<p;a++)assert(B[a]==B[p-a]);
  vector<int>missing;for(int a=1;a<=p/2;a++)if(!B[a])missing.push_back(a);
  for(int l=1;l<=p/2;l++){
   vector<int>omit;for(int a:missing){int t=mod(1LL*l*a);omit.push_back(min(t,p-t));}sort(omit.begin(),omit.end());
   step.clear();int parity=0;size_t mi=0;for(int a=1;a<=p/2;a++){if(mi<omit.size()&&a==omit[mi]){mi++;continue;}step.push_back(parity++%2?p-a:a);}int k=step.size();for(int i=k-2;i>=0;i--)step.push_back(p-step[i]);step.push_back(p-step[k-1]);int n=step.size();
   V.resize(n);alt.resize(n);fill(ix.begin(),ix.end(),-1);int s=0;for(int i=0;i<n;i++){assert(ix[s]<0);ix[s]=i;V[i]=s;where[step[i]]=i;s=mod(s+step[i]);}assert(s==0);for(int i=0;i<n;i++)alt[i]=mod(V[i]+step[i]-step[(i+n-1)%n]);
   for(int sg:{1,-1}){
    int dd=mod(1LL*d*l*sg),ee=mod(1LL*e*l*sg),u=V[where[dd]],v=V[where[ee]];
    do{do{
      candidates++;array<int,3>K{mod(u+1LL*D[0]*l*sg),mod(v+1LL*E[0]*l*sg),mod(v+1LL*(E[0]+E[1])*l*sg)};
      if(K[0]==K[1]||K[0]==K[2]||K[1]==K[2])continue;
      vector<int>need,used;bool good=true;for(int h:K)if(ix[h]>=0)need.push_back(ix[h]);
      for(size_t j=0;j<need.size()&&good;j++){
       int i=need[j],a=step[(i+n-1)%n],b=step[i],h=alt[i];
       if((cap>=0&&int(need.size())>cap)||i==0||a==dd||a==ee||b==dd||b==ee||find(K.begin(),K.end(),h)!=K.end()||find(used.begin(),used.end(),h)!=used.end()){good=false;break;}
       for(int t:need)if((i+1)%n==t||(t+1)%n==i){good=false;break;}if(!good)break;
       used.push_back(h);int t=ix[h];if(t>=0&&find(need.begin(),need.end(),t)==need.end())need.push_back(t);
      }
      if(good){
       // Independent direct validation in scaled coordinates.
       vector<int>w=step;for(int i:need)swap(w[i-1],w[i]);vector<int>out;for(int a:w){if(a==dd)for(int z:D)out.push_back(mod(1LL*z*l*sg));else if(a==ee)for(int z:E)out.push_back(mod(1LL*z*l*sg));else out.push_back(a);}
       vector<int>seen(p),labels(p);s=0;for(int a:out){assert(!labels[a]++);s=mod(s+a);assert(!seen[s]++);}assert(s==0);for(int a=1;a<p;a++)assert(A[a]==labels[mod(1LL*a*l*sg)]);
       cout<<"PASS "<<p<<" l="<<l<<" sign="<<sg<<" d="<<d<<" e="<<e<<" D=";for(int a:D)cout<<a<<",";cout<<" E=";for(int a:E)cout<<a<<",";cout<<" switches=";for(int i:need)cout<<i<<",";cout<<" candidates="<<candidates<<"\n";return 0;
      }
    }while(next_permutation(E.begin(),E.end()));}while(next_permutation(D.begin(),D.end()));
   }
  }
 }
 cout<<"FAIL "<<p<<" cap="<<cap<<" candidates="<<candidates<<"\n";
}
