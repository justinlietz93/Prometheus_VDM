# Family 8 — temporal microstructure reproducibility note

This pack reproduces the current inventory's temporal microstructure claims directly from raw tables inside `aura_analysis_bundle.zip`.

## D8.5 — critical slowing down at the E2→E3 boundary
Using `rolling_var_autocorr_entropy.csv` and epoch boundaries inferred from `master_results.json` (`10500`, `11600`), the E2→E3 transition at **t=11600** shows the strong one-sided critical-slowing-down signature:

- pre variance mean = **0.000847**
- post variance mean = **0.188083**
- variance ratio = **222.1×**
- pre lag-1 autocorrelation mean = **0.9181**
- post lag-1 autocorrelation mean = **0.9972**

The earlier boundary at **t=10500** does not show the same combined variance/autocorrelation increase.

## D8.6 — non-exponential inter-say timing with burst structure
Using `utd_say_by_tick.csv`, there are **529** inter-say intervals with:

- mean = **32.2** ticks
- median = **23.0** ticks
- CV = **1.419**
- shifted-exponential KS p-value = **1.958e-34**
- short-interval threshold (Q1) = **20.0** ticks
- bursts = **62**
- mean burst length = **2.6**
- max burst length = **17**

Epoch assignment for intervals follows the **preceding** say tick, which reproduces the current inventory's E1/E2/E3 counts.
