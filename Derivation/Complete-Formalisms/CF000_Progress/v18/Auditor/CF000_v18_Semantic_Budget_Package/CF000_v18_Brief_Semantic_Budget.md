# CF000 v18 Brief — Semantic Budget Update

## Settled baseline
- v13 remains the governing bifurcation frame.
- v15 remains the closure of the lowest-resolution positive articulation after origin.
- v18's HRDCL / HRDAP split is valid and should be preserved.
- The theorem spine is now mostly clean at the naming level.

## What is now the main risk
The main risk is no longer wording sludge in the abstract.

The main risk is:
- proving HRDAP with semantics that are only supposed to become legal after HRDAP closes.

## What the next pass should do
Add an explicit **semantic budget / unlocked definitions** mechanism for HRDAP:

- what semantics are legal now
- what imports are blocked now
- what definitions become newly live if HRDAP closes

## Why
This turns the dependency ladder into an operational guardrail instead of just a descriptive philosophy.
