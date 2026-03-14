# CF000 v11 — Migration Delta (Pass v2)

## What changed in the full manuscript

1. Converted the manuscript to GitHub-compatible MathJax syntax using `$...$` and `$$...$$`.
2. Refined the definitions table to distinguish flatness from sterility and non-vacuousness from realizability.
3. Added an explicit origin-candidate definition.
4. Recast flat-origin classification as a theorem-or-failure result.
5. Marked each first-machine-step item as proved / not proved / blocked / requires one new explicit principle.
6. Added an explicit contamination audit for:
   - the logical domain,
   - flatness,
   - realizability,
   - the anti-flatness law,
   - and the definitions table.
7. Tightened the wording of the exact first remaining burden to WNF.

## What did not change

- The manuscript still rejects the old v10 staircase as spine.
- A8 remains downstream of the root and is not treated as primitive.
- The paper still does not claim closure on multiplicity, apartness, recursive refinement, frontier, or differentiability.

## Why this delta matters

The previous merged draft had the right architectural direction but still allowed two early leaks:

- flatness and sterility were too easy to conflate,
- realizability and non-vacuousness were too easy to conflate.

This pass closes those leaks and makes the first machine-step failure modes explicit.
