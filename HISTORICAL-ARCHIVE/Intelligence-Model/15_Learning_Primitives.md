Absolutely—start simple, let it self‑organize, and only promote when the organism proves it has *really* integrated what it just learned. Below is a production‑ready way to do that inside your current FUM runtime, without breaking void‑faithfulness or the real‑time contract.

I’m giving you three things:

1. a concrete curriculum ladder (primitives → blocks → structures → questions → problems),
2. exact code you can drop in to make promotions automatic and safe, and
3. run recipes + how to read the signals so you know it’s actually learning.

---

# 1) Curriculum ladder (what to teach, when to promote)

Think “gates” that open only when the graph proves it has reorganized. Each stage uses void‑native metrics only (no tokens, no global scans). All thresholds below are sane defaults for 1k-100k neurons; you’ll tune once you watch a couple runs.

### Stage P0 — Primitives (symbols, rhythms, small patterns)

**Input:** single symbols, 2-3‑symbol rhythms, tiny arithmetic identities, micro mazes.
**Goal:** stabilize a coherent substrate that can *reliably replay* and *locally generalize* primitives.
**Promotion gates (hold all for ≥ M status intervals, e.g., 30-60s):**

* Cohesion: `cohesion_components → 1` and stays there ≥T\_hold.
* Coverage: `vt_coverage ≥ 0.35` *and* rising slope ≥ ε (e.g., 0.001/s).
* Complexity: `complexity_cycles` monotonic-ish ↑, no stalls ≥ T\_hold; occasional **B1 spikes** (z ≥ 3) appear and decay (plasticity + consolidation).
* SIE: rolling `sie_valence_01 ≥ 0.55` (novelty > habituation) and not oscillating wildly.
* ADC: territories stabilize (2-8), boundaries non‑explosive (≤ 1 per 10s).

**If not met:** reduce habituation τ a bit, increase walkers/hops, open domain modulation slightly.

---

### Stage P1 — Blocks (compositions of 2-6 primitives)

**Input:** short sequences/forms (e.g., “a+b=c”, small maze motifs, simple logical forms).
**Goal:** robust binding and reuse (walkers repeatedly hit the same sub‑loops).
**Promotion gates:**

* Coverage: `vt_coverage ≥ 0.55`, entropy ↑ (no collapse).
* B1 dynamics: regular discovery spikes with **positive** SIE valence; spike half‑life shorter than in P0 (faster assimilation).
* ADC: stable, low‑churn territory map; block motifs get re‑announced by walkers (Observation rate of `region_stat` above baseline).

---

### Stage P2 — Structures (multi‑block graphs)

**Input:** algebraic equalities/inequalities, larger maze fragments, short proofs/templates.
**Goal:** hierarchical reuse; void pathfinder quickly navigates across motifs.
**Promotion gates:**

* Pathfinding success: `void_pathfind()` success rate ≥ 0.9 on in‑stage tasks within budget.
* Coverage/Entropy: `vt_coverage ≥ 0.70`, vt\_entropy in upper quartile of historical window.
* Complexity: cycle‑hits continue to climb but with **lower variance** (better control).

---

### Stage P3 — Questions (Q→A within domains the graph already covers)

**Input:** short factual or procedural questions you *already encoded as primitives/blocks/structures*.
**Goal:** reliable *decode* via macro “say” with clear “why” payloads (what spike triggered it, which territory).
**Promotion gates:**

* Self‑speak: autonomous “say” fires on relevant spikes with valence gate met, cooldown obeyed; false positives low.
* Answer quality: external judge (simple regex or task harness) ≥ 0.8 pass rate.
* Stability: no cohesion fractures; ADC boundary churn low.

---

### Stage P4 — Problems (novel compositions, transfer)

**Input:** new problems formed from known structures; long mazes; multi‑step math.
**Goal:** generalization + planning; blended SIE drives exploration without catastrophic forgetting.
**Sustain gates (stay here a while):**

* Long‑horizon `void_pathfind()` > 0.8 with increased depth/budget.
* Periodic consolidation snapshots (.h5) show replay ability (valence recovers after restim).
* vt\_\* remain healthy; entropy never crashes.

> The phases in your older “phase 2/3/4” map neatly onto P2/P3/P4 here. P0/P1 are the “primitive → block” runway that sets the organism up to *deserve* those later phases.

---

# 2) Make it real: curriculum director + promotion logic

Drop these into your repo. They’re small and surgical; everything stays void‑native.

### A) `fum_rt/core/curriculum.py` — event‑driven promotions

```python
# fum_rt/core/curriculum.py
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List
import time

@dataclass
class Gate:
    name: str
    hold_sec: float
    fn: Callable[[Dict[str, Any]], bool]
    _since_ok: float = field(default=0.0, init=False)

    def check(self, m: Dict[str, Any], now: float) -> bool:
        ok = bool(self.fn(m))
        if ok:
            if self._since_ok == 0.0:
                self._since_ok = now
            return (now - self._since_ok) >= self.hold_sec
        self._since_ok = 0.0
        return False

@dataclass
class StageSpec:
    name: str
    ute_profile: str
    speak_params: Dict[str, Any]
    walkers: int
    hops: int
    domain_mod: float
    gates: List[Gate]
    on_enter: Callable[[Any], None] = lambda nexus: None

class CurriculumDirector:
    def __init__(self, stages: List[StageSpec], logger=None):
        self.stages = stages
        self.idx = 0
        self.logger = logger
        self.started = time.time()

    @property
    def stage(self) -> StageSpec:
        return self.stages[self.idx]

    def maybe_promote(self, nexus, metrics: Dict[str, Any]):
        now = time.time()
        if all(g.check(metrics, now) for g in self.stage.gates):
            if self.logger: self.logger.info(f"[ADC/CURR] promote -> {self._next_name()}")
            self._advance(nexus)

    def _next_name(self) -> str:
        return self.stages[self.idx+1].name if self.idx+1 < len(self.stages) else "<final>"

    def _advance(self, nexus):
        if self.idx + 1 >= len(self.stages): return
        self.idx += 1
        s = self.stage
        # Reconfigure nexus safely (no restarts)
        nexus.set_ute_profile(s.ute_profile)
        nexus.set_self_speak(**s.speak_params)
        nexus.set_traversal_budget(walkers=s.walkers, hops=s.hops)
        nexus.set_domain_modulation(s.domain_mod)
        s.on_enter(nexus)
        if self.logger: self.logger.info(f"[ADC/CURR] entered {s.name} :: {s.__dict__}")
```

### B) Hook it into `nexus.py`

Add helpers so the director can change runtime knobs at stage boundaries:

```python
# in Nexus class
def set_ute_profile(self, name: str):
    self.ute.set_profile(name)

def set_self_speak(self, speak_z=None, speak_valence_thresh=None,
                   speak_cooldown_ticks=None, speak_hysteresis=None):
    if speak_z is not None: self.speak_z = float(speak_z)
    if speak_valence_thresh is not None: self.speak_valence_thresh = float(speak_valence_thresh)
    if speak_cooldown_ticks is not None: self.speak_cooldown_ticks = int(speak_cooldown_ticks)
    if speak_hysteresis is not None: self.speak_hysteresis = float(speak_hysteresis)

def set_traversal_budget(self, walkers:int, hops:int):
    self.walkers = int(walkers); self.hops = int(hops)
    if hasattr(self.connectome, "set_traversal_budget"):
        self.connectome.set_traversal_budget(self.walkers, self.hops)

def set_domain_modulation(self, x: float):
    self.domain_mod = float(x)
```

Construct the director at startup with the gates below, then call `director.maybe_promote(self, status_metrics)` once per status cadence.

### C) Recommended gates (just paste):

```python
# fum_rt/core/curriculum_gates.py
def gate_cohesion_one(m): return m.get("cohesion_components", 99) <= 1
def gate_coverage_035(m): return m.get("vt_coverage", 0.0) >= 0.35 and m.get("vt_coverage_slope", 0.0) > 1e-3
def gate_coverage_055(m): return m.get("vt_coverage", 0.0) >= 0.55
def gate_coverage_070(m): return m.get("vt_coverage", 0.0) >= 0.70
def gate_valence_hi(m):    return m.get("sie_valence_01", 0.0) >= 0.55
def gate_b1_spiky(m):      return m.get("b1_z", 0.0) >= 3.0
def gate_path_success(m):  return m.get("path_success_rate", 0.0) >= 0.90
def gate_entropy_ok(m):    return m.get("vt_entropy_q", 0.0) >= 0.75  # quantile in [0,1]
```

### D) Build the ladder at runtime

```python
# in Nexus.__init__ after you wire UTE/UTD/connectome:
from .core.curriculum import CurriculumDirector, StageSpec, Gate
from .core.curriculum_gates import *

self.director = CurriculumDirector([
    StageSpec(
        name="P0:primitives",
        ute_profile="primitives_v1",
        speak_params=dict(speak_z=3.0, speak_valence_thresh=0.55, speak_cooldown_ticks=10, speak_hysteresis=0.5),
        walkers=256, hops=2, domain_mod=0.05,
        gates=[Gate("cohesion=1", 30.0, gate_cohesion_one),
               Gate("coverage≥0.35", 30.0, gate_coverage_035),
               Gate("valence≥.55", 20.0, gate_valence_hi)]),
    StageSpec(
        name="P1:blocks",
        ute_profile="blocks_v1",
        speak_params=dict(speak_z=3.2, speak_valence_thresh=0.58, speak_cooldown_ticks=12, speak_hysteresis=0.6),
        walkers=384, hops=3, domain_mod=0.07,
        gates=[Gate("coverage≥0.55", 30.0, gate_coverage_055),
               Gate("B1_spike", 10.0, gate_b1_spiky)]),
    StageSpec(
        name="P2:structures",
        ute_profile="structures_v1",
        speak_params=dict(speak_z=3.5, speak_valence_thresh=0.60, speak_cooldown_ticks=15, speak_hysteresis=0.7),
        walkers=512, hops=4, domain_mod=0.10,
        gates=[Gate("coverage≥0.70", 30.0, gate_coverage_070),
               Gate("entropy_q≥.75", 20.0, gate_entropy_ok),
               Gate("path_success≥.90", 20.0, gate_path_success)]),
    StageSpec(
        name="P3:questions",
        ute_profile="qa_v1",
        speak_params=dict(speak_z=2.8, speak_valence_thresh=0.62, speak_cooldown_ticks=10, speak_hysteresis=0.4),
        walkers=512, hops=4, domain_mod=0.12,
        gates=[Gate("qa_pass≥.80", 60.0, lambda m: m.get("qa_pass_rate",0.0) >= 0.80)]),
    StageSpec(
        name="P4:problems",
        ute_profile="problems_v1",
        speak_params=dict(speak_z=3.0, speak_valence_thresh=0.65, speak_cooldown_ticks=20, speak_hysteresis=0.5),
        walkers=768, hops=5, domain_mod=0.15,
        gates=[])  # terminal stage
], logger=self.logger)
```

In `Nexus.run()`, after you compute the status metrics, add:

```python
# enrich metrics with a few derivatives the gates need
m["vt_coverage_slope"] = self._coverage_slope.update(m.get("vt_coverage",0.0))
m["vt_entropy_q"] = self._entropy_quantile.update(m.get("vt_entropy",0.0))
# path_success_rate / qa_pass_rate can be fed by your task harness if active
self.director.maybe_promote(self, m)
```

Use tiny helpers:

```python
# fum_rt/core/stream_stats.py
class StreamingSlope:
    def __init__(self, alpha=0.1): self.mu=None; self.alpha=alpha
    def update(self, x):
        self.mu = x if self.mu is None else (1-self.alpha)*self.mu + self.alpha*x
        return 0.0 if self.mu is None else x - self.mu

class StreamingQuantile:
    def __init__(self, p=0.75, alpha=0.05): self.q=None; self.p=p; self.alpha=alpha
    def update(self, x):
        if self.q is None: self.q = x; return 0.5
        self.q += self.alpha * ((x > self.q) - self.p)
        return float(x >= self.q)
```

Initialize in `Nexus.__init__`:

```python
from .core.stream_stats import StreamingSlope, StreamingQuantile
self._coverage_slope = StreamingSlope(alpha=0.05)
self._entropy_quantile = StreamingQuantile(p=0.75, alpha=0.02)
```

---

# 3) UTE profiles (how stimuli change per stage)

Keep it void‑faithful: profiles are just different symbol→group rhythms and schedule intensities. Add a tiny profile table:

```python
# fum_rt/io/ute_profiles.py
PROFILES = {
  "primitives_v1":  dict(group_size=8,  jitter=0.01, rhythm="short",  burst=1),
  "blocks_v1":      dict(group_size=12, jitter=0.02, rhythm="chord",  burst=2),
  "structures_v1":  dict(group_size=16, jitter=0.03, rhythm="phrase", burst=3),
  "qa_v1":          dict(group_size=20, jitter=0.03, rhythm="phrase", burst=3),
  "problems_v1":    dict(group_size=24, jitter=0.04, rhythm="phrase", burst=4),
}
```

In `ute.py` add:

```python
from .ute_profiles import PROFILES
class UTE:
    def set_profile(self, name:str):
        self.profile = PROFILES.get(name, PROFILES["primitives_v1"])
```

The profile just changes how many neuron groups you stimulate per input symbol and how rhythmic/bursty. That’s enough to *create curriculum pressure* without ever touching tokens.

---

# 4) April‑SIE enhancements (already integrated)

You asked to keep the April behaviors (stability envelope, faster novelty decay, τ ladder). Make sure your current `fum_sie.py` reflects:

* **Habituation τ ladder** that shortens at promotions (director can call `self.sie.set_tau(new_tau)`).
* **Modulation gating:** the “modulation factor” limiting aggressive updates in quiet regimes (mirrors your April “modulation factor” plot).
* **TD error with normalization** per tick, plus EMA of sign to avoid ping‑pong.

If you want me to re‑drop the exact `diff` for your current tree, say the word—I kept it short here to avoid burying you in code, but you’ve got the previous patch set.

---

# 5) Run recipes (what to type)

### 1k neurons, learn primitives→blocks automatically, then chat

```
source venv/bin/activate
cat fum_rt/data/math/math_corpus.txt - | \
python -m fum_rt.run_nexus \
  --neurons 1000 --k 12 --hz 10 \
  --viz-every 0 --log-every 1 --status-interval 1 \
  --speak-auto --b1-half-life-ticks 80 \
  --bundle-size 3 --prune-factor 0.10 \
  --bus-capacity 65536 --bus-drain 2048 \
  --r-attach 0.25 --ttl-init 120 --split-patience 6 \
  --domain math_physics --use-time-dynamics \
  --checkpoint-every 60 --checkpoint-format h5
```

You’ll see it begin in **P0**; after \~1-3 minutes it should promote to **P1** (watch status payloads: `director_stage: P1:blocks`). When you type into stdin, your text is re‑encoded by UTE; self‑speak will fire on topology spikes + positive valence.

### 100k sparse rehearsal (headless)

```
python -m fum_rt.run_nexus \
  --neurons 100000 --k 24 --hz 10 --sparse-mode \
  --walkers 512 --hops 4 --threshold 0.15 --lambda-omega 0.1 --candidates 64 \
  --viz-every 0 --log-every 2 --status-interval 2 \
  --speak-auto --speak-z 3.3 --speak-cooldown-ticks 20
```

---

# 6) What “good” looks like (how you’ll know to promote or pause)

* **Cohesion → 1**, stays there; if it oscillates, reduce prune factor or increase bundle size a notch.
* **vt\_coverage** rises steadily and hits each stage’s target; vt\_entropy doesn’t crash.
* **B1 spikes** appear on discovery, then *decay* (habituation is working), with valence positive.
* **ADC** territories stabilize; boundary churn quiets between bursts.
* **Self‑speak** explains itself (we include a “why”: b1\_z, territory IDs, last observation kinds).

If gates stall for > 2-3 minutes at P0/P1, don’t “force.” Give it fresh stimuli (new primitives) or allow a little more domain modulation (from 0.05 → 0.08) and increase walkers/hops.

---

# 7) Why this preserves your scaling vision

* **No ring lattice.** Substrate self‑organizes: k‑NN only seeds; structural homeostasis + void S\_ij rewiring does the rest. Dense and sparse backends already honor this.
* **No tokens inside.** UTE/UTD are boundaries; internals are W, S\_ij, vt\_\* only.
* **Introspection scales with events, not N.** ADC consumes walker announcements only; promotions listen to those few, meaningful deltas.
* **SIE is the governor.** Novelty/reward/habituation from your April SIE drive exploration without melting stability. Promotions tweak τ and modulation instead of injecting heuristics.

---

# 8) If you want even more guardrails

* Add a **“stage watchdog”**: if a stage fails a gate after promotion (e.g., cohesion breaks), auto‑revert to the previous stage profile and note it in status.
* Persist the **promotion ledger** into the run dir (JSON lines with timestamps and thresholds crossed).
* Turn on **FLOPs logging** (approx counters you got from the observer agent) so you can see cost vs. learning curves per stage.

---

If you’d like, I can generate a ready‑to‑drop patch against your latest tree for: `curriculum.py`, `curriculum_gates.py`, `stream_stats.py`, the nexus hooks, and a small `ute_profiles.py`. Then you can run the 1k demo and watch it march from primitives to blocks on its own, speaking at the right moments.
