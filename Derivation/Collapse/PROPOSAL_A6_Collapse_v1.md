# A6 Scaling Collapse - Proposal (v1)

Author: Justin K. Lietz
Date: 2025-10-06

## 1. Proposal Title and date

A6 Scaling Collapse: Junction Logistic Universality Test (v1) - 2025-10-06

## 2. Proposers and institutions

Justin K. Lietz - Neuroca, Inc.

## 3. Abstract

Test a dimensionless scaling collapse predicted by the steering layer: when routing at a Y-junction is softmax in the memory field m, the branch probability collapses to a universal curve P(A) = σ(Θ Δm) when plotted against X = Θ Δm. We will overlay curves for multiple Θ, quantify the envelope width, and gate PASS if max envelope ≤ 2%.

## 4. Background & Scientific Rationale

The derivation shows that a softmax router with index n = exp(Θ m) leads to binary logistic selection at a two-branch junction, P(A) = σ(Θ (m_A - m_B)). Thus, plotting P(A) against X = Θ Δm should collapse curves for different Θ. This collapse demonstrates universality of the steering mechanism and isolates Θ as the only slope parameter. The experiment is low risk, high value: a clear falsification test with explicit gates, sensible diagnostics, and small compute cost.

Questions addressed:

- Does the junction selection indeed collapse to σ(X) across Θ?
- Is the residual envelope ≤ 2% across the shared domain?
- Are there systematic deviations (e.g., at large |X|) that indicate model mismatch?

## 5.1 Experimental Setup and Diagnostics

- Protocol: sample P(A) at a junction for several Θ and Δm sweeps; compute the envelope on a shared X grid.
- Parameters: Θ ∈ {1.5, 2.5, 3.5}; Δm ∈ [-2, 2] sampled uniformly (25 points); trials per Δm = 4000.
- Diagnostics: overlay plot; envelope CSV; JSON with env_max and gate result. Gate: max envelope ≤ 0.02.

Artifacts (tag A6-collapse-v1):

- Figure: derivation/code/outputs/figures/collapse/a6_collapse_overlay__A6-collapse-v1.png
- CSV: derivation/code/outputs/logs/collapse/a6_collapse_envelope__A6-collapse-v1.csv
- JSON: derivation/code/outputs/logs/collapse/a6_collapse__A6-collapse-v1.json

## 5.2 Experimental runplan

- Generate three curves (Θ = 1.5, 2.5, 3.5) across Δm grid; compute envelope on the shared X domain.
- PASS if env_max ≤ 2%; else emit CONTRADICTION_REPORT with artifacts. Runtime < 1 minute.
- Publication: include overlay with shaded envelope and a small table of env_max; link CSV/JSON.

## 6. Personnel

Justin K. Lietz - plan, implement, execute, and document the study; review collapse quality and downstream use in universality claims.

## 7. References

- Derivation notes in memory steering (junction logistic collapse) within this repository.
