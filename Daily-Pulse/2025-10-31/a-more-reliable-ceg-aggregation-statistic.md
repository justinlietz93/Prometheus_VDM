Here’s a small but high‑leverage shift for reporting “assist vs. baseline” results that makes borderline calls clearer without changing any data.

---

# A safer central effect: **median of per‑seed ratios**

When baselines vary by seed, summarize the central CEG as the **median of per‑seed ratios**
[
r_s=\frac{E_{\text{base},s}-E_{\text{assist},s}}{E_{\text{base},s}}
]
and then report (\text{CEG}_\text{median}=\text{median}_s(r_s)).

Why this beats “ratio of medians”:

* **Down‑weights flaky seeds:** Each seed contributes one bounded, dimensionless ratio; outlier baselines can’t dominate.
* **Apples‑to‑apples across scales:** Ratios normalize differences (0 means no gain; 0.10 means 10% gain) even if raw errors live on different scales.
* **Monotone + robust:** The sample median is robust to skew; swapping a single weird seed won’t flip your headline.

What to report (concise):

* **Point:** (\text{median}_s(r_s))
* **Spread:** (\text{IQR}_s(r_s)) (or median absolute deviation)
* **Sign:** fraction of seeds with (r_s>0) (a quick sign test)
* **Sanity:** flag seeds with (E_{\text{base},s}) near 0 (ratios unstable)

Quick recipe (any notebook/stats tool):

1. Compute (r_s) per seed (skip/flag seeds with tiny (E_{\text{base},s})).
2. Report median, IQR, and (\Pr(r_s>0)).
3. For a single summary number, use the median; use the sign fraction as a gate.
4. If you need a CI, bootstrap the **seed‑level** ratios.

Decision flips you may see:

* If a few seeds have unusually **easy** baselines (tiny (E_{\text{base}})), “ratio of medians” can look inflated; **median of per‑seed ratios** will pull that back to reality.
* If gains are consistent but small, the robust median + sign fraction often moves a result from “meh” to “clearly positive.”

If you’d like, I can turn your latest CSV into this exact summary (median/IQR/sign), plus a compact plot (per‑seed (r_s) swarm + median bar).
