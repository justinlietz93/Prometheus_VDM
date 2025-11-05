# 1. **T2 (Instrument)** — **STIV Macrostate & Gradient‑Flow Meters for A8 Boundary Hierarchies**

> **Created Date:** 2025-11-04
> **Provenance:** `{git rev-parse HEAD}` → `HEAD_SHA_HERE`; salted provenance: `base_sha256=…`, `salt_hex=…`, `salted_sha256=…` (to be inserted by prereg script).
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** (Repository `LICENSE`)
> **Short summary (TL;DR):** Proposed is a **T2 instrument** that instantiates a **STIV‑style macroscopic gradient‑flow** over A8 hierarchy observables—$E_{\rm exc}$, $N(L)$, $\rho$, $\alpha$, $\alpha_{\mathcal I}$—with **entropy‑production guarantees** and **meter gates** (H‑theorem, proxy concordance, degeneracy, grid invariance, and area‑law model selection) preregistered and machine‑checkable.

***Practical Provenance pattern.*** Follow the canonical steps in the template (salted hashes, signed prereg tag, push before runs; section **5.1.1** repeats exact artifacts and required keys).

---

## 2. List of proposers and associated institutions/companies

**Justin K. Lietz** — Neuroca, Inc. (PI, implementer, approver).

---

## 3. Abstract

A **structure‑preserving macroscopic closure** is introduced for A8 benches using **Stochastic Thermodynamics with Internal Variables (STIV)**. The macrostate $z$ collects **boundary‑hierarchy observables** and evolves by a **gradient flow** $\dot z=-K(z)\nabla F(z)$ ensuring **non‑negative entropy production** $\sigma(z)=\langle \nabla F, K \nabla F\rangle\ge0$. This instrument yields **meter‑grade** measurements for A8: boundary‑law exponent $\beta_E$, logarithmic depth $N(L)$, tubular energy fraction $\alpha(\varepsilon)$, information fraction $\alpha_{\mathcal I}(\varepsilon)$, and gap ratio $\rho$, with **pre‑declared pass/fail gates** and **QC invariants**. The device is explicitly **separable from phenomenon claims** (T2 only), but targets A8 P0 gaps (BN‑1.1..1.5) and **EBN‑A8‑Def/UQ** milestones.

---

## 4. Background & Scientific Rationale

### A8 program context and gaps

A8 (Infinity Resolution) posits that **finite excess energy** in tachyonic, pulled‑front systems **necessitates hierarchical scale breaks** with boundary energy/information concentration and $N(L)=\Theta(\log L)$ depth. The **PROPOSAL and status** files define gates (G1–G12) and list **P0 missing meters** (hierarchy detector, log‑depth tracker, tubular‑energy, information proxy, area‑law discriminator). This T2 instrument directly addresses those missing pieces as **bench‑native meters** with prereg QCs.

### STIV as the macroscopic scaffold

STIV proves that **coarse variables** (internal variables) can be advanced by a **thermodynamically consistent gradient flow** with **non‑negative entropy production** and **convergence as the internal‑variable basis is enriched**. That structure maps naturally onto A8’s **M‑limb** and A5 **entropy law**, providing a **first‑principles backbone** for meters and gates rather than ad‑hoc proxies.

### Canonical alignment

* **A5 (Entropy law)** supplies the sign convention and H‑theorem monitors used here.
* **A6 (Scale program)** frames the dimensionless envelopes and slope tests (e.g., $\beta_E=d-1\pm0.1$, grid invariance).
* **A7 (Measurability)** mandates prereg, approvals, KPIs, and machine‑actionable specs used in this T2.

### Repository‑local planning anchors

This T2 proposal operationalizes items flagged in **Insights Index** (A8 meters and gates; EBN‑Info‑Functional; G‑DEP; GPX; G‑GI; GALModelSel) and **Milestones** (EBN‑A8‑Def, EBN‑A8‑UQ).

---

## 5. Intellectual Merit and Procedure

**Importance.** A8’s claims hinge on **trustworthy meters** for boundary energy/information concentration and hierarchical depth. This instrument provides **thermodynamically structured** meters with **explicit QC** and **reproducible artifacts**.

**Broader impacts.** A general gradient‑flow meter for **boundary‑law vs volume‑law** and **information concentration** has implications for **active matter, materials, and cosmology** where interfaces dominate dynamics.

**Approach.** Build a **STIV macrostate** over hierarchy observables and evolve it by **gradient flow** to compute **σ**, **Lyapunov drop ΔF**, and **gate metrics**, while validating meters on analytic shapes and controlled RD/KG fields.

**Rigor.** All thresholds, CIs, and analysis windows are preregistered per template; **degeneracy diagnostics (g₁,g₂)**, **grid invariance**, **model selection**, and **bootstrap CIs** are enforced.

---

### 5.1 Experimental Setup and Diagnostics

#### 5.1.0 Macrostate, dynamics, and observables

**Macrostate (internal variables).**
Let $z=(A,,P,,\mathcal T_\varepsilon,,\kappa_m,,\rho,,N,,\alpha,,\alpha_{\mathcal I})$, where

* $A,P$ = area and perimeter (or $d$‑dimensional volume & $(d-1)$‑measure),
* $\mathcal T_\varepsilon$ = **tubular‑energy** in $N_\varepsilon(\cup_\ell \Gamma_\ell)$,
* $\kappa_m$ = curvature spectrum moments of boundaries,
* $\rho$ = inter‑level diameter ratio (gap),
* $N$ = hierarchy depth,
* $\alpha=\dfrac{E_{\rm exc}[N_\varepsilon(\cup_\ell \Gamma_\ell)]}{E_{\rm exc}[\Omega]}$,
* $\alpha_{\mathcal I} = \dfrac{\int_{N_\varepsilon} I(x),dx}{\int_{\Omega} I(x),dx}$ with two prereg proxies $I_1, I_2$ (below).

**Gradient‑flow closure (STIV).**
Define a **non‑equilibrium free energy** $F(z)$; evolve $z$ by
$$
\dot z ;=; -K(z),\nabla F(z),\qquad K(z)\succeq 0,
$$
so **entropy production** $\sigma(z)=\langle \nabla F, K,\nabla F\rangle\ge 0$ and/or a Lyapunov $F$ decreases (sign chosen once and kept consistent). **Gate G‑H:** $\Delta \Sigma\ge -10^{-12}$ (or $\Delta F\le +10^{-12}$) per step.

**Information proxies (GPX gate).**

* $I_1(x)=\log!\big(1+|\nabla\phi(x)|^2/\sigma^2\big)$ (operational, resolution $\sigma$ prereg).
* $I_2(x)$ = **Fisher‑type** proxy from a normalized, strictly positive density $p_\sigma$ derived from a smoothed field functional (preregister smoothing & positivity). GPX **pass:** $|\alpha_{\mathcal I}(I_1)-\alpha_{\mathcal I}(I_2)|\le 0.1,\alpha_{\mathcal I}(I_2)$. (Maps to **EBN‑Info‑Functional** item in Insights.)

**Meters to implement (BN‑1.1..1.5).**
Hierarchy detector (Γ_\ell); depth tracker $N(L)$; tubular‑energy α(ε); information α_{\mathcal I}(ε); area‑law discriminator β_E with ΔAIC/ΔBIC vs volume‑law; **degeneracy monitors** $(g_1,g_2)\le10^{-10}$ at grid‑refined tolerance; **grid invariance**: slope drift ≤0.05 with CI overlap.

### Required parameters (defaults & units)

| Key           | Meaning                     |                 Default | Unit       |
| ------------- | --------------------------- | ----------------------: | :--------- |
| $\varepsilon$ | tubular radius list         |              [1,2,3]×Δx | grid units |
| $\sigma$      | info‑proxy resolution       |                  1.0×Δx | grid units |
| $L$           | domain linear size          |      {128,256,512,1024} | grid       |
| seeds         | randomization seeds         |                 {0..19} | —          |
| K‑form        | dissipation metric          | diag; PSD check on init | —          |
| tol_H         | H‑theorem tolerance         |              $10^{-12}$ | —          |
| tol_GI        | grid‑invariance slope drift |                    0.05 | —          |

### Diagnostics (counts)

* **Hierarchy detector** (1), **Depth tracker** (1), **Tubular energy** (1), **Info metrics** (2 proxies), **Area‑law discriminator** (1), **Degeneracy monitor** (1), **Grid invariance** (1). Implementations under `Derivation/code/physics/hierarchy/*.py` per milestones.

---

#### 5.1.1 Pre‑Run Config Requirements

Create the following **machine‑readable artifacts** before any write‑artifacts run; this follows the repository’s **authorization** and **prereg** discipline.

* `Derivation/code/physics/hierarchy/APPROVALS.json`
* `Derivation/code/physics/hierarchy/schemas/STIV_A8_Meters.schema.json`
* `Derivation/code/physics/hierarchy/specs/STIV_A8_Meters.v1.json`
* `Derivation/experiments/prereg/STIV_A8_Meters.v1.json`

**APPROVALS.json (template):**

```json
{
  "preflight_name": "stiv_a8_preflight",
  "description": "Approval manifest for STIV-based A8 meters; preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs may execute under Derivation/code/tests. Artifact-writing runs require this PROPOSAL_T2_A8_STIV...",
  "pre_registered": true,
  "proposal": "Derivation/Proposals/PROPOSAL_T2_A8_STIV_Macrostate_and_Meters_v1.md",
  "allowed_tags": ["stiv-a8-meters-v1"],
  "schema_dir": "Derivation/code/physics/hierarchy/schemas",
  "approvals": {
    "stiv-a8-meters-v1": {
      "schema": "Derivation/code/physics/hierarchy/schemas/STIV_A8_Meters.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto",
      "approval_key": "auto"
    }
  }
}
```

(Conforms to the template’s approvals block.)

**PRE‑REGISTRATION.json (minimum keys):**

```json
{
  "proposal_title": "T2 — STIV Macrostate & Gradient-Flow Meters for A8",
  "tier_grade": "T2",
  "commit": "HEAD_SHA_HERE",
  "salted_provenance": "salted_sha256_here",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"Σ (or −F) is monotone along macrostate evolution.","direction":"increase"},
    {"id":"H2","statement":"Proxy concordance for α_I passes GPX gate.","direction":"no-change"},
    {"id":"H3","statement":"β_E matches d−1 within ±0.1 on analytic shapes.","direction":"no-change"},
    {"id":"H4","statement":"Grid-invariance slope drift ≤0.05 with CI overlap.","direction":"no-change"},
    {"id":"H5","statement":"Degeneracy g₂ ≤ 1e−10 at refined tolerance.","direction":"decrease"}
  ],
  "variables": {
    "independent": ["L","ε","σ","seed"],
    "dependent": ["β_E","α","α_I","N","ρ"],
    "controls": ["stencil","Δx","smoother"]
  },
  "pass_fail": [
    {"metric":"ΔΣ_min","operator":">=","threshold":-1e-12,"unit":""},
    {"metric":"|β_E-(d-1)|","operator":"<=","threshold":0.1,"unit":""},
    {"metric":"GPX_gap","operator":"<=","threshold":0.1,"unit":"fraction"},
    {"metric":"grid_slope_drift","operator":"<=","threshold":0.05,"unit":""},
    {"metric":"g2","operator":"<=","threshold":1e-10,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/hierarchy/specs/STIV_A8_Meters.v1.json"],
  "registration_timestamp": "AUTO-UTC"
}
```

(Fields mirror the template’s prereg spec.)

**Specs & Schemas.** Provide minimal JSON Schema and a spec with explicit parameter ladders (values for $L,\varepsilon,\sigma$, seeds). Follow the template’s **Specs** and **Schemas** blocks.

---

### 5.2 Experimental runplan

**Scope banner:** *T2 instrument calibration only; no phenomenon claim.* All A8 claims (G1–G12) remain governed by the separate T8 PROPOSAL.

**Datasets / testbeds.**
S1 **Analytic shapes** (2D/3D): disks, annuli, lattices of holes (Swiss‑cheese), extruded surfaces. **Truth** for area vs perimeter known → **β_E** oracle; **α, α_{\mathcal I}** computable from synthetic $I$ fields.
S2 **Static segmentations:** synthetic hierarchical partitions with prereg $N(L)$ ground truth.
S3 **Dynamic fields (bench)**: small RD/KG clips from existing instruments; *used only for meter stress* (not for A8 grading). (RD/KG evidence listed under milestones.)

**Independent variable ladders.**

* $L\in{128,256,512,1024}$, seeds $0..19$, $\varepsilon/\Delta x \in {1,2,3}$, $\sigma/\Delta x\in{1,2,3}$.
* Stencils: central‑diff (2nd,4th) for $\nabla$ and $\nabla^2$ (cross‑check GI).
* Smoothing: Gaussian mollifier radii ${0.5,1.0,2.0}\Delta x$ for $I_2$ positivity.

**QC / Gates (instrument pass/fail).**

* **G‑H** (A5): ΔΣ ≥ −1e−12 or ΔF ≤ +1e−12 per macrostep.
* **G‑PX**: proxy concordance for $\alpha_{\mathcal I}$ ≤10%. (Insights: EBN‑Info‑Functional.)
* **G‑DEP**: metriplectic degeneracy metric $g_2\le10^{-10}$ after refinement.
* **G‑GI**: grid‑invariance slope drift ≤0.05 with CI overlap across $(L,\Delta x)$ ladders.
* **G‑AL‑ModelSel**: **ΔAIC/ΔBIC ≥ 6** in favor of **area‑law** over **volume‑law** on S1; report β_E and CI.

**Outputs.**
JSON/CSV metrics, PDFs, and figures under `Derivation/code/outputs/meters/a8_stiv/{tag}/` with a RESULTS white‑paper following repo standards.

**Success path.** All gates pass on S1/S2 (instrument certified); S3 produces stable QC plots without asserting A8. **Failure path.** Auto‑spawn deconvolution and Minkowski‑morphometry tasks; tune $(\sigma,\varepsilon)$ ladders (as per EBN‑A8‑UQ note).

**Compute budget.** Analytic shapes and segmentations scale near‑linearly in pixel count; with $4$ sizes, $3$ radii, $3$ smoothers, $20$ seeds → $\approx720$ runs; each $<!1$ min on CPU for S1/S2; S3 clips budgeted separately (≤2 GPU‑hours). (HPC optimization in milestone **EBN‑HPC‑3D**.)

---

## 6. Personnel

**Justin K. Lietz** — implement STIV macrostate, meters, specs/schemas, prereg; run S1–S3; publish RESULTS and PASS/FAIL sheet; file promotion PRs on PASS (A8 meters go live).

---

## 7. References

* **STIV (origin)**: Leadbetter, Purohit, Reina, *PNAS Nexus* (2023): statistical‑mechanics framework ⇒ macroscopic non‑eq models; gradient‑flow structure.
* **STIV (general closure)**: Leadbetter, Purohit, Reina, *arXiv:2506.08156* (2025): **structure‑preserving** Langevin closure; **σ≥0**; non‑Gaussian families; convergence with internal‑variable dimension.
* **STIV (journalized)**: *J. Non‑Equilibrium Thermodynamics* (2025): **From Langevin dynamics to macroscopic thermodynamic models**; Penn Today coverage.
* **VDM Canon (A5–A7)**: program axioms and usage in QC/gates.
* **A8 PROPOSAL / Gates / Milestones / Insights**: formal A8 statement, gate set, missing meters, and bridge nodes this T2 satisfies.

---

## **Appendix A — Exact formulas and gate definitions**

**Excess energy:**
[
E_{\rm exc}[\phi;\Omega]=\int_{\Omega}\big(\kappa|\nabla\phi|^2+V(\phi)-V(\phi_\ast)\big),dx.
]

**Area‑law vs volume‑law:** Fit $E_{\rm exc}(L)\sim L^{\beta_E}$; **pass** if $|\beta_E-(d-1)|\le 0.1$ & $R^2\ge0.98$; report **ΔAIC/ΔBIC** vs $L^d$.

**Log‑depth:** $N(L)=c_N\log(L/\lambda)+b$ with finite‑size correction; instrument only reports fit (no A8 claim at T2). (Gate used later by T8.)

**Entropy production meter:** $\sigma(z)=\nabla F^\top K \nabla F \ge 0$; **H‑theorem pass** if minimum stepwise ΔΣ ≥ −1e−12 (or ΔF ≤ +1e−12).

---

### **5.1.1 (Provenance hashes — fill at run time)**

Include in the prereg: `base_sha256`, `salt_hex`, `salted_sha256`; record in the signed tag message (per template). The same values must appear in this section upon submission.  
