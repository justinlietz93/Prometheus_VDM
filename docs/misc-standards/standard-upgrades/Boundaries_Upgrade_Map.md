# Boundaries Upgrade Map — Nonequilibrium Grain Boundaries under Oscillating Load (VDM T2 Instrument)

Status: This standards note operationalizes the Nazarov–Murzaev (2018) GB relaxation mechanism as a VDM T2 meter with canon-aligned observables, validation gates, and artifact discipline. No equation duplication; anchors reserved below are to be registered in [Derivation/EQUATIONS.md](../Derivation/EQUATIONS.md) and referenced thereafter.

Provenance

- Extraction summary: [Nonequilibrium-grain-boundaries.md](../Derivation/References/Boundaries/Nonequilibrium-grain-boundaries.md)
- Primary PDF: [Nazarov & Murzaev (2018) Computational Materials Science](../Derivation/References/Boundaries/Nonequilibrium%20grain%20boundaries%20and%20their%20relaxation%20under%20--%20Nazarov,%20Ayrat%20A_;%20Murzaev,%20Ramil'%20T_%20--%20Computational%20Materials%20Science,%20151-pages-10_1016_j_commatsci_2018_05_015.pdf)

Canon linkage and reserved anchors (to be added)

- EQUATIONS registry (reserve IDs):
  - VDM-E-160: GB excess energy γ² law (disclination-lattice → E_ex ∝ γ²)
  - VDM-E-161: Asymmetric emission threshold rule (σ_int(γ) + p(t) triggers partial emission; net ΔE_ex < 0 over a cycle)
  - VDM-E-162: Cycle Lyapunov monotonicity for E_ex under oscillatory loading (M-limb)
  - VDM-E-163: Moiré-contrast observable definition
  - VDM-E-164: Dimensionless groups ĤE = E_ex/(G a), Π_p = p0/(G γ), ν̂ = ν
- Algorithms registry (reserve IDs):
  - VDM-A-047: GB Relaxation Meter (NI/EAM backend + elastic surrogate)
  - VDM-A-048: Moiré Contrast Index computation
  - VDM-A-049: Dislocation Emission Detector per cycle
  - VDM-A-050: Dimensionless scaling collapse procedure
- Existing canon to reference (do not duplicate): M-limb Lyapunov step [VDM-E-026](../Derivation/EQUATIONS.md#vdm-e-026) (use as the parent monotonicity principle)

Axiom alignment (VDM axioms, see [Derivation/AXIOMS.md](../Derivation/AXIOMS.md))

- A2 Local causality: EGBD networks store long-range elastic fields; emission events are local, thresholded by σ_int(γ)+p(t).
- A5 Entropy/energy monotonicity on metric limb: Per-cycle decrease of E_ex is a Lyapunov-like descent (instrumented gate).
- A6 Scale program: Report ĤE, Π_p, ν̂; enforce scaling collapse across length (a), modulus (G), and Poisson ratio (ν).

Scope and geometry (reproducibility sketch; details remain in instrument docs)

- Baseline: Four-grain columnar Ni (axis ~[112]), periodic BCs; EGBDs seeded via controlled simple shear γ applied to select grains (two relaxation protocols).
- Drive: Oscillatory uniaxial stress p(t) = p0 sin(2π t/τ), with amplitudes p0 ∈ {200, 300, 400} MPa in the reference study (MD frequency high due to timestep constraints).
- Backends:
  - MD/EAM Ni (Foiles–Baskes–Daw) for fidelity.
  - Elastic disclination-dipole-wall (DDW) surrogate for fast sweeps; both under a common interface.

Observables (registered in data-products; no equation duplication)

- E_ex: Grain-boundary excess energy per GB area (relative to equilibrium GB).
- Emission count per cycle: Number of partial dislocations emitted and absorbed asymmetrically across half-cycles.
- H_y: Sample height (proxy for densification/relaxation).
- Moiré-contrast index: Scalar from Fourier/phase analysis of Moiré overlays to quantify long-range lattice distortion.

Dimensionless groups (VDM-E-164)

- ĤE = E_ex / (G a)
- Π_p = p0 / (G γ)
- ν̂ = ν (Poisson ratio)
- Optional: normalized frequency Π_τ = τ c_s / a (if comparing across timesteps/speeds in surrogates), documented as needed without claims outside scope.

Validation gates (T2 instrument KPIs; to be registered in [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md))

- gate-gb-gamma2-law (VDM-E-160):
  - Fit E_ex = A γ² with R² ≥ 0.98.
  - On Ni baseline, |Â / 20.3 − 1| ≤ 0.20 (elastic vs MD tolerance; see provenance). Emit JSON of fit parameters and confidence bands.
- gate-gb-asym-threshold (VDM-E-161):
  - Threshold p0*= min amplitude with ≥ 50% of cycles showing ≥ 1 emission and net ΔE_ex < 0. Expect p0* ≈ 200 ± 25% MPa on the Ni geometry; pass if within band (shape validated, constants may differ in surrogates).
- gate-gb-lyapunov (VDM-E-162):
  - For p0 ≥ p0*, median per-cycle ΔE_ex < 0 and final E_ex reduced by ≥ 15% after 10 cycles (or equivalent steady-state attainment). Report cycle-wise trend with confidence intervals.
- gate-gb-protocol-insensitivity:
  - Across initialization protocols, |E_ex^(proto1) − E_ex^(proto2)| / mean ≤ 10% across γ levels.
- gate-gb-scaling-collapse (A6):
  - Plot ĤE vs γ and Π_p across sizes/materials; require an identifiable collapse band. Quantify with R² ≥ 0.98 versus a shared master curve for at least two scale factors.

Artifacts and IO routing

- Use [io_paths.py](../Derivation/code/common/io_paths.py) for all outputs. Domain: “materials/gb”.
- Required minimum per run (per VDM standards):
  - Figures (PNG):
    - fig_energy_vs_gamma2.png (E_ex vs γ², fit + CI)
    - fig_energy_vs_cycles.png (per-cycle E_ex trend with bands)
    - fig_moire_contrast.png (contrast vs γ, optional)
    - fig_threshold_detection.png (emission count vs cycle; threshold band)
    - fig_scaling_collapse.png (ĤE vs γ, Π_p collapse)
  - Logs (CSV):
    - table_thresholds.csv (estimated p0*, counts, confidence)
    - per_cycle_metrics.csv (E_ex, emission counts, H_y, Moiré index)
  - JSON:
    - runlog.json (commit, seeds, environment)
    - fit_energy_gamma2.json (A, CI, R²)
    - gates_summary.json (boolean pass/fail with metrics and bands)
- Formatting: JSON via json.dump(..., indent=2, sort_keys=True); CSV with header row (csv.DictWriter).

Implementation plan (repositories and tests)

- Instrument package location (to create): [Derivation/code/physics/materials/gb_relax_ust/](../Derivation/code/physics/materials/gb_relax_ust/)
  - Backends: md_eam.py (Ni/EAM harness); elastic_ddw.py (DDW surrogate)
  - Observables: observables.py (E_ex, Moiré index, emissions)
  - Driver: runner.py (parameter sweeps, gating, artifact writers)
  - Tests: tests/test_gb_meter.py (unit + regression against known fixtures)
- Approvals/Policy: Enforce pre-run approval and quarantine per [Derivation/code/ARCHITECTURE.md](../Derivation/code/ARCHITECTURE.md). Never use unapproved run flags.
- Results writeup: Conform to [RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md) with numeric captions and gate declarations.

Axiom-to-meter traceability

- M-limb Lyapunov: Use [VDM-E-026](../Derivation/EQUATIONS.md#vdm-e-026) for non-increase; instrument-level gate “gate-gb-lyapunov” operationalizes this in the boundary context.
- Locality (A2): Emission rules depend on σ_int(γ) and p(t) locally; instrument ensures causal locality in event detection.
- Scale program (A6): Collapse requirements translate ĤE and Π_p into a falsifiable scaling statement; failures log CONTRADICTION_REPORTs to failed_runs/.

Assumptions and limitations (risk-first)

- Frequency: MD frequencies are high vs. lab; we validate shape (γ² scaling; asymmetry rule) not absolute constants. Record Π_τ if required.
- Interatomic model dependence: A varies with potential; tolerance ±20% captures elasticity vs MD surrogacy drift.
- Protocol sensitivity: Two initialization protocols should differ ≤10%; if not, deem geometry preparation unstable and report.

Checklist (execution order)

1) Register EQUATIONS anchors VDM-E-160..164 in [Derivation/EQUATIONS.md](../Derivation/EQUATIONS.md) without duplicating formulas; point to source derivations by citation or cross-reference.
2) Add KPIs/gates to [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md) as listed above.
3) Extend algorithms in [Derivation/ALGORITHMS.md](../Derivation/ALGORITHMS.md) with VDM-A-047..050 (pseudocode only).
4) Create proposal: PROPOSAL_T2_GB_Oscillating_Load.md under [Derivation/Nonequilibrium/](../Derivation/Nonequilibrium/) from template; include prereg JSON for {γ, p0, τ}.
5) Implement instrument skeleton under [Derivation/code/physics/materials/gb_relax_ust/](../Derivation/code/physics/materials/gb_relax_ust/); wire IO and gating; add tests/fixtures.
6) Produce baseline Ni runs; publish artifacts and gates; attempt dimensionless collapse (A6).
7) If all gates pass, elevate to T3 smoke with variant geometries/materials; otherwise route to failed_runs/ with contradiction report.

Cross-links to ongoing self-organization program

- Entropy and branch diagnostics (Nicolis–Prigogine): Coordinate with anchors VDM-E-150..153 once added; this boundary meter is an M-limb instrument that can feed ExcessEntropyMonitor and BranchClassifier audits (see [prigogine_gates.py](../Derivation/code/common/instrument_helpers/prigogine_gates.py)).

Notes on documentation discipline

- Do not paste closed-form elasticity expressions into EQUATIONS.md; reference them by citation and reserve numerical targets only as gates in VALIDATION_METRICS.
- All measurable statements must map to observables above with units and thresholds; any deviations require documented tolerance bands and explicit failure routing.
