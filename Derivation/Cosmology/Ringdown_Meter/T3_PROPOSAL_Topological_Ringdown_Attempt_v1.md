# T3 PROPOSAL — Topological Ringdown Attempt (Topo‑RDM add‑on to DSI‑RDM) v1

Tier: T3 (Smoke)

Status: DRAFT (FROZEN) — Do not run until T2 validation completes. No phenomenon‑level runs or claims permitted (per Tier Standards).

Version: 1.0.0

Tag: dsi-topo-rdm-v1

Canonical anchors (reference-only; do not duplicate canon):

- Equations registry: Derivation/z.CANONICAL_Equations/00_EQUATIONS.md
- Symbols registry: Derivation/z.CANONICAL_Symbols/00_SYMBOLS.md
- Units normalization: Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md
- Validation metrics and gates: Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md
- Tier standards: Derivation/TIER_STANDARDS.md
- Proposal template: Derivation/Templates/PROPOSAL_PAPER_TEMPLATE.md

1) Hypothesis (H_topo_ringdown_v1)

After subtracting the dominant Kerr QNM(s) and mass-normalizing, the ringdown residuals contain loop topology in log-time scalograms, expressed as a statistically significant first Betti number β₁ across a Vietoris–Rips filtration of the ridge skeleton. Specifically, the maximum standardized Euler-rank proxy,

- β₁(ε) := E(ε) − V + C(ε),
- B1z_max := z-score of max_ε β₁(ε) against null maxima,
exceeds a decisive threshold with a contiguous band that survives multi-comparison control, while passing stringent null controls.

2) Meter and observables (from validated T2 instrument)

- Instrument: Topo‑RDM v1 (data-analysis meter, add‑on to DSI‑RDM)
  - Input: time–frequency ridge skeleton points from a log-time scalogram; or generated internally from timeseries via short-time Fourier transform and ridge picking.
  - Graph: ridge samples as nodes in (τ, f), edges by metric threshold ε (Vietoris–Rips 1‑skeleton).
  - Observable: β₁(ε) = E − V + C; null suite yields empirical distributions for p/q and z.

- Primary statistic
  - B1z_max := z-score of the observed max_ε β₁(ε) vs. the distribution of null maxima (phase-shuffled and, when supplied, Kerr-only injections).
  - Stable band length: longest contiguous run of ε where β₁ passes Benjamini–Hochberg (BH) FDR at level α and has per-ε z ≥ z_gate_primary.

- Secondary (alignment)
  - If DSI comb alignment parameters are provided, we record |ε_peak − ε_target| / ε_target and check within tol_pct (optional T2/T3 coherence).

3) Data, windows, preprocessing (preregistered)

- Events (initial set)
  - GW150914 (H1 and L1, when accessible), plus 2 additional loud O1/O2 events of comparable or higher SNR (exact list in run manifest; identical instrument settings across events).

- Channels
  - GWOSC strain: H1:GWOSC-4KHZ_R1_STRAIN, L1:GWOSC-4KHZ_R1_STRAIN (or matched R# if required by dataset availability).

- Time windows (relative to a reference t₀ near the amplitude peak/merger)
  - Two durations: W_short = 0.2 s, W_med = 0.5 s.
  - Start offsets grid (start-time sanity sweep): Δt ∈ {0.00, +0.02, −0.02} s.
  - Family of analyses per detector: 2 (durations) × 3 (offsets) = 6 windows.
  - FDR correction across the 6 windows per detector (BH, α_win = 0.05) applied to detection decisions.

- Residualization
  - Fit and subtract at least the dominant (2,2,0) Kerr damped sinusoid within the window (amplitude/phase/damping), leaving residuals for ridge extraction. When DSI‑RDM residuals are available, prefer those as input ridges_csv (no change to the meter).

- STFT and ridge skeleton (if timeseries mode is used)
  - Hann STFT: nperseg = 512, noverlap = 384.
  - Frequency cap: f_max = 1024 Hz (for GW150914-like bands).
  - Ridge picking: top_k = 5 peaks per frame above the power_quantile = 0.98 threshold.
  - τ := ln((t_c − t_ref)/T_span) computed per selected window; instrument computes ridge skeleton points (τ, f).

4) Filtration schedule and geometric scaling (preregistered)

- Points are scaled per dimension with robust percentiles (1–99%) to [0,1] before distance evaluation to avoid axis dominance.
- ε grid: num_scales = 64; base bounds set by quantiles of pairwise distances in the scaled space (qmin = 0.25, qmax = 0.75), then capped by 0.9× the MST connectivity radius to avoid trivial complete-graph degeneracy at top end.

5) Nulls and empirical statistics (preregistered)

- Phase-shuffled nulls (Null‑B): shuffle f across ridge points while preserving τ and marginal distributions; N_sim = 200 per window.
- Kerr-only ridges (Null‑A): when provided, use matched Kerr+noise ridge CSVs; appended to the null ensemble.
- Empirical p-values per ε:
  - One-sided tail against null β₁(ε) with mid‑p correction; BH FDR at α = 0.01 (per-ε testing within a window).
- z-score of maxima:
  - z_max := (max_ε β₁_obs − mean(null_max)) / sd(null_max).

6) Decision gates (pass/fail; preregistered)

- G1 (Topological signal, per detector and window family)
  - Require both:
    1) B1z_max ≥ 5.0, and
    2) stable_band_len ≥ 8 consecutive ε where (q ≤ 0.01 and per‑ε z ≥ 5.0),
  - After BH over the 6 preregistered windows (α_win = 0.05) the family-level decision is PASS if any window satisfies the above.

- G2 (Cross-detector coherence; applied only when both detectors have a G1 PASS)
  - |ε_peak(H1) − ε_peak(L1)| / ε_peak(H1) ≤ 0.05 (5%).

- G3 (Null control)
  - False-positive rate ≤ 0.05: fraction of null maxima exceeding (μ_N + 3 σ_N) must be ≤ 0.05.

- Overall PASS
  - PASS if (G1 PASS for at least one detector) and (G3 PASS) and (G2 PASS when applicable).
  - Otherwise FAIL (report as non-detection with full artifacts). No claims if any gate fails.

Notes:

- These are phenomenon-level gates (T3). The instrument-level validation was already satisfied separately (T2 meter positive-control run).

7) Artifacts and provenance (minimum set per run)

- PNG: two-panel figure (ridge skeleton and β₁(ε) with null bands and FDR mask).
- CSV: ε, β₁_obs, null_mean, null_std, p, q for the winning window; optional per-window CSVs for the family.
- JSON summary: seeds, commit hash, environment, parameterization, gate booleans (G1–G3), B1z_max, stable_band_len, p_threshold_bh, ε_at_peak, ε_target (if set), align_delta_pct, null maxima μ/σ, empirical FP rate.
- Routing and naming via io_paths helpers; failed runs routed under failed_runs/ with CONTRADICTION_REPORT JSON when applicable.
- Seeds: deterministic list [1,2,3]; record seed_used.
- Commit hash recorded from the Derivation/ tree at execution time.

8) Implementation binding (no code changes; inputs only)

- Use the existing Topo‑RDM runner and spec:
  - Runner module: Derivation/code/physics/cosmology/black_holes/topo_rdm/run_topo_rdm_v1.py
  - Spec (base): Derivation/code/physics/cosmology/black_holes/topo_rdm/specs/topo_rdm.v1.json
    - Parameters fixed as preregistered above (window durations/offsets enumerated in the run manifest).
  - For residual analyses, provide ridges_csv generated by the DSI‑RDM pipeline after QNM subtraction; otherwise pass gwpy_channel/start/end for timeseries mode (runner extracts ridges internally) and document residualization step.

- Example CLI (H1, timeseries mode; exact times chosen per window definition):
  - python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1
    --spec Derivation/code/physics/cosmology/black_holes/topo_rdm/specs/topo_rdm.v1.json
    --gwpy_channel "H1:GWOSC-4KHZ_R1_STRAIN"
    --gwpy_start <GPS_start> --gwpy_end <GPS_end>
    --tag gw150914_H1 --seed 1

- DSI residual mode (preferred when available):
  - python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1
    --spec Derivation/code/physics/cosmology/black_holes/topo_rdm/specs/topo_rdm.v1.json
    --ridges_csv path/to/dsi_residual_ridges.csv
    --tag gw150914_H1_resid --seed 1

9) Multiple-comparison control and reporting

- Within-detector window family: BH at α_win = 0.05 over the 6 predefined windows.
- Within-window per-ε testing: BH at α = 0.01 to determine kept ε and stable_band_len.
- Report:
  - The best (most significant) window per detector after family-wise control,
  - Cross-detector ε_peak proximity (G2) when both detectors pass G1,
  - Full null controls (G3) and empirical FP rate.

- If all gates fail:
  - Emit CONTRADICTION_REPORT (JSON) with gate booleans and key metrics; archive PNG/CSV/JSON under failed_runs/; log that the attempt did not detect the target topology with the preregistered settings.

10) Policy and approvals

- No runs without approvals: environment variables must indicate POLICY_APPROVED; the io layer will route any unapproved attempts to quarantine.
- This is a phenomenon attempt (T3). The underlying meter (T2) remains unchanged; any instrument modifications require separate T2 proposals/approvals.
- All outputs adhere to JSON/CSV schema discipline and naming conventions; units and dimensionless normalizations follow canon.

11) Success and interpretation

- PASS implies topological evidence for scale-recursive structure in ringdown residuals within the tested windows, subject to the cross-detector coherence and null controls.
- FAIL implies non-detection under these preregistered settings; it does not falsify the broader hypothesis outside this analysis scope. Future attempts may widen the window family, improve residualization, or analyze additional events, subject to separate preregistration.
