#!/usr/bin/env python3
import argparse, json, math, os
from typing import List, Dict, Any
from collections import defaultdict
import matplotlib.pyplot as plt

def _read_jsonl(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                # tolerate partial or invalid lines
                continue
    return out

def _safe_get(d: Any, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur

class StreamingZEMA:
    """Tick-based EMA z-score for first-difference of a scalar series."""
    def __init__(self, half_life_ticks: int = 120, eps: float = 1e-8):
        self.alpha = math.log(2.0) / max(1.0, float(half_life_ticks))
        self.m = 0.0
        self.v = 1e-6
        self.prev = None
        self.eps = float(eps)

    def update(self, x: float) -> float:
        if self.prev is None:
            self.prev = float(x)
            return 0.0
        dx = float(x) - float(self.prev)
        self.prev = float(x)
        a = 1.0 - math.exp(-self.alpha)
        self.m = (1.0 - a) * self.m + a * dx
        diff = dx - self.m
        self.v = (1.0 - a) * self.v + a * (diff * diff)
        std = math.sqrt(max(self.v, self.eps))
        return (dx - self.m) / (std + self.eps)

def extract_series(events: List[Dict[str, Any]]):
    ticks = []
    s = defaultdict(list)
    for e in events:
        t = (_safe_get(e, "t") or _safe_get(e, "tick") or
             _safe_get(e, "extra", "t") or _safe_get(e, "extra", "tick"))
        if t is None:
            continue
        try:
            tt = int(t)
        except Exception:
            try:
                tt = int(float(t))
            except Exception:
                continue
        ticks.append(tt)
        ex = e.get("extra", e)

        s["active_synapses"].append(_safe_get(ex, "active_synapses", default=None))
        s["avg_weight"].append(_safe_get(ex, "avg_weight", default=None))
        s["cohesion_components"].append(_safe_get(ex, "cohesion_components", default=None))
        s["complexity_cycles"].append(_safe_get(ex, "complexity_cycles", default=None))
        s["vt_coverage"].append(_safe_get(ex, "vt_coverage", default=None))
        s["vt_entropy"].append(_safe_get(ex, "vt_entropy", default=None))
        s["sie_valence_01"].append(_safe_get(ex, "sie_valence_01", default=None))
        s["connectome_entropy"].append(_safe_get(ex, "connectome_entropy", default=None))

    # Normalize lengths (pad with None to max length)
    L = max((len(v) for v in s.values()), default=0)
    for k in list(s.keys()):
        if len(s[k]) < L:
            s[k] += [None] * (L - len(s[k]))
    return ticks, s

def compute_offline_b1_z(cycles, half_life_ticks: int):
    ema = StreamingZEMA(half_life_ticks=half_life_ticks)
    z = []
    for c in cycles:
        cval = 0.0 if c is None else float(c)
        z.append(ema.update(cval))
    return z

def load_speak_ticks(utd_events_path: str):
    speaks = []
    for e in _read_jsonl(utd_events_path):
        name = (e.get("macro") or e.get("name") or e.get("kind") or "").lower()
        if name == "say":
            t = (e.get("tick") or e.get("t") or _safe_get(e, "meta", "tick") or _safe_get(e, "meta", "t"))
            if t is not None:
                try:
                    speaks.append(int(t))
                except Exception:
                    try:
                        speaks.append(int(float(t)))
                    except Exception:
                        pass
    return speaks

def _ffill(arr):
    out = []
    last = None
    for x in arr:
        if x is None:
            out.append(last)
        else:
            try:
                val = float(x)
            except Exception:
                val = last
            out.append(val)
            last = val
    return out

def plot_dashboard(run_dir: str, out1: str = None, out2: str = None, show: bool = False, b1_half_life: int = 120):
    events_path = os.path.join(run_dir, "events.jsonl")
    utd_path = os.path.join(run_dir, "utd_events.jsonl")
    events = _read_jsonl(events_path)
    if not events:
        raise SystemExit(f"No events found in {events_path}")
    ticks, s = extract_series(events)
    if not ticks:
        raise SystemExit("No ticks found; ensure your logger emits 't' or 'tick' in events.jsonl")

    active = _ffill(s["active_synapses"])
    avgW = _ffill(s["avg_weight"])
    coh = _ffill(s["cohesion_components"])
    comp = _ffill(s["complexity_cycles"])
    val = _ffill(s["sie_valence_01"])
    entro = _ffill(s["connectome_entropy"])

    b1z = compute_offline_b1_z(comp, b1_half_life)
    speak_ticks = set(load_speak_ticks(utd_path))

    # Figure 1: Dashboard
    fig = plt.figure(figsize=(18, 6))
    fig.suptitle(f"FUM Performance Dashboard — {os.path.basename(run_dir)}")
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25)

    ax1 = fig.add_subplot(gs[0,0])
    ax1.plot(ticks, active, linewidth=1)
    ax1.set_title("Sparsity (active synapses)")
    ax1.set_xlabel("Tick"); ax1.set_ylabel("# Active")

    ax2 = fig.add_subplot(gs[0,1])
    ax2.plot(ticks, avgW, linewidth=1, label="Avg W")
    ax2.plot(ticks, val, linewidth=1, alpha=0.7, label="SIE valence")
    ax2.set_title("Weights & Valence"); ax2.set_xlabel("Tick"); ax2.legend(loc="best")

    ax3 = fig.add_subplot(gs[1,0])
    ax3.plot(ticks, coh, color="red", linewidth=1)
    ax3.set_title("Cohesion (component count)"); ax3.set_xlabel("Tick"); ax3.set_ylabel("Components")

    ax4 = fig.add_subplot(gs[1,1])
    ax4.plot(ticks, comp, color="goldenrod", linewidth=1, label="Cycles")
    ax4.set_title("Complexity (cycle hits)"); ax4.set_xlabel("Tick"); ax4.set_ylabel("Cycle hits")
    ax4b = ax4.twinx()
    ax4b.plot(ticks, b1z, linewidth=0.8, color="tab:blue", label="B1 z")
    ax4b.set_ylabel("B1 z")
    if out1:
        fig.savefig(out1, dpi=180, bbox_inches="tight")

    # Figure 2: Discovery + speaks
    fig2 = plt.figure(figsize=(16, 6))
    fig2.suptitle(f"Discovery & Self‑Speak — {os.path.basename(run_dir)}")
    axd = fig2.add_subplot(111)
    axd.plot(ticks, comp, label="Cycle hits", linewidth=1)
    ymin, ymax = axd.get_ylim()
    if speak_ticks:
        for t in sorted(speak_ticks):
            axd.vlines(t, ymin, ymax, linestyles="dashed", colors="tab:green", alpha=0.35)
    axd.set_xlabel("Tick"); axd.set_ylabel("Cycle hits")
    axd2 = axd.twinx()
    axd2.plot(ticks, b1z, label="B1 z (offline)", linewidth=0.9, color="tab:blue")
    axd2.set_ylabel("B1 z")
    if out2:
        fig2.savefig(out2, dpi=180, bbox_inches="tight")

    if show:
        plt.show()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("run_dir", help="Path to a run directory containing events.jsonl (and optionally utd_events.jsonl)")
    p.add_argument("--out", default=None, help="Output image for dashboard")
    p.add_argument("--out2", default=None, help="Output image for discovery view")
    p.add_argument("--show", action="store_true", help="Show figures interactively")
    p.add_argument("--b1-half-life", dest="b1_half_life", type=int, default=120, help="Half-life (ticks) for offline B1 z-score")
    args = p.parse_args()
    plot_dashboard(args.run_dir, args.out, args.out2, args.show, args.b1_half_life)

if __name__ == "__main__":
    main()