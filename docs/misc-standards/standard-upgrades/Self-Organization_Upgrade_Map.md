# Self-Organization Upgrade Map (Nicolis–Prigogine → VDM)

Status: Adopted as meter stack (T2 instruments). No equations duplicated here; link to canon anchors and KPIs.

Sources

- Primary reference note: Derivation/References/Nonequilibrium_&_Entropy/self-organization.md
- Book (for human readers): Derivation/References/Nonequilibrium_&_Entropy/Self-organization in nonequilibrium systems _ from -- Nicolis, Gregoire, Prigogine, Ilya -- First Edition, 1977 -- John Wiley & Sons, Incorporated.pdf

Canon anchors (definitions)

- Excess entropy production (EEP, near steady): [VDM-E-150](../../Derivation/EQUATIONS.md#vdm-e-150)
- Open-system entropy balance (volume vs boundary flux): [VDM-E-151](../../Derivation/EQUATIONS.md#vdm-e-151)
- Leading-eigenvalue classification (steady/Hopf, βc): [VDM-E-152](../../Derivation/EQUATIONS.md#vdm-e-152)
- Local-potential Lyapunov (patterned steady states): [VDM-E-153](../../Derivation/EQUATIONS.md#vdm-e-153)

KPIs and artifacts

- EEP trend gate: [kpi-eep-trend](../../Derivation/VALIDATION_METRICS.md#kpi-eep-trend)
  - Artifacts: EEP time series PNG + CSV (t, eep, de_dt) + JSON gate summary
- Bifurcation card: [kpi-bifurcation-card](../../Derivation/VALIDATION_METRICS.md#kpi-bifurcation-card)
  - Artifacts: per-control JSON (control, Re(λ₁), Im(λ₁), branch, eigenmode_path?)
- Branch classifier (consistency): [kpi-branch-classifier](../../Derivation/VALIDATION_METRICS.md#kpi-branch-classifier)
- Localized structure detector: [kpi-localized-structure](../../Derivation/VALIDATION_METRICS.md#kpi-localized-structure)
  - Artifacts: overlay PNG + JSON with component measures
- Branch stability overlay: [kpi-branch-stability-plot](../../Derivation/VALIDATION_METRICS.md#kpi-branch-stability-plot)
  - Artifacts: overlay PNG; optional CSV/JSON inputs

Instrument implementations (helpers)

- EEP monitor: ExcessEntropyMonitor in prigogine_gates.py
- Bifurcation card: write_bifurcation_card in prigogine_gates.py
- Localized detector: detect_localized_structures and write_localized_artifacts in prigogine_gates.py
- Branch classifier: classify_branch in prigogine_gates.py
- Branch stability overlay: branch_stability_plot in prigogine_gates.py

Pseudocode entries (execution flows)

- EEP gate: VDM-A-043
- Bifurcation card: VDM-A-044
- Localized detector: VDM-A-045
- Branch stability overlay: VDM-A-046
See: Derivation/ALGORITHMS.md

Results standards (authoring requirements)

- Self-organization audits section specifies required artifacts/gates for any pattern-onset claims (EEP, bifurcation card+branch classifier, localized detector, stability overlay)
See: Derivation/Templates/RESULTS_PAPER_STANDARDS.md

Operational notes (no duplication, usage only)

- Near-equilibrium EEP criterion (d/dt δpσ^(e) ≤ 0) is enforced as a trend gate with tolerance; baseline σ⋆ must be computed at the same boundary conditions as the reference state. Thresholds: VALIDATION_METRICS.md
- Open-system entropy balance decomposes dS/dt into production vs boundary entropy flux (e.g., heat term) with outward normal convention; use this to annotate branch transitions in overlays.
- Leading-eigenvalue classification determines steady vs Hopf onset and logs null eigenmode shape (if available) for sanity checks vs domain size/BCs.
- Local-potential Lyapunov proxy distinguishes convergence to non-uniform steady states (Φ plateau with Re(λ₁) ≲ 0) from transient noise.

Integration guidance

- Runners should:
  1) Initialize ExcessEntropyMonitor with σ⋆ and log EEP over the sweep.
  2) Compute the leading eigenvalue (and eigenmode if feasible) across control values; emit bifurcation cards.
  3) Produce localized detector overlays at selected controls/time slices for quantitative morphology.
  4) Emit branch stability overlay with control vs Re(λ₁) and optional EEP trend/boundary entropy flux.
- Artifacts must be written via common/io_paths.py; filenames share basenames across PNG/CSV/JSON and include commit hash and seeds as per RESULTS standards.

Mapping table (concept → VDM artifacts)

- EEP stability (Nicolis–Prigogine Part I, Ch. 3–4) → [VDM-E-150](../../Derivation/EQUATIONS.md#vdm-e-150), [kpi-eep-trend](../../Derivation/VALIDATION_METRICS.md#kpi-eep-trend), ExcessEntropyMonitor
- Open-system entropy accounting (Part I, Ch. 1–2) → [VDM-E-151](../../Derivation/EQUATIONS.md#vdm-e-151), boundary flux overlay in branch plots
- Deterministic stability and RD bifurcation (Part II, Ch. 5–7) → [VDM-E-152](../../Derivation/EQUATIONS.md#vdm-e-152), [kpi-bifurcation-card](../../Derivation/VALIDATION_METRICS.md#kpi-bifurcation-card), [kpi-branch-classifier](../../Derivation/VALIDATION_METRICS.md#kpi-branch-classifier)
- Local potentials and order/dissipation (Part V/Ch. 8) → [VDM-E-153](../../Derivation/EQUATIONS.md#vdm-e-153), [kpi-phi-conduction-monotone](../../Derivation/VALIDATION_METRICS.md#kpi-phi-conduction-monotone) when applicable

Scope boundary

- This map is reference-only and does not restate equations or thresholds; those live in EQUATIONS.md and VALIDATION_METRICS.md, respectively. Implementations are in code helpers; derivations remain in the canonical docs.

Change log

- 2025-11-08: Initial creation aligning self-organization meters to VDM canon and KPIs.
