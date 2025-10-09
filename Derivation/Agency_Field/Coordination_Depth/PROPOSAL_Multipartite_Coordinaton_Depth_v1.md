# PROPOSAL_Multipartite_Coordination_Depth_v1.1.md

## 1) Title & date

**Multipartite Coordination Depth (MCD) in Agency Fields** - 2025-10-09

## 2) Proposers

Justin K. Lietz - VDM Project

## 3) Abstract

We pre-register a **device-independent depth witness** that detects and quantifies **genuine multipartite coordination** in a metriplectic/void-dynamics agent without inspecting internal states. The 2D domain is tiled into (B) disjoint spatial blocks. For a task performance metric (J) (hit probability of a registered target (\Omega_\star) within horizon (T)), we define per-block and joint performance drops under **blockwise phase-scrambled perturbations** that preserve **local statistics** at the agent’s position:
[
\Delta J_b \equiv J_{\mathrm{real}}-J_{\mathrm{scramble}(b)},\qquad
\Delta J_S \equiv J_{\mathrm{real}}-J_{\mathrm{scramble}(S)} .
]
The **superadditivity witness** for order (k) is
[
\mathcal{S}*k ;\equiv; \operatorname*{median}*{|S|=k}\bigg[;\Delta J_S ;-; \sum_{b\in S}\Delta J_b;\bigg].
]
We define the **Coordination Depth Index (CDI)** as
[
\mathrm{CDI};\equiv;\max{,k:\ \mathcal S_k \ge \tau \ \text{and 95% CI excludes }0 \ (\text{after FDR adjustment}),}.
]
Classically **local** or (k)-producible controllers predict (\mathcal S_k\approx 0) for (k\ge 2). A positive (\mathcal S_k) that survives controls implies **genuine (k)-partite coordination**. Primary gate: (\mathrm{CDI}\ge 3) with replication across discretizations and pre-registered sampling.

## 4) Background & scientific rationale

An agent evolving under a metriplectic J(\oplus)M scheme can, in principle, coordinate information across disjoint regions: the **J**-branch transports structure; the **M**-branch selects via Lyapunov descent. We adopt a classical analogue of **(k)-producibility** from many-body certification: a controller decomposable into independent blocks (or using only local features) is **additive** over disjoint perturbations, implying (\Delta J_S \approx \sum_{b\in S}\Delta J_b) and thus (\mathcal S_k\approx 0) for (k\ge 2). Deviations beyond uncertainty quantify **coordination depth**, independent of internal architecture (device-independent).

This proposal encodes that logic in a **block-scramble protocol** that preserves **local value, gradient, and curvature** around the agent while destroying coherence within specified blocks, plus **discretization replication** to reject numerical artifacts.

## 5) Objectives & hypotheses

* **H1 (Null additivity / (k)-producible control):** For a pre-registered local baseline policy (\mathcal P_{\mathrm{local}}) (ADC logistic using only radius-(r_{\mathrm{loc}}) features), (\mathcal S_k \approx 0) for all (k\ge 2), yielding (\mathrm{CDI}\le 1).
* **H2 (Genuine multipartite coordination):** For the VDM agent (\mathcal P_{\mathrm{vdm}}), (\exists,k_\star\ge 3) such that (\mathcal S_{k_\star}\ge\tau) with 95% CI (FDR-adjusted) excluding 0, hence (\mathrm{CDI}\ge 3).
* **H3 (Robustness):** (\mathrm{CDI}) and the set of significant (S) replicate across discretizations (FD-3pt vs spectral) with Jaccard overlap (\ge 0.7) and (|\Delta \mathrm{CDI}| \le 1).
* **H4 (Local-feature invariance):** After conditioning on matched local statistics at the agent location (x_0) (value (m), gradient (|\nabla m|), Laplacian (\Delta m), and a (3\times3) neighborhood), (\mathcal S_k) remains above threshold for (\mathcal P_{\mathrm{vdm}}), while (\mathcal S_k\approx 0) for (\mathcal P_{\mathrm{local}}).

## 6) Variables (pre-registered)

**Independent**

* **Partitioning:** (B\in{4,8,16}) (regular tiling).
* **Order sampling:** (k=1,\dots,k_{\max}) with a pre-registered count of sampled sets per (k) (e.g., 32).
* **Landscape generator:** RD steady state with parameters ((D,r_m,u)) or spectral synthesis with fixed power spectrum; seed list.
* **Discretization:** grid (N\in{128,256}); stencil (\in{\text{FD-3pt},\text{spectral}}).
* **Agent:** (\mathcal P_{\mathrm{vdm}}) (J(\oplus)M; scheme (\in{\text{jmj-strang},\text{jmj-spectralDG}})), and (\mathcal P_{\mathrm{local}}) baseline (radius-(r_{\mathrm{loc}}) features only).
* **Task:** target quantile (q) for (\Omega_\star); horizon (T).
* **Seeds:** number of seeds per configuration; tag.

**Dependent**

* (J) (primary: hit probability by (T); secondary: median time-to-hit).
* (\Delta J_b), (\Delta J_S), (\mathcal S_k), and (\mathrm{CDI}).
* Local match residuals at (x_0): (|m|), (|\nabla m|), (|\Delta m|), neighborhood mean/var.

**Controls**

* (\mathcal P_{\mathrm{local}}) null runs (entire protocol).
* **Near-block** perturbations that change only local features (negative control; expect (\mathcal S_k \approx 0)).

## 7) Equipment / Hardware

CPU; optional FFT backend if spectral operators are enabled. All code resides under `Derivation/code/physics/agency/coord_depth/` with shared helpers in `Derivation/code/common/`. No edits to prior experiments.

## 8) Methods & procedure

### 8.1 Field partition & block perturbations

1. Generate base field (m) (RD steady or spectral).
2. Tile the domain into (B) blocks ({\mathcal B_1,\dots,\mathcal B_B}).
3. For a chosen set (S) with (|S|=k), construct (m^{(S)}) by **phase-scrambling** the content restricted to (\cup_{b\in S} \mathcal B_b), preserving the global amplitude spectrum.
4. Enforce **local-match tolerances** at the agent’s (x_0):
   [
   |m-m^{(S)}| \le \varepsilon_m,\quad |\nabla m-\nabla m^{(S)}| \le \varepsilon_g,\quad |\Delta m-\Delta m^{(S)}| \le \varepsilon_\Delta
   ]
   and a (3\times3) neighborhood mean/var check. Mark trials **invalid** if any tolerance fails; record residuals in CSV.

### 8.2 Rollouts & metrics

* For each seed and each sampled (S), roll out (\mathcal P_{\mathrm{vdm}}) on (m) (real) and (m^{(S)}) (scrambled) with identical RNG streams to horizon (T); compute (J), (\Delta J_S).
* For (k=1) record all (\Delta J_b).
* Compute (\mathcal S_k) as median over sampled (S) sets and seeds (median-of-means aggregation).
* Repeat the full protocol with (\mathcal P_{\mathrm{local}}).

### 8.3 Statistics & multiple comparisons

* Bootstrap 95% CIs for (\mathcal S_k) at each (k).
* Apply Benjamini–Hochberg FDR across (k) (and over discretizations if pooled) and report **adjusted** CIs in CSV/JSON sidecars.
* Define threshold (\tau = 5,\sigma_{\mathrm{null}}(k)) using the pooled null standard deviation of (\Delta J_S - \sum_{b\in S}\Delta J_b) at that (k).

### 8.4 Discretization robustness

* Repeat for (FD-3pt, spectral) and (N\in{128,256}).
* Compute (\mathrm{CDI}) per discretization and the **Jaccard overlap** for the set of significant (S) (adjusted CI excludes 0). Require overlap (\ge 0.7) and (|\Delta\mathrm{CDI}|\le 1).

## 9) Metrics & acceptance gates

**Primary (Depth certificate)**

* **G1 (Depth):** (\mathrm{CDI}\ge 3) with adjusted 95% CI excluding (<3).
* **G2 (Replication):** Jaccard overlap (\ge 0.7) of significant (S) across discretizations; (|\Delta\mathrm{CDI}|\le 1).

**Null & controls**

* **G3 (Null additivity):** For (\mathcal P_{\mathrm{local}}), adjusted CIs for (\mathcal S_k) contain (0) for all (k\ge 2); (\mathrm{CDI}\le 1).
* **G4 (Local invariance):** After conditioning on local-match residuals passing tolerances, (\mathcal S_k) for (\mathcal P_{\mathrm{vdm}}) remains above (\tau) while (\mathcal P_{\mathrm{local}}) remains near (0).

**Failure plan**
Any failed gate emits `CONTRADICTION_REPORT__{tag}.json` with per-(S) histograms, adjusted vs unadjusted CIs, local-match diagnostics, and discretization ablations.

## 10) Data products & artifact paths (PAPER_STANDARDS)

**Domain folders**

* **Figures** → `Derivation/code/outputs/figures/coord_depth/`
* **Logs/CSVs/JSON** → `Derivation/code/outputs/logs/coord_depth/`

**Per run (suffixed by `__{tag}`)**

* `deltaJ_per_block__{tag}.csv` (all (\Delta J_b)); `heatmap_deltaJ_blocks__{tag}.png`
* `superadditivity_Sk__{tag}.csv` (k, median (\mathcal S_k), adjusted CI, seeds); `Sk_vs_k__{tag}.png`
* `coordination_depth_summary__{tag}.json` ((\mathrm{CDI}), CIs, gates)
* `discretization_overlap__{tag}.json` (Jaccard, (|\Delta\mathrm{CDI}|))
* `local_match_residuals__{tag}.csv`
* `spec_snapshot__{tag}.json`
* On fail: `failed_runs/CONTRADICTION_REPORT__{tag}.json`

All figures include **numeric captions** (CDI, CIs, gate verdicts) and have CSV/JSON sidecars.

## 11) Implementation plan (additive; no edits to prior results)

**Code layout**

* `Derivation/code/physics/agency/coord_depth/run_coord_depth.py` - CLI runner (`--spec path.json`)
* `Derivation/code/physics/agency/coord_depth/block_partition.py` - tiling utilities
* `Derivation/code/physics/agency/coord_depth/perturb_ops.py` - blockwise phase-scramble + local-match checks
* Reuse I/O, bootstrap, and discretization helpers from `Derivation/code/common/`

**StepSpec (example)** - `Derivation/specs/agency/coord_depth.v1b.json`

```json
{
  "grid": {"N": 256, "L": 10.0, "stencil": "fd3"},
  "field": {"type": "rd-steady", "D": 1.0, "r": 0.2, "u": 0.25, "seed": null},
  "partition": {"B": 8, "k_max": 4, "samples_per_k": 32},
  "agent": {"scheme": "jmj-strang", "v": 0.5, "Gamma": 0.8, "Theta": 3.0},
  "null_policy": {"radius_local": 1.0},
  "task": {"target_quantile": 0.9, "T": 50.0},
  "seeds": 40,
  "tolerances": {"m": 1e-6, "grad": 1e-6, "lap": 1e-6},
  "discretizations": [{"N": 256, "stencil": "fd3"}, {"N": 256, "stencil": "spectral"}],
  "fdr": {"enabled": true, "alpha": 0.05},
  "tau_sigma": 5.0,
  "tag": "MCD-v1b"
}
```

## 12) Risks & mitigations

* **Combinatorics:** the number of (S) grows quickly (\Rightarrow) pre-register `samples_per_k`; stratified uniform sampling.
* **Local leakage:** imperfect local-match at (x_0) (\Rightarrow) strict tolerances; mark trials invalid; log residuals.
* **Weak signal:** increase (T)/seeds; reduce (B) (larger blocks); enable spectral-DG (param-gated) for stronger nonlocal transport (report both profiles).
* **Discretization bias:** require CDI replication and Jaccard overlap gates.

## 13) Evidence & reproducibility

Every figure has numeric captions and CSV/JSON sidecars. Specs are snapshotted. Failed gates are quarantined to `failed_runs/`. Multiple-comparison adjustments (FDR) and sampling counts are recorded in sidecars. No post-hoc tuning of (B), (k_{\max}), or `samples_per_k` beyond the pre-registered values.

## 14) Timeline

Implementation & smoke: ~1–2 days. Full seeds/(k) sweeps on CPU: hours. RESULTS assembly: half-day.

## 15) References

* VDM canon on ADC/agency and metriplectic J(\oplus)M structure (EQUATIONS / CONSTANTS / SYMBOLS).
* Depth/(k)-producibility concepts adapted as classical coordination depth (device-independent spirit).
* Prior validation chapters (Lyapunov monotonicity, locality/dispersion, two-grid order) as substrate readiness checks.
