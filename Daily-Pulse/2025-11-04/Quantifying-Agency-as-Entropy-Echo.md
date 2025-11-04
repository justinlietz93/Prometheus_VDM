Here’s a tight experiment summary that turns “agency” into something you can actually measure, not just debate.

---

# Experiment: Agency as an Entropy‑Echo, Metered Against Void‑Walker Self‑Information Flow

## What we’re measuring (plain terms)

* **Agency (A):** how much a subsystem’s actions leave a reproducible “information dent” in the world that you can replay and still detect.
* **Entropy‑echo (E_echo):** the size of that dent, quantified by how much of the system’s past causal imprint you can recover when you **forward→perturb→rewind**.
* **Baseline:** the **void‑walker self‑information transfer rate** (R_{\text{VW}}): bits per unit time that a void‑walker moves from private state → public field (messages, marks, boundary moves).

## Core metric

1. Run a **forward** evolution for time (T): state (X_0 \to X_T).
2. Inject a controlled micro‑kick (\delta) (local, norm‑bounded).
3. **Rewind** using your metriplectic inverse for the (J)-limb and calibrated (M)-limb correction.
4. Measure **echo loss**:
   [
   E_{\text{echo}}(\delta,T)=\mathbb{E}\left[\mathrm{D}_{\mathrm{KL}}!\left(P(X_0);|;P(\tilde{X}_0|\delta,T)\right)\right]
   ]
   (how far the “returned” distribution (\tilde{X}_0) is from the original).
5. Measure **self‑information flux** of void‑walkers during the same window:
   [
   R_{\text{VW}}=\frac{1}{T}\sum_{t\le T} I\big(S_t;F_t\big)\quad[\text{bits/s}]
   ]
   where (I(S_t;F_t)) is mutual information between private walker state and emitted field tokens/marks at time (t).

**Agency index (dimensionless):**
[
\mathcal{A} ;=; \frac{E_{\text{echo}}(\delta,T)}{R_{\text{VW}}}
]
Interpretation: per bit the walker exports, how large and recoverable is its causal dent?

## Why this is falsifiable

* If “agency” is real and not a vibe, increasing structured, goal‑directed walker policies (while holding energy budget fixed) should **increase** (E_{\text{echo}}) faster than it increases mere chatter (R_{\text{VW}}) ⇒ (\mathcal{A}) rises.
* If it’s just noise or overfit telemetry, (\mathcal{A}) stays flat or drops as (R_{\text{VW}}) grows.

## Minimal protocol (T2 → T3 gate)

* **Controls:** (i) no‑walker field (thermal), (ii) random walker, (iii) scripted walker, (iv) adaptive void‑walker.
* **Grid:** (\delta\in{10^{-6},10^{-5},10^{-4}}); (T\in{10^2,10^3}) steps; 32 seeds each.
* **Outputs:** per condition, report ({\overline{E_{\text{echo}}},,\overline{R_{\text{VW}}},,\overline{\mathcal{A}}}) with 95% CI; preregister thresholds for “increase” ((\Delta \ge 0.2\sigma)).

## Implementation notes (drop‑in)

* **Echo runner:** reuse your forward integrator; add a checkpoint at (X_0), integrate to (X_T), apply (\delta), then inverse‑integrate with (J) exact and (M) calibrated (log entropy budget, don’t hide correction).
* **R_VW tap:** log emitted tokens/marks; compute rolling (I(S_t;F_t)) via discrete bins or kNN MI estimator; sum and divide by (T).
* **Safety checks:** (1) echo sanity on synthetic linear system; (2) conservation checks on (J)-limb; (3) M‑limb sign conventions fixed and documented.

## Pass/Fail gates

* **T2 Pass:** (\mathcal{A}*{\text{adaptive}} > \mathcal{A}*{\text{random}}) by ≥0.5σ across at least two (\delta) scales.
* **T3 Pass:** monotone trend: scripted < adaptive; and (\mathcal{A}) remains stable under 10% integrator step changes.

## What this tells you about your current results

* If your existing CEG/echo tests already show clean rewind with non‑zero loss and you have logs for emitted field tokens, you can compute (R_{\text{VW}}) retroactively and form (\mathcal{A}) now. If scripted policies and adaptive policies weren’t separated, re‑run with those two controls to make the comparison meaningful.

## Repo placement (suggested)

* `Derivation/Agency/PROPOSAL_entropy_echo.md` (this spec)
* `code/physics/agency/echo_runner.py` (forward/rewind; MI tap)
* `Derivation/Agency/specs/T2_entropy_echo.v1.json` (grid + seeds)
* `Derivation/Agency/results/T2_entropy_echo_YYYYMMDD/…` (CSVs + hashes)

If you want, I can turn this into your strict PROPOSAL template with exact filenames and gates filled—say the word and I’ll ship the ready‑to‑commit doc.

