import random, subprocess, sys, os
p = int(sys.argv[1]); sizes = list(map(int, sys.argv[2].split(","))); n = int(sys.argv[3]); walks = sys.argv[4]
rng = random.Random(p * 31 + 7)
for k in sizes:
    lines = []
    while len(lines) < n:
        A = rng.sample(range(1, p), k)
        if sum(A) % p == 0: lines.append(f"{k} " + " ".join(map(str, A)))
    r = subprocess.run(["experiments/exploration/gen_walk", str(p), walks], input="\n".join(lines) + "\n", capture_output=True, text=True, timeout=3000)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"
    nf = sum(1 for l in r.stdout.splitlines() if l.startswith("NOT FOUND"))
    print(f"k={k}: {last}; not found {nf}", flush=True)
