import sys, itertools, time
sys.path.insert(0, "experiments/irc")
from zigzag_sat import decide
V = int(sys.argv[1]); fails = []; n = 0; t = time.time()
for mask in range(1, 1 << V):
    S = [i + 1 for i in range(V) if mask >> i & 1]
    if len(S) < 2: continue
    r, st, it = decide(S, S); n += 1
    if r == "NONE": fails.append(S)
print(f"symmetric sets S ⊆ [1..{V}] (|S|>=2) tested {n}; with NO zigzag: {len(fails)}  [{time.time()-t:.0f}s]")
for S in fails: print(S)
