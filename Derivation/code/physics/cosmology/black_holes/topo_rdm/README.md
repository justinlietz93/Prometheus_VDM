# Topological Ringdown Meter (Topo‑RDM) v1 — T2 add‑on to DSI‑RDM

Scope (T2 instrument; no claims)

- Purpose: quantify loop topology in mass‑normalized ringdown residuals by constructing a time–frequency ridge skeleton, sweeping a Vietoris–Rips 1‑skeleton over filtration radii ε, computing the Euler‑rank proxy β₁(ε) = E − V + C, and standardizing the maximum against nulls to produce B1z.
- Position: add‑on diagnostic for the DSI Ringdown Meter. It does not alter the DSI steps; it consumes ridge points exported by DSI (or derives them from raw time‑series, minimally).
- Canon anchors (reference only; do not duplicate canon):
  - Validation metrics: [00_VALIDATION_METRICS.md](../../../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)
  - Equations registry: [00_EQUATIONS.md](../../../z.CANONICAL_Equations/00_EQUATIONS.md)
  - DSI proposal: Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md

What this meter is for

- It is a gated diagnostic that answers: “Do the ringdown residuals contain genuine loop structure across scales that survives strong nulls?” It is not a discovery claim; it is a meter that either passes (topology detected with discipline) or fails (no disciplined topology).
- Use it to corroborate DSI comb structure and to rule out spurious patterns via nulls.

Key implementation entry points

- Runner: [run_topo_rdm_v1.py](./run_topo_rdm_v1.py)
  - Robust import/bootstrap: [python.sys.path setup](./run_topo_rdm_v1.py:52)
  - Ridge CSV ingestion: [python.read_ridges_csv()](./run_topo_rdm_v1.py:108)
  - Pairwise distances: [python.pairwise_distances()](./run_topo_rdm_v1.py:204)
  - MST connectivity cap helper: [python.mst_connectivity_radius()](./run_topo_rdm_v1.py:213)
  - β₁ curve: [python.beta1_curve()](./run_topo_rdm_v1.py:200)
  - Null generation (phase‑shuffled): [python.null_phase_shuffled_curves()](./run_topo_rdm_v1.py:281)
  - Mid‑p corrected p‑values: [python.pvals_from_null()](./run_topo_rdm_v1.py:311)
  - Spec defaults (quantile‑bounded ε): [python.load_spec()](./run_topo_rdm_v1.py:353)
  - Core analysis/gates/artifacts: [python.run_topo()](./run_topo_rdm_v1.py:401)

Inputs

- Preferred: ridge CSV with columns ["tau","f"] or ["tau","freq"] exported by DSI.
- Optional: time‑series CSV ["t","strain"] or ["time","h"] (Topo‑RDM can derive a minimal ridge skeleton; helper at [python.ridge_points_from_timeseries()](../../../../common/instrument_helpers/topo_rdm_timeseries.py:120)).

Outputs and routing (io_paths policy)

- PNG figure + CSV curve + JSON summary are always written via canonical routers:
  - Figures: [python.figure_path()](../../../../common/io_paths.py:86)
  - Logs (CSV/JSON): [python.log_path()](../../../../common/io_paths.py:122), [python.write_log()](../../../../common/io_paths.py:137)
- Approval/quarantine policy:
  - If VDM_REQUIRE_APPROVAL=1 and VDM_POLICY_APPROVED≠1, artifacts are auto‑routed under code/outputs/.../failed_runs/, regardless of gates.
  - When approved (VDM_POLICY_APPROVED=1) and gates pass, artifacts route to the main domain directory.
- This is why you may see “failures” recorded in failed_runs/ while a later, distinct run shows “overall_pass=true” outside failed_runs/. Each run is independent and tagged in its filename.

Gates (pass/fail)

- G1 (Topological signal): B1z_max ≥ z_gate_primary at ε that also survive FDR (q ≤ fdr_q) with a small stability requirement (≥ 2 consecutive ε). Implemented in [python.run_topo()](./run_topo_rdm_v1.py:520).
- G2 (DSI alignment, optional): if an alignment target is provided (eps_target or mapping from ΔΩ), require the z‑peak ε within tolerance; enforcement is governed by alignment.require_dsi_alignment (default true). Implemented at [python.run_topo()](./run_topo_rdm_v1.py:549).
- G3 (Null control): empirical false‑positive rate ≤ 0.05 from null maxima using threshold μ_N + z_gate_null·σ_N on the null maxima distribution. Implemented at [python.run_topo()](./run_topo_rdm_v1.py:533).
- Overall routing decision: overall_pass = G1 and G3 and alignment_ok, where alignment_ok = (not require_dsi_alignment) or (no alignment target) or G2. See [python.run_topo()](./run_topo_rdm_v1.py:650).

Nulls (strong controls)

- Null‑B: phase‑shuffled ridge skeleton (destroys τ–f correlation; preserves marginals). [python.null_phase_shuffled_curves()](./run_topo_rdm_v1.py:281)
- Null‑A: Kerr‑only ridge CSVs can be supplied in spec.parameters.nulls.kerr_only_ridges (array of paths). [python.run_topo() stacking](./run_topo_rdm_v1.py:460)
- P‑values use a mid‑p correction to handle ties in degenerate null ensembles. [python.pvals_from_null()](./run_topo_rdm_v1.py:311)

Filtration policy (ε schedule)

- Default ε bounds are quantile‑bounded by the empirical pairwise distance distribution to avoid trivial complete‑graph degeneracy on toy inputs. [python.load_spec() defaults](./run_topo_rdm_v1.py:353), applied in [python.run_topo()](./run_topo_rdm_v1.py:422).
- Single‑linkage connectivity cap keeps ε_max below the MST connectivity threshold (configurable cap_pct). [python.mst_connectivity_radius()](./run_topo_rdm_v1.py:213), cap at [python.run_topo()](./run_topo_rdm_v1.py:431)

How to run

- From a ridge CSV:
  - Unapproved (quarantine by default):
    - MPLBACKEND=Agg python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1 --ridges_csv Derivation/code/physics/cosmology/black_holes/topo_rdm/testdata/ridges_smoke.csv --tag smoke --seed 1
  - Approved routing:
    - VDM_REQUIRE_APPROVAL=1 VDM_POLICY_APPROVED=1 MPLBACKEND=Agg python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1 --ridges_csv Derivation/code/physics/cosmology/black_holes/topo_rdm/testdata/ridges_circle_pass.csv --tag circle_approved --seed 1
- From a spec file:
  - MPLBACKEND=Agg python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1 --spec Derivation/code/physics/cosmology/black_holes/topo_rdm/specs/topo_rdm.smoke.json --tag smoke_spec --seed 1

Interpreting “passes” vs “failures” in logs

- Each invocation writes its own artifacts, stamped with a timestamp and tag in the filename.
- “Failures in the logs” refers to earlier runs that either:
  - failed gates (overall_pass=false) and thus routed under failed_runs/, or
  - were unapproved (VDM_POLICY_APPROVED≠1) and thus routed under failed_runs/ per policy, regardless of gates.
- A later, distinct run can legitimately “pass” (overall_pass=true) and route to the main directory, even while previous failed_runs/ remain for audit.
- To check any run, open its summary JSON and read gates.overall_pass. Examples:
  - PASS (approved): [topo_rdm_v1__dsi-topo-rdm-v1__circle_approved__summary.json](../../../../outputs/logs/cosmology/20251115_165826_topo_rdm_v1__dsi-topo-rdm-v1__circle_approved__summary.json)
  - FAIL (quarantined): see files under ../../../../outputs/logs/cosmology/failed_runs/

What changed to harden this meter

- Robust import path so it runs as a module: [python.sys.path bootstrap](./run_topo_rdm_v1.py:52)
- Adaptive ε bounds + MST cap to avoid complete‑graph trivialities on tiny inputs: [python.run_topo()](./run_topo_rdm_v1.py:422)
- Mid‑p p‑values for ties in degenerate null ensembles: [python.pvals_from_null()](./run_topo_rdm_v1.py:311)

Edge cases to be aware of

- Very small N ridge sets can produce degenerate null maxima with σ ≈ 0; mid‑p handles p, but z_max may be uninformative. Use richer DSI ridge exports for real events.
- Alignment gate (G2) contributes to overall_pass only when an alignment target is provided (eps_target or ΔΩ→ε via eps_scale) and alignment.require_dsi_alignment=true; otherwise it is informative only.

Next steps (project wiring)

- DSI integration: add --topo export in the DSI‑RDM runner to write ridge CSVs and invoke Topo‑RDM with consistent tags.
- Null‑A: include Kerr‑only ridge CSVs in spec.parameters.nulls.kerr_only_ridges for stronger null suites matched to fit/SNR/PSD.
- If desired, enable connectivity_cap=true with cap_pct≈0.95 for real data in the spec.

Contact points (code)

- Plotting helper (saves via io_paths): [python.plot_topo_rdm_panel()](../../../../common/plotting/topo_rdm_plots.py:28)
- Time‑series ridge extractor (optional): [python.ridge_points_from_timeseries()](../../../../common/instrument_helpers/topo_rdm_timeseries.py:120)

# Deterministic preprocessing pipeline (T2 support)

Purpose (Derived‑limit for instrument hygiene)

- Provide a deterministic, documented preprocessing stage that converts calibrated strain h(t) into a whitened, band‑passed series, optionally emitting a ridge sketch, so the Topo‑RDM can measure β₁ persistence during ringdown without toy generators.

Implementation

- Script: [preprocess_ringdown.py](../../../instruments/preprocess_ringdown.py:1)
  - Window: [t₀−ΔT_pre, t₀+ΔT_post] around merger (t₀ is peak amplitude if avoiding priors)
  - Detrend + mean‑remove on the selected window
  - PSD (Welch) from pre‑merger only; whiten via |H|/√Sₙ with floor ε for lines
  - Zero‑phase linear FIR band‑pass (default 25–512 Hz) to avoid phase warping
  - Optional line notching only if required by passband hygiene (first pass avoids heavy notching)
  - Downsample post‑filter (default 2048 Hz) with Nyquist safety
  - Outputs:
    - “_pre.csv”: two columns “t,h” (seconds, whitened+band‑passed strain)
    - “_pre.json”: parameters + diagnostics receipts (whiteness, band safety, SNR)
    - “_ridges.csv” (optional): STFT ridge maxima (t,f,amp) for drop‑in use

Why this matters for β₁

- The 1‑cycle in H₁ persists only when the decaying sinusoid is isolated and whitened; mixing inspiral or colored noise shortens or hides the loop. Preprocessing is an instrument dial, not a theory dial.

Gates (preprocess receipts)

- whiten_ok: max |ρ(τ)| (τ≠0, up to 1 s) ≤ 0.10 (JSON field “diagnostics.whiten_ok”)
- band_ok: requested [f_lo,f_hi] within [2/T, fs/2] (JSON field “diagnostics.band_ok”)
- snr_ringdown: RMS_post / σ_pre reported as “diagnostics.snr_ringdown” (set floors in spec/policy)
- On failure, a CONTRADICTION_REPORT is written alongside outputs (no silent drop).

How to run (either form works)

- As module (namespace package; preferred when PYTHONPATH includes repo root):

```bash
python3 -m Derivation.code.instruments.preprocess_ringdown \
  --in_csv data/gw150914_H1.csv \
  --out_root outputs/gw150914_H1 \
  --fs 4096 --t0 1126259462.423 \
  --t_pre 2.5 --t_post 2.5 \
  --f_lo 25 --f_hi 512 \
  --psd_seg 1.0 --psd_olap 0.5 \
  --down_fs 2048 \
  --emit_ridges
```

- As script path:

```bash
python3 Derivation/code/instruments/preprocess_ringdown.py \
  --in_csv data/gw150914_H1.csv \
  --out_root outputs/gw150914_H1 \
  --fs 4096 --t0 1126259462.423 \
  --t_pre 2.5 --t_post 2.5 \
  --f_lo 25 --f_hi 512 \
  --psd_seg 1.0 --psd_olap 0.5 \
  --down_fs 2048 \
  --emit_ridges
```

Integrating with Topo‑RDM (no code changes)

- Preferred (ridgelines): run the preprocessor with “--emit_ridges” and feed the emitted ridges directly:

```bash
# Approved routing (set both env vars)
VDM_REQUIRE_APPROVAL=1 VDM_POLICY_APPROVED=1 MPLBACKEND=Agg \
python3 -m Derivation.code.physics.cosmology.black_holes.topo_rdm.run_topo_rdm_v1 \
  --ridges_csv outputs/gw150914_H1_ridges.csv \
  --tag gw150914_H1_pre --seed 1
```

- Alternative (timeseries CSV): you may also pass the “*_pre.csv” time‑series to the runner (which will derive ridges internally). If using this path, ensure the CLI flag for timeseries is enabled in your invocation or supply it via spec. Ridge derivation uses [python.ridge_points_from_timeseries()](../../../../common/instrument_helpers/topo_rdm_timeseries.py:120) with STFT settings declared in the spec.

Receipts expected in logs

- Preprocess JSON: whiten_ok, band_ok, snr_ringdown with the exact parameters used
- Topo‑RDM summary JSON/gates created by [python.run_topo()](./run_topo_rdm_v1.py:401)
  - G1 topological signal (see [python.run_topo()](./run_topo_rdm_v1.py:520))
  - G3 null control (see [python.run_topo()](./run_topo_rdm_v1.py:533))
  - Optional G2 alignment (see [python.run_topo()](./run_topo_rdm_v1.py:549))

Diagnosis of common “instrument PASS, signal FAIL” cases

- Insufficient whitening (colored noise) ⇒ short H₁ lifetime → check whiten_ok
- Window mixes inspiral + ringdown ⇒ diffuse ridges → refit [t_pre,t_post]
- Band too wide or narrow ⇒ ridges blur or truncate the (2,2,0) power → adjust [f_lo,f_hi]
- ε ladder too coarse ⇒ loops merge or vanish → increase num_scales and keep MST cap

Promotion to RESULTS / PROPOSAL

- Results doc linking this preprocessing: [T2_RESULTS_Topological_Ringdown_Meter_v1.md](../../../../Cosmology/Ringdown_Meter/T2_RESULTS_Topological_Ringdown_Meter_v1.md)
- Update the DSI/Topo‑RDM T2 PROPOSAL to declare this pipeline and its receipts; pin PNG+CSV+JSON as per [RESULTS_PAPER_STANDARDS.md](../../../../Templates/RESULTS_PAPER_STANDARDS.md)

References (clickable code)

- Preprocessor: [preprocess_ringdown.py](../../../instruments/preprocess_ringdown.py:1)
- Runner: [run_topo_rdm_v1.py](./run_topo_rdm_v1.py:0)
- Ridge extractor helper: [python.ridge_points_from_timeseries()](../../../../common/instrument_helpers/topo_rdm_timeseries.py:120)
