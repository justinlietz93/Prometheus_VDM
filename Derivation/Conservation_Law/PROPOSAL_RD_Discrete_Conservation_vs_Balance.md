# PROPOSAL - Discrete Conservation vs. Balance in a Reaction-Diffusion Update (Void Dynamics Model)

**Date:** 2025-10-06 08:58:39Z  
**Proposers:** Justin K. Lietz - Independent Researcher (VDM Project)

## 1. Abstract

We will adjudicate whether the *one-step* FUM reaction-diffusion (RD) update admits an **exact global discrete conservation law** expressible as a per-site density plus an **antisymmetric edge term**, or whether the correct invariant content is a **balance law** (production + telescoping flux) and a **Lyapunov monotone**. We attempt a symbolic telescoping identity; failing that, we demonstrate an **order-of-accuracy** residual consistent with the chosen time integrator. All figures will be paired with CSV/JSON artifacts and numeric captions per PAPER_STANDARDS.

## 2. Background & Rationale

Two calibration truths already hold and will be reused:

- **On-site ODE invariant** $(Q_{\rm FUM}(W,t))$ for the logistic sub-dynamics (used as a QC tool).
- **Diffusion-only mass conservation** via antisymmetric edge fluxes on periodic/no-flux domains.

Open question: does the **coupled** RD update (reaction + diffusion) possess an exact discrete conservation built from local quantities, or only a balance + H-theorem? The experiment aligns the tested step with the actual discretization (adjacency/BCs/integrator) and checks both possibilities rigorously.

## 3. Objectives & Hypotheses

**Obj‑A (Exact Conservation):** Exhibit

$$
(S[W] = \sum_i Q_i(W_i) + \sum_{\langle i,j\rangle} H_{ij}(W_i,W_j))
$$

such that for the implemented step

$$
(W^{n+1} = \mathcal U(W^n))
$$

$$
[ \Delta S \equiv S(W^{n+1}) - S(W^n) \equiv 0. ]
$$

**Obj‑B (Asymptotic Conservation):** If exact fails, show

$$
[ \max_i \big|\Delta Q_i + \sum_j(H_{ij}-H_{ji})\big| = \mathcal O(\Delta t^{p+1}), ]
$$

with $(p)$ the order of the time integrator (e.g., Strang split: $(p=2)$\).

**Obj‑C (Balance + H‑theorem):** Quantify Lyapunov drop for the full RD step and document monotonicity under stated hypotheses.

## 4. Methods & Experimental Design

### 4.1 Model Step Under Test

One step of a reaction-diffusion update on a periodic lattice (or declared BCs):

$$[
W^{n+1} = W^n + \Delta t\,\big( f(W^n) + D\,\Delta_{\text{disc}} W^n \big)
]$$

or a composed scheme (Strang/RKp) explicitly specified.

- **Reaction** $(f(W))$\: logistic with linear decay (parameters $(r,u)$\).
- **Diffusion**: graph Laplacian $(L)$ from the chosen adjacency; coefficient $(D)$.
- **Adjacency/BCs**: saved with each run (used by the fitter/checker).

Default choices for conservation tests (Obj‑A/B):

- **BC:** periodic (simplest flux bookkeeping and Fourier diagnostics).  
- **Scheme order p:** start with Euler (p=1), then Strang (p=2) using exact logistic substep (see reaction_exact.py).  
- **Neumann BCs** are reserved only for the front‑speed control runs.

### 4.2 Symbolic Conservation Attempt

Construct $(Q_i,H_{ij})$ and reduce $(\Delta S)$ in a CAS to a **symbolic zero**. Export minimal forms and a substitution table mirroring the *implemented* update (no linearization unless declared).

### 4.3 Asymptotic Composition Test

If exact conservation fails, perform a $(\Delta t)$\-sweep (≥4 halvings) for the same scheme and regress $(\log \max_i|{\rm residual}|)$ vs. $(\log \Delta t)$ to estimate slope and $(R^2)$\.

### 4.4 Controls

- **Diffusion-only**: $(f\equiv0)$\; check mass conservation via antisymmetric flux telescoping to machine epsilon.
- **Reaction-only**: verify 4th‑order convergence and tiny drift for $(Q_{\rm FUM})$ (ODE invariant).

### 4.5 Implementation Notes

- Deterministic seeds; fixed commit hash and environment snapshot.
- No clipping/saturation in proof paths (no `tanh`, `nan_to_num` that alters algebra).

### 4.6 Discrete Lyapunov (Obj‑C) - precise grid form

Use the same discrete gradient operator that pairs with the Laplacian stencil to avoid stencil mismatch. For 1D periodic FD with spacing $\Delta x$:

$$
\mathcal{L}_h[W] \,=\, \sum_{i} \left[ \tfrac{D}{2}\,\lvert \nabla_h W_i \rvert^2 + \hat V(W_i) \right] \, \Delta x, \qquad \hat V'(W) = -\,f(W)
$$

with centered gradient

$$
\nabla_h W_i \,=\, \frac{W_{i+1} - W_{i-1}}{2\,\Delta x}, \qquad \Delta_h W_i \,=\, \frac{W_{i+1} - 2W_i + W_{i-1}}{\Delta x^2}.
$$

Report $\Delta \mathcal{L}_h \le 0$ per step under periodic/no‑flux BCs.

## 5. Diagnostics, Metrics & Acceptance Gates

### 5.1 Mathematical Gates (must all pass for Obj‑A)

1. **Exact identity:** $(\Delta S \equiv 0)$ for the *implemented* one-step map.
2. **Local flux form:** $(\Delta Q_i + \sum_{j\in\mathcal N(i)} (H_{ij} - H_{ji}) = 0)$ per node.
3. **Scope declared:** BCs, scheme (unsplit/split/RKp), parameter domain $((r,u,J,D,a,\Delta t))$\.
4. **Symbolic certificate:** CAS-reduced zero with saved minimal forms.

### 5.2 Validation Gates (CI)

- **V1 Seed sweep (exactness):** ≥40 random seeds per tuple; require $(\max |\Delta S| \le 1e{-12})$ (double).
- **V2 Parameter grid:** ≥6 tuples $((r,u,J,D,N))$\, $(N \in \{64,128\})$\; same tolerance.
- **V3 dt-slope (asymptotic path):** slope ≥ $(p+1-0.1)$\, $(R^2 \ge 0.999)$\.
- **V4 Negative controls:**
  - Diffusion-only mass conservation at machine epsilon.
  - Reaction-only $(Q_{\rm FUM})$ order‑4 convergence with $(R^2 \approx 1)$\.
- **V5 Out‑of‑sample:** If $(H_{ij})$ has any fitted parameters, freeze them and rerun on fresh seeds; identical tolerances must hold.

## 6. Variables & Ranges (stub - fill before run)

| Symbol | Description | Values / Range | Notes |
|---|---|---|---|
| $(r)$ | Logistic growth | `[...]` | Units nondim |
| $(u)$ | Logistic scale | `[...]` | carry‑capacity term |
| $(D)$ | Diffusion coeff. | `[...]` | grid units |
| $(J)$ | Coupling (if used) | `[...]` | map to $(D)$ via derivation |
| $(\Delta t)$ | Time step | `[dt0, dt0/2, dt0/4, ...]` | for dt-sweep |
| $(N)$ | Lattice size | `{64,128}` | 1D (extend as needed) |
| BC | Boundary conds | `periodic` / `no-flux` | must match code |
| Scheme | Time integrator | `Euler` / `Strang p=2` / `RKp` | declare p |

## 7. Data Products & File Layout

Adopt this layout so PAPER_STANDARDS checkers can auto‑lift artifacts:

```
experiments/rd_conservation/
  step_spec.schema.json       # JSON schema for step_spec.json
  step_spec.example.json      # example config (see Section 10)
  runs/<stamp>/
    step_spec.json            # map definition + adjacency, scheme, CFL log
    seeds.json                # list of seeds/tuples actually used
    cas_certificate.txt       # ΔS ≡ 0 proof (if Obj‑A passes)
    sweep_exact.json          # residuals per seed/tuple (V1/V2)
    sweep_dt.json             # slope, R^2 (V3)
    controls_diffusion.json   # mass conservation checks (control)
    controls_reaction.json    # Q_FUM order‑4 RK check (control)
    CONTRADICTION_REPORT.json # emitted if Obj‑A fails (see Section 9)
    figures/
      residual_vs_dt.png
      residual_hist.png
      control_diffusion.png
      control_qfum_convergence.png
```

Each figure is paired with its CSV/JSON and a numeric caption (slope, $(R^2)$\, RMSE).

## 8. Reproducibility & Provenance

- Git commit: `<hash>`
- Python: `<version>`, NumPy/SciPy/SymPy versions listed
- ROCm: `<version>` (if GPU used)
- Seeds: list embedded in `seeds.json`
- Hardware summary (CPU/GPU/RAM) in `env.txt`

## 9. Risks & Kill Criteria

- **Risk:** No exact $(H_{ij})$ exists in the tested class.  
  **Kill:** Publish **CONTRADICTION_REPORT.json** with residual plots and statement of the class explored.
- **Risk:** Symbolic explosion for $(H_{ij})$ forms.  
  **Mitigation:** Start with minimal rational/log forms; backstop with asymptotic gate.
- **Risk:** Harness mismatch (adjacency/BCs).  
  **Kill:** Block publication until step-spec equals production step; rerun controls.
  
- **Risk:** No exact $(H_{ij})$ within the explored family.  
  **Mitigation/Deliverable:** Emit `CONTRADICTION_REPORT.json` with residual histograms and the precise $(Q,H)$ families explored (symbol classes, exponents, rational forms), plus best‑fit params if any.

## 10. Timeline & Responsibilities

- **Day 1:** Wire step-spec + controls, dry run on tiny grid.
- **Day 2:** CAS attempt; if fail, configure dt-sweep.
- **Day 3:** Full sweeps (V1-V3), figures + CSV/JSON, draft **Results** section.
- **Owner:** Justin K. Lietz

## 11. Deliverables

- CAS certificate or contradiction report
- Sweep JSON/CSVs + figures with numeric captions
- Markdown **RESULTS.md** drafted to PAPER_STANDARDS (figures boxed, acceptance gates reported)

## 12. PAPER_STANDARDS Compliance Checklist (copy/paste into RESULTS.md)

- [ ] Every figure has a *numeric caption* with fit stats (slope, $(R^2)$, RMSE).
- [ ] Each figure has a paired CSV/JSON artifact in the same folder.
- [ ] Acceptance gates (V1-V5) are stated and marked PASS/FAIL with numbers.
- [ ] Provenance block lists commit, env, seeds, hardware.
- [ ] Boxed **LEMMA/THEOREM** or **CONTRADICTION_REPORT** as appropriate.
- [ ] Units and dimensionless groups stated; BCs and scheme declared.
- [ ] All plots readable in grayscale; axes labeled with symbols and units.

## Appendix A - Minimal Runner Pseudocode

```python
# build adjacency and step-spec
adj = make_adjacency(N, bc="periodic")
def step(W, dt, params):
    # reaction-diffusion Euler (replace with declared scheme)
    return W + dt*(f(W, params['r'], params['u']) + params['D']*laplacian(adj, W))

# exact conservation attempt
Q_i, H_ij = construct_candidates()   # symbolic or parametric
residuals = []
for seed in seeds:
    W0 = init_random(seed)
    W1 = step(W0, dt, params)
    dS = S(W1, Q_i, H_ij, adj) - S(W0, Q_i, H_ij, adj)
    residuals.append(dS)
# log, then dt-sweep if needed
```

## Appendix B - JSON Schema Snippets

**`sweep_exact.json`**

```json
{"commit":"<hash>","scheme":"Strang","bc":"periodic",
 "params":{"r":0.2,"u":0.25,"D":1.0,"N":128,"dt":0.01},
 "samples":[{"seed":123,"delta_S":-2.3e-13}, {"seed":124,"delta_S":7.8e-14}]}
```

**`sweep_dt.json`**

```json
{"commit":"<hash>","scheme":"Strang","grid":"N=128",
 "dt":[0.04,0.02,0.01,0.005],
 "max_abs_residual":[1.6e-6, 1.0e-7, 6.2e-9, 3.9e-10],
 "fit":{"slope":3.02,"R2":0.9996}}
```

**`step_spec.json` (example)**

```json
{
  "bc": "periodic",
  "scheme": "euler",
  "order_p": 1,
  "expected_dt_slope": 2,
  "grid": {"N": 128, "dx": 1.0},
  "params": {"D": 1.0, "r": 0.2, "u": 0.25},
  "dt_sweep": [0.04, 0.02, 0.01, 0.005],
  "seeds": 40,
  "safety": {"clamp": false, "nan_to_num": false},
  "cfl_used": true,
  "notes": "Obj-A/B periodic RD; Neumann only used in separate front-speed control runs."
}
```

**CFL (stability) note:** For explicit diffusion in 1D Euler, ensure $\Delta t \le \Delta x^2/(2D)$. Log the boolean `cfl_used` and record the actual `dt` chosen.

**Adjacency fidelity:** The fitter and all residual/flux calculations must use the actual neighbor list (same stencil and BC as used during stepping). No complete‑graph or dense approximations.
