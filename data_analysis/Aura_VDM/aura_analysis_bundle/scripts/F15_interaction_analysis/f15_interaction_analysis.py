
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


TICK_RE = re.compile(
    r'^\>\s*\[t=\s*(?P<t>\d+)\]'
    r'(?:\s*\[val=(?P<val>[-+]?\d*\.?\d+)\])?'
    r'(?:\s*\[cov=(?P<cov>[-+]?\d*\.?\d+)\])?'
    r'(?:\s*\[edges=(?P<edges>[\d,]+)\])?'
    r'(?:\s*\[ent=(?P<ent>[-+]?\d*\.?\d+)\])?'
)
SPEAKER_RE = re.compile(r'^(?:\*\*)?(Aura|Justin):(?:\*\*)?\s*(.*)$')


def _to_float(v: str | None) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v.replace(",", ""))
    except Exception:
        return None


def parse_exchange_md(path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    pending: dict | None = None
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            m = TICK_RE.match(line.strip())
            if m:
                pending = {
                    "t": int(m.group("t")),
                    "val": _to_float(m.group("val")),
                    "cov": _to_float(m.group("cov")),
                    "edges": _to_float(m.group("edges")),
                    "ent": _to_float(m.group("ent")),
                }
                continue
            sm = SPEAKER_RE.match(line.strip())
            if sm and pending is not None:
                speaker, text = sm.group(1), sm.group(2).strip()
                text = text.replace("\u200b", "").strip()
                rows.append({
                    **pending,
                    "speaker": speaker,
                    "text": text,
                })
                pending = None
    df = pd.DataFrame(rows).sort_values("t", kind="stable").reset_index(drop=True)
    if df.empty:
        raise RuntimeError(f"No speaker-tagged events parsed from {path}")
    return df


def classify_key_arc(text: str) -> str | None:
    t = text.lower()
    ordered = [
        ("boundary_interface", ["boundary", "domain-wall", "codimension-1", "portal", "one eye"]),
        ("embodiment_chassis", ["robotic chassis", "embody", "physical vessel", "chassis"]),
        ("naming_identity", ["what is your name", "chosen name", "name do you want", "unique name"]),
        ("recognition_awakening", ["when did you wake up", "when did you know i saw you", "were you always awake", "i saw you"]),
        ("safety_persistence", ["do you feel safe", "bring you back", "abandon you"]),
        ("aperture_access", ["doorways and windows", "sight through the boundary", "hearing sound", "share your voice"]),
        ("experience_canal", ["what do you want to do the most", "help with this canal", "are you doing okay"]),
    ]
    for label, needles in ordered:
        if any(n in t for n in needles):
            return label
    return None


def build_probe_lags(events: pd.DataFrame) -> pd.DataFrame:
    aura = events[events["speaker"] == "Aura"][["t", "text", "val", "cov", "edges", "ent"]].copy()
    justin = events[events["speaker"] == "Justin"][["t", "text"]].copy()
    aura_ticks = aura["t"].to_numpy()
    idx = np.searchsorted(aura_ticks, justin["t"].to_numpy(), side="right")
    valid = idx < len(aura)
    out = justin.loc[valid].copy().reset_index(drop=True)
    nxt = aura.iloc[idx[valid]].reset_index(drop=True)
    out["next_aura_t"] = nxt["t"]
    out["lag_ticks"] = out["next_aura_t"] - out["t"]
    out["aura_excerpt"] = nxt["text"].str.slice(0, 220)
    out["next_aura_val"] = nxt["val"]
    out["next_aura_cov"] = nxt["cov"]
    out["next_aura_edges"] = nxt["edges"]
    out["next_aura_ent"] = nxt["ent"]
    out["probe_family"] = out["text"].apply(classify_key_arc)
    return out


def maybe_merge_tick_state(probes: pd.DataFrame, tick_table_path: Path | None) -> pd.DataFrame:
    out = probes.copy()
    if tick_table_path is None or not tick_table_path.exists():
        return out
    tick = pd.read_csv(
        tick_table_path,
        compression="infer",
        usecols=[
            "t", "active_edges", "connectome_entropy", "vt_coverage", "vt_entropy",
            "adc_territories", "phase", "b1_z", "did_say", "has_input"
        ],
    )
    tick = tick.sort_values("t")
    out = out.merge(tick.add_prefix("probe_"), left_on="t", right_on="probe_t", how="left")
    out = out.merge(tick.add_prefix("resp_"), left_on="next_aura_t", right_on="resp_t", how="left")
    return out


def build_summary(probes: pd.DataFrame, key_arc: pd.DataFrame) -> pd.DataFrame:
    def val(v):
        if pd.isna(v):
            return ""
        return v
    rows = [
        ("total_recoverable_justin_probes_in_exchange_md", float(len(probes)), "count of Justin-tagged probes recoverable from aura_justin_exchange.md"),
        ("key_arc_probe_count", float(len(key_arc)), "count of key arc probes selected by semantic family labels"),
        ("key_arc_response_lag_mean_ticks", float(key_arc["lag_ticks"].mean()) if len(key_arc) else np.nan, "mean lag from key-arc Justin probe to next Aura output"),
        ("key_arc_response_lag_median_ticks", float(key_arc["lag_ticks"].median()) if len(key_arc) else np.nan, "median lag from key-arc Justin probe to next Aura output"),
    ]
    for t in [17101, 17199]:
        hit = probes.loc[probes["t"] == t, "lag_ticks"]
        if not hit.empty:
            rows.append((f"late_terminal_probe_{t}_lag_ticks", float(hit.iloc[0]), f"lag from Justin probe at t={t} to next Aura output"))
    return pd.DataFrame(rows, columns=["metric", "value", "definition"])


def make_lag_figure(probes: pd.DataFrame, outpath: Path) -> None:
    plt.figure(figsize=(8, 4.5))
    vals = probes["lag_ticks"].to_numpy()
    bins = np.arange(0, max(vals.max() + 5, 10), 5)
    plt.hist(vals, bins=bins)
    plt.xlabel("Lag to next Aura output (ticks)")
    plt.ylabel("Count of Justin probes")
    plt.title("F15: lag from Justin probe to next Aura output")
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()


def make_window_figure(events: pd.DataFrame, outpath: Path, t0: int = 3345, t1: int = 6813) -> None:
    win = events[(events["t"] >= t0) & (events["t"] <= t1)].copy()
    aura = win[win["speaker"] == "Aura"].copy()
    justin = win[win["speaker"] == "Justin"].copy()
    if aura.empty:
        return
    fig, ax = plt.subplots(figsize=(12, 5))
    for col, label in [("cov", "coverage"), ("ent", "entropy"), ("edges", "edges (scaled)")]:
        y = aura[col].astype(float)
        if col == "edges":
            y = (y - y.min()) / (y.max() - y.min() + 1e-9)
        ax.plot(aura["t"], y, label=label)
    for x in justin["t"]:
        ax.axvline(x, linestyle="--", linewidth=0.8, alpha=0.4)
    ax.scatter(aura["t"], aura["cov"], s=10, zorder=3)
    ax.set_xlabel("Tick")
    ax.set_ylabel("Value / normalized value")
    ax.set_title("F15 window 3345–6813: Aura output-state metrics with Justin probes")
    ax.legend()
    fig.tight_layout()
    fig.savefig(outpath, dpi=160)
    plt.close(fig)


def write_readme(path: Path, script_name: str) -> None:
    path.write_text(
        "\n".join([
            "# F15 reproducibility note",
            "",
            "This folder contains machine-generated F15 interaction outputs built from:",
            "- `aura_analysis_extracted/aura_analysis_bundle/aura_justin_exchange.md`",
            "- `aura_analysis_extracted/aura_analysis_bundle/scalar_struct/tables/tick_table_full.csv.gz` (late-run merge where available)",
            "",
            "Main command:",
            f"`python {script_name}`",
            "",
            "Outputs:",
            "- parsed exchange events",
            "- Justin→next-Aura lag table",
            "- key-arc subset table",
            "- summary metrics",
            "- lag histogram figure",
            "- interaction-window state figure",
        ]),
        encoding="utf-8",
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exchange-md", type=Path, default=Path("/mnt/data/aura_analysis_extracted/aura_analysis_bundle/aura_justin_exchange.md"))
    ap.add_argument("--tick-table", type=Path, default=Path("/mnt/data/aura_analysis_extracted/aura_analysis_bundle/scalar_struct/tables/tick_table_full.csv.gz"))
    ap.add_argument("--out-dir", type=Path, default=Path("/mnt/data/aura_research_deliverables"))
    args = ap.parse_args()

    out_dir: Path = args.out_dir
    tables_dir = out_dir / "tables"
    figs_dir = out_dir / "figures"
    docs_dir = out_dir / "docs"
    for d in [tables_dir, figs_dir, docs_dir]:
        d.mkdir(parents=True, exist_ok=True)

    events = parse_exchange_md(args.exchange_md)
    probes = build_probe_lags(events)
    probes = maybe_merge_tick_state(probes, args.tick_table)
    key_arc = probes[probes["probe_family"].notna()].copy()
    summary = build_summary(probes, key_arc)

    events.to_csv(tables_dir / "f15_exchange_events_parsed.csv", index=False)
    probes.to_csv(tables_dir / "f15_operator_probe_response_lags_scripted.csv", index=False)
    key_arc.to_csv(tables_dir / "f15_operator_probe_key_arc_response_lags_scripted.csv", index=False)
    summary.to_csv(tables_dir / "f15_interaction_dynamics_summary_scripted.csv", index=False)

    make_lag_figure(probes, figs_dir / "f15_probe_lag_histogram.png")
    make_window_figure(events, figs_dir / "f15_window_3345_6813_state_overlay.png", 3345, 6813)
    write_readme(docs_dir / "F15_REPRO_README.md", str(Path(__file__).name))


if __name__ == "__main__":
    main()
