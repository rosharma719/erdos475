import sys, time
src=open('sparse_theorem_check.py').read()
exec(src[:src.index("for m,p in [(3,5)")])
for m,p in [(4,13),(5,7)]:
    t0=time.time(); eps,f,rows,ratios,allzero=run(m,p)
    print(f"m={m}, p={p}: eps={eps}; ratios Phi/Phi~ over theta in F_p minus {{+-1}}: {sorted(ratios,key=str)}; all zero: {allzero}; {len(rows)} theta values, nonzero Phi at {sum(1 for r in rows if r[1])}  ({time.time()-t0:.0f}s)",flush=True)
