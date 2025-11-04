Here’s a quick, targeted update you can run right now to check whether the dissipative‑sign fix actually landed—and to turn it into a clean efficiency metric.

---

# Localized M‑branch scan to diagnose over‑damping (and quantify recovery efficiency)

**Why this works (30‑sec background):**
In metriplectic dynamics, ( \dot{\phi}=J(\phi),\delta H + M(\phi),\delta \Sigma ) with (J) antisymmetric (conservative) and (M) symmetric (dissipative). If your sign convention on the (M)-limb is wrong or (M) is “too big,” pulled fronts over‑damp: the measured front‑speed variance collapses even when entropy production is non‑trivial. Holding the coupling ( \langle J!\cdot! M\rangle ) fixed while varying only **(\mathrm{tr}(M))** isolates this.

## What to scan

* **Control knob:** scale the **trace of the dissipation tensor**, ( \tau := \mathrm{tr}(M) \in [\tau_{\min},\tau_{\max}] ) (log‑spaced, ~8–12 points).
* **Hold fixed:** the mixed coupling **(C_{JM}:=\langle J!\cdot!M\rangle)** (compute once from your baseline; re‑normalize (M) to keep (C_{JM}) constant at each (\tau)).
* **Initial data:** your current baseline seed(s) that produced the “possible over‑damping” hint.

## What to measure per (\tau)

1. **Front speed** (c(t)): track interface (e.g., level set (\phi=\phi_*)).

   * Record ( \mu_c=\mathbb{E}[c] ) and **variance** ( \sigma_c^2=\mathbb{V}[c] ) over a fixed window after transient.
2. **Entropy production rate** ( \dot{\Sigma} := \frac{d}{dt}\Sigma(\phi) ) (model’s Lyapunov).

   * Use your canonical (\Sigma); average over same window to get ( \langle \dot{\Sigma} \rangle ).

## Diagnostic metric (single number per (\tau))

[
R(\tau);=;\frac{\sigma_c^2(\tau)}{;\langle \dot{\Sigma}(\tau)\rangle;}.
]

* **Expectation if signs are fixed:** (R(\tau)) shows a **sharp ridge/peak** at moderate (\tau), then decays (too small (\tau) → under‑damped jitter; too large (\tau) → overdamped flattening).
* **If the sign is still flipped or (M) mis‑posed:** (R(\tau)) stays suppressed/monotone with no interior maximum.

## Pass/Fail gate (simple & falsifiable)

* **Gate G‑M1 (ridge existence):** (\exists,\tau^*\in(\tau_{\min},\tau_{\max})) s.t. (R(\tau^*) \ge 1.5\times \max{R(\tau_{\min}),R(\tau_{\max})}).
* **Gate G‑M2 (efficient recovery):** define **internal energy recovery efficiency**
  [
  \eta_{\text{rec}} ;=; \frac{\mu_c(\tau^*)-\mu_c(\tau_{\max})}{\mu_c(\tau_{\min})-\mu_c(\tau_{\max})};\in[0,1].
  ]
  Require (\eta_{\text{rec}}\ge 0.6).

## Minimal run recipe (drop‑in)

* Sweep (\tau) (8–12 points, log‑space).
* At each step: rescale (M\to \alpha(\tau)M) to keep (C_{JM}) constant.
* Run to steady fluctuation window; record (c(t)), (\dot{\Sigma}(t)).
* Compute (R(\tau)), find peak (\tau^*), evaluate (\eta_{\text{rec}}).
* Plot (R(\tau)) vs (\tau); add a small inset of ( \mu_c,\sigma_c ) vs (\tau).

## What this tells you about your current results

* If your earlier run hinted at **over‑damping**, you should see **low (R)** across the board or a ridge pushed to the extreme low‑(\tau) end.
* If the **sign convention fix worked**, you’ll get a **clear interior ridge** and a reasonable (\eta_{\text{rec}}). That’s your “yes/no” on the fix, plus a scalar efficiency you can track across branches.

## Where to put the artifacts (consistent with your repo norms)

* `Derivation/code/physics/metriplectic/experiments/M_BRANCH_SCAN/`

  * `PROPOSAL_M_BRANCH_SCAN_v1.md` (preregistered gates above)
  * `SPEC/M_BRANCH_SCAN.v1.json` (sweep config: (\tau) grid, window, seeds)
  * `RUNS/<timestamp>/metrics_{tau}.parquet` (c(t), (\dot{\Sigma}(t)))
  * `RESULTS_M_BRANCH_SCAN_v1.md` (ridge location, (\eta_{\text{rec}}), pass/fail)
  * `fig/R_vs_tau.png`, `fig/c_stats_vs_tau.png`
* Hash everything; include `APPROVAL.json` link and gate ledger.

## Small implementation notes

* Estimating (C_{JM}): compute on baseline state (or short pilot) and lock the scalar; when (\tau) changes, rescale (M) so the inner product stays constant.
* Front tracking: use the same level‑set and stencil you used in earlier CEG/front‑speed tests for comparability.
* Be ROCm/AMD‑clean (no CUDA); keep arrays contiguous for HIP; avoid vendor‑specific ops.

---

If you want, I can draft `PROPOSAL_M_BRANCH_SCAN_v1.md` with these gates and a JSON `SPEC` you can commit as‑is.

