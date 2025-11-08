# T2 — PROPOSAL_OQ‑021_VDM‑Fluids_Corner_Regularization_v1

> **Created:** 2025-11-08  
> **Commit:** 1240402c7fd761699bfcdc7d09ffe786c3f6ad63  
> **Salted provenance:** {base_sha256}:{salt}:{salted_sha256}  
> **Proposer contacts:** [justin@neuroca.ai](mailto:justin@neuroca.ai)  
> **License:** See [LICENSE](/LICENSE)  
> **TL;DR:** Instrument a lid‑driven cavity with *unmodified 90° corners* and show VDM’s void‑debt regularization enforces **finite transport rate** and **bounded corner overshoot** without geometric smoothing, while honoring divergence and Mach gates.  

## 1. Tier Grade

**T2 (Instrument).** This is a meter for fluids‑locality and singularity regularization; later T3+ smoke/phenomena can build on it. (Proposal structure/discipline per the canonical template.)  

## 2. Abstract

A D2Q9 lattice‑Boltzmann (LBM) lid‑driven cavity on $([0,1]^2)$ with *exact* sharp corners is exercised at modest Mach $((\mathrm{Ma}\le 0.10))$ and $(\mathrm{Re}\in[100,1000])$. We compare **baseline BGK+bounce‑back** vs **VDM‑void gating** (controlled by `void_gain`) and test: (G1) finite‑speed signal cone from lid to interior, (G2) bounded *corner overshoot* $(\max_{r\le 4h}|u|/U_{\rm lid})$, (G3) incompressibility proxy via $(|\nabla!\cdot!u|_2)$, (G4) stability/completion, and (G5) monotone trend of overshoot with grid refinement under VDM‑gain. Constants and default knobs are taken from **VDM Constants & Defaults** (LBM).  

## 3. Background & Scientific Rationale

**Why corners?** Lid‑cavity corners are the canonical stress‑singularity traps; numerically, they often trigger grid‑dependent overshoot or effectively “instantaneous” transport if regularization is naive. This proposal targets the spec’s *locality and finite‑propagation* commitments (M1) using a fluids meter instead of KG, aligning with the **Unification Program Spec**’s hyperbolic–diffusive split and locality gates.  Readiness is bolstered by existing results: KG J‑only light‑cone and dispersion pass with tight fits and $(v\approx 0.998)$, showing the locality meters work.  

**What is instrumented?**
A 2‑D D2Q9 BGK LBM with no‑slip bounce‑back on three walls, a moving lid at $(U_{\rm lid})$, and **no corner rounding**. We use repo defaults: $(c_s^2=1/3)$; typical $(\tau\in[0.51,1.95])$ (controller clamps); $(U_{\rm lid}=0.1)$; divergence gate; step counts and sampling; plus the **VDM fluids knob** `void_gain` to activate void‑debt regularization.  

## 4. Intellectual Merit & Procedure (concise)

* **Importance:** Tests whether VDM’s regularization enforces *finite transport rate* at geometric singularities without geometry edits.
* **Broader impacts:** Provides a fluids‑branch “locality meter” analogous to our KG meter.
* **Approach & rigor:** Pre‑registered gates with CSV/JSON/PNG artifacts; uncertainty and pass/fail reporting per the project’s experimentation rules.  

## 5. Experimental Setup and Diagnostics

### 5.1 Geometry, units, and knobs

* **Domain:** unit square; grid $(N!\times!N)$, $(N\in{128,192,256})$.
* **LBM:** D2Q9 BGK, bounce‑back; $(c_s^2=1/3)$. **Defaults from repo**:
  `U_lid=0.1`, `tau` controller $([0.51,1.95])$, `steps` (lid) (=15000), `sample_every=200`, `warmup=2000`, `div_target=1e-6`, `Ma_max=0.10`.  
* **VDM‑gain:** `void_gain ∈ {0.0 (off), 0.25, 0.5, 0.75}`. (0.5 is the default in lid‑cavity benchmark.)  
* **Dimensionless groups:** $(\mathrm{Ma}!=U_{\rm lid}/c_s\le 0.10)$ (cap), $(\nu=c_s^2(\tau!-!1/2))$, $(\mathrm{Re}=U_{\rm lid}L/\nu)$.
* **Start/stop:** from rest; step to steady lid speed at (t=0); run to (t=15000) steps.

### 5.2 Diagnostics (one artifact family per run)

1. **Finite‑speed cone (G1)** — pick interior probes at distances (d) from the lid; detect first arrival $(t^\star(d))$ of (u) above $(5\cdot 10^{-5})$. Gate uses LBM causal ceiling $(c_s=1/\sqrt{3})$:

$$[
t^\star(d)\ \ge\ d/c_s \quad\text{for all probes.}
]$$

   Report violations count and min margin (CSV/JSON + figure). Constants for $(c_s)$ from **CONSTANTS**.  
2. **Corner overshoot ratio (G2)** — $(\rho_{\rm over}=\max_{r\le 4h}|u|/U_{\rm lid})$ around both top corners vs baseline.
3. **Divergence gate (G3)** — $(|\nabla!\cdot!u|_2)$ history; require $(\le)$ target. **Target is repo’s `div_target=1e-6`.**  
4. **Stability/completion (G4)** — run terminates with no NaNs and Mach cap obeyed (`Ma_max=0.10`).  
5. **Refinement trend (G5)** — slope of $(\rho_{\rm over}(N))$ across $(N={128,192,256})$. Expect **negative** slope with VDM‑gain; baseline may be flat/positive.

## 6. Pass/Fail Gates (decisive; all must pass)

* **G1: Causal cone** — For each probe $(d)$, $(t^\star(d)\ge d/c_s)$; zero violations; report min margin $(\ge 0)$. (Finite propagation.)
* **G2: Bounded overshoot** — With VDM‑gain on (`void_gain≥0.5`), $(\rho_{\rm over}\le 1.05)$ at all (N) and both corners; baseline may exceed.
* **G3: Divergence** — median $(|\nabla!\cdot!u|_2) (\le 1\times 10^{-6})$ after warmup.  
* **G4: Stability** — 15 000 steps complete; $(\max)$ Mach $(\le 0.10)$; no NaNs.  
* **G5: Refinement monotonicity** — linear fit slope of $(\rho_{\rm over}(N))$ **< 0** under VDM‑gain; 95% CI excludes $(\ge 0)$.

**Failure policy:** Emit a **CONTRADICTION_REPORT** (gate id, thresholds, probe/seed, commit, artifact pointers) per RESULTS/standards and experimentation rules.

## 7. Provenance & Artifacts

* **Figures:** `code/outputs/figures/fluids/oq021_corner_*`
* **Logs:** `code/outputs/logs/fluids/oq021_corner_*.json`
* **CSV:** `code/outputs/csv/fluids/oq021_corner_*`
* **Minimum per run:** 1 PNG + 1 CSV + 1 JSON; include `commit`, `seed`, `N`, `tau`, `U_lid`, `void_gain`. (Standards per RESULTS/PROPOSALS overview.)

## 8. Approvals, Pre‑Reg, Specs, Schemas (machine‑actionable)

**APPROVALS.json (sketch)** — place at `Derivation/code/physics/fluid_dynamics/APPROVALS.json`
(Format per template; one tag `vdm-lid-corner-v1`.)  

**PRE‑REGISTRATION.json (minimum keys)** — `Derivation/code/physics/fluid_dynamics/PRE-REGISTRATION.json`  

```json
{
  "proposal_title": "OQ-021 VDM-Fluids Corner Regularization",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "VDM gain enforces finite-speed cone", "direction": "no-change" },
    { "id": "H2", "statement": "VDM gain bounds corner overshoot ≤ 1.05", "direction": "decrease" }
  ],
  "variables": {
    "independent": ["N", "tau", "void_gain"],
    "dependent": ["t_star_margin", "rho_over", "div_L2", "mach_max"],
    "controls": ["U_lid", "steps", "warmup"]
  },
  "pass_fail": [
    { "metric": "t_star_margin_min", "operator": ">=", "threshold": 0.0, "unit": "LBM time" },
    { "metric": "rho_over", "operator": "<=", "threshold": 1.05, "unit": "-" },
    { "metric": "div_L2_med", "operator": "<=", "threshold": 1e-6, "unit": "1/time" },
    { "metric": "mach_max", "operator": "<=", "threshold": 0.10, "unit": "-" }
  ],
  "spec_refs": ["Derivation/code/physics/fluid_dynamics/oq021_corner.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

**Spec (example)** — `Derivation/code/physics/fluid_dynamics/oq021_corner.v1.json`  

```json
{
  "run_name": "oq021-corner",
  "version": "1.0.0",
  "tag": "vdm-lid-corner-v1",
  "schema_ref": "Derivation/code/physics/fluid_dynamics/schemas/oq021_corner.schema.json",
  "parameters": {
    "N": [128, 192, 256],
    "tau": [0.7, 0.9],
    "U_lid": 0.1,
    "void_gain": [0.0, 0.5],
    "steps": 15000,
    "warmup": 2000,
    "sample_every": 200
  },
  "seeds": [0, 1, 2]
}
```

**Schema (minimum draft‑2020‑12)** — `.../schemas/oq021_corner.schema.json` (keys and types).  

## 9. Methods / Procedure

* Use existing lid‑cavity benchmark as the base runner; keep walls perfectly sharp. Set $(U_{\rm lid}=0.1)$ and clamp Mach to 0.10 (repo default). Sample velocities and $(\nabla!\cdot!u)$ every 200 steps; compute $(t^\star(d))$ per probe; compute $(\rho_{\rm over})$ in (4h) corner halos. (Constants, sampling and caps from the fluids benchmark defaults.)  
* Emit artifact trio per run; if any gate fails, emit **CONTRADICTION_REPORT** with seed/commit pointers (standards).  
* Report uncertainty with multi‑seed medians + bootstrap CI (discipline per measurement rules).  

## 10. Risk Notes & Kill‑Plans

* **Corner stress blow‑up at high Re:** start with $(\tau\in{0.7,0.9})$ to keep $(\nu)$ moderate; abort series if $(\mathrm{Ma})$ control or divergence gate trips repeatedly.  
* **False early‑arrival detections:** use a fixed detection floor $(5\times10^{-5})$ and verify against quiet baselines; increase floor 2× if noise dominates early steps. (Pre‑registered in PRE‑REG.)  
* **Controller imprint:** log `tau` and lid controller state; include matched baseline with `void_gain=0` to separate effects (discipline per RESULTS standards).  

---

## Interaction Pattern (VDM ops)

**Classification:** *Derived‑limit* (fluids branch meter).
**Objective recap:** Prove VDM’s void‑debt regularization enforces finite propagation and bounded corner overshoot in a sharp‑corner cavity without geometric smoothing.
**Action plan (≤7):**

1. Land this **T2 proposal** and **APPROVALS.json**.  
2. Add **PRE‑REG** + **spec/schema** under `.../fluid_dynamics/`.  
3. Wire the lid‑cavity runner to emit probes/overshoot/divergence logs (reuse defaults).  
4. Run baseline (`void_gain=0.0`) across (N) and (\tau).  
5. Run VDM‑gain (`void_gain=0.5`) across the same grid.  
6. Evaluate G1–G5; write RESULTS with pass/fail JSON and figures (standards).
7. If any gate fails, emit **CONTRADICTION_REPORT** and adjust detection floor / seeds per failure policy.  

**Verification:**

* Physics discipline: explicit uncertainty, side‑by‑side baselines, and pass/fail statements per experimentation rules.  
* Software gates: artifacts, provenance, and approvals/prereg JSON per proposal template.  
* Program‑level alignment: targets with locality/finite‑propagation (M1) in Unification Spec.  

**Assumptions/Risks:**

* LBM lid‑cavity already present and parameterized as per **CONSTANTS** (paths in the constants table).  
* `void_gain` implements the VDM fluid regularizer (as documented in constants), not a hidden body force.  
* Measurement floors $((5\times 10^{-5}))$ and Mach cap reflect practical noise/accuracy tradeoffs; if they bias G1, the kill‑plan is to raise the floor with prereg update (logged).  

**Next steps (≤5):**

1. Commit this PROPOSAL under `Derivation/Fluid_Dynamics/Fluids_Corner_Regularization/T2_PROPOSAL_OQ-021_VDM-Fluids_Corner_Regularization_v1.md`.
2. Add APPROVALS + PRE‑REG + spec/schema and tag `vdm-lid-corner-v1`.  
3. Execute baseline vs VDM‑gain runs; publish RESULTS with gates + artifacts.  
4. If PASS, escalate to **T3 smoke**: corner‑induced vortex map comparisons and parameter sweeps $((\mathrm{Re}, N))$.
5. If FAIL, file **CONTRADICTION_REPORT** and triage (detection floor, controller tuning, time‑windowing).  
