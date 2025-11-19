<!-- DOC-GUARD: REFERENCE -->
# VDM Overview (Compiled from Repository Evidence)

**Last updated**: 2025-11-05  
**Last commit**: HEAD  
**Scope:** High-level overview synced to canon files and proven instruments; all claims trace to in-repo sources by anchor.  
**Rules:** Overview includes synced canonical equations and formalisms for orientation; snippets are copied verbatim from canon (SYMBOLS/EQUATIONS/CONSTANTS/UNITS/ALGORITHMS/BC_IC/VALIDATION/DATA_PRODUCTS/SCHEMAS) with provenance and must be kept in sync with sources.

---

## Canonical Model Banner

- Canonical branch: Reaction–Diffusion (RD) • Evidence:
  - Equations: [E-015](Derivation/EQUATIONS.md#vdm-e-015), [E-016](Derivation/EQUATIONS.md#vdm-e-016), [E-017](Derivation/EQUATIONS.md#vdm-e-017), [E-018](Derivation/EQUATIONS.md#vdm-e-018)
  - Discrete → continuum and potential context: [E-011](Derivation/EQUATIONS.md#vdm-e-011), [E-012](Derivation/EQUATIONS.md#vdm-e-012)
- Scoped branches:
  - EFT/KG (J-only): [E-014](Derivation/EQUATIONS.md#vdm-e-014) (continuum KG representative)
  - Metriplectic J⊕M composition: [E-042](Derivation/EQUATIONS.md#vdm-e-042) (flow), composition diagnostics [E-091](Derivation/EQUATIONS.md#vdm-e-091), Strang JMJ map [E-125](Derivation/EQUATIONS.md#vdm-e-125)
- Validation gates overview: see [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
- Proven instruments (examples; see RESULTS):
  - KG Noether invariants, dispersion, light-cone; Metriplectic composition checks
  - RD front speed and RD linear dispersion; see domain RESULTS references below
- RB-Gate (fluids onset) as meter: [E-121](Derivation/EQUATIONS.md#vdm-e-121) – [E-124](Derivation/EQUATIONS.md#vdm-e-124)
- Causality meters:
  - Telegraph speed (spec-level): [E-105](Derivation/EQUATIONS.md#vdm-e-105)
  - KG J-only meters: see RESULTS (links below)

---
 
## Core Equations and Formalisms (synced excerpts)
All snippets below are verbatim copies from canon anchors and carry no independent authority. Edit sources in [EQUATIONS.md](Derivation/EQUATIONS.md) and domain docs; this overview mirrors them for quick reading.

- EFT/KG (continuum representative) — [VDM-E-014](Derivation/EQUATIONS.md#vdm-e-014)
  
  $$
  \partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0, \qquad c^{2}=2J a^{2}
  $$

- Reaction–Diffusion canonical PDE — [VDM-E-015](Derivation/EQUATIONS.md#vdm-e-015)
  
  $$
  \partial_t \phi = D \nabla^{2}\phi + f(\phi), \quad f(\phi)= r\phi - u\phi^{2} - \lambda \phi^{3}, \quad D=2J a^{2}
  $$

- RD Lyapunov functional and dissipation — [VDM-E-016](Derivation/EQUATIONS.md#vdm-e-016)
  
  $$
  \mathcal{L}[\phi]=\int_{\Omega}\left( \tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)\,dx,\qquad \hat V'(\phi)=-f(\phi)
  $$
  
  $$
  \frac{d}{dt}\mathcal{L}[\phi] = -\int_{\Omega} (\partial_t\phi)^2\,dx \le0
  $$

- Linear RD dispersion and KPP front speed — [VDM-E-017](Derivation/EQUATIONS.md#vdm-e-017), [VDM-E-018](Derivation/EQUATIONS.md#vdm-e-018)
  
  $$
  \sigma(k)=r-Dk^{2}
  $$
  
  $$
  c_{front}=2\sqrt{D r}
  $$

- Discrete → continuum mapping — [VDM-E-029](Derivation/EQUATIONS.md#vdm-e-029)
  
  $$
  \begin{aligned}
  D &= J a^{2} && \text{(site Laplacian)}\\
  D &= \tfrac{J}{z} a^{2} && \text{(neighbor-average form)}\\
  r &= \alpha - \beta,\quad u = \alpha
  \end{aligned}
  $$

- EFT kinetic normalization (per-site/per-edge) — [VDM-E-030](Derivation/EQUATIONS.md#vdm-e-030)
  
  $$
  c^{2} = 2 J a^{2} \quad \text{(per-site)}, \qquad c^{2} = \kappa a^{2},\; \kappa = 2J \quad \text{(per-edge)}
  $$

- RB-Gate (fluids onset meter) — [VDM-E-121](Derivation/EQUATIONS.md#vdm-e-121)–[VDM-E-124](Derivation/EQUATIONS.md#vdm-e-124)
  
  $$
  \mathrm{Ra} \;=\; \frac{g\,\alpha\,\Delta T\,H^3}{\nu\,\kappa}
  $$
  
  $$\begin{aligned}
  \partial_t \mathbf{u} + (\mathbf{u}\cdot\nabla)\mathbf{u} &= -\nabla p + \mathrm{Pr}\,\nabla^2 \mathbf{u} + \mathrm{Pr}\,\mathrm{Ra}\,\theta\,\hat{\mathbf{z}},\\
  \partial_t \theta + (\mathbf{u}\cdot\nabla)\theta - w &= \nabla^2 \theta,\\
  \nabla\cdot\mathbf{u} &= 0.
  \end{aligned}$$
  
  $$
  \mathrm{Nu} \;=\; \frac{\langle q_z\rangle}{k\,\Delta T/H},\qquad q_z=\rho c_p\,w\,T - k\,\partial_z T
  $$
  
  $$
  \mathrm{Nu} \;=\; 1 + \langle w\theta\rangle - \langle \partial_z \theta\rangle
  $$
  
  $$
  H \mapsto 2H \;\Rightarrow\; \mathrm{Ra} \mapsto 8\,\mathrm{Ra},\quad \lambda_c \mapsto \approx 2\,\lambda_c
  $$

- Metriplectic Strang composition (JMJ) — [VDM-E-125](Derivation/EQUATIONS.md#vdm-e-125)
  
  $$
  \Phi^{\mathrm{JMJ}}_{\Delta t} \;=\; \Phi^{\mathrm{J}}_{\Delta t/2} \;\circ\; \Phi^{\mathrm{M}}_{\Delta t} \;\circ\; \Phi^{\mathrm{J}}_{\Delta t/2}, \qquad \text{global error } \mathcal{O}(\Delta t^2)
  $$

- Causality meter (telegraph characteristic speed) — [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105)
  
  $$
  c \;=\; \sqrt{\frac{D}{\tau}}
  $$

## Branches

### Branch: Reaction–Diffusion (RD)  <a id="branch-rd"></a>

**Scope:** “Canonical RD banner + mapping (D = J a² or (J/z) a²; r = α − β; u = α)” ([Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:75-79))  
**Primary equations:** [E-015](Derivation/EQUATIONS.md#vdm-e-015), [E-016](Derivation/EQUATIONS.md#vdm-e-016), [E-017](Derivation/EQUATIONS.md#vdm-e-017), [E-018](Derivation/EQUATIONS.md#vdm-e-018)  
**Proven instruments (links):** RD front speed validation ([Derivation/rd_front_speed_validation.md](Derivation/rd_front_speed_validation.md:1)), RD dispersion experiment (see CHRONICLES entries at [Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:151-155))  
**Status:** Canonical; policy clarifications and mappings noted in [Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:54-56,68-71)

### Branch: EFT/Klein–Gordon (KG, J-only)  <a id="branch-kg"></a>

**Scope:** “EFT/KG is an active branch with explicit KPIs and acceptance gates… Kinetic normalization c² = 2 J a² (per‑site) or c² = κ a² (κ=2J)” ([Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:49-56))  
**Primary equations:** [E-014](Derivation/EQUATIONS.md#vdm-e-014) (continuum KG representative), discrete action/normalizations [E-011](Derivation/EQUATIONS.md#vdm-e-011), [E-012](Derivation/EQUATIONS.md#vdm-e-012)  
**Proven instruments (links):** KG Noether invariants ([Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md](Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md:1)), KG dispersion/energy-oscillation (see CHRONICLES summaries at [Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:151-155))  
**Status:** KPI-gated, instrument-proven; see [Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:49-56)

### Branch: Metriplectic J ⊕ M Composition  <a id="branch-metriplectic"></a>

**Scope:** “T2 (Instrument Certification) — PASS… composition diagnostics documented” ([Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:219-236))  
**Primary equations:** Metriplectic flow [E-042](Derivation/EQUATIONS.md#vdm-e-042); JMJ map/order [E-125](Derivation/EQUATIONS.md#vdm-e-125)  
**Proven instruments (links):** RESULTS (JMJ RD composition): [Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md](Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md:1)  
**Status:** T2 instrument suite validated; see [Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:219-236)

---

## Domains

### Metriplectic  <a id="dom-metriplectic"></a>

- Summary: “T2 certification of metriplectic operator structure… Composition diagnostics documented” ([Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:219-236))  
- Key proposals: see domain folder `Derivation/Metriplectic/` and [PROPOSALS.md](Derivation/z.CANONICAL_Proposals/00_PROPOSALS.md) (if present)  
- Key results: [RESULTS_Metriplectic_JMJ_RD_v1.md](Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md:1), KG Noether/dispersion/energy-oscillation (see `Derivation/Metriplectic/`)  
- Canon references: [SYMBOLS](Derivation/SYMBOLS.md), [EQUATIONS](Derivation/EQUATIONS.md), [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md), [ALGORITHMS](Derivation/ALGORITHMS.md)

### Conservation Law (RD Discrete Conservation vs Balance)  <a id="dom-conservation"></a>

- Summary (proposal): “Formal prereg structure: Obj-A (exact), Obj-B (asymptotic), Obj-C (H-theorem)” ([audits/2025-10-14_VDM-Progress-Findings.md](audits/2025-10-14_VDM-Progress-Findings.md:66-92))  
- Key proposals: [PROPOSAL_RD_Discrete_Conservation_vs_Balance.md](Derivation/Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md:1)  
- Key results: documented in CHRONICLES (two-grid, H-theorem) ([Derivation/CHRONICLES.md](Derivation/CHRONICLES.md:153-155))  
- Canon references: [EQUATIONS](Derivation/EQUATIONS.md#vdm-e-127), [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)

### Thermodynamic Routing  <a id="dom-thermo"></a>

- Summary: Wave Flux Meter instruments/results in Thermodynamic Routing domain ([Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md:1))  
- Key proposals/results: see `Derivation/Thermodynamic_Routing/*`  
- Canon references: [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md), [EQUATIONS](Derivation/EQUATIONS.md)

### Fluid Dynamics (RB-Gate, Benchmarks)  <a id="dom-fluids"></a>

- Summary: RB-Gate equations (Ra, RBC equations, Nu, depth scaling) [E-121–E-124](Derivation/EQUATIONS.md#vdm-e-121) and Taylor–Green energy decay benchmark ([Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py](Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1))  
- Key documents: [BENCHMARKS_FLUIDS.md](Derivation/Fluid_Dynamics/BENCHMARKS_FLUIDS.md:1)  
- Canon references: [EQUATIONS](Derivation/EQUATIONS.md#vdm-e-121), [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)

### Axioms / A8 Program  <a id="dom-axioms-a8"></a>

- Summary: A8 functional forms and interface concentration instruments ([E-115–E-120](Derivation/EQUATIONS.md#vdm-e-115))  
- Key proposals/results: `Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md` (see EQUATIONS notes/provenance)  
- Canon references: [EQUATIONS](Derivation/EQUATIONS.md#vdm-e-115), [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)

> Note: Additional domains (Agency_Field, Causality, Cosmology, Tachyon_Condensation, etc.) are present in the repository. Link domain summaries to their local READMEs/RESULTS/PROPOSALS and to canon registries as they are compiled.

---

## Instruments and KPIs (links only)

- Meter: KG Noether invariants • RESULTS: [Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md](Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md:1) • KPIs: [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)  
- Meter: RD front speed • RESULTS: [Derivation/rd_front_speed_validation.md](Derivation/rd_front_speed_validation.md:1) • KPIs: [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)  
- Meter: RD linear dispersion • RESULTS: see CHRONICLES entries • KPIs: [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)  
- Meter: Metriplectic JMJ structure • RESULTS: [Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md](Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md:1) • KPIs: [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)  
- Meter: Taylor–Green decay (viscosity recovery) • Code/analysis: [Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py](Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1) • KPIs: [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)  
- Meter: RB-Gate near onset • Equations: [E-121–E-124](Derivation/EQUATIONS.md#vdm-e-121) • KPIs: [VALIDATION_METRICS](Derivation/VALIDATION_METRICS.md)

---

## Artifacts & IO Policy

- IO helper paths: [code/common/io_paths.py](Derivation/code/common/io_paths.py:1)  
- Standards / templates: [Templates/PROPOSAL_PAPER_TEMPLATE.md](Derivation/Templates/PROPOSAL_PAPER_TEMPLATE.md:1), [Templates/RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md:1)  
- Quarantine / approvals: [code/common/authorization/README.md](Derivation/code/common/authorization/README.md:1)

---

## Tier Status Snapshot

- Proposals index: [Derivation/z.CANONICAL_Proposals/00_PROPOSALS.md](Derivation/z.CANONICAL_Proposals/00_PROPOSALS.md) (if present)  
- Results index: [Derivation/RESULTS.md](Derivation/RESULTS.md)  
- Change history and policy clarifications: [Derivation/CHRONICLES.md](Derivation/CHRONICLES.md)

---

<!-- BEGIN AUTOSECTION: OVERVIEW-INDEX -->
<!-- Tool-maintained list of overview anchors (branches/domains/instruments) -->
<!-- END AUTOSECTION: OVERVIEW-INDEX -->

**Change Log (ADD THIS TO CHRONICLES.md):**

```markdown
## Change Log
- 2025-11-05 • overview synced to canon • HEAD
```

---

## Validation checklist
 
- [ ] Every overview statement and equation snippet is backed by an in-repo anchor and/or file path
- [ ] All math blocks render in GitHub preview (MathJax-only syntax)
- [ ] Snippets match their canon sources verbatim (spot-check against [EQUATIONS.md](Derivation/EQUATIONS.md))
- [ ] Branch/domain/instrument ordering follows the rules above
- [ ] DOC-GUARD header present and accurate (date/commit filled)
- [ ] Any missing anchors are marked with `TODO: add anchor (see <path>:<line>)`

---

## Notes

- OVERVIEW includes synced canonical equations and formalisms; snippets are verbatim from canon anchors and carry no independent authority.
- Keep language minimal and sourced; authoritative edits must land in canon first, then be mirrored here.
- If CHRONICLES indicates policy clarifications affecting the overview, link those entries rather than paraphrasing.
