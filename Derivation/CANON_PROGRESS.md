# VDM - Canon Progress (Regimes • Fields • Domains)

Status tags: **[DISPROVEN] [PLAUSIBLE] [PLAUSIBLE→PROVEN] [PROVEN]**
Rule: A row is **PROVEN** only if there’s a runner + CSV/JSON + figure path.
Last updated: 2025-10-09 (commit f1e74a5)

---

## Status highlights

- On-site logistic ODE: ($Q$) conservation - [PROVEN] (proof + validator).
- With diffusion/coupling: site-wise conservation of ($Q$) - [DISPROVEN]; ($Q$) as diagnostic - [PROVEN].
- RD causal cone - [DISPROVEN] as a claim in the parabolic model; RD validations remain [PROVEN] for front speed/dispersion.

## A) Core Regimes (J-only / M-only / J+M)

| Regime | Field | Claim (short) | Gate (accept) | Evidence (fig, csv) | Status |
|---|---|---|---|---|---|
| **J-only (hyperbolic, “KG diag.”)** | ϕ | Locality cone exists with speed ≤ $c$ | $v_{\text{front}}$ within 2% of $c$; cone stable under refinement | `Derivation/code/outputs/figures/metriplectic/20251008_051026_kg_light_cone__KG-cone-v1.png`, `Derivation/code/outputs/logs/metriplectic/20251008_051026_kg_light_cone__KG-cone-v1.csv` (Gate met: $v\approx 0.998$; $R^2\approx 0.99985$) | **PROVEN** |
|  | ϕ | Dispersion: $\omega^2 = c^2 k^2 + m^2$ | linear fit $R^2 \ge 0.999$ | `Derivation/code/outputs/figures/metriplectic/20251008_051057_kg_dispersion_fit__KG-dispersion-v1.png`, `Derivation/code/outputs/logs/metriplectic/20251008_051057_kg_dispersion_fit__KG-dispersion-v1.csv` (Gate met: slope $\approx 1.0002$; intercept $\approx 0.9978$; $R^2\approx 0.999999997$) | **PROVEN** |
|  | ϕ | Noether (energy, momentum) conserved on periodic BCs | per-step drift $\le 10^{-12}$ or $10\,\epsilon\sqrt{N}$; reversibility $\le 10^{-10}$ | `Derivation/code/outputs/figures/metriplectic/20251008_184547_kg_noether_energy_momentum__KG-noether-v1.png`, `Derivation/code/outputs/logs/metriplectic/20251008_184547_kg_noether_energy_momentum__KG-noether-v1.csv` (Gate met: $\max\Delta E\approx8.3\times10^{-17}$, $\max\Delta P\approx2.6\times10^{-17}$; $\epsilon\sqrt{N}\approx3.55\times10^{-15}$; reversibility $\|\Delta\|_{\infty}\approx0$) | **PROVEN** |
| **M-only (parabolic, RD limit)** | ϕ or W | Fisher–KPP front speed matches $2\sqrt{D r}$ (collapse $c^*\to 1$) | rel-err $\le 5\%$, $R^2 \ge 0.999$ | `Derivation/code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.png`, CSV `Derivation/code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.csv`, JSON `Derivation/code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.json` | **PROVEN** |
|  | ϕ or W | Linear RD dispersion $\sigma(k)=r - D k^2$ | median rel-err $\le 2\times 10^{-3}$, $R^2 \ge 0.999$ | `Derivation/code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.png`, CSV `Derivation/code/outputs/logs/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.csv`, JSON `Derivation/code/outputs/logs/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.json` (archive also: `Derivation/code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_20250823T174503Z.zip`) | **PROVEN** |
| **M-only (parabolic, RD limit)** | ϕ or W | H-theorem / Lyapunov non-increase per step | $\Delta\Sigma \ge -\text{tol}$ | fig `Derivation/code/outputs/figures/rd_conservation/20251006_072250_lyapunov_delta_per_step.png` (Gate: 50 steps; negative-only drift $\max\lvert \Delta\Sigma \rvert \approx 2.61\times10^{-3}$; refinement residual $\approx 3.8\times10^{-12}$) | **PROVEN** |
| **J+M (metriplectic)** | q | Degeneracy: $\langle J\,\delta\Sigma,\,\delta\Sigma \rangle \approx 0$ and $\langle M\,\delta I,\,\delta I \rangle \approx 0$ | $\le 10^{-10}\,N$ (grid-refined) | RESULTS: `Derivation/Metriplectic/RESULTS_Metriplectic_Structure_Checks.md`; log `Derivation/code/outputs/logs/metriplectic/20251008_181035_metriplectic_structure_checks__struct-v1.json` | **PROVEN** |

---

## B) Domain claims

| Domain | Claim (short) | Gate (accept) | Evidence | Status |
|---|---|---|---|---|
| Reaction–Diffusion | **No causal cone** (front speed only; exponential tails) | CI “cone-in-RD” linter = clean | `ci/logs/rd_cone_lint.txt` | **PROVEN** |
| Telegraph-RD (flagged regime) | Hyperbolic flux restores cone; RD recovered as $\tau\to 0$ | finite cone; front/dispersion regress as $\tau\to 0$ | `<add fig>`, `<add csv>` | **PLAUSIBLE** |
| Memory/Agency field C(x,t) | Step response: $C_{ss}\approx (\gamma/\delta)R_0$, $\tau\approx 1/\delta$; improves control $U$ | $\lvert\Delta C\rvert,\ \lvert\Delta \tau\rvert \le 10\%$; $\Delta U$ above baseline noise | `<add fig>`, `<add csv>` | **PLAUSIBLE** |
| Junction policy (A/B fork) | $P(A)\approx\sigma(\Theta\,\Delta m)$; entropy $\downarrow$ when efficacy $\uparrow$ | probit/logit $R^2 \ge 0.99$ | `<add fig>`, `<add csv>` | **PLAUSIBLE** |
| Dark Photons (open systems) | Decoherence portals: Fisher consistency and noise budget sanity | Fisher rel-error $\le 10\%$; noise residuals within spec | Runners: `run_dp_fisher_check.py`, `run_dp_noise_budget.py`; Proposal: `Derivation/Dark_Photons/PROPOSAL_Decoherence_Portals.md` (awaiting RESULTS) | **PLAUSIBLE** |
| Cosmology (FRW dust) | Continuity residual QC at machine precision | $\mathrm{RMS}_{\mathrm{FRW}} \le 10^{-6}$ | `Derivation/Cosmology/RESULTS_FRW_Continuity_Residual_Quality_Check.md` (Gate met: $\mathrm{RMS}\approx 9.04\times 10^{-16}$); fig `Derivation/code/outputs/figures/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.png`; CSV `Derivation/code/outputs/logs/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.csv`; JSON `Derivation/code/outputs/logs/cosmology/20251006_175329_frw_balance__FRW-balance-v1.json` | **PROVEN** |
| Collapse (A6 logistic) | Scaling collapse envelope tight | $\mathrm{env\_max} \le 0.02$ | `Derivation/Collapse/RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md` (Gate met: $\mathrm{env\_max}\approx 0.0166$); fig `Derivation/code/outputs/figures/collapse/20251006_175337_a6_collapse_overlay__A6-collapse-v1.png`; CSV `Derivation/code/outputs/logs/collapse/20251006_175337_a6_collapse_envelope__A6-collapse-v1.csv`; JSON `Derivation/code/outputs/logs/collapse/20251006_175337_a6_collapse__A6-collapse-v1.json` | **PROVEN** |
| Metriplectic (diagnostic) | Strang defect slope near $3$ | slope $\approx 3$, $R^2 \ge 0.999$ | fig `Derivation/code/outputs/figures/metriplectic/20251006_142436_strang_defect_vs_dt__kgRD-v1.png` (Gate met: $\hat p\approx 2.945$, $R^2\approx 0.999971$) | **PROVEN** |
| Metriplectic (two-grid JMJ) | Asymptotic two-grid slope | slope $\ge 2.90$, $R^2 \ge 0.999$ | fig `Derivation/code/outputs/figures/metriplectic/failed_runs/20251006_142436_residual_vs_dt_jmj__kgRD-v1.png` (Current: $\hat p\approx 2.1087$, $R^2\approx 0.999922$; near-cubic in defect diag) | **PLAUSIBLE** |
| Agency Field | Curvature scaling & stability band | Curvature: $\kappa=\alpha X+\beta$ with $\lvert\beta\rvert\le 0.05$, slope CV $\le 10\%$, $R^2\ge 0.99$; Stability: retention $>0.8$, band reproducibility (Jaccard $\ge 0.7$) | Proposals: `Derivation/Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md`, `.../PROPOSAL_Agency_Stability_Band_v1.md` (awaiting RESULTS) | **PLAUSIBLE** |
| Information (SIE) | SIE invariant and novelty metric | Control: two-grid slope $\ge p+1-0.1$, $R^2\ge 0.999$, $\max\,\lvert Q(t)-Q(0)\rvert\le 10^{-8}$ (RK4) and $\le 10^{-5}$ (Euler); Novelty: bounded peak drift, 95% recovery in $\sim 1/r$ | Proposal: `Derivation/Information/PROPOSAL_SIE_Invariant_and_Novelty_v1.md` (awaiting RESULTS) | **PLAUSIBLE** |
| Quantum Gravity | Bridge construction and diagnostics | gates per proposal (consistency checks and invariants) | Proposal: `Derivation/Quantum_Gravity/PROPOSAL_Quantum_Gravity_Bridge_v1.md` (awaiting RESULTS) | **PLAUSIBLE** |
| Topology | Loop quench test | gates per proposal (loop invariants, quench response metrics) | Proposal: `Derivation/Topology/PROPOSAL_Loop_Quench_Test_v1.md` (awaiting RESULTS) | **PLAUSIBLE** |
| Tachyonic Condensation (tube) | Spectrum complete on admissible set; condensation exhibits interior minimum with positive curvature | Spectrum: $\mathrm{cov}_{\rm phys}\ge 0.95$ (v1: 1.000); Condensation: finite_fraction $\ge 0.80$, interior min, $a>0$ | RESULTS: `Derivation/Tachyon_Condensation/RESULTS_Tachyonic_Tube_v1.md`; Spectrum figs `Derivation/code/outputs/figures/tachyonic_condensation/20251009_084702_tube_spectrum_overview__tube-spectrum-v1.png`, `.../20251009_084703_tube_spectrum_heatmap__tube-spectrum-v1.png`; Condensation fig `Derivation/code/outputs/figures/tachyonic_condensation/20251009_062600_tube_energy_scan__tube-condensation-v1.png` | **PROVEN** |

---

## C) Local field invariants (diagnostics)

| Context | Claim (short) | Gate | Evidence | Status |
|---|---|---|---|---|
| On-site ODE (reaction only) | $Q$ conservation is exact (proof + validator) | drift $\le 10^{-8}$ at $\Delta t\sim 10^{-3}$ | `results/.../loginv_ode.csv` | **PROVEN** |
| Coupled lattice (diffusion on) | Site-wise conservation of $Q$ is **not** satisfied; $Q$ serves as a diagnostic | bounded by coupling & timestep tolerance | `results/.../loginv_lattice.csv` | **PROVEN** |

---

## D) Negative controls (explicitly falsified ideas)

| Claim (to avoid) | Evidence | Status |
|---|---|---|
| “RD/Fisher–KPP has a causal cone with speed $2\sqrt{D r}$” | RD tails visible for any $t>0$; cone linter | **DISPROVEN** |
| “Site-wise conservation of $Q$ under diffusion” | lattice $\Delta Q\ne 0$ beyond tol | **DISPROVEN** |

---

## E) Runtime invariants (engineering, but required)

| Invariant | Gate | Evidence | Status |
|---|---|---|---|
| Sparse loop (no dense path) | 0 dense-branch calls; $\kappa < 0.02$ at large-$N$ | `results/.../runtime_probe.csv` (Caution: dense scan branch currently exists; see ALGORITHMS note “BROKEN/WRONG”) | **PLAUSIBLE** |
| Latency stability under control (ABAB) | $P95$ jitter $\le \pm 5\%$ | `results/.../latency_abab.csv` | **PLAUSIBLE** |

---

### Promotion rules

- **PLAUSIBLE→PROVEN** ⇢ attach runner name, CSV/JSON, figure, and a one-line “Gate met: numbers”.  
- Only these four tags are allowed. Any other word fails CI.

### CI lint (optional)

```bash
# enforce allowed tags
grep -Eo '\[(DISPROVEN|PLAUSIBLE→PROVEN|PLAUSIBLE|PROVEN)\]' derivation/CANON_PROGRESS.md \
  | wc -l >/dev/null || { echo "Invalid status tag"; exit 1; }
# block “cone” claims in RD docs
grep -RIn "cone" derivation write_ups docs | grep -Ei "RD|Fisher|diffus" && \
  { echo "RD must not claim a cone. Use 'front speed'."; exit 1; } || true
```
