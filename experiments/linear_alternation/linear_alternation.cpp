// Exact integer computation of the Hicks--Ollis--Schmitt interval-polynomial
// alternation packet.  No finite-field sampling or floating point arithmetic.
// Build: g++ -O3 -std=c++17 erdos475_linear_alternation.cpp -o alternation
// Usage: ./alternation 14  (requires roughly 2.4 GB RAM at m=14)
// Output: all c_{m,r} in the sign convention Delta=prod_{i<j}(x_j-x_i),
// followed by their nonnegative gcd.
#include <iostream>
#include <vector>
#include <tuple>
#include <cstdlib>
#include <boost/multiprecision/cpp_int.hpp>
using namespace std;
using Z = boost::multiprecision::cpp_int;

static int pop(unsigned x) { return __builtin_popcount(x); }
static int append_sign(int set, int j) { return pop(unsigned(set >> (j+1))) % 2 ? -1 : 1; }
static Z gcdz(Z a, Z b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0) { Z r = a % b; a = b; b = r; }
    return a;
}

int main(int argc, char **argv) {
    if (argc != 2) { cerr << "usage: alternation m\n"; return 2; }
    int m = atoi(argv[1]);
    if (m < 3 || m > 20) { cerr << "m must be 3..20 (large m requires substantial RAM)\n"; return 2; }
    int d = m-1, N = 1<<m, L = 1<<d, full = N-1;
    vector<vector<int>> sm(m+1), bm(d+1);
    vector<int> pos(L);
    for (int s=0; s<N; ++s) sm[pop(s)].push_back(s);
    for (int s=0; s<L; ++s) {
        int k=pop(s); pos[s]=bm[k].size(); bm[k].push_back(s);
    }
    // Wedge coordinates: (old coordinate, new coordinate, signed basis index + 1).
    vector<vector<tuple<int,int,int>>> wedge(d);
    for (int k=0; k<d; ++k) for (int u:bm[k]) for (int j=0; j<d; ++j)
        if (!(u>>j&1)) wedge[k].push_back({pos[u],pos[u|(1<<j)],append_sign(u,j)*(j+1)});

    // Evaluate at x_j=j+1 (0-based).  For a proper nonempty subset S, use
    // v(S)_j=s(S)*(T-s(S))*s(S)^j, j=0,...,m-2.
    vector<vector<Z>> V(N);
    int total=m*(m+1)/2;
    for (int s=1; s<full; ++s) {
        int a=0; for (int j=0; j<m; ++j) if (s>>j&1) a+=j+1;
        V[s].resize(d); V[s][0]=a*(total-a);
        for (int j=1; j<d; ++j) V[s][j]=V[s][j-1]*a;
    }

    // Forward exterior DP. F[S] is the signed sum of prefix wedges over
    // all permutations of S (relative sign in increasing label order).
    vector<vector<Z>> F(N); F[0]={1};
    for (int k=1; k<=d; ++k) for (int s:sm[k]) {
        vector<Z> u(bm[k-1].size());
        for (int j=0; j<m; ++j) if (s>>j&1) {
            int t=s^(1<<j), sign=append_sign(t,j);
            for (size_t h=0; h<u.size(); ++h)
                if (sign>0) u[h]+=F[t][h]; else u[h]-=F[t][h];
        }
        F[s].resize(bm[k].size());
        for (auto [i,h,q]:wedge[k-1])
            if (q>0) F[s][h]+=u[i]*V[s][q-1];
            else F[s][h]-=u[i]*V[s][-q-1];
    }

    // Reverse/adjoint DP. G[S] is the linear functional completing a
    // prefix wedge to the scalar top exterior coordinate.  At each edge
    // S\{j}->S, multiply its scalar contribution by the appended label
    // j+1, and add to the weighted numerator for position |S|.
    vector<vector<Z>> G(N); vector<Z> c(m);
    for (int j=0; j<m; ++j) {
        int s=full^(1<<j), sign=append_sign(s,j);
        G[s]={sign}; c[m-1]+=sign*(j+1)*F[s][0];
    }
    for (int k=d; k>=1; --k) for (int s:sm[k]) {
        vector<Z> g(bm[k-1].size());
        for (auto [i,h,q]:wedge[k-1])
            if (q>0) g[i]+=G[s][h]*V[s][q-1];
            else g[i]-=G[s][h]*V[s][-q-1];
        for (int j=0; j<m; ++j) if (s>>j&1) {
            int t=s^(1<<j), sign=append_sign(t,j);
            if (G[t].empty()) G[t].resize(g.size());
            Z dot=0;
            for (size_t h=0; h<g.size(); ++h) {
                dot+=F[t][h]*g[h];
                if (sign>0) G[t][h]+=g[h]; else G[t][h]-=g[h];
            }
            c[k-1]+=sign*(j+1)*dot;
        }
        vector<Z>().swap(G[s]); vector<Z>().swap(F[s]);
    }

    // det(v(S_1),...,v(S_{m-1})) = m! F_m(x_pi).
    // Delta(1,2,...,m)=prod_{j=1}^{m-1} j!.
    Z denom=1;
    for (int i=1; i<=m; ++i) { denom*=i; for (int j=1; j<i; ++j) denom*=j; }
    Z gcd=0, sum=0;
    for (auto &x:c) {
        if (x%denom!=0) { cerr << "nonintegral alternant: error\n"; return 1; }
        x/=denom; gcd=gcdz(gcd,x); sum+=x;
    }
    int reversal=(m*(m-1)/2)%2 ? -1 : 1;
    if (sum!=0) { cerr << "sum check failed\n"; return 1; }
    for (int j=0; j<m; ++j) if (c[j]!=reversal*c[m-1-j]) {
        cerr << "reversal check failed\n"; return 1;
    }
    cout << "m=" << m << " [";
    for (int j=0; j<m; ++j) { if (j) cout << ","; cout << c[j]; }
    cout << "] gcd=" << gcd << '\n';
}
