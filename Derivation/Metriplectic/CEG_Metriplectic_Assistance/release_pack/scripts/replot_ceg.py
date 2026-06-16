"""
replot_ceg.py — Standalone replot script for CEG Metriplectic Assisted-Echo pack.

Reads the JSON run log and CSV summary produced by assisted_echo_runner and
regenerates two publication-quality figures:
  - ceg_vs_lambda.png  : CEG median ± (mean−median) vs assistance strength λ
  - gate_pass_rates.png: Instrument gate pass-rate bar chart (G1–G4)

Usage:
    python replot_ceg.py --json <run_log.json> --csv <ceg_summary.csv> --outdir <dir>
"""

import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load_data(json_path: str, csv_path: str):
    with open(json_path) as fh:
        run = json.load(fh)
    ceg_summary = run["ceg_summary"]           # {"0": {"mean":…, "median":…, "n":…}, …}
    gate_ledger = run["gate_ledger_per_seed"]  # list of per-seed dicts

    lambdas = sorted(float(k) for k in ceg_summary)

    medians, means = [], []
    for lam in lambdas:
        key = str(lam)
        if key not in ceg_summary:
            key = str(int(lam))
        entry = ceg_summary[key]
        medians.append(entry["median"])
        means.append(entry["mean"])

    return lambdas, medians, means, gate_ledger


def plot_ceg_vs_lambda(lambdas, medians, means, outdir: str):
    fig, ax = plt.subplots(figsize=(6, 4))

    x = np.array(lambdas)
    med = np.array(medians)
    mn = np.array(means)
    err = np.abs(mn - med)

    ax.bar(x, med, width=0.06, color="#4878CF", alpha=0.85, label="Median CEG",
           zorder=3)
    ax.errorbar(x, med, yerr=err, fmt="none", ecolor="#333333", capsize=4,
                linewidth=1.2, zorder=4, label="|mean − median|")

    ax.axhline(0.05, color="crimson", linestyle="--", linewidth=1.2,
               label="Preregistered threshold (0.05)")

    ax.set_xlabel("Assistance strength λ", fontsize=12)
    ax.set_ylabel("Counterfactual Echo Gain (CEG)", fontsize=12)
    ax.set_title("CEG vs Assistance Strength λ", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels([str(lam) for lam in lambdas])
    ax.yaxis.grid(True, linestyle=":", alpha=0.6)
    ax.set_axisbelow(True)

    fig.tight_layout()
    out = os.path.join(outdir, "ceg_vs_lambda.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved: {out}")


def plot_gate_pass_rates(gate_ledger, outdir: str):
    gate_names = ["G1_Noether_J", "G2_H_theorem_M", "G3_EnergyMatch", "G4_StrangDefect"]
    short_names = ["G1\nNoether J-drift", "G2\nH-theorem M", "G3\nEnergy match", "G4\nStrang defect"]

    counts = {g: {"pass": 0, "total": 0} for g in gate_names}
    for entry in gate_ledger:
        for gate in entry["gates"]:
            gname = gate["gate"]
            if gname in counts:
                counts[gname]["total"] += 1
                if gate["passed"]:
                    counts[gname]["pass"] += 1

    rates = [100.0 * counts[g]["pass"] / max(counts[g]["total"], 1) for g in gate_names]

    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(gate_names))
    bars = ax.bar(x, rates, color=["#4CAF50" if r >= 100 else "#FF5722" for r in rates],
                  alpha=0.85, width=0.5)

    for bar, rate in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{rate:.0f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylim(0, 115)
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, fontsize=9)
    ax.set_ylabel("Pass rate (%)", fontsize=12)
    ax.set_title("Instrument Gate Pass Rates (12 seeds)", fontsize=13, fontweight="bold")
    ax.yaxis.grid(True, linestyle=":", alpha=0.6)
    ax.set_axisbelow(True)

    fig.tight_layout()
    out = os.path.join(outdir, "gate_pass_rates.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved: {out}")


def main():
    parser = argparse.ArgumentParser(description="Replot CEG figures from run log.")
    parser.add_argument("--json", required=True, help="Path to run JSON log")
    parser.add_argument("--csv", required=True, help="Path to CEG summary CSV")
    parser.add_argument("--outdir", required=True, help="Output directory for figures")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    lambdas, medians, means, gate_ledger = load_data(args.json, args.csv)
    plot_ceg_vs_lambda(lambdas, medians, means, args.outdir)
    plot_gate_pass_rates(gate_ledger, args.outdir)


if __name__ == "__main__":
    main()
