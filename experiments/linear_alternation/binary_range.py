import sys, binary_alternation_check as B
from math import gcd
for n in range(int(sys.argv[1]), int(sys.argv[2])+1):
    res=B.run(n); g=0; worst=0
    for d,(q,err) in res.items():
        worst=max(worst,err)
        for v in q: g=gcd(g,abs(v))
        print(f"n={n} d={d} err={err:.1e} q0={q[0]} gcd_d={__import__('functools').reduce(gcd,[abs(v) for v in q])}",flush=True)
    print(f"n={n} beta={g} max_round_err={worst:.1e}",flush=True)
