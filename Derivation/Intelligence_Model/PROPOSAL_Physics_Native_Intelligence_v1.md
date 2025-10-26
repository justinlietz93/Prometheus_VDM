<!-- ATTENTION! Whitepaper-grade; follow the template and include explicit gates, MathJax equations, and provenance. -->
# Physics-Native Intelligence (VDM) — Substrate v1 Proposal

Author: Justin K. Lietz  
Date: 2025-10-22  
Status: Draft for approval  
Proposed Tag: im-substrate-v1  
Provenance: commit = {git rev-parse HEAD}; salted = SHA256(commit||"im-substrate-v1")

## 1. Proposal Title and date

Physics-Native Intelligence (VDM) — Substrate v1: Conservative field substrate and void-faithfulness receipts.  
Date: 2025-10-22

## 2. Proposers and institutions

Justin K. Lietz — Prometheus_VDM

## 3. Abstract

We propose the first step of a physics-native intelligence program that avoids training and operates in real time. Phase 1 establishes a conservative, reversible substrate in which information structures can persist and interact without external learning loops. The substrate will be a 2D Klein–Gordon (KG) J-only limb with periodic or reflecting walls chosen to match meter requirements. We will certify void-faithfulness via determinism, probe-limit receipts, and conservation gates. Success provides a stable base for subsequent routing, probe-only, and actuation phases, using shared scores and dimensionless knobs to test generality across domains.

## 4. Background & scientific rationale

Analogy: As a riverbed shapes currents without consuming energy, a conservative field substrate shapes information flow without training. We first certify the bed before releasing tracers.

Technical rationale: A physics-native agent must inherit invariants from its substrate. By using a conservative KG limb with discrete energy conservation, we obtain: (i) a controlled sandbox for spatiotemporal structure; (ii) crisp meters compatible with existing canon (energy, symmetry, dispersion); (iii) discipline for real-time-only computation. This aligns with prior VDM instrumentation (thermodynamic routing, metriplectic, KG Noether), ensuring our new line starts with a certified instrument rather than a novel model.

## 5. Intellectual merit and procedure

Importance: Does a conservative substrate support robust information transport without training?  
Impact: Establishes reproducible meters and shared scores for physics-native intelligence.  
Approach: Certify a substrate with strict gates, then use it to host routing and probe-only experiments.  
Rigor: Approvals-first, quarantine unapproved runs, schema-validated summaries, artifact minimum discipline.

### 5.1 Experimental setup and diagnostics

- Substrate: 2D KG J-only conservative dynamics with leapfrog time-stepping.
- Grid/time: $(N_x, N_y)$, spacings $a_x,a_y$, $\Delta t$ with CFL guard.  
- Boundaries: reflective walls or periodic; choose consistent with meters.  
- Diagnostics/meters: energy conservation, power balance, symmetry (when applicable), determinism receipts.
- Artifacts: at least one PNG figure + one CSV log + one JSON summary per run, via io_paths with tag routing.

Equation of motion and continuity residual:

$$ \partial_t^2\,\phi - c^2\,\nabla^2\phi + \mu^2\,\phi = 0 $$

$$ r = \partial_t e + \nabla\cdot s, \quad \text{expect }\lVert r \rVert_2 \propto \mathcal{O}(\Delta t^2) $$

### 5.2 Experimental runplan

Phases and gates for substrate-only certification (no agents):

1) Energy conservation gate  

   - Gate G1: RMS energy drift $\le \epsilon_E$ with scaling $\epsilon_E = K_E (\Delta t / a)^2$.  
   - Success criteria: PASS if drift bound satisfied over $T$ and warm-up excluded.

2) Power balance gate (closed box)  

   - Gate G2: coefficient of determination $R^2 \ge 0.9995$ for $\partial_t e$ vs $-\nabla\cdot s$.  
   - Gate G3: relative imbalance $\le 0.5\%$ after warm-up.  

3) Determinism receipts  

   - Gate G4: bitwise-equal or $L_\infty \le 1\,\text{ulp}$ repetition for seed 0.  

4) Void-faithfulness receipts  

   - Gate G5: real-time only (no batch fitting; no retrospective smoothing).  
   - Gate G6: probe-limit placeholder = TRUE for substratum (no walkers/actuators present).

Resource estimate: wall-clock 1–5 minutes per substrate profile on a single CPU thread for certification runs.  
Failure plan: quarantine artifacts, capture diagnostics, adjust $\Delta t$, stencils, or boundary model; re-run under same tag with explicit FAILURE in gate matrix.

## 6. Hypotheses, KPIs, and gates (explicit)

- H1 (Conservation): With leapfrog and CFL guard, discrete energy drift scales as $\mathcal{O}(\Delta t^2)$ and remains below threshold $\epsilon_E$.  
  KPI: $\Delta E_\mathrm{RMS}$; Gate: $\Delta E_\mathrm{RMS} \le K_E (\Delta t/a)^2$.
- H2 (Continuity): Power balance holds with high fidelity.  
  KPIs: $R^2(\partial_t e, -\nabla\cdot s)$, relative imbalance $\rho_B$.  
  Gates: $R^2\ge 0.9995$, $\rho_B \le 0.5\%$.
- H3 (Determinism): Repeat runs agree bitwise or within machine-precision envelope.  
  KPI: $L_\infty$ difference of cumulative energy/diagnostics; Gate: $\le 1$ ulp.
- H4 (Void-faithfulness): No training; real-time only; probe-only status TRUE in Phase 1.  
  KPI: compliance receipts; Gates: all TRUE.

Shared score and dimensionless knob definitions for later phases (declared here for continuity):

- Shared score $F$: a composite of balance fidelity and routing anisotropy once probes are introduced; for Phase 1, we record $F$ as undefined and out of scope.  
- Dimensionless knob $\Pi$: ratio of steps to correlation length (or walkers per cell when present). For Phase 1 we log $\Pi_\mathrm{step} = T/\tau_c$ placeholder and $\Pi_\mathrm{walk}$ is N/A.

## 7. Compliance and policy

- Approvals-first: default deny; unapproved runs must use the quarantine routing with JSON receipts.  
- Schema-validated JSON summaries must be emitted; artifacts must be routed via `common/io_paths`.  
- Script-scoped HMAC approval per `common.authorization`; proposal path and schema path must be registered in domain APPROVAL.json.

## 8. Personnel

Proposer: Justin K. Lietz — leads design, preregistration, approvals, execution, and RESULTS authoring.

## 9. References

- VDM canon: Thermodynamic Routing v2; KG Noether invariants; Metriplectic structure checks.  
- Numerical analysis of leapfrog energy conservation and CFL conditions.  
- Derivation/Templates: PROPOSAL_PAPER_TEMPLATE.md; RESULTS_PAPER_STANDARDS.md.
