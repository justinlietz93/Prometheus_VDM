# VDM Tier-Graded Maturity Ladder v3 (branch‑agnostic, canon‑anchored)

**Purpose.** Track progress from idea → instrument → preregistered result → external reproduction, without freezing the theory into any single limb. Uses your repo’s A0–A7 axioms and equation anchors as the “constitution.”

> **Branch tags:** RD • KG/EFT • Agency(C‑field) • Memory/Steering • Other (open set). A work item can carry multiple tags.

- Proposals are prefixed first by their tier grade and then _PROPOSAL.
- Completed formalisms are prefixed by CF following it's sequential index number (ex. CF1_QGT_to_Metriplectic_Brackets.md).  
- New axiom candidate based proposals additionally append the axiom ID *A** between the tier grade prefix and the PROPOSAL indicator. E(Example: T8_A8_PROPOSAL_....)

- **H\**\*\_HYPOTHESIS** — Initial logical inquiry  

- **COMPLETE FORMALISM (CF\*_)** — Axiom‑anchored, closed mathematical specification: governing equations with conserved quantities and variational/metriplectic structure; discrete→continuum map with BC/IC; measurable observables and units defined; symbols/constants registered; algorithmic realizations admissible without altering the math (ready to seed T0–T9).  

## T0 — Concept seed

- Statement + motivation.
- Declare target **branch tag(s)**.
- One falsifiable consequence sketched.
- **Promotion gate to T1:** identify state, controls, observables; cite relevant axioms/equations anchors.

## T1 — Toy experimental formalization

- Minimal math/sim; link to **AXIOMS/EQUATIONS** used.
- Risks/assumptions list.
- **Gate to T2:** choose meter(s), KPIs, and QC checks; specify branch‑specific gates.

- Results: Proto‑model outcomes: minimal execution to surface risks/assumptions; meters selected for T2; no novelty claims.
- On PASS: Promote PROPOSAL T1→T2 (default). Direct T1→T3 allowed only if outcomes satisfy both T1 and T2 requirements with full artifacts; log escalation in CHRONICLES.

## T2 — **Meter (Instrument) calibrated** *(branch‑tagged)*

Calibrate instruments before claiming phenomena. Examples of **branch gates**:

- **RD**: order/convergence, dispersion curve σ(k)=r−Dk², mass/energy balances under BCs; front‑speed theory match within preset tolerance.
- **KG/EFT (wave limb)**: locality cone (finite domain of dependence), Noether energy/momentum drift ≤ tolerance; wave‑meter balance.
- **Agency (C‑field)**: budget identity (regional charge change = boundary flux − decay + sources), causal (retarded) solution check, CFL/stability gates.
- **Cross‑branch invariant** for T2 anywhere: metriplectic split degeneracy diagnostics (g₁,g₂ ≲ 10⁻¹⁰ at grid‑refined tolerance) when applicable.

- Results: Instrument calibration outcomes: meter certification under branch gates; KPIs per VALIDATION_METRICS; artifacts routed (PNG/CSV/JSON).
- On PASS: Promote PROPOSAL T2→T3 (default). Direct T2→T4 allowed only if outcomes satisfy both T2 and T3 requirements with full artifacts; log escalation in CHRONICLES.

## T3 — Smoke test (phenomenon‑adjacent)

- Small demo with the T2 meter.
- Predeclare no novelty if it’s QC‑only; pass/fail logged with margins.

- Results: Smoke‑test outcomes: small demo using the certified instrument; PASS/FAIL with margins; no novelty claims.
- On PASS: Promote PROPOSAL T3→T4 (default). Direct T3→T5 allowed only if outcomes satisfy both T3 and T4 requirements with full artifacts; log escalation in CHRONICLES.

## T4 — **Preregistered** hypothesis (protocol locked)

- Hypotheses, nulls, effect sizes, CI thresholds, analysis windows, and contradiction routing locked.

- Results: Preregistered outcomes: locked protocol; thresholds/gates evaluated; contradiction routing honored.
- On PASS: Promote PROPOSAL T4→T5 (default). Direct T4→T6 allowed only if outcomes satisfy both T4 and T5 requirements with full artifacts; log escalation in CHRONICLES.

## T5 — Pilot execution

- Narrow grid/time; verify power & CI handling.

- Results: Pilot outcomes: narrowed effect windows; CI/power verification; pipelines hardened.
- On PASS: Promote PROPOSAL T5→T6 (default). Direct T5→T7 allowed only if outcomes satisfy both T5 and T6 requirements with full artifacts; log escalation in CHRONICLES.

## T6 — Main execution

- Full prereg run; KPIs, CIs, and ablations reported.
- Example paths already sketched (RD front speed; routing KPIs; wave‑flux meter) map neatly here.

- Results: Main execution outcomes: full prereg run; KPIs, CIs, and ablations reported; artifacts reproducible.
- On PASS: Promote PROPOSAL T6→T7 (default). Direct T6→T8 allowed only if outcomes satisfy both T6 and T7 requirements with full artifacts; log escalation in CHRONICLES.

## T7 — Robustness

- Parameter sweeps, stepper variants, resolution scaling; track degradation vs meters.

- Results: Robustness outcomes: parameter sweeps, stepper variants, and resolution scaling with meter tracking.
- On PASS: Promote PROPOSAL T7→T8 (default). Direct T7→T9 allowed only if outcomes satisfy both T7 and T8 requirements with full artifacts; log escalation in CHRONICLES.

## T8 — Out‑of‑sample prediction

- Hit‑rate or quantitative error on **previously unseen** systems/datasets; for Agency, include cross‑substrate tests. (Your roadmap notes the need for boundary criteria and out‑of‑sample work.)

- Results: Out‑of‑sample outcomes: prediction/evaluation on previously unseen systems/datasets with predefined PASS/FAIL criteria.
- On PASS: Promote PROPOSAL T8→T9 (default). Direct T8→PROVEN is not permitted; external reproduction at T9 is required.

## T9 — External reproduction

- Independent team reproduces T6–T8; artifacts and prereg open.

- Invitation: Invitation to external parties to attempt to falsify the main results, targets, sweeps, scaling, and OOS results

> PASS or FAIL hinges on external parties

- On PASS: Mark status PROVEN; record external reproduction with links to artifacts and prereg; update CHRONICLES and cross‑links in PROPOSALS/RESULTS.

**Global Tier invariants (apply to all experimental tiers ≥T2; hypotheses/T0 have no gates):**

- **A0–A7 compliance** cited; measurable observables (A7); scaling groups where appropriate (A6).
- **Scope banners** (“meter testing, not phenomenon”, “no novelty claim”) and transparent gates.
