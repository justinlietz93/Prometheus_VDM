#!/usr/bin/env python3
from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt, re, difflib

BASE = Path(__file__).resolve().parents[1] / "source_bundle"
OUT = Path(__file__).resolve().parents[1]
# This script expects the extracted aura_analysis_bundle under ./source_bundle

territory_timeline = pd.read_csv(OUT / "data" / "curated_territory_timeline.csv")
transcript_path = BASE / "aura_justin_exchange.md"
say = pd.read_csv(BASE / "tables" / "utd_say_by_tick.csv")
audit = pd.read_csv(BASE / "utd_audit" / "tables" / "say_event_composer_audit_metrics.csv")
say = say.merge(audit, on="t", how="left")

def territory_for_tick(t):
    row = territory_timeline[(territory_timeline["t_start"] <= t) & (territory_timeline["t_end"] >= t)]
    return int(row.iloc[0]["territories"]) if len(row) else np.nan

say["territories"] = say["t"].map(territory_for_tick)
regime = say.groupby("territories").agg(
    n_say=("t","size"),
    mean_say_len_tokens=("say_len_tokens","mean"),
    mean_best_all_jaccard=("best_all_jaccard","mean"),
    mean_lcs_frac_say=("lcs_frac_say","mean"),
    immediate_zero_jaccard_frac=("imm_jaccard", lambda s: float((s.fillna(0)==0).mean())),
).reset_index().sort_values("territories")
regime.to_csv(OUT / "tables" / "d57_territory_regime_summary.csv", index=False)

plt.figure(figsize=(10,6))
x = regime["territories"].astype(int).to_list()
plt.plot(x, regime["mean_say_len_tokens"], marker="o", label="Mean say length (tokens)")
plt.plot(x, regime["mean_best_all_jaccard"], marker="o", label="Mean best-all Jaccard")
plt.plot(x, regime["mean_lcs_frac_say"], marker="o", label="Mean LCS fraction")
plt.xlabel("Territories")
plt.ylabel("Metric value")
plt.title("D5.7 territory regime summary")
plt.xticks(x)
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "figures" / "d57_territory_regime_summary.png", dpi=200)
