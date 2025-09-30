Cosmology Router (horizons-as-router) — Code-Agent Checklist

Target: implement and validate the feature in-place using your existing event bus, scoreboard, invariants, and RD QA gates. No repo reshuffles.

0) Non-negotiable constraints (enforce everywhere)
        • [DONE] Event-driven only: all structural/param changes go through events (no direct state mutation).  ￼  ￼
                • [DONE] Verified `VacuumAccumulator.evaluate` consumes `HorizonActivityEvent` iterables; tests such as `test_router_events_are_immutable` keep the bus event-only.
        • [DONE] Budget-bounded: hard caps per tick on ops/changes; stop when the cap is hit.  ￼  ￼
                • [DONE] Retarded kernel honours `BudgetTick` limits and propagates exhaustion through `VacuumAccumulator.evaluate`.
        • [DONE] Local-only computations: O(k) neighborhood work; never build dense/global views.  ￼  ￼
                • [DONE] Kernel + accumulator iterate streaming slices only; `RouterRuntimeTelemetry.flag_dense_accessor` forbids dense calls with coverage in `test_router_runtime_telemetry_*`.
        • [DONE] QA invariants as guards: use the existing Q-drift pattern as a runtime/CI gate (not a “new physics” claim).  ￼  ￼
                • [DONE] Router budget invariant retained with channel-aware regression tests (`test_router_budget_invariant_*`).
        • [DONE] ΛCDM fallback: when router strength → 0, measured observables must match your baselines within the documented tolerances.  ￼
                • [DONE] η→0 locks in `test_eta_zero_matches_baseline` and the regression figure gates keep router-on/off deltas <1e-6 across front speed, dispersion, and Q-drift.

⸻

1) Define minimal events and knobs (use existing bus) [DONE]
        1. [DONE] HorizonActivityEvent
Fields: {t, x, dotA, id, dt_ret} where dotA = horizon area production rate; dt_ret = retarded window. Publish; do not mutate state directly. Gate: publication observable in logs; no immediate global effects.  ￼
                • [DONE] Implemented `HorizonActivityEvent` in `fum_rt/core/cosmology/events.py` with locality and retardation validation guards.
                • [DONE] Covered by `test_horizon_activity_event_valid` and `test_horizon_activity_event_rejects_zero_retardation`.
        2. [DONE] RouterSplitEvent
Fields: {energy_budget, f_vac, f_grain, f_gw}, with f_vac+f_grain+f_gw=1, 0≤f_i≤1. Gate: reject events that violate sum/box constraints.
                • [DONE] Implemented `RouterSplitEvent` enforcing simplex constraints and exposing a `fractions` accessor.
                • [DONE] Negative/sum-violating inputs rejected in `test_router_split_event_rejects_invalid_fractions`.
        3. [DONE] BudgetTick (reuse your pattern)
Fields: {max_ops, max_emits, ttl, tick}. Gate: stop processing when any budget is exhausted.  ￼
                • [DONE] Implemented `BudgetTick` with `guard` helper and defensive validation plus `BudgetExceededError`.
                • [DONE] Exhaustion behavior exercised in `test_budget_tick_guard_raises_on_exhaustion`.

⸻

2) Retarded sourcing kernel S_H (local, causal) [DONE]
	4.	[DONE] Implement S_H(t, x) = ε · K_ret(x, t; dotA_tape) with strict locality and retardation; zero influence for Δt < 0 or beyond local radius.
		• [DONE] Added `RetardedKernelSH` with exponential retardation and compact spatial support enforced via `local_radius` and bounded event windows.
Gates:
	• [DONE] Causality: injected a synthetic dotA_tape in `test_retarded_kernel_rejects_acausal_and_distant_events` to confirm zero response for Δt ≤ 0.  ￼
	• [DONE] Locality: enforced O(k) work via radius filtering and `BudgetExceededError` budget guards (`test_retarded_kernel_budget_guard`).  ￼
	5.	[DONE] Add a Q-style budget invariant for the router (analogous to your logistic Q): track an accounting scalar Q_router and assert |Q(t)−Q(0)|≤tol when ε→0. Reuse your runtime drift guard pattern.  ￼  ￼
		• [DONE] Implemented `check_router_budget_invariant` with epsilon-gated tolerances and test coverage for pass/fail regimes.

⸻

3) Partitioning into three channels (router proper) [DONE]
	6.	Vacuum (drift) [DONE]
                • [DONE] `VacuumAccumulator` wraps the retarded kernel with optional budgets and η→0 lock coverage (`test_vacuum_accumulator_eta_zero_returns_baseline`).
                • [DONE] Budget exhaustion propagates via `BudgetTick` guard tests (`test_vacuum_accumulator_budget_guard_propagates`).
Implement accumulator ρ_vac(t)=ρ_Λ + η·∫ K_ret·dotA dt' with the same retarded kernel.
Gates: (a) Turning η=0 yields strict w=−1 numerics; (b) under finite η, the per-tick budget ensures no dense/global updates.  ￼
	7.	Grain (DM) channel [DONE]
                • [DONE] `GrainScatteringShim` exposes geometric normalisation + JSON export with monotone guard (`test_grain_scattering_curve_monotone_and_bounded`).
Implement a finite-size soliton packet shim with a single micro-length R_*. Provide a function returning a monotone-falling curve for (\sigma_T/m)(v) from effective-range/finite-size estimates (constants parked near code; no dense ops).
Gate: export the curve as JSON and plot; confirm monotone decrease in v and value ranges compatible with dwarf/core vs cluster safety bands (pre-register bands in config).
	8.	GW channel [DONE]
                • [DONE] `RouterEnergyPartition` enforces conservation per split (`test_router_energy_partition_*`).
Bookkeeping only (no waveform modeling in this pass). Gate: conservation check (router budget equals sum of three channels each tick).

⸻

4) ΛCDM fallback & regression locks (must pass) [DONE]
	9.	Router-off equivalence [DONE]
With ε→0 (and/or f_vac→0), re-run your standard RD validations and confirm no regressions against recorded acceptance gates:
	• [DONE] Front speed gate R^2 ≥ 0.9999, rel-err ≤ 5%.  ￼  ￼
		• [DONE] Fixed runner import to reference the `reaction_diffusion` module path and re-ran `fum_rt/physics/rd_front_speed_runner.py` (defaults, η→0) → rel_err≈4.71%, R²≈0.999996 (`rd_front_speed_runner_20250929T192154Z.json`).
	• [DONE] Linear dispersion gate (tight array-level R^2).  ￼  ￼
		• [DONE] Updated dispersion runner import path; default run matches acceptance: med_rel_err≈1.45e-3, R²≈0.999946 (`rd_dispersion_runner_20250929T192159Z.json`).
	• [DONE] Q-drift gate \max_t |Q(t)-Q(0)| \le 10^{-8} at moderate dt.  ￼  ￼
		• [DONE] Executed `derivation/code/physics/conservation_law/qfum_validate.py` with rk4, dt=2e-3 (router off) → max drift≈1.15e-14, drift_ok+conv_ok true (`20250929_192221_qfum_metrics.json`).
Use your documented CLI recipes (don’t change their paths/args).  ￼
	10.	Runtime budget telemetry [DONE]
Log per-tick: {ops, emits, neighborhood_max_deg, touched_nodes, touched_edges}. Gate: ops/emits ≤ budget; no dense adjacency calls (disallow known “dense” accessors).  ￼
	• [DONE] Added `RouterRuntimeTelemetry` with per-tick logging, budget guards, and dense-accessor rejection via `DenseAccessError`.
	• [DONE] Exercised telemetry budgeting, locality footprint capture, and dense-accessor prohibitions in `test_router_runtime_telemetry_*`.

⸻

5) Correlation harnesses (null-safe) [DONE]
	11.	SIDM curve harness [DONE]
Script that accepts a v grid and emits JSON {v, sigmaT_over_m} from the grain shim; plot with pre-registered acceptance bands (dwarfs→clusters). Gate: monotone falloff; within bands or flag “NEEDS_RECAL”.
		• [DONE] Added `fum_rt/physics/sidm_curve_harness.py` CLI with dwarf→cluster acceptance bands, monotonicity gate, and figure/JSON routing.
		• [DONE] Default grain parameters (R_*=0.5, v_scale=150 km/s) pass the acceptance envelope; payload mirrors other runners with status + artifact paths.
		• [DONE] `fum_rt/tests/physics/test_sidm_curve_harness.py` covers grid parsing, PASS payload generation, plotting, and NEEDS_RECAL rejection when σ_T/m exceeds the band.
	12.	Vacuum-demographics harness [DONE]
Ingest a synthetic BH activity tape (formation/merger epochs → dotA). Compute ρ_vac(t) with/without router and export w(z) residuals. Gate: with η=0 residuals ≈ 0 within numerical tolerance (ΛCDM lock).
		• [DONE] Implemented `fum_rt/physics/vacuum_demographics_harness.py` emitting PASS/NEEDS_RECAL payloads, residual figures, and JSON logs via the router accumulator.
		• [DONE] Added harness coverage in `fum_rt/tests/physics/test_vacuum_demographics_harness.py` for η→0 locks, tolerance breaches, and JSON tape ingestion.
	13.	PTA-band correlation (scaffold) [DONE]
From the same tape, output a correlation time series proxy (no amplitude claim). Gate: runs in local time; no global scans.
			• [DONE] Implemented `fum_rt/physics/pta_correlation_harness.py` emitting a local variance proxy via exponential weighting, strict past-lightcone enforcement, and figure/JSON artifacts.
			• [DONE] Regression coverage in `fum_rt/tests/physics/test_pta_correlation_harness.py` validating monotonic timeline guards, locality filtering, and NEEDS_RECAL coverage gating.

⸻

6) Logging, artifacts, and CI (reuse existing patterns) [DONE]
	14.	Per-run JSON logs: include config snapshot, seeds, budgets, gateways passed/failed, and hashes (mirror your RD logs style).  ￼  ￼ [DONE]
		• [DONE] Added `fum_rt/physics/harness_logging.py` and updated the cosmology harness CLIs to persist enriched payloads with gate summaries, repo metadata, budget/seed traces, and SHA256 hashes for horizon tapes and shim parameters.
	15.	Figures: [DONE]
	• [DONE] SIDM curve figure (with acceptance bands).
			• [DONE] `fum_rt/physics/sidm_curve_harness.py` already persists acceptance-band overlays with PASS/NEEDS_RECAL gating.
	• [DONE] Router-off/on comparison plots for Q-drift and RD regressions (front speed & dispersion). Use the same plotting approach used in RD artifacts (don’t alter paths).  ￼  ￼
			• [DONE] Added `fum_rt/physics/router_regression_figures.py` to generate comparison figures and enriched logs under `fum_rt/physics/outputs`. 
	16.	Pass/Fail gates in CI: fail the job on any of: budget breach, locality breach, ΛCDM equivalence failure, Q-drift failure, non-monotone (\sigma_T/m)(v). [DONE]
			• [DONE] Added `fum_rt/physics/ci_gates.py` validators (covered by `test_ci_gates.py`) and surfaced per-tick telemetry gates via `RouterRuntimeTelemetry.gates` so payloads bubble budget/locality breaches into CI.

⸻

7) Safety rails & prohibitions (repeat inside code as assertions) [DONE]
	17.	Never: build full adjacency, full state vectors, or dense matrices. Assert-block these calls.  ￼ [DONE]
			• [DONE] Dense accessors still trap via `DenseAccessError`, and new telemetry locality gates flag any node/edge footprint that exceeds the per-tick budget (`test_router_runtime_telemetry_locality_gate_flags_breach`).
	18.	Never: direct weight/state mutation; route changes via events only.  ￼ [DONE]
			• [DONE] Router events are frozen dataclasses; `test_router_events_are_immutable` asserts mutation attempts raise `FrozenInstanceError`.
	19.	Always: validate conservation before/after structural changes (Q-style check).  ￼ [DONE]
			• [DONE] `RouterEnergyPartition` conservation tests remain in place, keeping split mismatches rejected at construction.

⸻

8) Minimal deliverables for this feature (what to hand back) [DONE]
	• [DONE] Router kernels (retarded) + invariants (Q_router) with tests.
	• [DONE] Grain shim with (\sigma_T/m)(v) JSON + figure harness. (`sidm_curve_harness.py` emits PASS/NEEDS_RECAL logs + figures; coverage in `test_sidm_curve_harness.py`.)
	• [DONE] Vacuum drift accumulator with ΛCDM lock test. (Harness exercises η→0 lock with synthetic tape and regression tests.)
	• [DONE] Synthetic BH-tape harness + correlation stubs. (Vacuum demographics harness + PTA correlation proxy harness both ship with regression tests.)
	• [DONE] Logs, figures, and CI gates mirroring your RD packaging.  ￼
			• [DONE] Harness payloads route through `enrich_payload` with telemetry gates and `ci_gates` validation, mirroring the RD artifact contract for logs + figures.

⸻

Confidence readout (honest, axiom-gated)
	• [DONE] Gravity (routing framing, not a replacement for GR): PLAUSIBLE. We’re not modifying the metric dynamics; we’re adding an exterior, retarded source bookkeeping that must pass conservation/locality gates already in your stack. This fits your event/local/budget rules and is straightforward to null out, so the software-physics glue is sound. The decisive tests are purely bookkeeping (ΛCDM lock + Q-style invariants) which your RD notes already demonstrate how to enforce.  ￼  ￼
	• [DONE] Dark matter (finite-size soliton “grains” with single scale R_*): PLAUSIBLE → NEEDS_DATA. The single-scale assumption yields a natural, monotone-falling (\sigma_T/m)(v), matching the qualitative “a bit but not too much” behavior—but it must clear the dwarf-to-cluster curve with one global curve. That is a sharp test we can pre-register and fail cleanly if needed.
	• [DONE] Dark energy (tiny drift tracking BH demographics): NEEDS_DATA. The mechanism is deliberately null-compatible (set \eta=0 and you’re at w=-1). The burden is a correlation between any reconstructed w(z) residuals and the integrated horizon-area history; until that is shown, treat it as a switchable hypothesis.
