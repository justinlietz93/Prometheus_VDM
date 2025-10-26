# Causal DAG Audits for the Void Dynamics Model (VDM)

**Date:** 2025-10-08
**Commit:** 09f571e8edaf344582b2db86aa4e5e1bee25c615

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz - Neuroca, Inc.

## 3. Abstract

We propose a lightweight, order-only causality audit for VDM that complements existing, metric-based gates (light-cone locality and dispersion) with background-free diagnostics derived from event precedence. The experiment constructs an event directed acyclic graph (DAG) from timestamped events and: (i) verifies acyclicity (modulo jitter tolerance), (ii) computes a transitive reduction (TR) to expose the minimal causal skeleton, (iii) samples Alexandrov intervals I(p, q) to estimate the Myrheim–Meyer ordering fraction and an effective dimension d̂, and (iv) tests diamond growth scaling |I| vs Δt. Optional checks compare the causal frontier with the previously validated light-cone bound. Outputs are figures/CSV/JSON under the standard outputs/ tree with approval/quarantine policy. These audits provide an orthogonal consistency lens that can reveal timebase, scheduling, or hidden nonlocalities that metric gates may miss, without changing the runtime.

## 4. Background & Scientific Rationale

The VDM program established calibrated locality via a light-cone gate (front speed v_front ≤ c(1+ε)) and dispersion via ω² ≈ c²k² in a Klein–Gordon J-only regime. These tests rely on substrate geometry and a normalized speed scale c. Causal-set theory instead probes spacetime structure using only event precedence: causal order defines intervals and combinatorial statistics (Bombelli et al., PRL 59, 521; Myrheim 1978; Meyer 1988). Translating this idea to VDM provides three benefits: (1) geometry-agnostic hygiene (acyclicity, minimal causal skeleton), (2) emergent-dimension probes that should be consistent with the substrate and dynamics in a statistically stationary window, and (3) cross-validation of cone-like frontiers without assuming distances. Agreement between order-only and metric-based diagnostics strengthens the physical consistency of VDM; discrepancies localize issues (e.g., clock skew, batching artifacts, or implicit shortcuts).

Novelty: Applying order-only causal audits as gates alongside PDE-calibrated cones/dispersion within VDM’s approvals-and-artifacts discipline. Impact: increases robustness of claims about locality and propagation without architectural changes.

## 5. Intellectual Merit and Procedure

- Importance: Tests whether causality, as a partial order, is coherent with measured cones/dispersion; detects nonlocal artifacts.
- Potential impact: Cross-domain generalization; reusable audits across VDM domains (metriplectic, RD, dark photons) with minimal effort.
- Approach clarity: Implemented as a separate, approved runner; uses a common helper for reuse; bounded algorithms with budgets to avoid scans.
- Rigor: Pre-registered gates, proposal approval, quarantined artifacts by default; figures and CSV/JSON logged; row-hashed DB entries.

### 5.1 Experimental Setup and Diagnostics

Known parameters and inputs:

- Event list: tuples (id, t[, payload]) from existing logs; strictly increasing time per edge with jitter tolerance δ.
- Optional edges: supplied or inferred by time ordering within a tolerance window and a max-successors cap.
- Optional node positions: for optional cone-frontier comparison.
- Speed scale c and ε from prior KG cone normalization.

Diagnostics (generated):

- DAG acyclicity (boolean) and counts of negative-lag edges within/outside δ.
- Transitive reduction edge count m_TR versus original m.
- Interval samples: tuples (p, q, Δt, |I|, r) with ordering fraction r and effective dimension d̂ per interval; bootstrap CIs.
- Diamond scaling: slope of log |I| vs log Δt across a mid-scale window; compare to mean d̂ within tolerance δ_d.
- Optional cone frontier consistency (when positions exist): frontier alignment with v_front ≤ c(1+ε).

Tools/scripts to fabricate:

- Common helper: Derivation/code/common/causality/{event_dag,intervals,diagnostics}.py (already created).
- Runner: Derivation/code/physics/causal/run_causal_dag_audit.py (new), using io_paths and results_db, with approval checks.

### 5.2 Experimental runplan

- Step 1: Approve tag Causal-DAG-audit-v1 for script run_causal_dag_audit with script-scoped HMAC and proposal path.
- Step 2: Ingest event logs; build times/adj with edge inference off by default; optionally enable inference with conservative caps.
- Step 3: Compute DAG summary and TR; sample K intervals (K≈128–512), compute r and d̂ per sample; fit diamond scaling.
- Step 4: Gates: (G1) acyclicity true (within δ jitter), (G2) slope(log|I| vs log Δt) ≈ mean d̂ ± δ_d, (G3 optional) frontier ≤ c(1+ε).
- Step 5: Persist artifacts: PNG (hist d̂, |I| vs Δt), CSV (interval samples, violations), JSON (summary), DB rows with row_hash.
- Step 6: RESULTS note under Derivation/Causality with tagged assets and gate outcomes.

Runtime estimate: seconds to minutes depending on event count and K; algorithms are bounded by edge and reachability budgets.

Success plan: All gates pass, figures/CSV/JSON produced, DB updated, RESULTS published.

Failure plan: Quarantine artifacts, report which gate failed and likely cause (jitter, nonstationarity, shortcut density); iterate with adjusted caps or clarified logs.

## 6. Personnel

- Justin K. Lietz: Design and execution; approves tag; curates event sources; interprets outcomes and authors RESULTS.

## 7. References

- L. Bombelli, J. Lee, D. Meyer, R. Sorkin, "Space-Time as a Causal Set," Phys. Rev. Lett. 59, 521 (1987).
- J. Myrheim, CERN preprint (1978); D. Meyer, "The Dimension of Causal Sets," PhD thesis (1988).
- S. Weinberg, "The Quantum Theory of Fields, Vol. 1" (Cambridge, 1995) - dispersion context.
- Wolfram Physics Project, causal graph resources (2020–).
