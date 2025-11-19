# PROPOSALS: Overview of Research Proposals

This document provides a comprehensive overview of all research proposals in the Void Dynamics Model (VDM) repository. Each proposal follows the whitepaper-grade template standards and includes explicit gates, MathJax-rendered equations, and full provenance. Proposals are organized by domain and follow the T0-T9 maturity ladder.

**Total Proposals: 32**

> Last Updated: 2025-11-19  
> Template: `Templates/PROPOSAL_PAPER_TEMPLATE.md`  
> Standards: All proposals must be approved before experiments can run  
> Authorization: See `code/common/authorization/README.md`

---

## Table of Contents

- [Agency_Field](#agency-field) (5 proposals)
- [Causality](#causality) (2 proposals)
- [Collapse](#collapse) (1 proposal)
- [Conservation_Law](#conservation-law) (1 proposal)
- [Cosmology](#cosmology) (2 proposals)
- [Dark_Photons](#dark-photons) (1 proposal)
- [Information](#information) (1 proposal)
- [Intelligence_Model](#intelligence-model) (1 proposal)
- [Metriplectic](#metriplectic) (5 proposals)
- [Qualia](#qualia) (1 proposal)
- [Quantum_Gravity](#quantum-gravity) (2 proposals)
- [Tachyon_Condensation](#tachyon-condensation) (1 proposal)
- [Thermodynamic_Routing](#thermodynamic-routing) (7 proposals)
- [Topology](#topology) (2 proposals)

---

## Agency Field (5 proposals)

- **PROPOSAL_ADC_Response_Slope_v1.md**
  Path: `Agency_Field/PROPOSAL_ADC_Response_Slope_v1.md`
  *PROPOSAL_ADC_Response_Slope_v1.md*
  - **Summary**: We test the decision coupling law at forks: the probability of choosing branch (A) is [ P(A)=\sigma!\big(\Theta,\Delta m\big),\quad \Delta m=m_A-m_B. ] We will generate controlled junctions with prescribed (\Delta m), record choices, and verify that the **fitted logistic slope equals the programmed (\Theta)** within (\pm5%). This upgrades prior A6 collapse (shape) to a parameter-identification test (slope).
  - **Research Question(s)**:
  - The A6 logistic universality is established; tying slope to (\Theta) connects meso-scale agency to micro-level steering gain. This is a necessary calibration for coupling agency to tasks and environments.
  - **Gate(s)**:
  - Gates:** (|\hat\Theta/\Theta-1|\le 0.05); (R^2\ge 0.99); KS (p>0.1).
  - **Personnel**: Justin K. Lietz.
  - **References**: RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md; Agency_Field.md; EQUATIONS.md (A6).

---

- **PROPOSAL_Agency_Curvature_Scaling_v1.md**
  Path: `Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md`
  *PROPOSAL_Agency_Curvature_Scaling_v1.md*
  - **Summary**: We propose to validate the steering component of the agency field by measuring path curvature of test pulses moving in a memory field (m(x)). The theory predicts curvature (\kappa_{\text{path}}) scales linearly with the transverse gradient magnitude (X=\Theta,|\nabla_\perp m|), independent of pulse details. We will generate smooth (m), launch narrow pulses, and fit (\kappa)–vs–(X) across (\Theta) to demonstrate a scaling collapse and quantify residuals. Primary KPI: linear fit slope stability wi...
  - **Research Question(s)**:
  - The agency/steering law posits a slow bias field that deflects trajectories:
[
\mathbf r''(t)=\Theta,\nabla_\perp m(\mathbf r(t)) \quad\Rightarrow\quad \kappa_{\text{path}}\propto \Theta,|\nabla_\perp m|.
]
This provides an operational measure of goal-directedness: stronger, consistent bias yields reproducible curvature irrespective of carrier dynamics. Demonstrating a dimensionless collapse validates that agency is a physical field with predictable transport.

**Novelty.** Prior work establishe
  - **Gate(s)**:
  - Gates:** (|\beta|\le 0.05,\alpha,\bar X); slope CV (\le 10%) across (\Theta); (R^2\ge 0.99).
  - **Personnel**: Justin K. Lietz: design, implementation, analysis, and write-up.
  - **References**: Agency_Field.md; EQUATIONS.md (steering/agency sections); Axiomatic_theory_development.md (A0–A7).

---

- **PROPOSAL_Agency_Stability_Band_v1.md**
  Path: `Agency_Field/PROPOSAL_Agency_Stability_Band_v1.md`
  *PROPOSAL_Agency_Stability_Band_v1.md*
  - **Summary**: We will map the stability/retention regime of the memory/agency substrate predicted by the dimensionless groups (D_a) (advective/steering), (\Lambda) (loss/decay), and (\Gamma) (diffusion/spread). The memory field (m) obeys [ \partial_t m=\gamma R - \delta m + \kappa\nabla^2 m, ] with (R) as localized writes. We predict stable, high-SNR retention when (D_a\gtrsim \Lambda) at intermediate (\Gamma). KPI: a distinct band in the ((D_a,\Lambda)) plane with retention (>0.8) and boundary reproducibilit...
  - **Research Question(s)**:
  - Memory steering requires a persistent field (m) that is neither washed out (too diffusive) nor sticky (too slow to adapt). Casting the PDE in dimensionless form yields a stability band. Establishing this band experimentally ties “memory” to measurable physics.
  - **Gate(s)**:
  - Gates:** contiguous band where retention (>0.8), half-life within target window, and cross-slice reproducibility (Jaccard index (\ge 0.7)).
  - **Personnel**: Justin K. Lietz.
  - **References**: Agency_Field.md; EQUATIONS.md (memory law).

---

### Coordination Depth

- **PROPOSAL_Multipartite_Coordinaton_Depth_v1.md**
  Path: `Agency_Field/Coordination_Depth/PROPOSAL_Multipartite_Coordinaton_Depth_v1.md`
  *PROPOSAL_Multipartite_Coordination_Depth_v1.1.md*
  - **Summary**: We pre-register a **device-independent depth witness** that detects and quantifies **genuine multipartite coordination** in a metriplectic/void-dynamics agent without inspecting internal states. The 2D domain is tiled into (B) disjoint spatial blocks. For a task performance metric (J) (hit probability of a registered target (\Omega_\star) within horizon (T)), we define per-block and joint performance drops under **blockwise phase-scrambled perturbations** that preserve **local statistics** at th...
  - **Research Question(s)**:
  - An agent evolving under a metriplectic J(\oplus)M scheme can, in principle, coordinate information across disjoint regions: the **J**-branch transports structure; the **M**-branch selects via Lyapunov descent. We adopt a classical analogue of **(k)-producibility** from many-body certification: a controller decomposable into independent blocks (or using only local features) is **additive** over disjoint perturbations, implying (\Delta J_S \approx \sum_{b\in S}\Delta J_b) and thus (\mathcal S_k\ap
  - **Gate(s)**:
  - gated) for stronger nonlocal transport (report both profiles).
  - **Variables**:
    - *Independent*:
      - **Partitioning:** (B\in{4,8,16}) (regular tiling).
      - **Order sampling:** (k=1,\dots,k_{\max}) with a pre-registered count of sampled sets per (k) (e.g., 32).
      - **Landscape generator:** RD steady state with parameters ((D,r_m,u)) or spectral synthesis with fixed power spectrum; seed list.
      - **Discretization:** grid (N\in{128,256}); stencil (\in{\text{FD-3pt},\text{spectral}}).
      - **Agent:** (\mathcal P_{\mathrm{vdm}}) (J(\oplus)M; scheme (\in{\text{jmj-strang},\text{jmj-spectralDG}})), and (\mathcal P_{\mathrm{local}}) baseline (radius-(r_{\mathrm{loc}}) features only).
      - *(... and 2 more)*
    - *Dependent*:
      - (J) (primary: hit probability by (T); secondary: median time-to-hit).
      - (\Delta J_b), (\Delta J_S), (\mathcal S_k), and (\mathrm{CDI}).
      - Local match residuals at (x_0): (|m|), (|\nabla m|), (|\Delta m|), neighborhood mean/var.
    - *Control*:
      - (\mathcal P_{\mathrm{local}}) null runs (entire protocol).
      - **Near-block** perturbations that change only local features (negative control; expect (\mathcal S_k \approx 0)).
  - **Personnel**: Justin K. Lietz - VDM Project

### Witness

- **PROPOSAL_Agency_Witness_v1.md**
  Path: `Agency_Field/Witness/PROPOSAL_Agency_Witness_v1.md`
  *PROPOSAL_Agency_Witness_v1.1.md*
  - **Summary**: We pre-register a **device-independent agency witness** that detects **nonlocal, predictive coordination** in a metriplectic/void-dynamics agent **without** inspecting internal states. For a scalar landscape $m(\mathbf{x})$, we compare task performance on a baseline field $m_1$ to a counterfactual where the **far field** (beyond radius $r$ from the agent) is replaced by an **isospectral surrogate** $m_2$ that preserves **local statistics** at the agent position (value, gradient, curvature). Defi...
  - **Research Question(s)**:
  - Let $m(\mathbf{x})$ arise from an RD steady state or spectral synthesis. The agent under test, $\mathcal{P}*{\mathrm{vdm}}$, evolves under metriplectic dynamics (J$\oplus$M composition), while a **baseline local policy** $\mathcal{P}*{\mathrm{local}}$ uses only radius-$r$ features (ADC logistic on $\Delta m$ and local derivatives). We adopt a **$k$-producibility / depth** mindset from many-body certification: controllers restricted to radius $r$ are “$r$-local,” hence **invariant** to any transf
  - **Gate(s)**:
  - gated).
  - **Variables**:
    - *Independent*:
      - **Radius** $r\in{r_1,\dots,r_K}$.
      - **Landscape generator**: RD $(D,r_m,u)$ to steady state *or* spectral synthesis with fixed power spectrum.
      - **Discretization**: grid $N\in{128,256}$; stencil $\in{\text{FD-3pt},\text{spectral}}$.
      - **Agent parameters**: speed $v$, gain $\Gamma$, ADC slope $\Theta$; scheme $\in{\text{jmj-strang},\text{jmj-spectralDG}}$ (param-gated).
      - **Horizon** $T$; seed list; tag.
    - *Dependent*:
      - **Primary metric** $J$: hit-probability for $\Omega_\star$ by time $T$ (secondary: median time-to-hit).
      - **Witness** $W(r)=J_{\mathrm{real}}-J_{\mathrm{swap}}$.
      - **Local-match residuals** at $x_0$: $|m|$, $|\nabla m|$, $|\Delta m|$ mismatches; small neighborhood statistic.
    - *Control*:
      - **$\mathcal{P}_{\mathrm{local}}$**: ADC logistic with features restricted to radius $r$; no lookahead.
      - **$r=0$** (“no swap”) and **near-swap** $r=r_{\text{near}}$ (well below the field correlation length).
  - **Personnel**: Justin K. Lietz - VDM Project

## Causality (2 proposals)

- **PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md**
  Path: `Causality/PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md`
  *Causal DAG Audits for the Void Dynamics Model (VDM)*
  - **Summary**: We propose a lightweight, order-only causality audit for VDM that complements existing, metric-based gates (light-cone locality and dispersion) with background-free diagnostics derived from event precedence. The experiment constructs an event directed acyclic graph (DAG) from timestamped events and: (i) verifies acyclicity (modulo jitter tolerance), (ii) computes a transitive reduction (TR) to expose the minimal causal skeleton, (iii) samples Alexandrov intervals I(p, q) to estimate the Myrheim–...
  - **Research Question(s)**:
  - The VDM program established calibrated locality via a light-cone gate (front speed v_front ≤ c(1+ε)) and dispersion via ω² ≈ c²k² in a Klein–Gordon J-only regime. These tests rely on substrate geometry and a normalized speed scale c. Causal-set theory instead probes spacetime structure using only event precedence: causal order defines intervals and combinatorial statistics (Bombelli et al., PRL 59, 521; Myrheim 1978; Meyer 1988). Translating this idea to VDM provides three benefits: (1) geometry
  - **Experimental Setup**: Known parameters and inputs: - Event list: tuples (id, t[, payload]) from existing logs; strictly increasing time per edge with jitter tolerance δ. - Optional edges: supplied or inferred by time ordering within a tolerance window and a max-successors cap. - Optional node positions: for optional cone-frontier comparison. - Speed scale c and ε from prior KG cone normalization. Diagnostics (generat...
  - **Personnel**: - Justin K. Lietz: Design and execution; approves tag; curates event sources; interprets outcomes and authors RESULTS.
  - **References**: - L. Bombelli, J. Lee, D. Meyer, R. Sorkin, "Space-Time as a Causal Set," Phys. Rev. Lett. 59, 521 (1987).
- J. Myrheim, CERN preprint (1978); D. Meyer, "The Dimension of Causal Sets," PhD thesis (1988).
- S. Weinberg, "The Quantum Theory of Fields, Vol. 1" (Cambridge, 1995) - dispersion context.
- Wolfram Physics Project, causal graph resources (2020–).

- **PROPOSAL_Metriplectic_Causal_Dominance_v1.md**
  Path: `Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md`
  *Why I think this is a strong proposal (and not a foundation error)*
  - **Diagnostics**: And to keep the zeitgeist thread visible for folks outside VDM: Google’s posts make the echo/OTOC mechanism and its verifiability explicit; if you echo‑test on lattice and show the same phenomenology (power‑law echo decay, cone‑bounded influence), you’ve built the bridge from your classical substrat...
  - **Gate(s)**:
  - gate.**

## Collapse (1 proposal)

- **PROPOSAL_A6_Collapse_v1.md**
  Path: `Collapse/PROPOSAL_A6_Collapse_v1.md`
  *A6 Scaling Collapse - Proposal (v1)*
  - **Date**: 2025-10-06
  - **Summary**: Test a dimensionless scaling collapse predicted by the steering layer: when routing at a Y-junction is softmax in the memory field m, the branch probability collapses to a universal curve P(A) = σ(Θ Δm) when plotted against X = Θ Δm. We will overlay curves for multiple Θ, quantify the envelope width, and gate PASS if max envelope ≤ 2%.
  - **Research Question(s)**:
  - The derivation shows that a softmax router with index n = exp(Θ m) leads to binary logistic selection at a two-branch junction, P(A) = σ(Θ (m_A - m_B)). Thus, plotting P(A) against X = Θ Δm should collapse curves for different Θ. This collapse demonstrates universality of the steering mechanism and isolates Θ as the only slope parameter. The experiment is low risk, high value: a clear falsification test with explicit gates, sensible diagnostics, and small compute cost.

Questions addressed:

- D
  - **Experimental Setup**: - Protocol: sample P(A) at a junction for several Θ and Δm sweeps; compute the envelope on a shared X grid. - Parameters: Θ ∈ {1.5, 2.5, 3.5}; Δm ∈ [-2, 2] sampled uniformly (25 points); trials per Δm = 4000. - Diagnostics: overlay plot; envelope CSV; JSON with env_max and gate result. Gate: max envelope ≤ 0.02. Artifacts (tag A6-collapse-v1): - Figure: Derivation/code/outputs/figures/collapse/a...
  - **Diagnostics**: Questions addressed: - Does the junction selection indeed collapse to σ(X) across Θ? - Is the residual envelope ≤ 2% across the shared domain? - Are there systematic deviations (e.g., at large |X|) that indicate model mismatch?
  - **Gate(s)**:
  - Is the residual envelope ≤ 2% across the shared domain?
  - **Personnel**: Justin K. Lietz - Neuroca, Inc.
  - **References**: - Derivation notes in memory steering (junction logistic collapse) within this repository.

## Conservation Law (1 proposal)

- **PROPOSAL_RD_Discrete_Conservation_vs_Balance.md**
  Path: `Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md`
  *PROPOSAL - Discrete Conservation vs. Balance in a Reaction-Diffusion Update (Void Dynamics Model)*
  - **Diagnostics**: - **Scheme order p:** start with Euler (p=1), then Strang (p=2) using exact logistic substep (see reaction_exact.py). - **Neumann BCs** are reserved only for the front‑speed control runs.

## Cosmology (2 proposals)

- **PROPOSAL_FRW_Balance_v1.md**
  Path: `Cosmology/PROPOSAL_FRW_Balance_v1.md`
  *FRW Continuity Balance - Proposal (v1)*
  - **Date**: 2025-10-06
  - **Summary**: We will implement a simple, dimensionless continuity-law residual for FRW cosmology, testing discrete consistency of input (ρ(t), a(t)). The diagnostic computes the residual of d/dt(ρ a³) + w ρ d/dt(a³) (default dust w=0) and gates PASS when the RMS residual ≤ tolerance. This provides a low-cost sanity check for background bookkeeping prior to full cosmological embeddings.
  - **Research Question(s)**:
  - Energy conservation in FRW for a perfect fluid obeys \( \frac{d}{dt}(\rho a^3) + p \frac{d}{dt}(a^3) = 0 \). For an effective equation-of-state parameter w with p = w ρ, this becomes \( \frac{d}{dt}(\rho a^3) + w\rho \frac{d}{dt}(a^3) = 0 \). Our diagnostic computes a finite-difference residual of the LHS and reports RMS; a reference dust case (ρ ∝ a⁻³) should yield residuals near machine precision.
  - **Experimental Setup**: - Input: arrays ρ(t), a(t), t covering a monotone time span. - Default test: dust (ρ ∝ a⁻³). - Output: figure of residual vs t, CSV with (t, ρ, a, residual), JSON summary and PASS/FAIL vs tol. - Gate: RMS residual ≤ tol (default 1e-6); emit CONTRADICTION_REPORT on fail. Artifacts (tag FRW-balance-v1): - Figure: Derivation/code/outputs/figures/metriplectic/.../frw_continuity_residual__FRW-balance...
  - **Gate(s)**:
  - Gate: RMS residual ≤ tol (default 1e-6); emit CONTRADICTION_REPORT on fail.
  - **Personnel**: Justin K. Lietz - Neuroca, Inc.
  - **References**: - Standard FRW continuity equation; internal notes on background bookkeeping and transfer currents in this repository.

- **PROPOSAL_FRW_Continuity_Predictive_v2.md**
  Path: `Cosmology/PROPOSAL_FRW_Continuity_Predictive_v2.md`
  *FRW Continuity Predictive v2*

## Dark Photons (1 proposal)

- **PROPOSAL_Decoherence_Portals.md**
  Path: `Dark_Photons/PROPOSAL_Decoherence_Portals.md`
  *Proposal: Decoherence Portals via Dark-Photon Mixing: Noise-Spectrum and Fisher-Budget Tests of Kinetic Mixing in Shielded Cavities (DP-Portal-v1)*
  - **Summary**: We propose a disciplined, pre-registered investigation of dark-photon (DP) kinetic mixing as a decoherence portal that leaves measurable imprints in precision electromagnetic noise spectra and parameter-estimation Fisher budgets in shielded resonant cavities. The central hypothesis is that a small kinetic-mixing parameter $\varepsilon$ produces: (i) a predictable modification of the power spectral density (PSD) in well-characterized frequency bands, and (ii) a reproducible scaling of information...
  - **Research Question(s)**:
  - Dark photons arise from an additional $U(1)$ gauge sector with kinetic mixing with the Standard Model photon parameterized by $\varepsilon$ [Holdom 1986]. Precision laboratory searches often target resonant enhancement or low-noise readout to reveal feeble signals [Jaeckel & Ringwald 2010; Fabbrichesi et al. 2020]. A pragmatic intermediate step toward discovery is to pre-register robust, instrument-level signatures that are insensitive to detailed UV model choices yet directly test kinetic-mixin
  - **Experimental Setup**: Instrumentation (baseline): - Shielded resonant RF cavity (Q characterized), tunable center frequency covering $f\in[\,10^3,10^6\,]$ Hz (example band; exact band to be set by available hardware). - Cryogenic front-end with known $T_{\mathrm{phys}}$ and calibrated readout chain; spectrum analyzer or digitizer with anti-alias filters. - Calibration injection path (synthesizer) for known narrowband ...
  - **Diagnostics**: Instrumentation (baseline): - Shielded resonant RF cavity (Q characterized), tunable center frequency covering $f\in[\,10^3,10^6\,]$ Hz (example band; exact band to be set by available hardware). - Cryogenic front-end with known $T_{\mathrm{phys}}$ and calibrated readout chain; spectrum analyzer or...
  - **Personnel**: Proposer: Justin K. Lietz - responsible for modeling, pre-registration, runplan compliance, data acquisition oversight, and open-artifacts publication following the PAPER_STANDARDS.
  - **References**: - B. Holdom, Two U(1)’s and Epsilon Charge Shifts, Phys. Lett. B 166 (1986) 196-198.
- J. Jaeckel and A. Ringwald, The Low-Energy Frontier of Particle Physics, Ann. Rev. Nucl. Part. Sci. 60 (2010) 405-437.
- M. Fabbrichesi, E. Gabrielli, and G. Lanfranchi, The Physics of the Dark Photon, SpringerBriefs in Physics (2020), arXiv:2005.01515.

## Information (1 proposal)

- **PROPOSAL_SIE_Invariant_and_Novelty_v1.md**
  Path: `Information/PROPOSAL_SIE_Invariant_and_Novelty_v1.md`
  *PROPOSAL_SIE_Invariant_and_Novelty_v1.md*
  - **Summary**: We certify a clean first integral (Q) for the local information engine (SIE) in the reaction-only limit and quantify controlled deviations under novelty. For logistic-like kinetics [ \dot W=rW-uW^2,\qquad Q(W,t)=\ln!\frac{r-uW}{W}-rt, ] (Q) is constant. With a brief parameter kick, (Q) drifts and returns. KPIs: (i) two-grid slope matches integrator order; (ii) (Q)-drift is bounded and reversible when the perturbation ends.
  - **Research Question(s)**:
  - This converts “novelty/surprise” into a falsifiable, low-dimensional physics statement without any runtime. A clean invariant anchors the information-processing story to A5 (entropy/H-theorem analogs) and standard convergence theory.
  - **Experimental Setup**: * **Domain:** `Derivation/code/physics/information/` * **ODE:** as above; integrators: Euler and RK4. * **Diagnostics:** two-grid error (E(\Delta t)), log–log slope; (Q)-drift time series with/without kick; recovery time.
  - **Diagnostics**: * **Domain:** `Derivation/code/physics/information/` * **ODE:** as above; integrators: Euler and RK4. * **Diagnostics:** two-grid error (E(\Delta t)), log–log slope; (Q)-drift time series with/without kick; recovery time.
  - **Personnel**: Justin K. Lietz.
  - **References**: logarithmic_constant_of_motion.md; EQUATIONS.md; Axiomatic_theory_development.md.

---

## Intelligence Model (1 proposal)

- **PROPOSAL_Physics_Native_Intelligence_v1.md**
  Path: `Intelligence_Model/PROPOSAL_Physics_Native_Intelligence_v1.md`
  *Physics-Native Intelligence (VDM) — Substrate v1 Proposal*
  - **Date**: 2025-10-22
  - **Summary**: We propose the first step of a physics-native intelligence program that avoids training and operates in real time. Phase 1 establishes a conservative, reversible substrate in which information structures can persist and interact without external learning loops. The substrate will be a 2D Klein–Gordon (KG) J-only limb with periodic or reflecting walls chosen to match meter requirements. We will certify void-faithfulness via determinism, probe-limit receipts, and conservation gates. Success provid...
  - **Research Question(s)**:
  - Analogy: As a riverbed shapes currents without consuming energy, a conservative field substrate shapes information flow without training. We first certify the bed before releasing tracers.

Technical rationale: A physics-native agent must inherit invariants from its substrate. By using a conservative KG limb with discrete energy conservation, we obtain: (i) a controlled sandbox for spatiotemporal structure; (ii) crisp meters compatible with existing canon (energy, symmetry, dispersion); (iii) di
  - **Experimental Setup**: - Substrate: 2D KG J-only conservative dynamics with leapfrog time-stepping. - Grid/time: $(N_x, N_y)$, spacings $a_x,a_y$, $\Delta t$ with CFL guard. - Boundaries: reflective walls or periodic; choose consistent with meters. - Diagnostics/meters: energy conservation, power balance, symmetry (when applicable), determinism receipts. - Artifacts: at least one PNG figure + one CSV log + one JSON ...
  - **Diagnostics**: - Substrate: 2D KG J-only conservative dynamics with leapfrog time-stepping. - Grid/time: $(N_x, N_y)$, spacings $a_x,a_y$, $\Delta t$ with CFL guard. - Boundaries: reflective walls or periodic; choose consistent with meters. - Diagnostics/meters: energy conservation, power balance, symmetry (wh...
  - **Gate(s)**:
  - Gate G1: RMS energy drift $\le \epsilon_E$ with scaling $\epsilon_E = K_E (\Delta t / a)^2$.
  - Gate G2: coefficient of determination $R^2 \ge 0.9995$ for $\partial_t e$ vs $-\nabla\cdot s$.
  - Gate G3: relative imbalance $\le 0.5\%$ after warm-up.
  - Gate G4: bitwise-equal or $L_\infty \le 1\,\text{ulp}$ repetition for seed 0.
  - Gate G5: real-time only (no batch fitting; no retrospective smoothing).
  - Gate G6: probe-limit placeholder = TRUE for substratum (no walkers/actuators present).
  - **Personnel**: Justin K. Lietz — Prometheus_VDM
  - **References**: - VDM canon: Thermodynamic Routing v2; KG Noether invariants; Metriplectic structure checks.  
- Numerical analysis of leapfrog energy conservation and CFL conditions.  
- Derivation/Templates: PROPOSAL_PAPER_TEMPLATE.md; RESULTS_PAPER_STANDARDS.md.

## Metriplectic (5 proposals)

- **PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md**
  Path: `Metriplectic/PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md`
  *Metriplectic Composition KGplusRD v2*

- **PROPOSAL_Metriplectic_Lindblad_T4.md**
  Path: `Metriplectic/PROPOSAL_Metriplectic_Lindblad_T4.md`
  *Metriplectic Lindblad T4*
  - **Tier**: T0 (Foundational/Instrument)
  - **Diagnostics**: 3. **Clarify symmetry assumptions in the two T4s** * **PROPOSAL_SIE_Invariant_and_Novelty_v1**: add a one‑line lemma defining (Q) and the exact discrete symmetry/closure assumptions; place the drift threshold in a boxed gate. * **PROPOSAL_False‑Vacuum_Metastability_and_Void‑Debt_Asymmetry**: front‑...
  - **Gate(s)**:
  - Gate:** saturation slope (\partial n/\partial N\to 0) beyond (n\simeq 1) (units set by your normalization) across (>90%) of modes tested.
  - Gate:** an explicit algebra showing ({\hat\psi_i,\hat\psi_j}=0) in the effective theory (not yet required to be microscopic).
  - Gates:**
  - Gates:** invariant drift (|\Delta Q|/Q \le 10^{-6}) over (10^6) steps; two‑grid order (\ge 2.0) with (R^2\ge 0.999) on error vs (\Delta t).
  - Gates:** net charge/void‑debt production rate (>0) with CI not crossing zero across seeds; scaling collapse in dimensionless variables across box sizes; asymmetry vanishes when you restore the SIE assumptions.
  - Gates:**
  - Gates:**
  - Gate:** retarded support only (no pre‑response above **5σ** noise); cone slope **c** agrees with KG fit ± **2%**.
  - *(... and 2 more)*

- **PROPOSAL_Metriplectic_SymplecticPlusDG.md**
  Path: `Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md`
  *Proposal: Metriplectic - Symplectic (KG) + Discrete-Gradient (RD)*
  - **Date**: 2025-10-08
  - **Commit**: `fa2d126`
  - **Experimental Setup**: - Discretization: periodic 1D lattice, N ∈ {256}, dx = 1.0; spectral ∇, Δ for KG. - Parameters: c = 1.0, m = 0.5. - Time stepping: Störmer–Verlet with dt = min(dt_sweep) = 0.005, steps = 512 (baseline). - Diagnostics (KG-noether-v1): - Discrete energy E_d(t) and momentum P_d(t) time series; reversibility by forward/backward integration. - Artifacts: PNG (E_d, P_d vs t), CSV (t, E_d, P_...
  - **Gate(s)**:
  - gated policy with tag-scoped schemas to support canon promotion and downstream integration.
  - Gates and Success Criteria:

### Strang Defect vs dt kg RD

- **PROPOSAL_KG_plus_RD_Metriplectic.md**
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_KG_plus_RD_Metriplectic.md`
  *Proposal: KG ⊕ RD Metriplectic Experiment (Two-Field)*
  - **Date**: 2025-10-06
  - **Diagnostics**: 3. Run a minimal sweep - N=256, seeds=10, dt = [0.02, 0.01, 0.005, 0.0025]. - Record gates and artifacts; update a new RESULTS file `Derivation/kg_metriplectic/RESULTS_KG_plus_RD.md`.

- **PROPOSAL_Metriplectic_JMJ_RD_v1.md**
  Path: `Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_Metriplectic_JMJ_RD_v1.md`
  *1. Metriplectic Integrator for Mixed Conservative-Dissipative Dynamics: Symplectic J-step ⊕ Discrete-Gradient M-step*
  - **Summary**: We propose to implement and certify a **metriplectic time integrator** that composes a **symplectic step** for the conservative (J) sector with a **discrete-gradient (DG) step** for the dissipative (M) sector: $J(\Delta t/2) \to M(\Delta t) \to J(\Delta t/2)$ (Strang composition). The J-step preserves Noether invariants (to machine precision) and is time-reversible/volume-preserving; the M-step enforces an exact discrete H-theorem via the DG chain rule for the reaction-diffusion (RD) Lyapunov fu...
  - **Research Question(s)**:
  - Context.** The RD study established: (i) scheme-dependent near-conservation (Euler$\approx2$, Strang$\approx3$ two-grid slopes), (ii) no exact global invariant for Euler RD within tested $Q'$/$H$ classes (contradiction report), and (iii) a DG RD step that certifiably obeys a per-step H-theorem with identity residuals at machine precision. This motivates metriplectic composition: keep conservative structure in a **symplectic** update and dissipative structure in a **DG** update, then compose.
  - **Experimental Setup**: **State & domains.** 1D periodic lattice with spacing $\Delta x$ and size $N$. Primary field $W$ (or $(\phi,\pi)$ for an optional two-field J-test). **Functionals.** - **J Hamiltonian (example choices):** - linear wave/transport surrogate for $W$ with $$ H_J \;=\; \tfrac{c^2}{2}\,\|\nabla_h W\|^2. $$ - two-field KG toy $$ H_J \;=\; \tfrac12\|\pi\|^2 + \tfrac12 c^2\|\nabla_h \phi\|^2 ...
  - **Personnel**: **Justin K. Lietz** - design, implementation (new modules only), CAS/analysis, and write-up. No changes to prior RD scripts; reproducibility preserved.
  - **References**: - Prior RD results document (canonical reference for harness, gates, and artifact style).
- Symplectic (Verlet/leapfrog) and discrete-gradient/AVF methods (to be cited in the paper).
- PAPER_STANDARDS.md for figure/CSV pairing, numeric captions, provenance, and acceptance gate reporting.

## Qualia (1 proposal)

- **PROPOSAL_vdm_qualia_program.md**
  Path: `Qualia/PROPOSAL_vdm_qualia_program.md`
  *VDM–Qualia Program: Coupled‑Field Explanations of Psychedelic Phenomenology (Sober Proxies)*
  - **Gate(s)**:
  - Gate:** ≥2 significant spectral peaks (z>3 over baseline) at eigenmodes predicted by simulated $K_{vv}$; color/opponent alternation rate matches band spacing.
  - Gate:** Condition A: $\Delta S>0$, priming drop during session, **no** 24h bias shift. Condition B: same acute effects **plus** significant 24h bias shift (p<0.01).
  - Gate:** Inter‑trial phase coherence (ITPC) at drive frequency increases by ≥0.1; depth‑order error rate increases monotonically with $\chi$.
  - Gate:** Reported duration bias grows with $\rho_\tau$; loop reports spike at $\rho_\tau\in[0.8,1.2]$.

## Quantum Gravity (2 proposals)

- **PROPOSAL_Dark_Photon_Bridge.md**
  Path: `Quantum_Gravity/PROPOSAL_Dark_Photon_Bridge.md`
  *Quantum Gravity Bridge - Proposal (v1)*
  - **Date**: 2025-10-06
  - **Diagnostics**: - Tooling: - Cosmology: CLASS or CAMB CLI bindings; results marshalled into JSON/CSV with provenance. - Portals: Python analyses for noise budgets and Fisher quick estimates. - Diagnostics & acceptance gates: - FRW: `RMS_FRW ≤ tol_rms` with default `1e-6`; figure + CSV series; CONTRADICTION_RE...
  - **Personnel**: Justin K. Lietz - implement pipelines, set gates, produce artifacts, and write up; review acceptance results and adjust thresholds.
  - **References**: - CLASS: Blas, Lesgourgues, Tram (2011). CAMB: Lewis, Challinor, Lasenby (2000).
- Dark photons overview: Jaeckel & Ringwald (2010); Alexander et al. (2016) Snowmass; NA64/BaBar/LHCb constraints.
- Cosmology datasets: Planck 2018 results; DES Y3.

- **PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md**
  Path: `Quantum_Gravity/PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md`
  *VDM ↔ Quantum-Gravity Bridge: Causal Geometry and Holonomy Tests*
  - **Summary**: We propose decisive, falsifiable tests connecting the Void Dynamics Model (VDM) to quantum-gravity style causal structure. From the VDM axioms (A0–A7) and master evolution $$ \partial_t q ;=; J(q),\frac{\delta \mathcal I}{\delta q};+;M(q),\frac{\delta \Sigma}{\delta q}, $$ we extract (i) an operational **causal partial order** from retarded responses of the conservative (symplectic) $J$-flow, and (ii) discrete **holonomy/flux** observables from phase transport along lattice loops. We then apply ...
  - **Research Question(s)**:
  - VDM is axiom-first: local, causal, metriplectic evolution with symmetry/Noether and H-theorem gates already demonstrated in separate RD (dissipative) and KG (hyperbolic) chapters. The present question is whether VDM’s **emergent geometry** (from excitations on the lattice) admits the same structural diagnostics used by causal-set and loop-style programs:

* **Causal-set viewpoint**: a discrete spacetime is a locally finite partial order $(C,\prec)$ with acyclicity and order-interval statistics c
  - **Experimental Setup**: **Domains & runners (new):** * `Derivation/code/physics/quantum_gravity/run_vdm_causal_order.py` * `Derivation/code/physics/quantum_gravity/run_vdm_myrheim_dimension.py` * `Derivation/code/physics/quantum_gravity/run_vdm_bd_action_proxy.py` * `Derivation/code/physics/quantum_gravity/run_vdm_holonomy_loops.py` **State & equations:** * Fields $q$ as in VDM (KG-branch and RD-branch available); use...
  - **Diagnostics**: Date: YYYY-MM-DD
  - **Gate(s)**:
  - gates**. Passing these gates would establish that VDM realizes a micro-causal, hyperbolic geometry consistent with a causal-set-like substrate while supporting gauge-like loop transport—an essential bridge to research-grade quantum-gravity programs without importing them as axioms.
  - Gate**: $|\hat d-d_{\text{phys}}|/d_{\text{phys}}\le 0.05$ with CI ≤ 0.03.
  - Gate**: normalized residual mean $\le 0.05$, R² ≥ 0.98 vs baseline curve.
  - Gate**: one term dominates with R² ≥ 0.98; sign(α,β) physically consistent (non-negative).
  - gates pass.
  - gates pass; exactly one of G/H fails with a quantitative commutator/finite-size explanation (slope or residual study attached).
  - **Personnel**: * **Justin K. Lietz** (independent) — PI

## Tachyon Condensation (1 proposal)

- **PROPOSAL_Tachyonic_Tube_Condensation.md**
  Path: `Tachyon_Condensation/PROPOSAL_Tachyonic_Tube_Condensation.md`
  *Tachyonic Tube Condensation and Spectrum (Proposal)*
  - **Date**: 2025-10-09
  - **Summary**: We propose to compute and validate the discrete tachyonic spectrum and condensation profile of a finite-radius cylindrical tube in the FUM scalar EFT with piecewise mass term $m^2(r)$ featuring an unstable interior ($m_{\text{in}}^2=-\mu^2$) and stabilized exterior ($m_{\text{out}}^2=2\mu^2$). We will (1) solve the secular equation for modified Bessel radial modes across a sweep of radii $R$, (2) project the quartic self-interaction $\lambda \phi^4$ onto individual modes (diagonal baseline) to o...
  - **Research Question(s)**:
  - Finite-radius tachyonic domains arise in early-universe symmetry breaking and metastable phase defects. The tube geometry gives a controlled testbed for radial confinement and boundary stabilization relevant to cosmic strings and condensed matter analogues. Existing derivation notes (finite_tube_mode_analysis.md) outline the secular equation:
$$\left(\frac{\kappa_{\text{in}}}{\kappa_{\text{out}}}\right) \frac{I'_{\ell}(\kappa_{\text{in}} R)}{I_{\ell}(\kappa_{\text{in}} R)} + \frac{K'_{\ell}(\kap
  - **Experimental Setup**: Parameters: $\mu$, $\lambda$, $c$, $\ell_{\max}$. Diagnostics: (a) root-finding convergence counts, (b) per-mode $\kappa_\ell$, $N4_\ell$, $v_\ell$, $M_\ell^2$, (c) energy scan $E(R)$ and minima statistics. Artifacts: spectrum CSV per tag, condensation summary JSON, energy scan figure + CSV. Scripts: `cylinder_modes.py`, new runner `run_tachyon_tube.py`. No new external libraries beyond SciPy.
  - **Diagnostics**: Parameters: $\mu$, $\lambda$, $c$, $\ell_{\max}$. Diagnostics: (a) root-finding convergence counts, (b) per-mode $\kappa_\ell$, $N4_\ell$, $v_\ell$, $M_\ell^2$, (c) energy scan $E(R)$ and minima statistics. Artifacts: spectrum CSV per tag, condensation summary JSON, energy scan figure + CSV. Scripts...
  - **Personnel**: Justin K. Lietz - Neuroca, Inc.

## Thermodynamic Routing (7 proposals)

- **PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md**
  Path: `Thermodynamic_Routing/PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md`
  *PROPOSAL_Thermodynamic_Routing_NoSwitch_v2.md*
  - **Summary**: We pre-register a **passive routing** experiment in a metriplectic reaction–diffusion (RD) medium that certifies **thermodynamic, no-switch control**. The field ( \phi(\mathbf{x},t) ) evolves by a discrete-gradient (DG) **metric** step that monotonically decreases a discrete Lyapunov functional ( L_h[\phi] ); **no rule-based controllers or switches** are used. A 2-channel geometry creates a controlled **free-energy bias** favoring outlet ( \mathcal O_{\mathrm A} ) over ( \mathcal O_{\mathrm B} )...
  - **Research Question(s)**:
  - We consider an RD evolution on a 2-D domain,
$$
\partial_t \phi ;=; D \nabla^2 \phi + f(\phi),
$$
with a discrete **energy** (Lyapunov) functional
$$
L_h[\phi] ;=; \sum_{i}\Big(\tfrac{D}{2},|\nabla_h \phi_i|^2 + \hat V(\phi_i)\Big),\Delta x^d,
\qquad \hat V'(\phi) \equiv -f(\phi).
$$
A DG step ensures ( \Delta L_h \le 0 ) (H-theorem) under periodic/no-flux boundaries. We embed a **thermodynamic funnel** (geometry + potential bias) so that descending ( L_h ) **passively** steers flux to ( \mathca
  - **Gate(s)**:
  - gated).
  - gated).
  - gates produce a `CONTRADICTION_REPORT` with ablations. No post-hoc tuning beyond the pre-registered grids.
  - **Variables**:
    - *Independent*:
      - **Geometry:** 2-channel mask with outlet widths (w_{\mathrm A}\ge w_{\mathrm B}), channel length (L_c), obstacles; no-flux walls; outlet segments at right boundary.
      - **RD parameters:** ( D, r, u ) for ( f(\phi)=r\phi-u\phi^2 ) (or alternative (f) with ( \hat V'=-f )).
      - **Grid/discretization:** ( (N_x,N_y)\in{(256,128),(512,256)} ), ( \Delta x ); stencil ( \in{\text{FD-3pt},\text{spectral}} ) (param-gated).
      - **Stepper:** primary **DG M-only**; optional **JMJ** (symplectic half-steps around DG).
      - **Time:** ( \Delta t ), horizon (T).
      - *(... and 2 more)*
    - *Dependent*:
      - **Lyapunov series:** ( L_h(t) ), per-step ( \Delta L_h ).
      - **Outlet fluxes:** ( F_{\mathrm A}, F_{\mathrm B} ) (integrated normal flux through outlet edges).
      - **Efficiencies:** ( \eta_{\text{route}}\equiv \frac{F_{\mathrm A}}{F_{\mathrm A}+F_{\mathrm B}} ), ( \eta_{\text{shed}}\equiv 1-\eta_{\text{route}} ) (shed to side walls or ( \mathcal O_{\mathrm B} )).
      - **Modal thermodynamics:** ( {\lambda_k,\langle |c_k|^2\rangle} ) and RJ fit ( (T,\mu,R^2) ) in post-collapse window.
      - **Defect (optional JMJ):** two-grid slope and JMJ vs MJM defect scaling.
    - *Control*:
      - **Symmetric geometry:** ( w_{\mathrm A}=w_{\mathrm B} \Rightarrow B\approx 0 ).
      - **Local baseline:** explicit **local descent** on ( -\nabla L_h ) (no DG correction), same stencil and ( \Delta t ), no switches.
      - **Injection robustness:** (i) injection-site sweep (distance to funnel apex), (ii) two-source superposition test (split ratio invariance).
  - **Personnel**: Justin K. Lietz - VDM Project

### Passive Thermodynamic Routing

- **PROPOSAL_Flux_Through_Memory_Channels_v1.md**
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Flux_Through_Memory_Channels_v1.md`
  *Flux Through Memory Channels (Frozen Landscape) — Passive Thermodynamic Routing v2 (Pre‑Registration)*
  - **Date**: 2025-10-13
  - **Commit**: `9c27e65`
  - **Summary**: We will test whether a fast transport field (“river”) selectively follows a fixed channel landscape derived from a separate “memory” field (or any exogenous map). Unlike Memory Steering, the channel map is frozen (read-only) during the run. We pre‑register KPIs that quantify adherence and selectivity to the channels—channel‑adherence efficiency $\eta_{\rm ch}$, bias change relative to a geometry baseline $\Delta B_{\rm ch}$, and anisotropy $\mathcal A$ (parallel vs. transverse flux)—along with i...
  - **Research Question(s)**:
  - Passive thermodynamic routing (metric descent) in structured domains can bias outflux without active control. Here we probe a stronger form of passive selectivity: adherence to pre‑declared channels (e.g., high mobility $\mu(x,y)$ or low potential $U(x,y)$ corridors) representing the “memory” landscape but not evolving during the experiment. This isolates the claim “the river follows the channels” from Memory Steering’s online write/read feedback. A metriplectic RD model for the fast field $\phi
  - **Experimental Setup**: - Domain & BCs: 2‑outlet geometry; reflecting sidewalls; open right boundary with two outlet segments A/B. Port closure ablation yields zero outflux by construction. - Channel map: either mobility $\mu(x,y)$ or potential $U(x,y)$ supplied as an input raster; treated as immutable during runs (content hash recorded at start/end; must match). - Dynamics: Eq. (1) with bounded $(D, r, u)$ for $R(\phi)$...
  - **Personnel**: - Justin K. Lietz — Prometheus VDM Project

- **PROPOSAL_Passive_Thermodynamic_Routing_v2.md**
  Path: `Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Passive_Thermodynamic_Routing_v2.md`
  *PROPOSAL: Passive Thermodynamic Routing v2 (Pre-Registration)*
  - **Date**: 2025-10-13
  - **Commit**: `2bb143a`
  - **Diagnostics**: Assumptions and exclusions: - Discrete operator stability respected (Δt ≤ 0.8/ω_max from discrete spectral operator) - Single-thread numerics, deterministic FFT/plan where applicable - Seeds: fixed band-limited set; seed-band aggregation via median - Geometry masks: preregistered; any changes trigg...
  - **Gate(s)**:
  - gated diagnostics for the J⊕M coupling limb. No parameter tuning post hoc; windowing and masks are predeclared.
  - gated).
  - Gate: zero violations of $\Delta L_h \le 0$
  - Gate: arrays identical at checkpoints (bitwise) or $\lVert\cdot\rVert_\infty \le 10^{-12}$
  - Gate: $S_k \propto \tfrac{T}{\lambda_k - \mu}$ with array-level $R^2 \ge 0.99$
  - Gate: preregister scalar bias $B$ and fraction $\varrho$ with 95% CI excluding $0$ and margin $\delta$; report $(B,\varrho, \text{CI}, \delta)$
  - Gate: final $L_h$ strictly below matched baseline; $\ge 5\sigma$; CI excludes $0$
  - Gates: symmetric-geometry control (~0 bias); injection-site monotone trend; two-source split (≤ 5% change)
  - *(... and 2 more)*

### Prereg Biased Main

- **PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md**
  Path: `Thermodynamic_Routing/Prereg_Biased_Main/PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md`
  *PROPOSAL: Thermodynamic Routing v2 — Prereg Biased Main*
  - **Date**: 2025-10-13
  - **Commit**: `9c27e65`
  - **Summary**: We will execute the preregistered biased-geometry run of Thermodynamic Routing v2 with full gates enforced. The metric (DG) step must satisfy the H-theorem (ΔL_h ≤ 0), no-switch identity must hold bitwise or within ∞-norm ≤ 1e−12, the RJ spectral fit must achieve R² ≥ 0.99 on a predeclared band and time window with residual whiteness diagnostics (Durbin–Watson, Ljung–Box(5), ρ₁), routing bias must exhibit nonzero B and ρ with 95% CI excluding 0 meeting a preregistered margin δ, the energy-floor ...
  - **Research Question(s)**:
  - A metriplectic RD system with passive descent provides a testbed for thermodynamic routing without explicit control. The discrete Lyapunov functional

$$
L_h[\phi] = \sum_i \Big( \tfrac{D}{2} |\nabla_h \phi_i|^2 + \hat V(\phi_i) \Big) \, \Delta x^2, \quad \hat V'(\phi) \equiv -f(\phi),\ f(\phi)= r\phi - u\phi^2 
$$

is monotonically non-increasing under the DG metric step. In a geometry with biased outlet widths $(w_A > w_B)$ and outflux-only boundary accounting, we hypothesize a positive routin
  - **Experimental Setup**: - Grid: 96×48, Lx=6.0, Ly=3.0; stencil=FD-3pt; periodic interior, outflux on right boundary. - Geometry: outlet widths (w_A=0.55, w_B=0.35) on right boundary; injection packet near x0=0.25, y0 ∈ {0.9,1.5,2.1} (robustness sweep). - RD params: D=1.0, r=0.2, u=0.25, λ=0.0. - Time: T=1.5, dt=0.01 (adjustable down if overflow risk), checkpoints K=25. - RJ: k-band [3,24]; window t ∈ [0.8, 1.5]. - Seeds:...
  - **Personnel**: - Justin K. Lietz — design, execution, analysis, and documentation.
  - **References**: - Metriplectic integrators and discrete gradient methods (e.g., Gonzalez 1996; Quispel & Turner 1996).
- Rayleigh–Jeans spectral statistics in discretized systems; standard econometrics tests for residual whiteness (DW, Ljung–Box).

### Wave Flux Meter

- **PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md**
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md`
  *Wave Flux Meter PhaseC OpenPorts v1*
  - **Tier**: T2 (Foundational/Instrument)
  - **Diagnostics**: * **Dimensionless KPIs.** Report and gate on the dimensionless groups in your symbols sheet (e.g., (M_v,\ \Sigma,\ \Lambda,\ \Pi_{Dr},\ c^*)). Scale‑collapse and regime classification live here. * **Writeup discipline.** Draft proposals and results with your white‑paper template and results standa...

- **PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md**
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`
  *Proposal: Wave Flux Meter — Phase B (Open-Ports with Absorber) v1*
  - **Date**: 2025-10-13

- **PROPOSAL_Wave_Flux_Meter_v1.md**
  Path: `Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md`
  *Proposal: Wave Poynting-Meter Instrument v1 (Thermodynamic Routing — Photonic Track)*
  - **Commit**: `9c27e65`

## Topology (2 proposals)

- **PROPOSAL_Loop_Quench_Test_Robustness_v2.md**
  Path: `Topology/PROPOSAL_Loop_Quench_Test_Robustness_v2.md`
  *Loop Quench Test Robustness v2*

- **PROPOSAL_Loop_Quench_Test_v1.md**
  Path: `Topology/PROPOSAL_Loop_Quench_Test_v1.md`
  *PROPOSAL_Loop_Quench_Test_v1.md*
  - **Summary**: We test whether dissipative dynamics suppress long-lived cycle pathologies. In a 2D RD toy system we threshold an excursion set and count simple cycles (graph cycle basis) while logging the discrete Lyapunov (L_h). KPI: negative correlation between (\Delta L_h<0) and cycle count; loop lifetime distribution with a fast decay tail, consistent with “loops as transient but governed.”
  - **Research Question(s)**:
  - Your model treats persistent loops as pathological “sinks” and healthy concepts as clustered territories. The H-theorem suggests dissipation quenches pathologies. This experiment upgrades that claim into a measurable coupling between energy descent and loop suppression.
  - **Experimental Setup**: * **Domain:** `Derivation/code/physics/topology/` * **Dynamics:** 2D RD with stable explicit scheme; no-flux boundaries. * **Observables:** binary mask of (\phi>\tau); simple cycle count via cycle basis; (L_h=\sum(D/2|\nabla\phi|^2+\hat V(\phi))). * **Diagnostics:** Kendall (\tau) between loop count and (-\Delta L_h); loop lifetime histogram; budget residual sanity.
  - **Diagnostics**: * **Domain:** `Derivation/code/physics/topology/` * **Dynamics:** 2D RD with stable explicit scheme; no-flux boundaries. * **Observables:** binary mask of (\phi>\tau); simple cycle count via cycle basis; (L_h=\sum(D/2|\nabla\phi|^2+\hat V(\phi))). * **Diagnostics:** Kendall (\tau) between loop count...
  - **Gate(s)**:
  - Gates:** Kendall (\tau \le -0.7) with (p<10^{-6}); lifetime tail fit slope (>2) (fast decay).
  - **Personnel**: Justin K. Lietz.
  - **References**: SIE stability plots; tda_analysis_results.txt; Rules-for-Physics-Experimentation-and-Data-Analysis.md.

---

## Notes

- All proposals must follow the template at `Templates/PROPOSAL_PAPER_TEMPLATE.md`
- Proposals are graded T0-T9 according to maturity ladder (see `TIER_STANDARDS.md`)
- Each proposal requires approval before experiments can run
- Proposals must include: explicit gates, provenance, equations, and artifact paths
- Higher-tier proposals (T4+) must reference supporting work from lower tiers
- Experimental setup, diagnostics, variables, methods, and schema documentation must be comprehensive and rigorous
- All gates must have explicit pass/fail thresholds with units and normalization specified

### Cross-Reference Guidelines

For each proposal, verify:

* **Maturity tier**: If higher-tier proposals (T4+) reference supporting work, document those dependencies
* **Canonical references**: Ensure proposals reference canonical files where applicable:
  * Equations → `z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-...`
  * Symbols → `z.CANONICAL_Symbols/00_SYMBOLS.md#sym-...`
  * Constants → `z.CANONICAL_Constants/00_CONSTANTS.md#const-...`
  * Units → `z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md#...`
  * Algorithms → `z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-...`
  * Schemas → `z.CANONICAL_Schemas/00_SCHEMAS.md#schema-...`
* **Downstream results**: If a corresponding RESULTS_*.md file exists, note it for tracking proposal → execution → results lineage
* **Code locations**: Document planned experiment runner paths (e.g., `code/physics/{domain}/run_{experiment}.py`)
* **Authorization status**: Note if proposal has been approved for execution (reference authorization README)

<!-- BEGIN AUTOSECTION: PROPOSALS-INDEX -->
<!-- Tool-maintained list of proposals by domain -->
<!-- Agency_Field: PROPOSAL_ADC_Response_Slope_v1.md, PROPOSAL_Agency_Curvature_Scaling_v1.md, PROPOSAL_Agency_Stability_Band_v1.md, PROPOSAL_Agency_Witness_v1.md, PROPOSAL_Multipartite_Coordinaton_Depth_v1.md -->
<!-- Causality: PROPOSAL_Causal_DAG_Audits_for_Void_Dynamics_Model.md, PROPOSAL_Metriplectic_Causal_Dominance_v1.md -->
<!-- Collapse: PROPOSAL_A6_Collapse_v1.md -->
<!-- Conservation_Law: PROPOSAL_RD_Discrete_Conservation_vs_Balance.md -->
<!-- Cosmology: PROPOSAL_FRW_Balance_v1.md, PROPOSAL_FRW_Continuity_Predictive_v2.md -->
<!-- Dark_Photons: PROPOSAL_Decoherence_Portals.md -->
<!-- Information: PROPOSAL_SIE_Invariant_and_Novelty_v1.md -->
<!-- Intelligence_Model: PROPOSAL_Physics_Native_Intelligence_v1.md -->
<!-- Metriplectic: PROPOSAL_KG_plus_RD_Metriplectic.md, PROPOSAL_Metriplectic_Composition_KGplusRD_v2.md, PROPOSAL_Metriplectic_JMJ_RD_v1.md, PROPOSAL_Metriplectic_Lindblad_T4.md, PROPOSAL_Metriplectic_SymplecticPlusDG.md -->
<!-- Qualia: PROPOSAL_vdm_qualia_program.md -->
<!-- Quantum_Gravity: PROPOSAL_Dark_Photon_Bridge.md, PROPOSAL_Quantum-Gravity-Bridge_Causal-Geometry-and-Holonomy.md -->
<!-- Tachyon_Condensation: PROPOSAL_Tachyonic_Tube_Condensation.md -->
<!-- Thermodynamic_Routing: PROPOSAL_Flux_Through_Memory_Channels_v1.md, PROPOSAL_Passive_Thermodynamic_Routing_v2.md, PROPOSAL_Thermodynamic_Routing_NoSwitch_v1.md, PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md, PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md, PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md, PROPOSAL_Wave_Flux_Meter_v1.md -->
<!-- Topology: PROPOSAL_Loop_Quench_Test_Robustness_v2.md, PROPOSAL_Loop_Quench_Test_v1.md -->
<!-- END AUTOSECTION: PROPOSALS-INDEX -->

---

## Validation Checklist

Before finalizing updates to this document:

* [ ] Every PROPOSAL_*.md file in the repository is listed exactly once
* [ ] Each entry extracts: tier, research questions, experimental setup, diagnostics, gates, variables, methods, schema, equipment, risks, personnel, references, summary
* [ ] Experimental setup includes parameter ranges, sampling strategy, trial configuration
* [ ] Diagnostics describe measurement instruments and metric computation
* [ ] All gates are explicitly documented with thresholds and pass criteria
* [ ] Variables section documents independent, dependent, and control variables with rationales
* [ ] Methods/Protocol section details numerical methods, integrators, and algorithmic steps
* [ ] Schema documentation specifies planned artifact structure (figures, CSVs, JSONs)
* [ ] Equipment/Software lists runner scripts and dependencies
* [ ] Risk assessment documents identified risks and mitigations
* [ ] Domain organization matches the repository folder structure
* [ ] Total proposals count in header is accurate
* [ ] All MathJax renders correctly on GitHub preview
* [ ] No equations, code blocks, or detailed math duplicated from source files—use links/brief summaries only
* [ ] Maturity tier documented (T0-T9) when specified
* [ ] Authorization status noted where applicable
* [ ] Links to corresponding RESULTS_*.md files when they exist

---

**Change Log (documented in `z.CANONICAL_Chronicles/00_CHRONICLES.md`):**

```markdown
## Change Log
- {today} • Created/Updated canonical PROPOSALS index • comprehensive extraction of all proposals
```

---

*This document is auto-generated from proposal files. For updates, modify the source proposal documents and regenerate this index.*
