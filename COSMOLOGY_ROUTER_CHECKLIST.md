Cosmology Router (horizons-as-router) — Code-Agent Checklist

Target: implement and validate the feature in-place using your existing event bus, scoreboard, invariants, and RD QA gates. No repo reshuffles.

0) Non-negotiable constraints (enforce everywhere)
	•	Event-driven only: all structural/param changes go through events (no direct state mutation).  ￼  ￼
	•	Budget-bounded: hard caps per tick on ops/changes; stop when the cap is hit.  ￼  ￼
	•	Local-only computations: O(k) neighborhood work; never build dense/global views.  ￼  ￼
	•	QA invariants as guards: use the existing Q-drift pattern as a runtime/CI gate (not a “new physics” claim).  ￼  ￼
	•	ΛCDM fallback: when router strength → 0, measured observables must match your baselines within the documented tolerances.  ￼

⸻

1) Define minimal events and knobs (use existing bus)
	1.	HorizonActivityEvent
Fields: {t, x, dotA, id, dt_ret} where dotA = horizon area production rate; dt_ret = retarded window. Publish; do not mutate state directly. Gate: publication observable in logs; no immediate global effects.  ￼
	2.	RouterSplitEvent
Fields: {energy_budget, f_vac, f_grain, f_gw}, with f_vac+f_grain+f_gw=1, 0≤f_i≤1. Gate: reject events that violate sum/box constraints.
	3.	BudgetTick (reuse your pattern)
Fields: {max_ops, max_emits, ttl, tick}. Gate: stop processing when any budget is exhausted.  ￼

⸻

2) Retarded sourcing kernel S_H (local, causal)
	4.	Implement S_H(t, x) = ε · K_ret(x, t; dotA_tape) with strict locality and retardation; zero influence for Δt < 0 or beyond local radius.
Gates:
	•	Causality: inject a synthetic dotA_tape and prove no events before their causes.
	•	Locality: bound per-tick touched nodes/edges; verify O(k) neighborhood work.  ￼
	5.	Add a Q-style budget invariant for the router (analogous to your logistic Q): track an accounting scalar Q_router and assert |Q(t)−Q(0)|≤tol when ε→0. Reuse your runtime drift guard pattern.  ￼  ￼

⸻

3) Partitioning into three channels (router proper)
	6.	Vacuum (drift)
Implement accumulator ρ_vac(t)=ρ_Λ + η·∫ K_ret·dotA dt' with the same retarded kernel.
Gates: (a) Turning η=0 yields strict w=−1 numerics; (b) under finite η, the per-tick budget ensures no dense/global updates.  ￼
	7.	Grain (DM) channel
Implement a finite-size soliton packet shim with a single micro-length R_*. Provide a function returning a monotone-falling curve for (\sigma_T/m)(v) from effective-range/finite-size estimates (constants parked near code; no dense ops).
Gate: export the curve as JSON and plot; confirm monotone decrease in v and value ranges compatible with dwarf/core vs cluster safety bands (pre-register bands in config).
	8.	GW channel
Bookkeeping only (no waveform modeling in this pass). Gate: conservation check (router budget equals sum of three channels each tick).

⸻

4) ΛCDM fallback & regression locks (must pass)
	9.	Router-off equivalence
With ε→0 (and/or f_vac→0), re-run your standard RD validations and confirm no regressions against recorded acceptance gates:
	•	Front speed gate R^2 ≥ 0.9999, rel-err ≤ 5%.  ￼  ￼
	•	Linear dispersion gate (tight array-level R^2).  ￼  ￼
	•	Q-drift gate \max_t |Q(t)-Q(0)| \le 10^{-8} at moderate dt.  ￼  ￼
Use your documented CLI recipes (don’t change their paths/args).  ￼
	10.	Runtime budget telemetry
Log per-tick: {ops, emits, neighborhood_max_deg, touched_nodes, touched_edges}. Gate: ops/emits ≤ budget; no dense adjacency calls (disallow known “dense” accessors).  ￼

⸻

5) Correlation harnesses (null-safe)
	11.	SIDM curve harness
Script that accepts a v grid and emits JSON {v, sigmaT_over_m} from the grain shim; plot with pre-registered acceptance bands (dwarfs→clusters). Gate: monotone falloff; within bands or flag “NEEDS_RECAL”.
	12.	Vacuum-demographics harness
Ingest a synthetic BH activity tape (formation/merger epochs → dotA). Compute ρ_vac(t) with/without router and export w(z) residuals. Gate: with η=0 residuals ≈ 0 within numerical tolerance (ΛCDM lock).
	13.	PTA-band correlation (scaffold)
From the same tape, output a correlation time series proxy (no amplitude claim). Gate: runs in local time; no global scans.

⸻

6) Logging, artifacts, and CI (reuse existing patterns)
	14.	Per-run JSON logs: include config snapshot, seeds, budgets, gateways passed/failed, and hashes (mirror your RD logs style).  ￼  ￼
	15.	Figures:
	•	SIDM curve figure (with acceptance bands).
	•	Router-off/on comparison plots for Q-drift and RD regressions (front speed & dispersion). Use the same plotting approach used in RD artifacts (don’t alter paths).  ￼  ￼
	16.	Pass/Fail gates in CI: fail the job on any of: budget breach, locality breach, ΛCDM equivalence failure, Q-drift failure, non-monotone (\sigma_T/m)(v).

⸻

7) Safety rails & prohibitions (repeat inside code as assertions)
	17.	Never: build full adjacency, full state vectors, or dense matrices. Assert-block these calls.  ￼
	18.	Never: direct weight/state mutation; route changes via events only.  ￼
	19.	Always: validate conservation before/after structural changes (Q-style check).  ￼

⸻

8) Minimal deliverables for this feature (what to hand back)
	•	Router kernels (retarded) + invariants (Q_router) with tests.
	•	Grain shim with (\sigma_T/m)(v) JSON + figure.
	•	Vacuum drift accumulator with ΛCDM lock test.
	•	Synthetic BH-tape harness + correlation stubs.
	•	Logs, figures, and CI gates mirroring your RD packaging.  ￼

⸻

Confidence readout (honest, axiom-gated)
	•	Gravity (routing framing, not a replacement for GR): PLAUSIBLE. We’re not modifying the metric dynamics; we’re adding an exterior, retarded source bookkeeping that must pass conservation/locality gates already in your stack. This fits your event/local/budget rules and is straightforward to null out, so the software-physics glue is sound. The decisive tests are purely bookkeeping (ΛCDM lock + Q-style invariants) which your RD notes already demonstrate how to enforce.  ￼  ￼
	•	Dark matter (finite-size soliton “grains” with single scale R_*): PLAUSIBLE → NEEDS_DATA. The single-scale assumption yields a natural, monotone-falling (\sigma_T/m)(v), matching the qualitative “a bit but not too much” behavior—but it must clear the dwarf-to-cluster curve with one global curve. That is a sharp test we can pre-register and fail cleanly if needed.
	•	Dark energy (tiny drift tracking BH demographics): NEEDS_DATA. The mechanism is deliberately null-compatible (set \eta=0 and you’re at w=-1). The burden is a correlation between any reconstructed w(z) residuals and the integrated horizon-area history; until that is shown, treat it as a switchable hypothesis.