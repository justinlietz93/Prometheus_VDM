# 1. **T2 (Instrument)** — **Surface Condensate Exchange Coarsening Meters (β_surf vs Exchange)**

> **Created Date:** 2025-11-24  
> **Provenance:** `{git rev-parse HEAD}` → `HEAD_SHA_HERE`; salted provenance: `base_sha256=…`, `salt_hex=…`, `salted_sha256=…`.  
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)  
> **License:** (Repository `LICENSE`)  
> **Short summary (TL;DR):** Proposed is a **T2 instrument** that measures the **surface‑condensate coarsening exponent β_surf** and pattern arrest as a function of **bulk‑surface exchange parameters**, to probe A2/A6 links between transport, coarsening, and pattern coexistence.

***Practical Provenance pattern.*** Follow the canonical template (salted hashes, signed prereg tag, push before runs; section **5.1.1** lists the required machine‑readable artifacts).

---

## 2. List of proposers and associated institutions/companies

**Justin K. Lietz** — Neuroca, Inc. (PI, implementer, approver).

---

## 3. Abstract

This **T2 instrument** calibrates how **material exchange between a 2D surface condensate and a 3D bulk reservoir** modifies **coarsening laws** and leads to **accelerated or arrested coarsening**, as recently demonstrated in exchange‑controlled surface condensate models (arXiv:2511.03619). The device measures mean droplet radius $R(t)$, droplet counts, and a fitted surface coarsening exponent $\beta_{\rm surf}$ across a ladder of passive and active exchange parameters. Primary outputs are **β_surf(k_p,k_a)**, interface statistics, and high‑R² fits suitable for use as an A2/A6 diagnostic of nonlocal transport and pattern arrest. No Axiom‑level claim is made here; the instrument only characterizes meter behaviour.

---

## 4. Background & Scientific Rationale

### Exchange‑controlled coarsening

Experimental and theoretical studies of **surface condensates** show that **exchange with a bulk phase** can dramatically modify coarsening: passive exchange often **accelerates** droplet growth, while **active exchange** (biased unbinding) can **arrest coarsening** and produce multi‑scale patterns. (arXiv:2511.03619). These effects arise from a competition between surface diffusion, bulk diffusion, and active source/sink terms.

In the VDM program, A2 focuses on **causal, finite‑speed transport**, and A6 on **scale‑dependent structure** and **hierarchical interfaces**. Exchange‑controlled surface condensates give a concrete, thermodynamically consistent setting where:

* transport is effectively nonlocal (surface ↔ bulk coupling), yet finite‑speed, and  
* interface‑rich patterns can persist with **β_surf≈0** (arrested coarsening).

This proposal turns that scenario into a **standardized meter**.

### Canonical alignment

* **A2 (Local causality):** bulk diffusion and surface dynamics obey local PDEs, with finite propagation speed enforced numerically via meters already in the VDM stack.
* **A6 (Scale program):** β_surf and droplet statistics become scale‑diagnostics for “exchange‑controlled” pattern vs coarsening.
* **STIV / A8:** surface condensates supply a complementary setting where interface hierarchies are driven by exchange rather than kernel‑range; the same A8 interface metrics can later be applied.  

---

## 5. Intellectual Merit and Procedure

**Importance.** Many biological and soft‑matter systems involve surface condensates coupled to reservoirs; understanding how **exchange rates** control **structure vs homogenization** is central to A2/A6. This instrument provides a reusable meter to quantify that dependence.

**Broader impacts.** The same machinery can be applied to **cellular condensates**, **membrane organization**, and **active emulsions**, where β_surf vs exchange parameters is directly experimentally accessible.

**Approach.** Implement a surface‑plus‑bulk model with passive and active exchange terms; simulate on 2D surfaces with 3D bulk or an effective bulk variable; track $R(t)$, droplet counts, and interface length; fit β_surf across exchange ladders; enforce R² and monotonicity gates.

---

### 5.1 Experimental Setup and Diagnostics

#### 5.1.0 Model, parameters, and observables

**Model (minimal form).**

* Surface order parameter: $\phi(\mathbf r,t)$ on a 2D periodic lattice.
* Bulk mean concentration: $\psi(t)$ (or a 3D field if desired for extensions).
* Exchange flux: $s(\mathbf r,t)$ containing passive and active parts:
  \[
  s(\mathbf r,t) = k_p(\psi-\phi) + k_a\,\Delta\mu(\mathbf r,t),
  \]
  where $\Delta\mu$ is a chemical‑potential bias term (sign and form preregistered).

**Surface evolution:**
\[
\partial_t \phi = -\nabla_s\cdot J_s + s(\mathbf r,t),
\]
with $J_s$ a surface diffusive current derived from a free‑energy functional $F[\phi]$ (e.g. Cahn–Hilliard‑type).

**Bulk evolution (effective reservoir):**
\[
\partial_t \psi = -\frac{1}{V_b}\int_{\rm surf} s(\mathbf r,t)\,dA,
\]
or explicit 3D diffusion with coupling at the surface.

**Independent variables.**

* Passive exchange rate: $k_p\in\{0, k_p^{(1)},k_p^{(2)},k_p^{(3)}\}$.
* Active exchange strength: $k_a\in\{0, k_a^{(1)},k_a^{(2)},k_a^{(3)}\}$.
* System size: $L/\Delta x\in\{256,512\}$.
* Seeds: ${\rm seed}\in\{0..15\}$.

**Observables.**

* Mean droplet radius: $R(t)$ from area‑weighted droplet segmentation.
* Droplet count: $N_{\rm drop}(t)$.
* Interface length: $P(t)$.
* Coarsening exponent: $\beta_{\rm surf}(k_p,k_a)$ from $R(t)\sim t^{\beta_{\rm surf}}$ in a prereg log–log window.
* Arrest indicator: slope $s_R(k_p,k_a)$ from $\log R(t)$ vs $\log t$; values near zero indicate arrest.

#### Diagnostics and gates

* **Fit gate (G‑β_surf‑Fit).** For each $(k_p,k_a)$, the late‑time linear fit of $\log R(t)$ vs $\log t$ must have $R^2\ge0.98$ to report $\beta_{\rm surf}$.
* **Passive‑accelerate gate (G‑Passive).** For increasing passive exchange $k_p$ with $k_a=0$, the estimated $\beta_{\rm surf}(k_p)$ must be **non‑decreasing** within CI overlap (accelerated coarsening).
* **Active‑arrest gate (G‑Active‑0).** For sufficiently strong active exchange $k_a$ at fixed small $k_p$, the exponent must satisfy $|\beta_{\rm surf}(k_a)|\le 0.05$ and $|s_R|\le0.05$ (arrested coarsening window).
* **Pattern gate (G‑Pattern).** In arrested regimes, droplet counts $N_{\rm drop}(t)$ and interface length $P(t)$ must plateau (slope magnitude ≤0.05), indicating pattern persistence.
* **Grid‑invariance gate (G‑GI).** β_surf estimates for the same $(k_p,k_a)$ across $L/\Delta x$ ladders must show slope drift ≤0.05 with overlapping CIs.

Outputs: CSV/JSON of β_surf, R², slopes, and pattern statistics; PNGs of $R(t)$ and $N_{\rm drop}(t)$; summary PDFs under `Derivation/code/outputs/meters/surface_exchange_coarsening/{tag}/`.

---

#### 5.1.1 Pre‑Run Config Requirements

Prepare the following artefacts before artifact‑writing runs:

* `Derivation/code/physics/surface_exchange/APPROVALS.json`
* `Derivation/code/physics/surface_exchange/schemas/Surface_Exchange_Coarsening_Meters.schema.json`
* `Derivation/code/physics/surface_exchange/specs/Surface_Exchange_Coarsening_Meters.v1.json`
* `Derivation/experiments/prereg/Surface_Exchange_Coarsening_Meters.v1.json`

**APPROVALS.json (template):**

```json
{
  "preflight_name": "surface_exchange_coarsening_preflight",
  "description": "Approval manifest for surface-exchange coarsening meters; preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs may execute under Derivation/code/tests. Artifact-writing runs require this T2 proposal to be approved.",
  "pre_registered": true,
  "proposal": "Derivation/Hierarchy/A2A6_Surface_Condensates/T2_PROPOSAL_Surface_Exchange_Coarsening_Meters_v1.md",
  "allowed_tags": ["surface-exchange-coarsening-v1"],
  "schema_dir": "Derivation/code/physics/surface_exchange/schemas",
  "approvals": {
    "surface-exchange-coarsening-v1": {
      "schema": "Derivation/code/physics/surface_exchange/schemas/Surface_Exchange_Coarsening_Meters.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto",
      "approval_key": "auto"
    }
  }
}
````

**PRE‑REGISTRATION.json (minimum keys):**

```json
{
  "proposal_title": "T2 — Surface Condensate Exchange Coarsening Meters",
  "tier_grade": "T2",
  "commit": "HEAD_SHA_HERE",
  "salted_provenance": "salted_sha256_here",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"β_surf increases with passive exchange k_p at k_a=0.","direction":"increase"},
    {"id":"H2","statement":"Strong active exchange k_a can drive |β_surf| ≤ 0.05 (coarsening arrest).","direction":"decrease"},
    {"id":"H3","statement":"R(t) plateau in arrested regimes has |s_R| ≤ 0.05.","direction":"no-change"},
    {"id":"H4","statement":"N_drop and P(t) plateau in arrested regimes (|s_N|,|s_P| ≤ 0.05).","direction":"no-change"},
    {"id":"H5","statement":"β_surf is grid-invariant within 0.05 across L for fixed (k_p,k_a).","direction":"no-change"}
  ],
  "variables": {
    "independent": ["k_p","k_a","L","seed"],
    "dependent": ["β_surf","R2_β","s_R","s_N","s_P"],
    "controls": ["Δx","Δt","volume_fraction"]
  },
  "pass_fail": [
    {"metric":"R2_β_min","operator":">=","threshold":0.98,"unit":""},
    {"metric":"β_passive_monotone_flag","operator":"==","threshold":1,"unit":""},
    {"metric":"β_arrest_max","operator":"<=","threshold":0.05,"unit":""},
    {"metric":"|s_R|_max","operator":"<=","threshold":0.05,"unit":""},
    {"metric":"GI_drift_β","operator":"<=","threshold":0.05,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/surface_exchange/specs/Surface_Exchange_Coarsening_Meters.v1.json"],
  "registration_timestamp": "AUTO-UTC"
}
```

---

### 5.2 Experimental runplan

**Scope banner:** *T2 instrument calibration only; no phenomenon claim.* Any A2/A6/A8 claims about exchange‑controlled hierarchies are deferred to higher‑tier proposals.

**Datasets / testbeds.**

* S1: Passive‑only ladder $(k_a=0)$ to benchmark acceleration of coarsening.
* S2: Active‑only ladder $(k_p$ small, $k_a$ varied$)$ to identify arrested regimes.
* S3: Mixed ladders $(k_p,k_a)$ to map a coarse phase diagram of β_surf and arrest.

**QC / Gates.** Instrument passes if PRE‑REG gates are satisfied on S1–S2 with stable β_surf across seeds and grids; S3 is exploratory but must not violate causality or numerical stability constraints from existing meters.

**Outputs.** Metrics and figures under `Derivation/code/outputs/meters/surface_exchange_coarsening/{tag}/` plus a RESULTS white‑paper per repository standards.

---

## 6. Personnel

**Justin K. Lietz** — implement exchange model and meters, specs/schemas, prereg; run S1–S3; publish RESULTS and PASS/FAIL sheet; file promotion PRs on PASS.

---

## 7. References

* Exchange controls coarsening of surface condensates, arXiv:2511.03619 (2025).
* CF3 — A8 Scaling and Hierarchical Interfaces (VDM).
* T2 — STIV Macrostate & Gradient-Flow Meters for A8 (hierarchy instrumentation).
