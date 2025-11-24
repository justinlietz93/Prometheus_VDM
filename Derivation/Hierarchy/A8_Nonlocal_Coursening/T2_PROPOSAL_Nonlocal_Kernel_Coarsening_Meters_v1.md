# 1. **T2 (Instrument)** — **Nonlocal Kernel Coarsening Meters for A8 Interface Scaling**

> **Created Date:** 2025-11-24  
> **Provenance:** `{git rev-parse HEAD}` → `HEAD_SHA_HERE`; salted provenance: `base_sha256=…`, `salt_hex=…`, `salted_sha256=…` (to be inserted by prereg script).  
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)  
> **License:** (Repository `LICENSE`)  
> **Short summary (TL;DR):** Proposed is a **T2 instrument** that measures **coarsening exponents and interface counts** in nonlocal phase‑separation models as a function of interaction‑kernel range ξ, to probe A6’s “hierarchical interface” program under controlled nonlocality.

***Practical Provenance pattern.*** Follow the canonical steps in the template (salted hashes, signed prereg tag, push before runs; section **5.1.1** repeats exact artifacts and required keys).

---

## 2. List of proposers and associated institutions/companies

**Justin K. Lietz** — Neuroca, Inc. (PI, implementer, approver).

---

## 3. Abstract

A **T2 instrument** is introduced to benchmark how **nonlocal interactions** modify **phase‑separation coarsening laws** and **interface statistics**. Starting from a conserved Cahn–Hilliard‑type model with a **finite‑range interaction kernel** $K_\xi$, the instrument measures (i) coarsening exponents $\beta(\xi)$ from domain size $L_{\rm dom}(t)$, and (ii) interface counts $N_{\rm iface}(t;\xi)$ over time, across a ladder of kernel ranges $\xi$. The primary goal is instrument‑grade calibration of **“coarsening suppression” vs interaction range**, motivated by recent nonlocal phase‑separation work (e.g. arXiv:2511.05214), and alignment with A6’s scale‑program for **hierarchical interfaces and pattern coexistence**. No A8/A6 phenomenon claim is made at T2; only meter behaviour and gates are tested.

---

## 4. Background & Scientific Rationale

### A8/A6 context

A8 (Infinity Resolution) posits that finite excess energy in tachyonic systems necessitates **hierarchical interface structures** with $N(L)=\Theta(\log(L/\lambda))$ and boundary‑law excess energy.:contentReference[oaicite:1]{index=1}  
CF3 formalizes this via **hierarchical interface counts and tubular‑energy fractions**. Short‑range dynamics (local RD / Cahn–Hilliard) typically yield **classical coarsening** (domain size $L_{\rm dom}\sim t^\beta$ with $\beta\approx1/3$ in many cases). The open question for A6 is how **nonlocal interactions** alter these scaling laws and whether they naturally generate **patterned, interface‑rich phases** that arrest coarsening and coexist with homogeneous phases.

Recent work on **phase separation with nonlocal interactions** shows: (i) long‑range kernels tend to suppress coarsening, and (ii) short‑range nonlocal kernels can generate **finite‑length‑scale patterns** and coexistence of patterned and homogeneous phases, with a mapping to a conserved Swift–Hohenberg model. (arXiv:2511.05214). These results match the qualitative scenarios anticipated in CF3 (patterned phases vs classical coarsening) but have not yet been integrated into the A8 meter stack.

### Canonical alignment

* **A2 (Local causality)** is respected by keeping nonlocal kernels **finite range** with explicit ξ‑ladder and regularity assumptions.
* **A6 (Scale program)** motivates the **dimensionless coarsening exponents** $\beta(\xi)$ and interface‑count slopes as functions of kernel range.
* **A7 (Measurability)** enforces preregistration, QC gates, and machine‑readable artefacts.

This T2 instrument bridges the nonlocal phase‑separation literature and the A8 interface‑hierarchy program by providing **coarsening meters** that can later be coupled to A8 hierarchy gates (T3) and scaling conjectures (T8).:contentReference[oaicite:2]{index=2}  

---

## 5. Intellectual Merit and Procedure

**Importance.** A8’s hierarchical‑interface claims require meters that can distinguish **classical coarsening** from **coarsening suppression and pattern arrest** as interaction range varies. This instrument provides a controlled nonlocal testbed with explicit β(ξ) and interface‑count metrics.

**Broader impacts.** Nonlocal phase‑separation and pattern‑forming systems appear in **soft matter, active matter, and biological condensates**; a calibrated meter for “coarsening vs nonlocality” is widely reusable beyond VDM.

**Approach.** Implement a conserved nonlocal phase‑separation model on a periodic grid, sweep **interaction‑range ξ**, and compute domain size, interface counts, and structure‑factor peaks as functions of time. Fit $\beta(\xi)$ and interface‑count slopes with preregistered windows and QC criteria (R² thresholds, monotonicity checks).

**Rigor.** All metrics, windows, and ξ‑ladders are preregistered; gates enforce **fit quality**, **monotone suppression of β with ξ**, and **plateau behaviour** in interface counts for large ξ.

---

### 5.1 Experimental Setup and Diagnostics

#### 5.1.0 Model, parameters, and observables

**Model.** Conserved nonlocal phase‑separation in $d=2$ (extendable to $d=3$):

\[
\partial_t \phi = \nabla^2\mu,\qquad 
\mu = f'(\phi) - (K_\xi\*\phi),
\]

where $f(\phi)$ is a double‑well potential (e.g. $f(\phi)=\tfrac14(\phi^2-1)^2$) and $K_\xi$ is a normalized, finite‑range kernel with characteristic length ξ (e.g. Gaussian or top‑hat). Discretization uses a conservative finite‑difference or spectral scheme with CFL‑safe time‑stepping.

**Independent variables.**

* Kernel range: $\xi/\Delta x\in\{1,2,4,8,16\}$.
* System size: $L/\Delta x\in\{256,512,1024\}$.
* Volume fraction: $\bar\phi\in\{-0.3,0.0,0.3\}$.
* Seeds: $ {\rm seed}\in\{0..15\}$.

**Observables.**

* **Domain size** $L_{\rm dom}(t;\xi)$ from correlation function $C(r,t)$ (e.g. first zero crossing) or dominant wavenumber $q^\*(t)$ from structure factor $S(q,t)$ with $L_{\rm dom}\approx 2\pi/q^\*$.
* **Interface length / area** $P(t;\xi)$ from level‑set segmentation (e.g. $|\phi|=\phi_{\rm th}$ contour).
* **Interface counts** $N_{\rm iface}(t;\xi)$ from connected‑component labeling of domains.
* **Coarsening exponent** $\beta(\xi)$ from log–log fit $L_{\rm dom}(t)\sim t^{\beta(\xi)}$ in a preregistered late‑time window.
* **Interface‑count slope** $s_N(\xi)$ from $\log N_{\rm iface}(t)$ vs $\log t$ over the same window.

#### Diagnostics and gates

* **Fit quality gate (G‑β‑Fit).** For each ξ, the log–log fit of $L_{\rm dom}(t)$ vs $t$ must satisfy $R^2\ge0.98$ to report $\beta(\xi)$.
* **Classical baseline gate (G‑β‑0).** For the smallest kernel range ξ_min, $\beta(\xi_{\min})$ must lie within $[0.25,0.40]$ (classical diffusive coarsening) with CI reported.
* **Suppression gate (G‑β‑Supp).** Across the ξ‑ladder, $\beta(\xi)$ must be **non‑increasing** within CI overlap; for the largest ξ, $\beta(\xi_{\max})\le0.05$ (arrested coarsening regime).
* **Interface‑plateau gate (G‑N‑Plateau).** For ξ in the patterned regime (identified by finite $q^\*$), the interface‑count slope $s_N(\xi)$ must satisfy $|s_N(\xi)|\le0.05$ over the late‑time window (plateau in $N_{\rm iface}(t)$).
* **Grid‑invariance gate (G‑GI).** Repeating runs across $L/\Delta x$ ladders must yield β‑slopes with drift ≤0.05 and overlapping CIs (A6 grid‑invariance).

Outputs: CSV/JSON metrics per ξ, PNGs of $L_{\rm dom}(t)$ and $N_{\rm iface}(t)$ vs $t$, and summary PDFs under `Derivation/code/outputs/meters/a8_nonlocal_coarsening/{tag}/`.

---

#### 5.1.1 Pre‑Run Config Requirements

Create the following **machine‑readable artifacts** before any artifact‑writing run:

* `Derivation/code/physics/hierarchy_nonlocal/APPROVALS.json`
* `Derivation/code/physics/hierarchy_nonlocal/schemas/Nonlocal_Coarsening_Meters.schema.json`
* `Derivation/code/physics/hierarchy_nonlocal/specs/Nonlocal_Coarsening_Meters.v1.json`
* `Derivation/experiments/prereg/Nonlocal_Coarsening_Meters.v1.json`

**APPROVALS.json (template):**

```json
{
  "preflight_name": "nonlocal_coarsening_preflight",
  "description": "Approval manifest for nonlocal-kernel coarsening meters; preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs may execute under Derivation/code/tests. Artifact-writing runs require this T2 proposal to be approved.",
  "pre_registered": true,
  "proposal": "Derivation/Hierarchy/A8_Nonlocal_Coarsening/T2_PROPOSAL_Nonlocal_Kernel_Coarsening_Meters_v1.md",
  "allowed_tags": ["a8-nonlocal-coarsening-v1"],
  "schema_dir": "Derivation/code/physics/hierarchy_nonlocal/schemas",
  "approvals": {
    "a8-nonlocal-coarsening-v1": {
      "schema": "Derivation/code/physics/hierarchy_nonlocal/schemas/Nonlocal_Coarsening_Meters.schema.json",
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
  "proposal_title": "T2 — Nonlocal Kernel Coarsening Meters for A8",
  "tier_grade": "T2",
  "commit": "HEAD_SHA_HERE",
  "salted_provenance": "salted_sha256_here",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"For ξ→ξ_min, β(ξ) matches classical coarsening within ±0.1.","direction":"no-change"},
    {"id":"H2","statement":"β(ξ) is non-increasing with ξ within CI overlap.","direction":"decrease"},
    {"id":"H3","statement":"β(ξ_max) ≤ 0.05 (coarsening suppression/arrest).","direction":"decrease"},
    {"id":"H4","statement":"Interface-count slope |s_N(ξ)| ≤ 0.05 in patterned regimes.","direction":"no-change"},
    {"id":"H5","statement":"Grid-invariance drift in β(ξ) across L is ≤ 0.05.","direction":"no-change"}
  ],
  "variables": {
    "independent": ["ξ","L","seed","φ_bar"],
    "dependent": ["β(ξ)","R2_β(ξ)","s_N(ξ)","q_star(ξ)"],
    "controls": ["Δx","Δt","kernel_shape"]
  },
  "pass_fail": [
    {"metric":"R2_β_min","operator":">=","threshold":0.98,"unit":""},
    {"metric":"|β(ξ_min)-β_ref|","operator":"<=","threshold":0.1,"unit":""},
    {"metric":"β_monotone_flag","operator":"==","threshold":1,"unit":""},
    {"metric":"β(ξ_max)","operator":"<=","threshold":0.05,"unit":""},
    {"metric":"|s_N|_max","operator":"<=","threshold":0.05,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/hierarchy_nonlocal/specs/Nonlocal_Coarsening_Meters.v1.json"],
  "registration_timestamp": "AUTO-UTC"
}
```

---

### 5.2 Experimental runplan

**Scope banner:** *T2 instrument calibration only; no phenomenon claim.* All A8/A6 claims remain governed by separate T1/T3/T8 proposals.

**Testbeds.**

* S1: 2D phase separation with local Cahn–Hilliard (ξ≈Δx) → classical coarsening baseline.
* S2: 2D nonlocal kernels with increasing ξ (Gaussian and top‑hat families) → probe suppression and patterned phases.
* S3: Optional 3D runs on reduced grid for robustness (lower priority).

**Independent variable ladders.** As specified above; detailed values enumerated in the SPEC.

**QC / Gates (instrument pass/fail).** Instrument passes if all PRE‑REG gates pass on S1/S2, and metrics are stable across seeds and grid sizes.

**Outputs.** JSON/CSV/PNG under `Derivation/code/outputs/meters/a8_nonlocal_coarsening/{tag}/` plus a RESULTS white‑paper per repository standards.

---

## 6. Personnel

**Justin K. Lietz** — implement nonlocal model, meters, schemas/specs, prereg; run S1–S3; publish RESULTS and PASS/FAIL sheet; file promotion PRs on PASS.

---

## 7. References

* Phase separation with non-local interactions, arXiv:2511.05214 (2025).
* CF3 — A8 Scaling and Hierarchical Interfaces (VDM).
* STIV Macrostate & Gradient-Flow Meters T2 proposal (for A8 interface metrics).
