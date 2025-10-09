# PROPOSAL_Agency_Witness_v1.1.md

## 1) Title & date

**Agency Witness (Swap-Test) for Nonlocal, Predictive Control** - 2025-10-09

## 2) Proposers

Justin K. Lietz - VDM Project

## 3) Abstract

We pre-register a **device-independent agency witness** that detects **nonlocal, predictive coordination** in a metriplectic/void-dynamics agent **without** inspecting internal states. For a scalar landscape $m(\mathbf{x})$, we compare task performance on a baseline field $m_1$ to a counterfactual where the **far field** (beyond radius $r$ from the agent) is replaced by an **isospectral surrogate** $m_2$ that preserves **local statistics** at the agent position (value, gradient, curvature). Define
$$
W(r);\equiv;J_{\mathrm{real}}(r);-;J_{\mathrm{swap}}(r),
$$
where $J$ is the hit-probability of entering a registered target set $\Omega_\star$ within horizon $T$. For any **$r$-local** policy whose action depends only on features inside radius $r$, the **null prediction** is $\mathbb{E}[W(r)]=0$. A **positive witness** ($W(r)>\tau$ with pre-registered confidence) certifies **genuine nonlocal coordination**. Primary gate: $\exists,r_\star>0$ with $\operatorname{median}W(r_\star)\ge 5\sigma_{\text{null}}$, CI excluding $0$, and replication across discretizations.

## 4) Background & scientific rationale

Let $m(\mathbf{x})$ arise from an RD steady state or spectral synthesis. The agent under test, $\mathcal{P}*{\mathrm{vdm}}$, evolves under metriplectic dynamics (J$\oplus$M composition), while a **baseline local policy** $\mathcal{P}*{\mathrm{local}}$ uses only radius-$r$ features (ADC logistic on $\Delta m$ and local derivatives). We adopt a **$k$-producibility / depth** mindset from many-body certification: controllers restricted to radius $r$ are “$r$-local,” hence **invariant** to any transformation of the far field that preserves sufficient local statistics at the agent. The **swap-test** constructs exactly such counterfactuals.
**Interpretation:** $W(r)\approx 0$ for $r$-local policies; $W(r)>0$ indicates **nonlocal prediction/coordination** transported by the conservative J-branch and selected by the metric M-branch. This witness is **device-independent** with respect to inner architecture: it reasons purely from I/O under matched local cues.

## 5) Objectives & hypotheses

* **H1 (Null locality):** For the pre-registered local baseline $\mathcal{P}*{\mathrm{local}}$, $\operatorname{median}W(r)\approx 0$ for all tested $r$ (within $2\sigma*{\text{null}}$).
* **H2 (Nonlocal agency):** For $\mathcal{P}*{\mathrm{vdm}}$, $\exists,r*\star>0$ s.t. $\operatorname{median}W(r_\star)\ge 5\sigma_{\text{null}}$, 95% bootstrap CI excludes $0$, and the **lower bound** $\widehat r_{\min}$ (smallest $r$ with CI excluding $0$) replicates across discretizations within one grid step.
* **H3 (Local-feature invariance):** After conditioning on matched local value $m$, gradient $|\nabla m|$, and Laplacian $\Delta m$ at the agent location $x_0$ (and a $3\times 3$ neighborhood check), $W(r)$ remains above threshold (no leakage).
* **H4 (Monotonic onset):** On a pre-registered small-$r$ grid, $W(r)$ increases monotonically up to $r_\star$ (Spearman $\rho\ge 0.8$), then saturates.

## 6) Variables (pre-registered)

**Independent**

* **Radius** $r\in{r_1,\dots,r_K}$.
* **Landscape generator**: RD $(D,r_m,u)$ to steady state *or* spectral synthesis with fixed power spectrum.
* **Discretization**: grid $N\in{128,256}$; stencil $\in{\text{FD-3pt},\text{spectral}}$.
* **Agent parameters**: speed $v$, gain $\Gamma$, ADC slope $\Theta$; scheme $\in{\text{jmj-strang},\text{jmj-spectralDG}}$ (param-gated).
* **Horizon** $T$; seed list; tag.

**Dependent**

* **Primary metric** $J$: hit-probability for $\Omega_\star$ by time $T$ (secondary: median time-to-hit).
* **Witness** $W(r)=J_{\mathrm{real}}-J_{\mathrm{swap}}$.
* **Local-match residuals** at $x_0$: $|m|$, $|\nabla m|$, $|\Delta m|$ mismatches; small neighborhood statistic.

**Controls**

* **$\mathcal{P}_{\mathrm{local}}$**: ADC logistic with features restricted to radius $r$; no lookahead.
* **$r=0$** (“no swap”) and **near-swap** $r=r_{\text{near}}$ (well below the field correlation length).

## 7) Equipment / Hardware

CPU runs; FFT backend if spectral options are enabled. All code **additive** under `Derivation/code/physics/agency/witness/`; shared helpers only from `Derivation/code/common/`. No edits to prior experiments or results.

## 8) Methods & procedure

### 8.1 Landscape generation and far-field swap

1. Generate $m_1$ (RD steady or spectral).
2. Generate $m_2$ with identical amplitude spectrum and randomized phases.
3. Construct a **far-field swap** for radius $r$: replace the contribution of modes whose real-space influence kernel peaks outside $r$ with those from $m_2$, while preserving **local statistics** at $x_0$:

   * value: $|m_1(x_0)-m_{\text{swap}}(x_0)|\le \varepsilon_m$,
   * gradient: $|\nabla m_1(x_0)-\nabla m_{\text{swap}}(x_0)|\le \varepsilon_g$,
   * curvature proxy: $|\Delta m_1(x_0)-\Delta m_{\text{swap}}(x_0)|\le \varepsilon_\Delta$,
   * plus a $3\times 3$ neighborhood check (mean/var) within tolerances.
4. **Blinded swap control**: use another seed $\tilde m_2$ with re-matching; identical tolerances.
5. Mark trials **invalid** (excluded) if any tolerance fails; log residuals in CSV.

### 8.2 Task and rollouts

* Target set $\Omega_\star$: top-quantile (e.g., 90th) of $m$ or a registered region; horizon $T$.
* For each seed: roll out $\mathcal{P}_{\mathrm{vdm}}$ on $m_1$ and on the swapped field with identical RNG streams; compute $J$ and $W(r)$.
* Repeat for $\mathcal{P}_{\mathrm{local}}$ to validate the null ($W(r)\approx 0$).

### 8.3 Aggregation & statistics

* Use **median-of-means** across seeds for $J$ before differencing to $W(r)$ (heavy-tail robustness).
* Bootstrap 95% CIs for $\operatorname{median}W(r)$.
* **Multiple comparisons** across $r$: store adjusted CIs (BH-FDR) in sidecar CSV; gates use adjusted CIs.

### 8.4 Discretization robustness

* Repeat full sweep for $(N,\text{FD-3pt})$ and $(N,\text{spectral})$.
* Report **replication** of $\widehat r_{\min}$ (within one grid step) and **Jaccard overlap** of the significant-$r$ sets ($\ge 0.7$).

## 9) Metrics & acceptance gates

**Primary (Nonlocal agency)**

* $\exists,r_\star>0$ with
  $$
  \operatorname{median}W(r_\star)\ \ge\ 5,\sigma_{\text{null}},
  $$
  the 95% adjusted CI excludes $0$, and $\widehat r_{\min}$ replicates across discretizations (within one step).
* Significant-$r$ set overlap across discretizations: Jaccard $\ge 0.7$.

**Null and controls**

* $\mathcal{P}*{\mathrm{local}}$: for all $r$, $|\operatorname{median}W(r)|\le 2\sigma*{\text{null}}$, adjusted CIs contain $0$.
* $r=0$ and $r_{\text{near}}$: $|\operatorname{median}W(r)|\le 2\sigma_{\text{null}}$ (both policies).

**Robustness**

* Monotonic onset up to $r_\star$: Spearman $\rho\ge 0.8$.
* Local-match residuals below $(\varepsilon_m,\varepsilon_g,\varepsilon_\Delta)$ thresholds in the **local_match_residuals** CSV, else trial invalid.

**Failure plan**
Any failed gate emits `CONTRADICTION_REPORT__{tag}.json` with per-seed $W(r)$ histograms, adjusted vs unadjusted CIs, local-match residuals, ablations (different $N$, stencil), and the blinded-swap result.

## 10) Data products & artifact paths (PAPER_STANDARDS compliant)

**Domain folders**

* **Figures** → `Derivation/code/outputs/figures/agency_witness/`
* **Logs/CSVs/JSON** → `Derivation/code/outputs/logs/agency_witness/`

**Per run (all suffixed by `__{tag}`):**

* `witness_vs_radius__{tag}.png` with numeric caption (median, CI, $\widehat r_{\min}$, gates).
* `witness_vs_radius__{tag}.csv` (r, median, CI, adjusted CI, seeds).
* `witness_vs_radius__{tag}.json` (summary, $\widehat r_{\min}$, Jaccard, verdicts).
* `null_witness_vs_radius__{tag}.{png,csv,json}` for $\mathcal{P}_{\mathrm{local}}$.
* `local_match_residuals__{tag}.csv` (value/grad/Laplacian/neighbor stats and tolerances).
* `discretization_overlap__{tag}.json` (Jaccard, $\widehat r_{\min}$ replication).
* `spec_snapshot__{tag}.json` (full StepSpec).
* On fail: `failed_runs/CONTRADICTION_REPORT__{tag}.json`.

## 11) Implementation plan (additive; no edits to prior results)

**Code layout**

* `Derivation/code/physics/agency/witness/run_agency_witness.py` - CLI runner (`--spec path.json`).
* `Derivation/code/physics/agency/witness/swap_ops.py` - Fourier phase-scramble + far-field mask + local-match checks.
* Shared I/O & bootstrap from `Derivation/code/common/`.

**StepSpec (example)** - `Derivation/specs/agency/agency_witness.v1b.json`

```json
{
  "grid": {"N": 256, "L": 10.0, "stencil": "fd3"},
  "field": {"type": "rd-steady", "D": 1.0, "r": 0.2, "u": 0.25, "seed": null},
  "agent": {"scheme": "jmj-strang", "v": 0.5, "Gamma": 0.8, "Theta": 3.0},
  "task": {"target_quantile": 0.9, "T": 50.0},
  "radii": [0.5, 1.0, 1.5, 2.0, 3.0],
  "seeds": 40,
  "tolerances": {"m": 1e-6, "grad": 1e-6, "lap": 1e-6},
  "discretizations": [{"N": 256, "stencil": "fd3"}, {"N": 256, "stencil": "spectral"}],
  "fdr": {"enabled": true, "alpha": 0.05},
  "tag": "AW-v1b"
}
```

## 12) Risks & mitigations

* **Local leakage:** enforce tight local-match tolerances; mark trials invalid; log residuals.
* **Small effect size:** increase seeds, horizon $T$, or choose $r$ beyond the correlation length; reduce agent speed $v$ (quasi-static).
* **Discretization bias:** require replication of $\widehat r_{\min}$ and Jaccard $\ge 0.7$ across stencils.
* **Multiple comparisons:** store adjusted CIs (BH-FDR) and base gates on adjusted intervals.

## 13) Evidence & reproducibility

All figures have numeric captions and CSV/JSON sidecars. Specs are snapshotted. Failed gates are quarantined to `failed_runs/`. No post-hoc tuning of $r$ beyond the pre-registered set.

## 14) Timeline

Implementation & smoke: ~1 day. Full seed/radius grid on CPU: hours. RESULTS page assembly: half day.

## 15) References

* VDM canon notes on ADC and metriplectic J$\oplus$M structure (EQUATIONS/CONSTANTS/SYMBOLS).
* Many-body depth / producibility concepts (adapted here as classical coordination depth).
* Prior RD/KG validation chapters in this repo (Lyapunov, dispersion/locality, two-grid order).
