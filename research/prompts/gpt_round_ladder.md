# Next round: the explicit all-M B-shape family via a "zigzag ladder" (supersedes gpt_round_zigzag_gadgets.md)

Your last round: multimerge (scale-separated) and the rainbow spanning tree are correct but do not touch the dense
Hamiltonicity problem. Here is concrete structure for that problem (Claude, from canonical solutions; data in
research/data/B_canonical_paths.txt, vertices written relative to M: "M-5" means M-5).

1. Universal header, for every a and M tested (a=4..11, M=24..33):
     ... , M+1, a, 0, M-3, -1, M-2, 2, M-4, 3, M-5, ...
   labels along it: b, a, M-3, M-2, M-1, M-4, M-6, M-7, M-8.
2. The rest is a LADDER of inward zigzag blocks. Block with low run [l, l+k-1] and high run [h-k+1, h], started at h:
     h, l, h-1, l+1, ..., ends at l+k-1; uses the 2k-1 consecutive labels h-l down to h-l-2k+2.
   Consecutive blocks traversed outward (inner block first) are joined by a link whose label is exactly the next
   label, so a ladder tiles a consecutive label range; gaps in the label range appear only where a vertex is skipped
   or a block boundary is shifted. Example a=10, M=31 (full path):
     15 14 M-15 M-12 11 M-13 12 M-14 13 | M-9 7 M-10 8 M-11 9 | M-6 4 M-7 5 M-8 6 | M+1 10 0 M-3 -1 M-2 2 M-4 3 M-5
   block (M-6,4,M-7,5,M-8,6) uses labels M-10..M-14; block (M-9,7,M-10,8,M-11,9) uses M-16..M-20;
   links: 6->M+1 has label M-5, 9->M-6 has label M-15 (so the runs join up);
   the single gap M-9 is filled by b = M+1-a = M-9. The vertex a is skipped inside a block; the inner end gadget
   (15 14 M-15 M-12 11 M-13 12 M-14 13) absorbs the remaining small labels.
3. So the design freedom is: block sizes k_j, which block attaches to M+1 (that link has label M+1-x), and where the
   skipped vertex a sits. Choose them so that the ladder's label gaps are exactly {a, b} (plus what the header uses),
   then close with an end gadget in the middle.

TASK: give, for each residue class needed (M mod 2 or mod 6, a mod 3, small exceptional a), an explicit ladder
(header + block sizes + attachment + end gadget) and PROVE: vertex set {-1,0}∪[2,M-2]∪{M+1}, edge lengths exactly
{1..M-1}, triple 0,a,M+1 consecutive. Cases with M<=21 are covered by the 90 audited certificates.
Deliver proof + stdlib verifier for all M<=400, all a. This closes the tight family for every prime p>=2M+3.
