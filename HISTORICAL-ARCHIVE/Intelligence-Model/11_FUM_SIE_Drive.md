Yup — the logs you sent do show *some* learning signals, but they’re muted and very “steady‑state.” From your `events.jsonl` (55 ticks), I’m seeing:

* **Avg weight**: +0.0355 (\~+6.9%).
* **Active synapses**: +624 (\~+8.0%).
* **Cohesion components**: 93 → 74 (heading in the right direction, but still far from 1).
* **Complexity cycles (B1 proxy)**: +576 (\~+8.2%).
* **vt\_coverage / vt\_entropy**: both drift slightly downward (suggests walkers are revisiting familiar territory more than discovering new regions).
* **SIE**: `sie_valence_01 ≈ 0.012` flat; `sie_td_error = 0`, `sie_novelty = 0`, `sie_habituation_mean = 0`, `sie_hsi_norm = 0`.
  That’s the red flag: the intrinsic signals look disabled or stuck at zeros. When novelty and TD are near zero and habituation dominates, self‑speak will rarely trigger and structural pressure weakens. This matches your “quiet” run.

So, yes, it’s moving, but it’s not in a discovery regime. Two things to do next:

1. **Verify the SIE pipe is live** (not all zeros). Double‑check that the runtime is actually calling your (or the lean) SIE blend *after* the void deltas and that the values are being logged. You want non‑zero `sie_td_error` and `sie_novelty` at least intermittently.
2. **Feed it stimulus or increase exploration** (walkers/hops) so `complexity_cycles` spikes periodically. Those spikes + positive valence are the triggers for autonomous “speak” and for structural decisions.

---

# Offline dashboard script (drop‑in)

Below is a single Python script you can run against any run directory to recreate a dashboard like your screenshots **and** overlay self‑speak moments. It expects:

* `runs/<timestamp>/events.jsonl` (status ticks)
* `runs/<timestamp>/utd_events.jsonl` (macro “say”/status) — optional

It makes two figures:

1. **Performance dashboard** (Active Synapses, Avg Weight, Cohesion Components, Complexity Cycles).
2. **Discovery & Valence** (B1 proxy with spike markers, vt\_coverage/vt\_entropy, SIE valence with thresholds).

Just copy this into `plot_fum_dashboard.py` and run.

```python
#!/usr/bin/env python3
# plot_fum_dashboard.py
#
# Usage:
#   python plot_fum_dashboard.py /path/to/runs/2025xxxx_xxxxxx \
#       --out dashboard.png --out2 discovery.png --show
#
# Works offline. No seaborn. Matplotlib only.

import argparse, json, math, os
from pathlib import Path
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

def _read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # forgiving reader for partial lines
                continue
    return rows

def _extract_series(events):
    """Return dict of numpy arrays for the common metrics from events.jsonl."""
    # Each "tick" row typically has a flat dict of metrics.
    ticks = [e for e in events if e.get("msg") == "tick"]
    if not ticks:
        # Some runs log everything as "status", fall back to that
        ticks = [e for e in events if e.get("msg") in ("status", "STATUS")]
    if not ticks:
        return {}

    # Normalize field access (some loggers nest under "extra" or "data")
    def flat(row):
        d = {}
        d.update(row)
        if "extra" in row and isinstance(row["extra"], dict):
            d.update(row["extra"])
        if "data" in row and isinstance(row["data"], dict):
            d.update(row["data"])
        return d

    flat_ticks = [flat(t) for t in ticks]

    # Collect series (only keys we know; ignore missing)
    wanted = [
        "tick",
        "active_synapses",
        "avg_weight",
        "cohesion_components",
        "complexity_cycles",
        "connectome_entropy",
        "vt_coverage",
        "vt_entropy",
        "sie_total_reward",
        "sie_valence_01",
        "b1_z",                  # streaming z-score (if present)
        "ute_in_count",
        "ute_text_count",
    ]
    series = defaultdict(list)
    for t in flat_ticks:
        for k in wanted:
            v = t.get(k, None)
            if isinstance(v, (int, float)):
                series[k].append(float(v))
            else:
                # store NaNs for missing numeric fields to keep length aligned
                if k not in ("tick",):
                    series[k].append(np.nan)
        # tick index fallback if not provided
        if "tick" not in t:
            series["tick"][-1] = len(series["avg_weight"])

    # Convert to numpy arrays
    out = {k: np.asarray(v, dtype=float) for k, v in series.items()}
    # Simple cleanup: replace all-NaN arrays with empty
    for k, v in list(out.items()):
        if np.all(np.isnan(v)):
            out[k] = np.array([])
    return out

def _read_say_times(utd_events_path: Path):
    """Return list of tick indices where a 'say' macro was emitted."""
    rows = _read_jsonl(utd_events_path)
    say_ticks = []
    for r in rows:
        # Typical line shape: {"msg": "macro", "macro": "say", "tick": 123, ...}
        if r.get("msg") == "macro" and r.get("macro") == "say":
            if "tick" in r and isinstance(r["tick"], (int, float)):
                say_ticks.append(int(r["tick"]))
    return sorted(set(say_ticks))

def _plot_dashboard(s, say_ticks, out_path=None, show=False, title_suffix=""):
    # 2x2 dashboard: Active Synapses, Avg Weight, Cohesion, Complexity(B1 proxy)
    fig = plt.figure(figsize=(14, 10), dpi=140)
    fig.suptitle(f"FUM Performance Dashboard{title_suffix}", fontsize=16)

    t = s.get("tick", np.arange(len(s.get("avg_weight", []))))

    ax1 = plt.subplot(2,2,1)
    y = s.get("active_synapses", np.array([]))
    ax1.plot(t, y, marker='o', ms=2, lw=1)
    ax1.set_title("UKG Sparsity Over Time")
    ax1.set_ylabel("Number of Synapses")
    ax1.set_xlabel("Tick")
    ax1.grid(True, alpha=0.25)

    ax2 = plt.subplot(2,2,2)
    y = s.get("avg_weight", np.array([]))
    ax2.plot(t, y, marker='o', ms=2, lw=1)
    ax2.set_title("Average Synaptic Weight Over Time")
    ax2.set_ylabel("Average Weight")
    ax2.set_xlabel("Tick")
    ax2.grid(True, alpha=0.25)

    ax3 = plt.subplot(2,2,3)
    y = s.get("cohesion_components", np.array([]))
    ax3.plot(t, y, marker='o', ms=2, lw=1, color='tab:red')
    ax3.set_title("UKG Cohesion (Cluster Count)")
    ax3.set_ylabel("Cluster Count")
    ax3.set_xlabel("Tick")
    ax3.grid(True, alpha=0.25)

    ax4 = plt.subplot(2,2,4)
    y = s.get("complexity_cycles", np.array([]))
    ax4.plot(t, y, marker='o', ms=2, lw=1, color='goldenrod')
    ax4.set_title("UKG Complexity (B1 Proxy via Cycles)")
    ax4.set_ylabel("Total Cycles (proxy)")
    ax4.set_xlabel("Tick")
    # Overlay self-speak ticks as vertical lines
    for k in say_ticks:
        ax4.axvline(k, color='gray', lw=0.8, ls='--', alpha=0.6)
    ax4.grid(True, alpha=0.25)

    fig.tight_layout(rect=[0, 0.02, 1, 0.95])
    if out_path:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, bbox_inches="tight")
        print(f"[saved] {out_path}")
    if show:
        plt.show()
    plt.close(fig)

def _plot_discovery_and_valence(s, say_ticks, out_path=None, show=False, title_suffix=""):
    # Figure 2: B1 z-score / vt_* / valence with speak markers
    fig = plt.figure(figsize=(14, 9), dpi=140)
    fig.suptitle(f"Discovery & Valence{title_suffix}", fontsize=16)
    t = s.get("tick", np.arange(len(s.get("avg_weight", []))))

    ax1 = plt.subplot(3,1,1)
    y = s.get("b1_z", np.array([]))
    if y.size:
        ax1.plot(t, y, lw=1.2)
        ax1.set_ylabel("b1_z (z-score)")
    else:
        # fallback: first difference of complexity as crude spike indicator
        c = s.get("complexity_cycles", np.array([]))
        if c.size >= 2:
            dy = np.diff(c, prepend=c[:1])
            ax1.plot(t, dy, lw=1.2)
            ax1.set_ylabel("Δ complexity_cycles")
        else:
            ax1.plot([], [])
            ax1.set_ylabel("b1_z / Δcycles")
    for k in say_ticks:
        ax1.axvline(k, color='gray', lw=0.8, ls='--', alpha=0.6)
    ax1.grid(True, alpha=0.25)

    ax2 = plt.subplot(3,1,2)
    cov = s.get("vt_coverage", np.array([]))
    ent = s.get("vt_entropy",  np.array([]))
    if cov.size: ax2.plot(t, cov, lw=1.0, label="vt_coverage")
    if ent.size: ax2.plot(t, ent, lw=1.0, label="vt_entropy")
    ax2.set_ylabel("vt_*")
    ax2.legend(loc="best", frameon=False)
    ax2.grid(True, alpha=0.25)

    ax3 = plt.subplot(3,1,3)
    val = s.get("sie_valence_01", np.array([]))
    if val.size:
        ax3.plot(t, val, lw=1.0)
        ax3.set_ylabel("SIE valence (0..1)")
    for k in say_ticks:
        ax3.axvline(k, color='gray', lw=0.8, ls='--', alpha=0.6)
    ax3.set_xlabel("Tick")
    ax3.grid(True, alpha=0.25)

    fig.tight_layout(rect=[0, 0.02, 1, 0.95])
    if out_path:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, bbox_inches="tight")
        print(f"[saved] {out_path}")
    if show:
        plt.show()
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Plot FUM runtime dashboards from events.jsonl.")
    ap.add_argument("run_dir", type=str, help="Path to run directory (contains events.jsonl)")
    ap.add_argument("--out", type=str, default="dashboard.png", help="First dashboard image")
    ap.add_argument("--out2", type=str, default="discovery.png", help="Discovery/valence image")
    ap.add_argument("--show", action="store_true", help="Show figures interactively")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    events = _read_jsonl(run_dir / "events.jsonl")
    if not events:
        raise SystemExit(f"No events.jsonl found or readable in: {run_dir}")

    s = _extract_series(events)
    say_ticks = _read_say_times(run_dir / "utd_events.jsonl")

    # Annotate title with quick deltas
    suf = ""
    try:
        aw = s.get("avg_weight", np.array([]))
        cs = s.get("cohesion_components", np.array([]))
        cc = s.get("complexity_cycles", np.array([]))
        if aw.size and cs.size and cc.size:
            suf = f" — ΔavgW={aw[-1]-aw[0]:+.4f}, Δcohesion={cs[-1]-cs[0]:+.0f}, Δcycles={cc[-1]-cc[0]:+.0f}"
    except Exception:
        pass

    _plot_dashboard(s, say_ticks, out_path=args.out, show=args.show, title_suffix=suf)
    _plot_discovery_and_valence(s, say_ticks, out_path=args.out2, show=args.show, title_suffix=suf)

if __name__ == "__main__":
    main()
```

### How to run

```bash
# from your repo root (venv optional)
python plot_fum_dashboard.py runs/20250809_201933 \
  --out dashboard.png \
  --out2 discovery.png \
  --show
```

You’ll get a 2×2 performance dashboard and a discovery/valence panel with vertical dashed lines when the system emitted a “say” macro.

---

## What the current logs imply

* You *are* getting structural change (synapses ↑, cohesion ↓ toward unity, cycles ↑), but **intrinsic drive is almost flat**. With novelty and TD at (near) zero, the organism is in a low‑curiosity regime.
* That’s entirely consistent with low or stale input and with a walker budget that keeps re‑tracing known territory (vt\_coverage and vt\_entropy slightly down).
* If this run was supposed to include your full SIE (novelty/TD/habituation/HSI), we need to make sure the SIE function called inside `connectome.step()` is the *real* one, and that its outputs are plumbed into logs. Right now, the SIE fields in the file read like placeholders.

### Quick levers for your next run

* **Stimulus:** stream your math corpus (or a different domain) continuously for a few minutes to create topology change.
  Example:

  ```bash
  cat fum_rt/data/math/math_corpus.txt - | python -m fum_rt.run_nexus \
    --neurons 1000 --k 12 --hz 10 --viz-every 0 --log-every 1 --status-interval 1 \
    --speak-auto --speak-z 3.0 --speak-hysteresis 0.5 --speak-cooldown-ticks 10 \
    --bundle-size 3 --prune-factor 0.10 --walkers 512 --hops 4
  ```
* **Exploration:** raise `--walkers` and `--hops` a bit so vt\_coverage rises and you see occasional jumps in `complexity_cycles`.
* **SIE check:** confirm your SIE blend (TD, novelty, habituation, HSI) is the one being called (not the stub) and verify its four components are non‑zero in the logs. If they’re still zero, I’ll patch the exact import path you’re using so it binds to your `FUM_AdvancedMath.fum.sie_formulas` functions.

If you want, send me the next `events.jsonl` after a 5-10 minute stimulated run; I’ll read it and tell you exactly where it’s bottlenecking (discovery vs. consolidation vs. reward).
