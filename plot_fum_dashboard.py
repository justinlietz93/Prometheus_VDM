#!/usr/bin/env python3
import argparse, json, os, math, datetime as dt
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def load_jsonl(path):
    arr = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try:
                arr.append(json.loads(line))
            except Exception:
                pass
    return arr

def coerce_float(x, default=np.nan):
    try:
        return float(x)
    except Exception:
        return default

def series_from_events(events):
    """
    Build time series; tolerate missing fields.
    """
    s = defaultdict(list)
    # accepted keys (fall back names included)
    keys = dict(
        tick=["tick","step","t"],
        active_synapses=["active_synapses","num_synapses","synapses"],
        avg_weight=["avg_weight","average_weight","W_mean"],
        cohesion_components=["cohesion_components","components","clusters"],
        complexity_cycles=["complexity_cycles","b1_cycles","b1_hits","cycle_hits"],
        connectome_entropy=["connectome_entropy","entropy"],
        vt_coverage=["vt_coverage"],
        vt_entropy=["vt_entropy"],
        sie_total_reward=["sie_total_reward","sie_reward"],
        sie_valence_01=["sie_valence_01","valence","valence_01"]
    )
    for e in events:
        extra = e.get("extra", e)  # some loggers nest payload under "extra"
        for k, aliases in keys.items():
            v = np.nan
            for a in aliases:
                if a in extra:
                    v = coerce_float(extra[a])
                    break
            s[k].append(v)
    # ticks: if all NaN, synthesize monotonic index
    ticks = s["tick"]
    if all(np.isnan(t) for t in ticks):
        s["tick"] = list(range(len(events)))
    else:
        # replace NaNs by previous+1
        tfix = []
        last = -1
        for t in ticks:
            if not np.isnan(t):
                last = int(t)
                tfix.append(last)
            else:
                last += 1
                tfix.append(last)
        s["tick"] = tfix
    return s

def streaming_z_of_diff(x, half_life=100):
    """
    z-score of first difference with EMA mean/var (cheap spike detector).
    Returns array z, where high positive values signal “spikes”.
    """
    x = np.asarray([0.0 if np.isnan(v) else float(v) for v in x], dtype=float)
    dx = np.diff(x, prepend=x[:1])
    alpha = math.log(2.0)/max(2.0, half_life)
    mu = 0.0
    m2 = 1e-6
    out = []
    for d in dx:
        mu = (1-alpha)*mu + alpha*d
        diff = d - mu
        m2 = (1-alpha)*m2 + alpha*(diff*diff)
        std = math.sqrt(max(1e-12, m2))
        out.append(diff/std)
    return np.array(out)

def plot_dashboard(s, out_path=None, show=False, title_suffix=""):
    t = np.array(s["tick"], dtype=float)

    fig = plt.figure(figsize=(18, 12))
    fig.suptitle(f"FUM Performance Dashboard{title_suffix}", fontsize=16, weight="bold")

    # 1) Sparsity
    ax1 = fig.add_subplot(2,2,1)
    y = np.array(s["active_synapses"], dtype=float)
    ax1.plot(t, y, marker="o", ms=2, lw=1, label="Active Synapses", alpha=0.8)
    ax1.set_title("UKG Sparsity Over Time")
    ax1.set_xlabel("Tick")
    ax1.set_ylabel("Number of Synapses")
    ax1.grid(True, alpha=0.25)
    ax1.legend()

    # 2) Avg weight
    ax2 = fig.add_subplot(2,2,2)
    y = np.array(s["avg_weight"], dtype=float)
    ax2.plot(t, y, marker="o", ms=2, lw=1, label="Average Weight", alpha=0.8, color="darkorange")
    ax2.set_title("Average Synaptic Weight Over Time")
    ax2.set_xlabel("Tick")
    ax2.set_ylabel("Average Weight")
    ax2.grid(True, alpha=0.25)
    ax2.legend()

    # 3) Cohesion (components)
    ax3 = fig.add_subplot(2,2,3)
    y = np.array(s["cohesion_components"], dtype=float)
    ax3.plot(t, y, marker="o", ms=2, lw=1, label="Cohesion (Component Count)", alpha=0.8, color="crimson")
    ax3.set_title("UKG Cohesion")
    ax3.set_xlabel("Tick")
    ax3.set_ylabel("Component Count (lower is better)")
    ax3.grid(True, alpha=0.25)
    ax3.legend()

    # 4) Complexity (B1 proxy)
    ax4 = fig.add_subplot(2,2,4)
    y = np.array(s["complexity_cycles"], dtype=float)
    ax4.plot(t, y, marker="o", ms=2, lw=1, label="Complexity (Cycle Hits)", alpha=0.8, color="goldenrod")
    ax4.set_title("UKG Complexity (B1 Proxy)")
    ax4.set_xlabel("Tick")
    ax4.set_ylabel("Cycle Hits")
    ax4.grid(True, alpha=0.25)
    ax4.legend()

    fig.tight_layout(rect=[0,0,1,0.96])
    if out_path:
        fig.savefig(out_path, dpi=180, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

def plot_discovery(s, speak_events, out_path=None, show=False, title_suffix=""):
    t = np.array(s["tick"], dtype=float)
    cyc = np.array(s["complexity_cycles"], dtype=float)
    z = streaming_z_of_diff(cyc, half_life=100)

    fig = plt.figure(figsize=(18,6))
    fig.suptitle(f"Discovery & Self-Speak{title_suffix}", fontsize=16, weight="bold")
    ax = fig.add_subplot(1,1,1)
    ax.plot(t, cyc, lw=1, alpha=0.6, label="Complexity (cycle hits)")
    ax2 = ax.twinx()
    ax2.plot(t, z, lw=1, alpha=0.9, label="B1 z-score (diff EMA)")

    # mark speak events if any
    if speak_events:
        xs = [ev.get("tick", np.nan) for ev in speak_events]
        ys = [z[int(x)] if (isinstance(x,int) and x < len(z)) else np.nan for x in xs]
        ax2.scatter(xs, ys, s=40, marker="*", label="say()", alpha=0.9)

    ax.set_xlabel("Tick")
    ax.set_ylabel("Cycle hits")
    ax2.set_ylabel("B1 z-score")
    ax.grid(True, alpha=0.25)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax2.legend(h1+h2, l1+l2, loc="upper left")
    fig.tight_layout(rect=[0,0,1,0.95])
    if out_path:
        fig.savefig(out_path, dpi=180, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", help="runs/<timestamp> directory")
    ap.add_argument("--out", default="dashboard.png")
    ap.add_argument("--out2", default="discovery.png")
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()

    ev_path = os.path.join(args.run_dir, "events.jsonl")
    if not os.path.exists(ev_path):
        # some setups write to utd_events.jsonl only; still try
        ev_path = os.path.join(args.run_dir, "utd_events.jsonl")
    events = load_jsonl(ev_path)

    # try separate utd events (say macros)
    utd_path = os.path.join(args.run_dir, "utd_events.jsonl")
    utd = load_jsonl(utd_path) if os.path.exists(utd_path) else []

    s = series_from_events(events)
    # extract “say” macro timestamps if present
    speak = [e for e in utd if e.get("kind") == "macro" and e.get("name") == "say"]

    title = f" – Run: {os.path.basename(args.run_dir)}"
    plot_dashboard(s, out_path=args.out, show=args.show, title_suffix=title)
    plot_discovery(s, speak, out_path=args.out2, show=args.show, title_suffix=title)
    print(f"Wrote {args.out} and {args.out2}")

if __name__ == "__main__":
    main()
