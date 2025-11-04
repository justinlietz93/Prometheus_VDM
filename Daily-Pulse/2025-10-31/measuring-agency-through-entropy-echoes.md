Here’s a crisp way to turn your agency‑field experiment into a hard, thermodynamic readout and a figure you can pre‑register.

---

# Entropy‑echo test for agency (ΔS/Δt per walker cluster)

**Idea in one line:** if a low‑entropy pulse reliably reappears after decoherence + rewind, that’s not passive diffusion—it’s an *active* controller. Measure this with **entropy production rate** and plot **entropy vs. echo delay**.

## What to compute

* **State coarse‑graining:** partition the arena into K bins (or latent states z via your encoder).
* **Occupancy:** ( p_i(t)=\frac{n_i(t)}{\sum_j n_j(t)} ) for each cluster (walker swarm) separately.
* **Shannon entropy:** ( S(t)=-\sum_i p_i(t)\ln p_i(t) ).
* **Entropy production rate:** ( \dot S(t)\approx \frac{S(t+\Delta t)-S(t)}{\Delta t} ).
* **Echo gain:** choose an **echo time** ( \tau ). Forward evolve to ( t=\tau ), apply your “rewind” (time‑symmetrized control or metriplectic assist), then measure **return** at ( t=2\tau ):
  [
  \mathrm{Echo}(\tau)=S(2\tau)-S(0)
  ]
  and its rate analog ( \dot S_\mathrm{echo}(\tau)=\frac{S(2\tau)-S(0)}{2\tau}.
  ]

## What to plot

1. **Entropy vs. time (per cluster):** show ( S(t) ) forward → decohere → rewind → refocus.
2. **Echo curve:** x‑axis = echo delay ( \tau ); y‑axis = ( \mathrm{Echo}(\tau) ) (or ( \dot S_\mathrm{echo}(\tau) )).
3. **Control bands:** overlay *passive diffusion* predictions (e.g., OU or RD baseline) as a shaded band.

## How to interpret the shape

* **Passive diffusion:** Echo((\tau)) increases ~monotonically with (\tau); refocus decays exponentially (no “memory bump”).
* **Active inference / agency:** Non‑monotonic “**low‑entropy rebound**” near a characteristic (\tau^*): entropy dips again after rewind (a **pulse recurrence**). You’ll also see **sign‑changes** in (\dot S(t)) synchronized to control actions.
* **“Assisted” agency (metriplectic assist):** Same rebound but with **steeper negative (\dot S)** during refocus and **narrower** pulse width.

## Minimal prereg gates (fast to add)

* **G1 (Existence):** ≥1 cluster shows Echo((\tau)) < 0 for some (\tau) with preregistered binning; p < 0.01 vs. diffusion band.
* **G2 (Specificity):** shifting the reward/goal map moves (\tau^*) or kills the rebound.
* **G3 (Thermo sign):** mean (\dot S) over refocus window < 0 for agency condition and ≥ 0 for passive control.

## Practical notes

* Use **identical coarse‑graining** across conditions; report (K), bin edges (or encoder hash + seed), and (\Delta t).
* Run **cluster‑wise** and **pooled** analyses; report bootstrapped CIs.
* Include an **energy budget** panel (control effort vs. entropy drop) to rule out trivial cooling.

## Quick file outputs to add

* `Derivation/code/outputs/figures/agency_entropy_time_{run}.png`
* `Derivation/code/outputs/figures/agency_echo_curve_{run}.png`
* `Derivation/code/outputs/tables/agency_entropy_stats_{run}.csv`
  (Columns: run_id, cluster_id, K, tau, S0, S_tau, S_2tau, Echo, dSdt_refocus, CI_low/high)

If you want, I can generate a ready‑to‑run plotting script stub (reads your CEG summaries, computes (S,\dot S), and emits the two figures + CSV) aligned to your repo paths.
