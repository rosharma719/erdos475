# Next round: turn the a=2 certificates into explicit formulas (they are almost there)

Audit (Claude): all 57 of your junction certificates re-verified with independent code (vertex set, labels
[1..M]\{2}, no distance-2 pair, span <= 2M, and the full signed cycle with range <= 2M+2): 0 invalid. Theorems A, C, G
read and accepted; B, D, E, F accepted as stated (vertex-level only).

KEY OBSERVATION. Your certificates for M ≡ 5 (mod 8) are already a uniform template. Written relative to M
(e.g. "M-13", "-M+21"), M = 61, 69, 77, 85 all read:
  0, M-1, M-2, M-9,                          (header)
  4, M-13, 8, M-17, 12, M-21, ...            (zigzag Z1: 4i <-> M-9-4i)
  [middle gadget of ~8-10 vertices]          (the only part that changes with M)
  -M+33?, ..., -M+21, -25, -M+17, -21, ..., -M+1, -5   (zigzag Z2)
  M-8, -1, M-12, 3, M-16, 7, ..., 23, M-36   (zigzag Z3: 4i-1 <-> M-8-4i)
  [short gadget], -M+28, -28, -M+24, ..., -M+4, -4, -M  (zigzag Z4)
e.g. M=77: 0 M-1 M-2 M-9 4 M-13 8 M-17 12 M-21 16 M-25 20 | 28 -M+37 M-45 M-41 M-29 M-5 M-33 24 M-37 | -M+40 -M+29
-M+44 -M+25 -29 -M+21 -25 ... -M+1 -5 | M-8 -1 M-12 3 ... 27 M-40 | M-46 -M+33 -M+36 -M+41 -M+32 -M+45 -M+28 | -28
-M+24 -24 ... -M+4 -4 -M.
TASK: for each residue class of M modulo 8 (or 16 if the middle gadget needs it), write the path as explicit zigzag
blocks + bounded gadgets with endpoints given as linear functions of M, and PROVE that the edge lengths are exactly
[1..M]\{2} (each zigzag block uses a consecutive run of labels, the gadgets fill the gaps) and the vertex set avoids
distance 2 with span <= 2M. Small M by certificates. This proves a=2 for every M (together with H_k for M ≡ 2 mod 4).
Then do the same for a=3 (Claude L32: blocks + a step-2 run) and a=4.
