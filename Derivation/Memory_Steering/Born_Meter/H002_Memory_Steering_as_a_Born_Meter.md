# H002 — Memory‑Steering as a Born‑Meter

**Classification:** Axiom‑core (metering)
**Author:** Justin K. Lietz
**Date:** 2025-11-06
**Status:** HYPOTHESIS
**One‑line objective:** The existing memory‑steering plus void‑announcer stack acts as a **basis‑agnostic** readout whose frequencies match (|Ua|^2) after arbitrary J‑basis rotations.

**Formal statement**
With mode energies (E_k) estimated **locally** and memory variable (m_k \approx \alpha \log(E_k+\epsilon)), the softmax meter (P(k)\propto e^{\Theta m_k}) yields outcome frequencies (f_k) with **KL**((f, |Ua|^2) \le 10^{-3}) across random unannounced (U).

## **Predictions (decisive metrics)**

* **P1:** Born‑meter KL ≤ (10^{-3}) over seeds after random (U).
* **P2:** Witness (W>0) in no‑signaling‑in‑time test with a nonselective M blip.
* **P3:** Locality: walkers never read global (a); cone audit clean.

**Rationale**
Re(QGT) is the Fubini–Study metric; in the classical‑probability embedding it reduces to ¼·Fisher information. That supports using *log‑probability/energy* as the natural coordinate for a meter that’s invariant to reparametrization.

**Preconditions & scope**
Echo‑verified J window; fixed α learned once and frozen; no global peeking in meter code.

## **Experiment plan (tentative)**

* **E1:** Fit α on held‑out; freeze. Randomize (U); run 10³–10⁵ shots. **Gate:** KL ≤ (10^{-3}).
* **E2:** NST witness with/without nonselective M‑blip. **Gate:** (W>0) beyond error bars.

**Risks & kill‑methods**
Meter cheating (reads (a)) → API guardrails + tests; basis overfit → (U) drawn after J.

**Links**
S*: (to be added) | T0_*: `T0_born_meter/` | Results: `results/born_meter/*.json`
