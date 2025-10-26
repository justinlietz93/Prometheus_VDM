# Tier Standards v2 (branch‑agnostic, canon‑anchored)

**Purpose.** Track progress from idea → instrument → preregistered result → external reproduction, without freezing the theory into any single limb. Uses your repo’s A0–A7 axioms and equation anchors as the “constitution.”

> **Branch tags:** RD • KG/EFT • Agency(C‑field) • Memory/Steering • Other (open set). A work item can carry multiple tags.

## T0 — Concept seed

* Statement + motivation.
* Declare target **branch tag(s)**.
* One falsifiable consequence sketched.
* **Promotion gate to T1:** identify state, controls, observables; cite relevant axioms/equations anchors.

## T1 — Toy formalization

* Minimal math/sim; link to **AXIOMS/EQUATIONS** used.
* Risks/assumptions list.
* **Gate to T2:** choose meter(s), KPIs, and QC checks; specify branch‑specific gates.

## T2 — **Meter (Instrument) calibrated** *(branch‑tagged)*

Calibrate instruments before claiming phenomena. Examples of **branch gates**:

* **RD**: order/convergence, dispersion curve σ(k)=r−Dk², mass/energy balances under BCs; front‑speed theory match within preset tolerance.
* **KG/EFT (wave limb)**: locality cone (finite domain of dependence), Noether energy/momentum drift ≤ tolerance; wave‑meter balance.
* **Agency (C‑field)**: budget identity (regional charge change = boundary flux − decay + sources), causal (retarded) solution check, CFL/stability gates.
* **Cross‑branch invariant** for T2 anywhere: metriplectic split degeneracy diagnostics (g₁,g₂ ≲ 10⁻¹⁰ at grid‑refined tolerance) when applicable.

## T3 — Smoke test (phenomenon‑adjacent)

* Small demo with the T2 meter.
* Predeclare no novelty if it’s QC‑only; pass/fail logged with margins.

## T4 — **Preregistered** hypothesis (protocol locked)

* Hypotheses, nulls, effect sizes, CI thresholds, analysis windows, and contradiction routing locked.

## T5 — Pilot execution

* Narrow grid/time; verify power & CI handling.

## T6 — Main execution

* Full prereg run; KPIs, CIs, and ablations reported.
* Example paths you already sketched (RD front speed; routing KPIs; wave‑flux meter) map neatly here.

## T7 — Robustness

* Parameter sweeps, stepper variants, resolution scaling; track degradation vs meters.

## T8 — Out‑of‑sample prediction

* Hit‑rate or quantitative error on **previously unseen** systems/datasets; for Agency, include cross‑substrate tests. (Your roadmap notes the need for boundary criteria and out‑of‑sample work.)

## T9 — External reproduction

* Independent team reproduces T6–T8; artifacts and prereg open.

**Global Tier invariants (apply to all Tiers ≥T2):**

* **A0–A7 compliance** cited; measurable observables (A7); scaling groups where appropriate (A6).
* **Scope banners** (“meter testing, not phenomenon”, “no novelty claim”) and transparent gates.
