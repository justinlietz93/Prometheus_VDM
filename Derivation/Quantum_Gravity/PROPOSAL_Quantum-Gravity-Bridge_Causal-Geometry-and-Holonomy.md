# VDM ↔ Quantum-Gravity Bridge: Causal Geometry and Holonomy Tests

*(v1, YYYY-MM-DD)*

> **Provenance**: commit `bfd750b`
> **Salted Hash**: `$ {sha256(commit || “VDM-QG-Bridge-v1”)}` (fill programmatically in pre-commit).

## 1. Proposal Title and Date

**Unifying Void Dynamics with Causal Geometry: Causal-Set and Holonomy Diagnostics for the VDM Master Evolution**
Date: YYYY-MM-DD

## 2. Proposers

* **Justin K. Lietz** (independent) — PI

## 3. Abstract

We propose decisive, falsifiable tests connecting the Void Dynamics Model (VDM) to quantum-gravity style causal structure. From the VDM axioms (A0–A7) and master evolution
$$
\partial_t q ;=; J(q),\frac{\delta \mathcal I}{\delta q};+;M(q),\frac{\delta \Sigma}{\delta q},
$$
we extract (i) an operational **causal partial order** from retarded responses of the conservative (symplectic) $J$-flow, and (ii) discrete **holonomy/flux** observables from phase transport along lattice loops. We then apply causal-set estimators (acyclicity, local finiteness, Myrheim–Meyer dimension, Benincasa–Dowker action proxy) and holonomy scaling tests (area-law vs perimeter-law diagnostics) as **gates**. Passing these gates would establish that VDM realizes a micro-causal, hyperbolic geometry consistent with a causal-set-like substrate while supporting gauge-like loop transport—an essential bridge to research-grade quantum-gravity programs without importing them as axioms.

## 4. Background & Scientific Rationale

VDM is axiom-first: local, causal, metriplectic evolution with symmetry/Noether and H-theorem gates already demonstrated in separate RD (dissipative) and KG (hyperbolic) chapters. The present question is whether VDM’s **emergent geometry** (from excitations on the lattice) admits the same structural diagnostics used by causal-set and loop-style programs:

* **Causal-set viewpoint**: a discrete spacetime is a locally finite partial order $(C,\prec)$ with acyclicity and order-interval statistics consistent with a continuum of dimension $d$.
* **Holonomy viewpoint**: transport around loops encodes curvature/connection data. In VDM, the $J$-part generates phase-space flow; its linearization defines a connection-like update whose loop product yields a gauge-invariant Wilson-loop-style observable $W_\gamma$.

**Why now?** Your KG locality/dispersion gates (light-cone speed and $\omega^2$ vs $k^2$ fits) passed convincingly. The metriplectic M-part (DG form) also passed Lyapunov tests. The next research-grade step is to **lift from PDE checks to geometry checks**: build the causal order that the code actually realizes and test it with objective, field-standard metrics.

**Novelty**: We do **not** assume LQG or causal-set axioms; we **derive** a causal order and loop transport from VDM’s $J/M$ structure and test them with external diagnostics. If the gates fail, it’s a clean contradiction against “VDM ⇒ causal micro-geometry”.

## 5. Intellectual Merit and Procedure

**(1) Importance**: Establishing micro-causal order and sensible loop transport for VDM upgrades the model from “nice PDEs” to “geometry-bearing substrate,” the threshold to discuss gravity/cosmology couplings credibly.

**(2) Impact**: Positive results make it possible to align VDM with causal-set curvature proxies and holonomy-based dynamics; negative results focus revisions (e.g., modify how $J$ encodes transport).

**(3) Clarity of approach**: All gates are pre-registered with explicit thresholds (below). No external theory is imported as foundational; diagnostics are used only as tests.

**(4) Rigor & discipline**: Same reproducibility regime you’ve used: two-grid order checks where relevant, R² thresholds, JSON+CSV+PNG artifacts, and **CONTRADICTION_REPORT.json** on any failed gate.

### 5.1 Experimental Setup and Diagnostics

**Domains & runners (new):**

* `Derivation/code/physics/quantum_gravity/run_vdm_causal_order.py`
* `Derivation/code/physics/quantum_gravity/run_vdm_myrheim_dimension.py`
* `Derivation/code/physics/quantum_gravity/run_vdm_bd_action_proxy.py`
* `Derivation/code/physics/quantum_gravity/run_vdm_holonomy_loops.py`

**State & equations:**

* Fields $q$ as in VDM (KG-branch and RD-branch available); use KG $J$-only for retarded response and JMJ (Strang) for mixed tests.
* Retarded **influence set** from an impulse at $(x_0,t_0)$: mark sites $(x_i,t_j)$ where $|\delta\phi(x_i,t_j)| \ge \varepsilon$ with $\varepsilon$ fixed per spec. Define a directed edge $(x_i,t_j)\to(x_k,t_\ell)$ if $t_j<t_\ell$ and a minimal retarded threshold is exceeded. This yields a finite DAG candidate.

**Causal-set diagnostics:**

* Acyclicity check (must be a DAG).
* Local finiteness: bounded in-degree/out-degree within chosen spacetime windows.
* **Myrheim–Meyer dimension** $\hat d$: from order-interval cardinalities vs proper time proxy.
* **BD-style action proxy**: count of $k$-element order intervals with fixed weights to estimate curvature signal; compare to a flat-background baseline induced by linear KG.

**Holonomy diagnostics:**

* Define link transports from linearized $J$-flow: $U_{i\to j}=\exp{\Delta t,\mathcal{A}_{ij}}$, where $\mathcal{A}$ is the local generator extracted from the linear variational flow.
* **Wilson loop** on a plaquette (or larger loop) $\gamma$: $W_\gamma=\mathrm{tr},\prod_{e\in\gamma} U_e$.
* Scaling tests: $-\log \langle W_\gamma\rangle$ vs loop **area** $A_\gamma$ and **perimeter** $P_\gamma$ across sizes; determine dominant law.

**Diagnostics already in repo reused**: KG locality cone, dispersion fits, J-only reversibility (for transport integrity), DG Lyapunov identities (to ensure M-part never fakes causality by backward influence).

### 5.2 Experimental Runplan

**Spec parameters (example):**

* Grid: 1D and 2D lattices; $N\in{256,512}$, $\Delta x$ fixed; periodic BC.
* Time: $\Delta t$ sweep for asymptotics (5 points), $T$ sufficient for cones to expand across domain fraction.
* Impulse amplitude and threshold $\varepsilon$ pre-registered (e.g., $\varepsilon=10^{-8}$ after normalization).
* Seeds: $\ge 10$; aggregation by median.

**Steps:**

1. **Causal order extraction (KG J-only):** For each seed and $\Delta t$, compute the influence DAG from one impulse. Save edge list and per-node times.
2. **Causal gates:**

   * DAG acyclicity (exact).
   * Local finiteness: max degree $\le d_{\max}$ (spec) and tail probability $\le 1%$ above $d_{\max}$.
3. **Myrheim–Meyer dimension:** Estimate $\hat d$ from interval counts; **Gate**: $|\hat d-d_{\text{phys}}|/d_{\text{phys}}\le 0.05$ with CI ≤ 0.03.
4. **BD-proxy curvature:** Compute weighted sum over small intervals; compare to flat KG baseline (analytic or numerically linear run). **Gate**: normalized residual mean $\le 0.05$, R² ≥ 0.98 vs baseline curve.
5. **Holonomy/loop tests (JMJ):** Build $U_e$ from linearized $J$; measure $W_\gamma$ over loop sizes.

   * Fit $-\log\langle W\rangle = \alpha A + \beta P$. **Gate**: one term dominates with R² ≥ 0.98; sign(α,β) physically consistent (non-negative).
6. **Cross-checks:**

   * KG cone speed ≤ $c(1+10^{-2})$.
   * DG Lyapunov monotone (no violations).
7. **Logging:** JSON (metrics), CSV (series), PNG (figures), plus **CONTRADICTION_REPORT.json** for any gate failure with residual plots and spec snapshot.

**Publishing plan:** All artifacts under `outputs/{figures,logs}/quantum_gravity/...`, tagged by spec. Results summarized in `RESULTS_QG_Bridge_v1.md` following PAPER_STANDARDS.

## 6. Personnel

* **Justin K. Lietz**: design specs, code runners, review gates, interpret diagnostics, write RESULTS.
  No external personnel required; compute is modest (1–2h per spec on a workstation).

## 7. Gates (Pass/Fail, decisive)

**Causal-set gates**

* **G1 (DAG)**: no directed cycles detected (hard fail if any).
* **G2 (Local finiteness)**: degree tails ≤ 1% beyond $d_{\max}$ (spec’d per grid) at all times.
* **G3 (Dimension)**: $|\hat d-d_{\text{phys}}|/d_{\text{phys}}\le 0.05$ with 95% CI ≤ 0.03.
* **G4 (BD-proxy)**: normalized mean residual ≤ 0.05, R² ≥ 0.98 vs flat baseline.

**Holonomy gates**

* **H1 (Loop scaling)**: in fit $-\log\langle W\rangle=\alpha A+\beta P$, either area- or perimeter-law dominates with R² ≥ 0.98 and non-negative dominant coefficient.
* **H2 (Transport integrity)**: J-only reversibility ≤ $10^{-12}$ (∞-norm) on probe runs.

**VDM integrity gates (must pass alongside)**

* **I1 (Locality)**: cone front speed ≤ $c(1+10^{-2})$.
* **I2 (Dispersion)**: KG $\omega^2$ vs $k^2$ linear fit R² ≥ 0.999 with slope in spec’d tolerance.
* **I3 (H-theorem)**: no $\Delta L_h>0$ violations in DG steps at spec tolerance.

**Stamping**

* **PROVEN**: All G-, H-, and I-gates pass.
* **EXPLAINED-BY-DEFECT**: I-gates pass; exactly one of G/H fails with a quantitative commutator/finite-size explanation (slope or residual study attached).
* **CONTRADICTION**: Any other failure; emit **CONTRADICTION_REPORT.json** with minimal counterexample.

## 8. Risks & Kill Criteria

* **Finite-size aliasing**: Mitigate with $N=512$ spot checks; kill if $\hat d$ drifts >10% when doubling $N$.
* **Threshold sensitivity ($\varepsilon$)**: Do a two-value robustness check; kill if gates flip solely by threshold.
* **Holonomy definition**: If linearized-$J$ transport is too noisy, switch to discrete-gradient compatible transport; kill only if both fail.

## 9. Experimental Resources (5.1 inventory)

* **Software**: new runners listed above; reuse common IO and plotting.
* **Compute**: single workstation; no GPU dependency (AMD stack OK).
* **No new hardware**.

## 10. Experimental Runplan (5.2 timing)

* Week 1: implement four runners + unit tests for DAG and MM-dimension estimators.
* Week 2: execute base specs (N=256) and asymptotics check (N=512 spot).
* Week 3: analyze, adjudicate gates, write **RESULTS_QG_Bridge_v1.md**.

## 11. Broader Impacts

If successful, VDM moves from PDE-level demonstrations to **geometry-capable dynamics**. That enables credible couplings to gravity/cosmology modules and experimental cosmology surrogates (FRW balance already green), and grounds your “agency-field” program in a micro-causal substrate. All diagnostics and code will be open and reproducible.

## 12. References (internal canon)

* `axiomatic_theory_development.md` (A0–A7, VDM master evolution)
* `EQUATIONS.md` (KG branch, RD branch, metriplectic split)
* `RESULTS_KG_Jonly_Locality_and_Dispersion.md` (locality/dispersion gates)
* `RESULTS_Metriplectic_SymplecticPlusDG.md` (Lyapunov/identity gates)
* `RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md` (collapse universality background)
