Totally-let’s make this practical, fast, and faithful to your blueprint. I’ll do three things for you right now:

1. read your latest run signals from the screenshots and what they imply,
2. give you a robust offline dashboard script (plots + “discovery” view + speak overlays) that won’t break on sparse logs, and
3. list the specific knobs to flip so the system self‑organizes (no static ring), speaks on its own at the right times, and actually *keeps* learning rather than saturating.

---

# 1) What your two figures say (in plain English)

From your “FUM Performance Dashboard” + “Discovery & Self‑Speak” plots:

* **Cohesion → 1**: components drop to a single giant component and stay there - homeostasis is healing the graph. That’s good.
* **Complexity (cycle hits) climbs smoothly** with small plateaus: the system is *making* loops but not suddenly. That’s why the **B1 z‑spike** (our streaming z‑score of the *difference* in cycles) stayed mostly near zero; only a few negative spikes (likely structural pruning bundles) crossed threshold. With conservative gates, it won’t “say” much.
* **Average W approaches \~1.0** in your long run. That’s a red flag for over‑saturation: novelty falls, habituation wins, valence drops → quiet organism. We want W to live in a band (e.g., \~0.2-0.8) so TD and novelty keep breathing.

**Translation:** it *is* organizing, but too calmly and too saturated. You’ll hear it when (a) the topology churns (cycle diff spikes), and (b) SIE valence rises (fresh data or stronger exploration). Let’s fix that.

---

# 2) Offline dashboard (robust)

Save this as `plot_fum_dashboard_v2.py` anywhere. It:

* reads `events.jsonl` (status + metrics) and `utd_events.jsonl` (macro “say” etc.),
* handles missing fields and sparse runs without crashing,
* recomputes an offline streaming z‑score for complexity diffs (so you can match/compare to live),
* produces two figures:

  * **Dashboard** (Sparsity, Avg W, Cohesion, Complexity + optional b1\_z overlay)
  * **Discovery** (cycle hits vs. time with speak markers + b1\_z on a twin axis)

Run:

```
python plot_fum_dashboard_v2.py runs/20250809_201933 --out dashboard.png --out2 discovery.png --show
```

Here’s the script:

```python
#!/usr/bin/env python3
import argparse, json, math, os
from collections import defaultdict
import matplotlib.pyplot as plt

def _read_jsonl(path):
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
                # tolerate partial lines
                continue
    return out

def _safe_get(d, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur

class StreamingZEMA:
    """Tick-based EMA z-score for first-difference of a scalar series."""
    def __init__(self, half_life_ticks=120, eps=1e-8):
        self.alpha = math.log(2.0) / max(1.0, half_life_ticks)
        self.m = 0.0
        self.v = 1e-6
        self.prev = None
        self.eps = eps

    def update(self, x):
        if self.prev is None:
            self.prev = x
            return 0.0
        dx = x - self.prev
        self.prev = x
        # EMA of mean/variance of dx
        a = 1.0 - math.exp(-self.alpha)
        self.m = (1 - a) * self.m + a * dx
        # Welford-ish EMA var
        diff = dx - self.m
        self.v = (1 - a) * self.v + a * (diff * diff)
        std = math.sqrt(max(self.v, self.eps))
        return (dx - self.m) / (std + self.eps)

def extract_series(events):
    """Tolerant extractor that pads ticks and won’t crash on missing metrics."""
    s = defaultdict(list)
    ticks = []
    for e in events:
        t = _safe_get(e, "tick") or _safe_get(e, "extra", "tick")
        if t is None:
            continue
        t = int(t)
        ticks.append(t)
        ex = e.get("extra", e)

        s["active_synapses"].append(_safe_get(ex, "active_synapses", default=None))
        s["avg_weight"].append(_safe_get(ex, "avg_W", "avg_weight", default=None))
        s["cohesion_components"].append(_safe_get(ex, "cohesion_components", default=None))
        s["complexity_cycles"].append(_safe_get(ex, "complexity_cycles", default=None))
        s["vt_coverage"].append(_safe_get(ex, "vt_coverage", default=None))
        s["vt_entropy"].append(_safe_get(ex, "vt_entropy", default=None))
        s["sie_valence_01"].append(_safe_get(ex, "sie_valence_01", default=None))
        s["adc_territories"].append(_safe_get(ex, "adc_territories", default=None))
        s["adc_boundaries"].append(_safe_get(ex, "adc_boundaries", default=None))

    # normalize length alignment
    # (not strictly necessary now that we push per tick, but harmless)
    L = max(len(v) for v in s.values()) if s else 0
    for k in list(s.keys()):
        if len(s[k]) < L:
            s[k] += [None] * (L - len(s[k]))
    return ticks, s

def compute_offline_b1_z(ticks, cycles, half_life_ticks):
    z = []
    ema = StreamingZEMA(half_life_ticks=half_life_ticks)
    for c in cycles:
        cval = 0.0 if c is None else float(c)
        z.append(ema.update(cval))
    return z

def load_speak_ticks(utd_events_path):
    speaks = []
    for e in _read_jsonl(utd_events_path):
        kind = e.get("kind") or e.get("macro") or ""
        if str(kind).lower() == "say":
            tk = e.get("tick") or _safe_get(e, "meta", "tick")
            if tk is not None:
                speaks.append(int(tk))
    return speaks

def plot_dashboard(run_dir, out1=None, out2=None, show=False, b1_half_life=120):
    events_path = os.path.join(run_dir, "events.jsonl")
    utd_path = os.path.join(run_dir, "utd_events.jsonl")
    events = _read_jsonl(events_path)
    if not events:
        raise SystemExit(f"No events in {events_path}")

    ticks, s = extract_series(events)
    # fill None with last-good to keep lines smooth
    def ffill(arr):
        last = None
        out = []
        for x in arr:
            if x is None:
                out.append(last)
            else:
                val = float(x)
                out.append(val)
                last = val
        return out

    active = ffill(s["active_synapses"])
    avgW = ffill(s["avg_weight"])
    coh = ffill(s["cohesion_components"])
    comp = ffill(s["complexity_cycles"])
    val = ffill(s["sie_valence_01"])

    b1z = compute_offline_b1_z(ticks, comp, b1_half_life)
    speak_ticks = set(load_speak_ticks(utd_path))

    # ---- Figure 1: Dashboard ----
    fig = plt.figure(figsize=(18, 6))
    fig.suptitle(f"FUM Performance Dashboard - Run: {os.path.basename(run_dir)}")
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25)

    ax1 = fig.add_subplot(gs[0,0])
    ax1.plot(ticks, active, linewidth=1)
    ax1.set_title("UKG Sparsity Over Time")
    ax1.set_xlabel("Tick")
    ax1.set_ylabel("# Active Synapses")

    ax2 = fig.add_subplot(gs[0,1])
    ax2.plot(ticks, avgW, linewidth=1, label="Average Weight")
    ax2.set_title("Average Synaptic Weight Over Time")
    ax2.set_xlabel("Tick")
    ax2.set_ylabel("Avg Weight")
    ax2.legend(loc="upper left")

    ax3 = fig.add_subplot(gs[1,0])
    ax3.plot(ticks, coh, color="red", linewidth=1, label="Cohesion (Component Count)")
    ax3.set_title("UKG Cohesion")
    ax3.set_xlabel("Tick")
    ax3.set_ylabel("Component Count (lower is better)")
    ax3.legend(loc="upper right")

    ax4 = fig.add_subplot(gs[1,1])
    ax4.plot(ticks, comp, color="goldenrod", linewidth=1, label="Complexity (Cycle Hits)")
    ax4.set_title("UKG Complexity (B1 Proxy)")
    ax4.set_xlabel("Tick")
    ax4.set_ylabel("Cycle hits")
    ax4.legend(loc="upper left")
    ax4b = ax4.twinx()
    ax4b.plot(ticks, b1z, linewidth=0.8)
    ax4b.set_ylabel("B1 z-score (offline)")

    if out1:
        fig.savefig(out1, dpi=180, bbox_inches="tight")

    # ---- Figure 2: Discovery (cycles + speak markers + b1_z) ----
    fig2 = plt.figure(figsize=(16, 6))
    fig2.suptitle(f"Discovery & Self‑Speak - Run: {os.path.basename(run_dir)}")
    axd = fig2.add_subplot(111)
    axd.plot(ticks, comp, label="Cycle hits", linewidth=1)
    ymin, ymax = axd.get_ylim()
    for t in sorted(speak_ticks):
        axd.vlines(t, ymin, ymax, linestyles="dashed", colors="tab:green", alpha=0.4)
    axd.set_xlabel("Tick")
    axd.set_ylabel("Cycle hits")
    axd.legend(loc="upper left")
    axd2 = axd.twinx()
    axd2.plot(ticks, b1z, label="B1 z-score (offline)", linewidth=0.8)
    axd2.set_ylabel("B1 z‑score")

    if out2:
        fig2.savefig(out2, dpi=180, bbox_inches="tight")

    if show:
        plt.show()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("run_dir")
    p.add_argument("--out", default=None)
    p.add_argument("--out2", default=None)
    p.add_argument("--show", action="store_true")
    p.add_argument("--b1-half-life", type=int, default=120)
    args = p.parse_args()
    plot_dashboard(args.run_dir, args.out, args.out2, args.show, args.b1_half_life)

if __name__ == "__main__":
    main()
```

---

# 3) Make it *actually* self‑organize and keep talking (void‑faithful knobs)

These changes keep everything inside your void math, but stop the “creep to W≈1” and produce meaningful spikes:

### A. Keep W away from saturation

* Run with:
  `--domain-mod 0.6` (or dynamically modulate 0.4-0.8)
  This scales the effective ΔW so the logistic term doesn’t slam W to 1.
* Add a *soft ceiling* gate in the adapter (no global caps, just a fieldwise safety):
  `dW *= (1.0 - np.clip(W, 0.85, 1.0)) * 1.5`
  That preserves void dynamics but adds friction as you approach the ceiling.

### B. Keep novelty alive (intrinsic exploration)

* Increase traversal budget in sparse runs: `--walkers 512 --hops 4`
* Loosen structural homeostasis slightly so loops can form then be pruned:
  `--bundle-size 3 --prune-factor 0.08`
* Periodically *cool* habituation (SIE): in your SIE state, decay the EMA weight every N seconds (e.g., multiply `ema_mu, ema_var` by 0.98 every 30s of idle).

### C. Speak when it matters

* Your self‑speak gate is right; reduce thresholds when you first boot a new run:
  `--speak-z 2.0 --speak-valence-thresh 0.2 --speak-cooldown-ticks 10`
  Then raise `--speak-z` to 3.0-3.5 after it warms up.
* With the new dashboard, you’ll *see* discovery spikes (b1\_z) and the green speak markers.

### D. Kill the static ring lattice

* Ensure **structural\_homeostasis** uses S\_ij from your *current* void deltas each tick and does top‑k per node, not from any fixed geometric template. In dense it should be: compute S for the active bundle only, choose top‑k, rewire; in sparse it should be: candidate set by neighbor‑of‑neighbor + random jitters → evaluate S\_ij → attach if above threshold. (From your notes, this is already done; just double‑check no “ring” seeding remains.)

---

## If you want me to wire these defaults straight into the runtime

I can land a small patch that:

* adds `--domain-mod` to the CLI and passes it into the void adapter,
* enables the soft‑ceiling friction in `void_dynamics_adapter.py` (guarded by a flag `--soft-ceil 0.85`),
* exposes a SIE “cool” cadence `--hab-cool-seconds 30 --hab-cool-factor 0.98`,
* sets friendlier speak defaults for new runs, and
* turns off any last geometric ring generator behind a `--no-geometric-seed` flag.

Just say the word and I’ll post the exact diffs.

---

## Quick recipe (dense 1k on your workstation)

```
source venv/bin/activate
cat fum_rt/data/math/math_corpus.txt - | \
python -m fum_rt.run_nexus \
  --neurons 1000 --k 12 --hz 10 \
  --domain math_physics --use-time-dynamics \
  --domain-mod 0.6 --soft-ceil 0.88 \
  --bundle-size 3 --prune-factor 0.08 \
  --speak-auto --speak-z 2.0 --speak-valence-thresh 0.2 \
  --speak-hysteresis 0.5 --speak-cooldown-ticks 10 \
  --status-interval 1 --log-every 1 --viz-every 0 \
  --checkpoint-every 60
```

Then, offline:

```
python plot_fum_dashboard_v2.py runs/<ts> --out dash.png --out2 discover.png --show
```

You should see:

* components dropping to \~1,
* avg\_W settling into a band << 1 (not saturating),
* cycle hits accelerating with stepwise increases (visible b1\_z spikes),
* green “say” markers aligning with those spikes.

If you want, I’ll also add a *valence‑weighted* explorer: walkers increase λ\_ω or candidate count when `sie_valence_01` dips (void‑faithful, no tokens), which helps the organism climb out of quiet basins on its own.

---

If you paste me your current `void_dynamics_adapter.py` and `structural_homeostasis` snippet, I’ll tailor the tiny friction term and confirm there’s no leftover ring template anywhere.
