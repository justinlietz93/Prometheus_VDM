import numpy as np, pandas as pd, math, os
import matplotlib.pyplot as plt

# Parameters
gamma = 0.5772156649015329  # Euler–Mascheroni constant

# Node counts (log-spaced for smooth curve)
Ns = np.unique(np.round(np.logspace(2, 7, 200)).astype(int))  # 1e2 .. 1e7

# Scenarios: visits per tick (total "vt_touch" budget devoted to coverage)
scenarios = {
    "visits_per_tick=16 (default SentinelScout)": 16,
    "visits_per_tick=64": 64,
    "visits_per_tick=256": 256,
    "visits_per_tick=0.01*N (1% of nodes/tick)": None,  # computed per N
}

rows = []
for N in Ns:
    lnN = math.log(N)
    for label, s in scenarios.items():
        if s is None:
            s_eff = max(1, int(round(0.01 * N)))
        else:
            s_eff = s
        # Expected time to cover ~95% of nodes (mean-field)
        t95 = (N / s_eff) * math.log(1 / (1 - 0.95))
        # Expected full-coverage time (coupon collector expectation approximation)
        tfull = (N / s_eff) * (lnN + gamma)
        # Mean inter-visit time per node (Poisson approx)
        tmean = N / s_eff
        rows.append({
            "N": N,
            "scenario": label,
            "visits_per_tick": s_eff,
            "mean_intervisit_ticks": tmean,
            "t_95pct_coverage_ticks": t95,
            "t_expected_full_coverage_ticks": tfull,
        })

df = pd.DataFrame(rows)

# Save CSV
csv_path = "C:/Users/jliet/Downloads/vdm_all_artifacts_bundle/data/refresh_horizon_vs_N.csv"
df.to_csv(csv_path, index=False)

# Plot: expected full coverage horizon vs N for each scenario
plt.figure()
for label in scenarios.keys():
    sub = df[df["scenario"] == label].sort_values("N")
    plt.plot(sub["N"], sub["t_expected_full_coverage_ticks"], label=label)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("N (number of nodes)")
plt.ylabel("Expected ticks to full coverage (≈ (N/s)*(ln N + γ))")
plt.title("Coverage refresh horizon vs N (coupon-collector approximation)")
plt.legend(loc="best")

png_path = "C:/Users/jliet/Downloads/vdm_all_artifacts_bundle/data/refresh_horizon_vs_N.png"
plt.savefig(png_path, dpi=200, bbox_inches="tight")
plt.close()

# Plot 2: mean and 95% coverage for the default sentinel budget
default_label = "visits_per_tick=16 (default SentinelScout)"
sub = df[df["scenario"] == default_label].sort_values("N")

plt.figure()
plt.plot(sub["N"], sub["mean_intervisit_ticks"], label="Mean inter-visit per node (N/s)")
plt.plot(sub["N"], sub["t_95pct_coverage_ticks"], label="Time to 95% coverage (≈ (N/s)*ln(20))")
plt.plot(sub["N"], sub["t_expected_full_coverage_ticks"], label="Expected full coverage (≈ (N/s)*(ln N + γ))")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("N (number of nodes)")
plt.ylabel("Ticks")
plt.title("Default SentinelScout (16 visits/tick): refresh times vs N")
plt.legend(loc="best")

png_path2 = "C:/Users/jliet/Downloads/vdm_all_artifacts_bundle/data/refresh_horizon_default_sentinel.png"
plt.savefig(png_path2, dpi=200, bbox_inches="tight")
plt.close()

csv_path, png_path, png_path2

