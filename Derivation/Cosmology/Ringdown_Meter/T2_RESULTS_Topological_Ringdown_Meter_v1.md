# T2 RESULTS — Topological Ringdown Meter (Topo‑RDM) v1 — Add‑on to DSI‑RDM

> Author: Justin K. Lietz
> Date: 2025-11-16
> Commit: 0f2e8ef
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.  
> Commercial use requires citation and written permission from Justin K. Lietz.
> See LICENSE file for full terms.

## Tier Grades

Tier: T2 (Instrument). This document certifies a data-analysis meter that detects loop topology in mass‑normalized ringdown residuals. No astrophysical claim is made.

Supporting lineage within this repository (referenced, not duplicated):
- Proposal (DSI‑RDM): [T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md)
- Proposal (VDM Ringdown Meter): [T2_PROPOSAL_Ringdown_Meter_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Ringdown_Meter_v1.md)
- Standards: [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md)
- Canon registries: [00_VALIDATION_METRICS.md](Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md), [00_EQUATIONS.md](Derivation/z.CANONICAL_Equations/00_EQUATIONS.md)

## Authoring Policy (Comprehensiveness)

This RESULTS document follows [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md). All claims are bounded by artifacts and gates; the numerical method is treated as the measuring instrument.

## Introduction

Question: after Kerr QNM subtraction and whitening in the DSI pipeline, do ringdown residuals exhibit scale‑robust loop topology in the time–frequency skeleton that survives strong nulls?

Significance: topology provides a metric‑free diagnostic complementary to log‑comb coherence. As a T2 instrument, Topo‑RDM only reports meter PASS/FAIL; it makes no cosmological or astrophysical claims.

Methodology: construct a ridge skeleton in log‑time τ=ln(θ/θ₀) and frequency f/ω₀, sweep a Vietoris–Rips 1‑skeleton over radii ε, compute an Euler‑rank proxy β₁(ε)≈E−V+C, and standardize its peak against null ensembles to obtain B1z.

Pinned artifact (TL;DR): [20251115_165825_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved.png](Derivation/code/outputs/figures/cosmology/20251115_165825_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved.png)

## Research question

Independent variables: filtration quantiles q_min, q_max; ε schedule length; MST cap (cap_pct); seeds; ridge‑link thresholds; window [t₀,t₁]; whiten/taper choice; QNM basis size K.

Dependent variables: B1z_max; stable_band_len (consecutive ε with FDR‑significant z); fp_rate (false‑positive rate under nulls); alignment_ok (optional DSI comb alignment).

Controls: PSD estimator; phase‑coherence threshold; ε quantile bounds; connectivity cap; RNG seeds; approval policy.

Falsifiable thresholds (gates):
- G1 (Topological signal): B1z_max ≥ z_gate_primary with FDR q ≤ 0.01 and stable_band_len ≥ 2.
- G2 (DSI alignment, optional): if alignment target ε⋆ is provided, require |ε̂_peak−ε⋆|/ε⋆ ≤ tol_pct. Enforcement controlled by alignment.require_dsi_alignment.
- G3 (Null control): null maxima threshold μ_N + z_gate_null·σ_N; require empirical false‑positive rate ≤ 0.05.

## Background Information

This instrument leverages persistent‑homology‑style loop counting on a ridge graph without claiming topological invariants of the underlying field. The relevant computation is encoded in [run_topo_rdm_v1.py](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:401) with gates at [run_topo_rdm_v1.py](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:520), [run_topo_rdm_v1.py](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:533), and [run_topo_rdm_v1.py](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:549).

Equations (dimensionless program):

β₁(ε) proxy:

$$\beta_1(\varepsilon) \approx E(\varepsilon) - V(\varepsilon) + C(\varepsilon),$$

where V, E, C are counts of vertices, edges, and connected components of the ridge graph under ε‑radius connections.

B1z score:

$$\mathrm{B1z} = \frac{\max_\varepsilon \beta_1(\varepsilon) - \mu_{\mathrm{null}}}{\sigma_{\mathrm{null}}}, \quad p\text{-values via mid-}p$$

with μ_null, σ_null the null maxima mean and standard deviation over the ensemble.

Canon discipline: for validation metrics and symbol conventions, see [00_VALIDATION_METRICS.md](Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md) and [00_SYMBOLS.md](Derivation/z.CANONICAL_Symbols/00_SYMBOLS.md).

## Variables

Independent (values used in PASS runs):
- ε quantiles: q_min=0.10, q_max=0.75; scales=64; cap_pct=0.90 (MST cap on).
- Window [t₀,t₁]=[0,8]; ω₀ reference: qnm220; K_QNM=3; taper: planck; whitener: median‑psd.
- Ridge linking: k_neighbors=2; max_gap=2; phase_coherence_min=0.6.

Dependent:
- circle_approved: B1z_max=25.95; stable_band_len=59; fp_rate=0.005.
- sweep_q10_q75_noalign: B1z_max=34.46; stable_band_len=49; fp_rate=0.01.

Controls:
- Nulls: phase‑shuffled enabled (200 sims); Kerr‑only disabled in the PASS spec but supported (see Methods).
- Alignment: require_dsi_alignment=false for PASS sweep; no ε⋆ for circle_approved.

## Equipment / Hardware

Environment (from PASS run logs): CPU x86_64; OS Linux 6.14; Python 3.13.5; NumPy 2.2.6; Matplotlib 3.10.6. Full environment is recorded in each summary JSON.

## Methods / Procedure

Reproducible pipeline:
1) Input ridges CSV ["tau","f"] exported by DSI or derived from a time‑series.
2) Pairwise distances in (τ,f) with robust per‑axis scaling; quantile‑bounded ε grid and MST connectivity cap to avoid trivial complete graphs.
3) Compute β₁(ε) curve and locate z‑significant peaks after BH‑FDR at q=0.01.
4) Generate null ensembles: phase‑shuffled ridge clouds; optionally add Kerr‑only ridge CSVs; compute null maxima distribution.
5) Apply gates G1–G3; write PNG+CSV+JSON via io_paths; route under approved or failed_runs per policy.

Software/data pointers:
- Runner: [run_topo_rdm_v1.py](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py)
  - read_ridges_csv: [python.read_ridges_csv()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:108)
  - beta1_curve: [python.beta1_curve()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:200)
  - pairwise_distances: [python.pairwise_distances()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:204)
  - mst_connectivity_radius: [python.mst_connectivity_radius()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:213)
  - null_phase_shuffled_curves: [python.null_phase_shuffled_curves()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:281)
  - pvals_from_null: [python.pvals_from_null()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:311)
  - load_spec: [python.load_spec()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:353)
  - run_topo (core + gates): [python.run_topo()](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:401)

Materials:
- Spec example (PASS sweep): [topo_rdm.sweep_q10_q75_noalign.json](Derivation/code/physics/cosmology/black_holes/topo_rdm/specs/topo_rdm.sweep_q10_q75_noalign.json)
- README (instrument details): [README.md](Derivation/code/physics/cosmology/black_holes/topo_rdm/README.md)

Security/Integrity:
- Seeds, commit hash, and environment recorded in JSON sidecars; artifacts routed per approval policy; failed gates trigger CONTRADICTION_REPORT JSONs in failed_runs/.

## Formal Derivation Writeup

The meter operates on a dimensionless program. Let τ=ln(θ/θ₀) and ω₀ a reference frequency. Construct the ridge set R={(τ_i,f_i)}. Define ε‑neighborhood graph G_ε over R. The Euler‑rank proxy uses counts (V,E,C) on G_ε. The standardized statistic is the B1z defined above; the FDR‑controlled discovery set is the set of ε with adjusted p≤q. No physical invariants beyond those in the DSI preprocessing are assumed.

## Results / Data

PASS run A (approved routing)
- Summary JSON: [circle_approved__summary.json](Derivation/code/outputs/logs/cosmology/20251115_165826_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved__summary.json)
- CSV (β₁ curve): [circle_approved__betti_curve.csv](Derivation/code/outputs/logs/cosmology/20251115_165826_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved__betti_curve.csv)
- Figure (PNG): [circle_approved.png](Derivation/code/outputs/figures/cosmology/20251115_165825_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved.png)
- Gates: G1=true; G3=true; overall_pass=true; z_max=25.95; stable_band_len=59; fp_rate=0.005; tag=dsi-topo-rdm-v1__circle_approved.

PASS run B (alignment optional)
- Summary JSON: [circle_pass_sweep_q10_q75_noalign__summary.json](Derivation/code/outputs/logs/cosmology/20251115_193433_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_sweep_q10_q75_noalign__summary.json)
- CSV (β₁ curve): [circle_pass_sweep_q10_q75_noalign__betti_curve.csv](Derivation/code/outputs/logs/cosmology/20251115_193433_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_sweep_q10_q75_noalign__betti_curve.csv)
- Figure (PNG): [circle_pass_sweep_q10_q75_noalign.png](Derivation/code/outputs/figures/cosmology/20251115_193433_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_sweep_q10_q75_noalign.png)
- Gates: G1=true; G3=true; alignment.require_dsi_alignment=false; overall_pass=true; z_max=34.46; stable_band_len=49; fp_rate=0.01.

Determinism/control run (expected FAIL on G2 when alignment required)
- Summary JSON: [circle_pass_det1_determinism_rerun__summary.json](Derivation/code/outputs/logs/cosmology/20251115_192837_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_det1_determinism_rerun__summary.json)
- CSV (β₁ curve): [circle_pass_det1_determinism_rerun__betti_curve.csv](Derivation/code/outputs/logs/cosmology/20251115_192837_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_det1_determinism_rerun__betti_curve.csv)
- Figure (PNG): [circle_pass_det1_determinism_rerun.png](Derivation/code/outputs/figures/cosmology/20251115_192837_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_det1_determinism_rerun.png)
- Gates: G1=true; G3=true; G2=false with align_delta_pct≈33.33% against ε⋆=0.12 (tol=5%); overall_pass=false by policy (alignment required).

Sample calculation (B1z):

From PASS run B, with μ_null_max=1.650, σ_null_max=0.879 and β₁_max≈(μ_null + z·σ_null) at z=34.46, the standardized peak is reported as z_max=34.46 with BH‑FDR q=0.01, satisfying G1.

Figures (numeric captions)

Figure 1 (Topo‑RDM PASS; circle_approved): z_max=25.95; stable_band_len=59; fp_rate=0.005; G1=PASS; G3=PASS; seed=[1]; commit=0f2e8ef. [PNG](Derivation/code/outputs/figures/cosmology/20251115_165825_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved.png), [CSV](Derivation/code/outputs/logs/cosmology/20251115_165826_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved__betti_curve.csv), [JSON](Derivation/code/outputs/logs/cosmology/20251115_165826_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved__summary.json).

Figure 2 (Topo‑RDM PASS; sweep_q10_q75_noalign): z_max=34.46; stable_band_len=49; fp_rate=0.01; G1=PASS; G3=PASS; alignment not enforced; seed=[1]; commit=0f2e8ef. [PNG](Derivation/code/outputs/figures/cosmology/20251115_193433_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_sweep_q10_q75_noalign.png), [CSV](Derivation/code/outputs/logs/cosmology/20251115_193433_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_sweep_q10_q75_noalign__betti_curve.csv), [JSON](Derivation/code/outputs/logs/cosmology/20251115_193433_topo_rdm_v1__dsi-topo-rdm-v1__circle_pass_sweep_q10_q75_noalign__summary.json).

## Discussion / Analysis

The instrument passes on positive controls with strong margins (z_max≫5) and low empirical false‑positive rate (≤1%), consistent with G1 and G3. Enforcement of G2 depends on alignment policy: when require_dsi_alignment=true and ε⋆ is specified, a synthetic control intentionally misaligned in ε fails overall_pass, as designed. Stability under modest filtration changes (q_min/q_max) preserves PASS; see the “sweep_q10_q75_noalign” run.

Risks and mitigations:
- Spectral leakage/aliasing: mitigated by tapering and quantile‑bounded ε; if z flips sign under ±25% window shifts, G1 must fail in future runs.
- False loops from over‑connection: controlled via MST cap and null suite; Kerr‑only nulls are supported in spec to harden controls further.
- Provenance drift: approval policy and io_paths routing ensure quarantining on policy/gate failure with CONTRADICTION_REPORTs.

## Conclusions

The Topo‑RDM instrument (v1) meets T2 standards on positive controls and under phase‑shuffled nulls. PASS runs exhibit B1z_max ≥ 25 with long stability bands and empirical FP ≤ 0.01. Alignment with DSI comb spacing is optional and governed by the require_dsi_alignment flag; when enforced on intentionally misaligned inputs, overall_pass correctly fails.

Next gates:
- Add Kerr‑only ridge CSVs to Null‑A for matched controls.
- Run additional stability sweeps (q_min∈{0.05,0.25}, q_max∈{0.60,0.90}, cap_pct∈{off,0.95}).
- I/O invariance: compare ridge clouds from time‑series vs ridge CSV exports and enforce decision consistency.
- Integrate a barcode/persistence panel in figures and include numeric captions per standards.
- Wire a --topo export in the DSI‑RDM runner to invoke this meter automatically after ridge export.

## References / Works Cited

- Canonical validation metrics: [00_VALIDATION_METRICS.md](Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)
- Canonical symbols: [00_SYMBOLS.md](Derivation/z.CANONICAL_Symbols/00_SYMBOLS.md)
- Canonical equations registry: [00_EQUATIONS.md](Derivation/z.CANONICAL_Equations/00_EQUATIONS.md)
- DSI ringdown proposal: [T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md)
- Topo‑RDM instrument README: [README.md](Derivation/code/physics/cosmology/black_holes/topo_rdm/README.md)

---

Appendix: Reproduction commands

Approved PASS (routes outside failed_runs):

[bash](Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py:0)

```bash
VDM_REQUIRE_APPROVAL=1 VDM_POLICY_APPROVED=1 MPLBACKEND=Agg \
python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1 \
  --ridges_csv Derivation/code/physics/cosmology/black_holes/topo_rdm/testdata/ridges_circle_pass.csv \
  --tag circle_approved --seed 1
```

PASS sweep (no alignment requirement):

```bash
MPLBACKEND=Agg python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1 \
  --spec Derivation/code/physics/cosmology/black_holes/topo_rdm/specs/topo_rdm.sweep_q10_q75_noalign.json \
  --tag circle_pass_sweep_q10_q75_noalign --seed 1
```

Determinism/control (alignment enforced → expected overall FAIL):

```bash
MPLBACKEND=Agg python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1 \
  --spec Derivation/code/physics/cosmology/black_holes/topo_rdm/specs/topo_rdm.v1.json \
  --tag circle_pass_det1_determinism_rerun --seed 1
```

Provenance:
- Artifacts share basenames across PNG/CSV/JSON; seeds and commit recorded in JSON; routing follows approval policy via [io_paths.py](Derivation/code/common/io_paths.py).

End of document.