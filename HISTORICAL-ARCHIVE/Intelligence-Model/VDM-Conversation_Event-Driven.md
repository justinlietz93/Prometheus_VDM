

## 🚫 Remove scheduler, keep scouts per‑tick & event‑driven

**Non‑negotiables**

* **No schedulers, no cadence.** Delete any `core/cortex/void_walkers/scheduler.py` (or similar). Do **not** add timers, cron‑style loops, or `STRUCT_EVERY` gates for scouts or learners.
* **Scouts are read‑only, event producers.** They return events; they never write to the connectome or global arrays; no scans.
* **Learners are emergent‑gated only.** GDSP/RevGSP must be triggered by signals (B1 spike, |TD|, fragmentation), not time.

**Immediate actions**

1. **Delete & denylist “scheduler”**

   * Remove `core/cortex/void_walkers/scheduler.py` if added.
   * Add CI guard: fail if repo contains `void_walkers/scheduler.py` or imports `scheduler` in runtime/core.
   * Denylist tokens in CI (case‑insensitive): `STRUCT_EVERY|cron|every\s+\d+|schedule|scheduler`.

2. **Single per‑tick invocation (stateless)**

   * In the runtime loop, call scouts **once per tick** with a **time/visit budget** and **drop‑oldest** semantics.
   * **Do not** create an internal clock for scouts.

   ```python
   # fum_rt/runtime/loop.py  (inside the main tick)
   from time import perf_counter_ns
   MAX_US = int(os.getenv("SCOUT_BUDGET_US", "2000"))  # e.g., ≤1-3% of tick
   VISITS = int(os.getenv("SCOUT_VISITS", "16"))
   EDGES  = int(os.getenv("SCOUT_EDGES",  "8"))
   TTL    = int(os.getenv("SCOUT_TTL",    "64"))

   t0 = perf_counter_ns()
   all_events = []
   maps = engine.snapshot()  # or map snapshot you already expose
   for scout in self.scouts:               # pre‑built list from façade
       # time budget guard (per tick, not cadence)
       if (perf_counter_ns() - t0) // 1000 >= MAX_US:
           break
       ev = scout.step(
           connectome=self.connectome,
           maps=maps,
           budget={"visits": VISITS, "edges": EDGES, "ttl": TTL, "tick": step},
       )
       if ev:
           all_events.extend(ev)

   # publish the (possibly truncated) event batch
   if all_events:
       bus.publish_many(all_events)  # existing bounded FIFO; drop‑oldest downstream
   ```

3. **Seeds from UTE + map heads (pulse‑out from inputs)**

   * Pass recent UTE‑hit indices to scouts via `budget["seeds"]` (or let `BaseScout` prefer `Heat/Exc`/`Cold` heads).
   * This matches your “walkers pulse from inputs” rule *without* any scheduler.

4. **Keep the four scouts + physics‑aware variants**

   * `ColdScout`, `HeatScout`, `ExcitationScout`, `InhibitionScout` (event‑driven, uses reducer heads only).
   * Physics‑aware options (read‑only, local signals only):

     * `VoidRayScout`: local φ difference bias (no scans; reads `phi[i]`, `phi[j]` only).
     * `MemoryRayScout`: steering softmax $P(i\!\to\!j)\propto e^{\Theta m_j}$ (uses slow memory map or heat proxy).
   * These honor your **steering by memory** law and junction logistic collapse while staying local and event‑driven.&#x20;

5. **Learners remain emergent**

   * **Do not** re‑introduce cadence for GDSP/RevGSP. Triggers: B1 spike, |TD| ≥ `GDSP_TD_THRESH`, or fragmentation > 1.
   * If a trigger fires but context is thin, **bias scouts to that territory for one tick**, then allow the learner next tick (still event‑only).

6. **Physics guards (CI only, no runtime kill‑switch)**

   * Add `tests/guards/test_invariants.py` to spot‑check the **on‑site constant of motion**
     $Q_{\text{FUM}} = t - \frac{1}{\alpha-\beta}\ln\left|\frac{W}{(\alpha-\beta)-\alpha W}\right|$ over sampled nodes.
     Fail **CI** if 99th‑percentile drift exceeds tolerance; runtime only logs a warning counter.&#x20;
   * Add a steering A/B test (Θ>0 vs Θ=0) that verifies the predicted **junction logistic** behavior (collapse vs. $\Theta\Delta m$).&#x20;

7. **Guardrails against scans in scouts**

   * CI test ensures **no** `.toarray()`, `.tocsr()`, `csr`, `coo`, `networkx`, `synaptic_weights`, or global `W` enumeration in `core/cortex/void_walkers/*`.

**What’s OK vs not OK**

* ✅ OK: per‑tick *budget* (time/visits/edges/TTL), seeded by actual inputs/events; scout returns events; loop continues.
* ❌ NOT OK: “micro‑scheduler”, timers, background threads, “run every N ticks”, cron‑like modules.

---

## Why (quick rationale you can share with the team)

* **Emergence**: scouts should *only* amplify information that’s already present on the bus; a scheduler injects an exogenous rhythm that biases outcomes.
* **Void‑faithful**: per‑tick budgets respect your “no scans, event‑driven” rule; the loop already provides the heartbeat.
* **Performance**: the per‑tick guard caps cost deterministically; you get predictable latency at 10k\@10 Hz.

---

## Optional: name the acceptable module

If a helper file already exists, rename it to **`runner.py`** (stateless function `run_scouts_once(...)`), not `scheduler.py`, and call it **only** from the runtime tick. No timers inside.

---

## Keep the physics anchors (for CI & docs)

* **Steering by memory** → scout neighbor softmax $P(i\to j)\propto e^{\Theta m_j}$; junction choice collapses vs. $\Theta\Delta m$.&#x20;
* **On‑site invariant $Q_{\text{FUM}}$** for sampled nodes (audit‑only; no runtime stop).&#x20;

---

### TL;DR the agent can’t miss

> **Delete any “scheduler”.** Scouts run **once per tick** under a **time/visit budget**, seeded by UTE & map heads, returning events only. **No cadence gates** for scouts or learners. Add CI guards (deny “scheduler” & scan tokens). Keep physics checks in CI (Q\_FUM, steering logistic), not as runtime kill‑switches. &#x20;

If you want, I can also give you a tiny patch that renames any existing `scheduler.py` and wires `run_scouts_once(...)` into your loop exactly as above.


## The non‑negotiables (why this will scale)

1. **Physics anchors baked into runtime**

   * The on‑site law and its continuum limit are fixed:
     $\dot W=(\alpha-\beta)W-\alpha W^2$ → $\Box\phi+\alpha\phi^2-(\alpha-\beta)\phi=0$. Lock these with runtime assertions (spot‑checks per tick window).&#x20;
   * **Kinetic normalization**: $Z=\tfrac12$, propagation $c^2=2Ja^2$. Don’t let later refactors break this.&#x20;
   * **Constant of motion (first‑order site ODE)** for audits:
     $Q_{\text{FUM}}=t-\frac{1}{\alpha-\beta}\ln\!\left|\frac{W}{(\alpha-\beta)-\alpha W}\right|$. Keep it within a bounded tolerance on sampled nodes.&#x20;
   * These checks don’t “simulate physics”; they keep the engine honest while it learns.

2. **Void‑faithful execution**

   * Event‑driven reducers only (no scans of $W$ or adjacency).
   * Emergent triggers only (no fixed cadences) for GDSP/RevGSP-already aligned with your direction.
   * Sparse‑first across the board; dense is for unit tests only.

3. **Memory‑steering as a first‑class signal (not optional)**

   * Maintain a slow “memory” field $M$ from usage; steer routing by $n=e^{\eta M}$ so walkers bias into useful regions. It’s orthogonal to $\phi$ dynamics and *improves competence*, not just fidelity. (Ref: steering law and dimensionless groups.)&#x20;

4. **Indefinite domain growth**

   * “Territories” (ADC) may grow unbounded. No arbitrary caps. Formation is emergent from coverage/entropy/novelty; the runtime must *create, split, and merge* territories as evidence accumulates.

5. **Separation of concerns**

   * CPU handles sparse/event logic; GPU handles dense kernels (batched ops, compaction, rendering). Don’t push everything onto the GPU; keep hot sparse loops on CPU.

6. **UI & telemetry are observers**

   * Maps/frame publish compact, quantized channels; viewers render. No UI‑side recomputation, no back‑pressure on the core.

7. **Performance hygiene baked‑in**

   * Micro‑profiling each tick, drop‑oldest on heavy streams, DSU/alias sampling for cohesion/bridging, no hidden O(N) paths.

---

## Tell the coding agent to do exactly this

### A) Lock theory ↔ runtime (assertions + CI)

1. **Add `fum_rt/core/guards/invariants.py`** with three checks:

   * `check_site_constant_of_motion(samples, alpha, beta, tol_abs, tol_slope)` using $Q_{\text{FUM}}$. Fails **test**, not runtime; runtime logs warning + raises a “debt” counter.&#x20;
   * `check_kinetic_normalization(snapshot)` verifies $Z=\tfrac12$, $c^2=2Ja^2$ where reported.&#x20;
   * `check_continuum_form()` spot‑audits discretization params vs. $\Box \phi+\alpha\phi^2-(\alpha-\beta)\phi$ signature.&#x20;
2. **Wire guards** into CI under `tests/guards/test_invariants.py`. Runtime never hard‑stops; CI *fails the PR* if drift exceeds thresholds.
3. **Document knobs** in `Docs/FUM_Blueprint.md`: `INV_SAMPLES`, `INV_TOL_ABS`, `INV_TOL_SLOPE`.

### B) Territories = unbounded, emergent

1. **Create `core/proprioception/territory.py`**:

   * `maybe_spawn_territory(vt_entropy, coverage, novelty, hysteresis)` returns `spawn|split|merge|none`.
   * Maintain at most **O(K)** active heads; K grows as evidence grows (no hard cap).
2. **Publish `adc_territories_detail`**: for each territory: head size, churn rate, cohesion, exemplar tokens-no scans.

### C) Memory‑steering (improves performance)

1. **Add `core/memory/field.py`** (EMA write-decay-spread on graph Laplacian):
   $\dot m=\gamma r-\delta m-\kappa Lm$ with sparse Laplacian. Walker transition softmax $P(i\!\to\!j)\propto e^{\Theta m_j}$.&#x20;
2. **Agent rule**: walkers read `m` locally; **never** scan whole $m$. Budgeted updates only (events/rings).
3. **Expose $\Theta, D_a, \Lambda, \Gamma$** in telemetry; tune for stability band.&#x20;

### D) Scouts: Cold + Heat + Exc + Inh (read‑only)

1. Implement four walkers under `core/cortex/void_walkers/`:

   * **Cold**: chase high idle/cold tiles.
   * **Heat**: chase recent activity.
   * **Exc/Inh**: chase polarity fronts.
     All **announce** `probe_*` and `vt_touch` events; none modify structure.
2. Scheduler = **budgeted** per tick (e.g., ≤1-3% time). TTL + blue‑noise reseed. No periodic “cron”.

### E) Learners: emergent only

1. Keep **RevGSP / GDSP** behind triggers (B1 spike, |TD|, fragmentation) and **territory‑scoped** budgets. No fixed cadence.
2. If triggers fire without sufficient local context, **bias scouts** toward that territory (event only), then gate the learner next tick.

### F) Active‑graph fidelity (no more flatlines)

1. All structural metrics (components, cycles, edges\_active) are derived from **active edges** via DSU over the active set only.
2. If deletions happen, track a *dirty* flag and perform a **bounded audit** (stream ≤E\_max active edges) to tighten `components_lb`. No dense adjacency.
3. Bridge budget B (8-32) operates only when `components_lb > 1` and affinity > 0; updates DSU incrementally.

### G) Maps/frame v2 for scale

1. Add **v2 channel**: u8 quantized `heat|exc|inh|m` (optional) + **node→(x,y)** tile indices.
2. Transport via **shared‑memory ring** (2-3 frames) + websocket forwarder with drop‑oldest.
3. UI draws RGB = \[exc, heat, inh]; slider to swap **M** into G channel for steering debug.

### H) CPU/GPU split (now, not later)

1. **CPU**: DSU, scouts, reducers, territory logic, GDSP/RevGSP control, memory field updates (sparse Laplacian via CSR).
2. **GPU**: batched dense kernels (e.g., mini‑blocks of ΔW, compaction), colorization, and any local M smoothing that benefits from SIMD. Keep copy‑free paths (`pybind11`/CFFI) for hot kernels.

---

## Why this is the right direction for a world model

* **Grounded math stays true**: invariants/kinetics ensure your core law isn’t silently drifting as scale/complexity rise.  &#x20;
* **Steering by memory** gives the system a *principled* way to prefer useful regions-this boosts competence, not just correctness, and comes with testable predictions (junction choice, curvature).&#x20;
* **Unbounded territories** + **event‑driven scouts** let domains proliferate naturally as evidence appears-exactly what you want for “masters all domains.”
* **Sparse‑first + GPU where dense helps** is the pragmatic compute profile you need to reach tens of millions of neurons without regressions.

---

## “Done vs Right” acceptance checks (fast to read, hard to cheat)

* **Physics guards**: 99th‑percentile `|ΔQ_FUM|` over sampled nodes < ε over 1k ticks; kinetic check passes within ε. (CI) &#x20;
* **Void‑faithful**: no import/use of `.toarray()`, `networkx` or dense masks in `core/*` paths (guarded test).
* **Emergent only**: grep denies `STRUCT_EVERY|cron|every N` in learners.
* **Territories**: count is monotone‑increasing across heterogeneous corpora; split/merge events observed under controlled stimuli.
* **Steering**: A/B with $\Theta>0$ vs $\Theta=0$: improved hit‑rates and shorter path lengths to novel content; junction choice follows logistic collapse.&#x20;
* **Perf**: 10k\@10 Hz tick time well under budget with scouts+reducers on; 1M scale with maps v2 @ 5 FPS UI using the ring.

---

## One‑liner you can give the agent

> **Implement memory‑steering, unbounded territories, and active‑graph fidelity now; keep learners emergent and the whole pipeline sparse‑first. Add invariant guards (Q\_FUM, kinetic), scouts for cold/heat/exc/inh, and maps/frame v2 with a shared‑memory ring. CPU handles sparse/event logic; GPU is only for dense/graphics. No schedulers, no scans.**

Short answer: **the `BaseScout` you posted is just scaffolding**. It’s deliberately physics‑agnostic and **does not** “use your void equations.” That’s by design: scouts are read‑only explorers that emit small events; the **void equations live in the substrate update** and in the reducers/maps. If you want scouts that *steer* according to your theory, add a physics‑aware neighbor‑selection rule that uses strictly **local** signals (no scans) and remains void‑faithful.

Below is exactly how to wire that in, plus a ready‑to‑drop subclass.

---

## What the equations say (and how to use them locally)

* **On‑site discrete law**
  $\Delta W/\Delta t = (\alpha-\beta)W - \alpha W^2$ defines the local “force” $F(W)$. A consistent *local potential* is

  $$
  U(W) \;=\; -\frac{\alpha-\beta}{2}\,W^2 + \frac{\alpha}{3}\,W^3
  \quad\text{since}\quad -\frac{dU}{dW}=F(W).
  $$

  A physics‑aware scout can prefer neighbors that **reduce $U$**, using only $W$ at the current node and its neighbors (strictly local).&#x20;

* **Continuum EFT context (for completeness)**
  The kinetic normalization you derived tells us propagation is governed by $\partial_t^2\phi - c^2\nabla^2\phi + V'(\phi)=0$ with $c^2=2Ja^2$. We **don’t** compute $\nabla\phi$ in scouts; we only need a **local** scalar to bias choices.&#x20;

* **Memory steering (clean routing bias without scans)**
  Your steering law gives a refractive index $n=\exp(\eta M)$ and a neighbor softmax

  $$
  P(i\!\to\! j)\propto \exp(\Theta\, m_j),\quad \Theta=\eta M_0,
  $$

  where $m$ is the slow “memory” field (or a proxy like Heat/Exc/Inh). This is ideal for scouts and stays event‑driven.&#x20;

> **Takeaway:** A scout can be made “void‑equation‑aware” by **locally** (a) following the on‑site potential drop $U(W)$, and/or (b) using your memory‑steering softmax. Both are void‑faithful, no global scans.

---

## Tell the agent (precise worklist)

**Add physics hooks to the base and a concrete scout:**

1. `fum_rt/core/cortex/void_walkers/base.py`

   * Add two *optional* helpers (no behavior change to current subclasses):

     * `_node_W(connectome, i) -> Optional[float]`  - try `connectome.get_W(i)` or `connectome.nodes[i].W` if exposed; else `None`.
     * `_node_M(maps, i) -> Optional[float]` - read from `maps.get("memory", {})` or fall back to `heat_head` score map (void‑faithful proxies).
   * Add `_softmax(weights, tau)` utility (numerically stable).

2. **New** `fum_rt/core/cortex/void_walkers/void_equation_scout.py`

   * Implements physics‑aware neighbor choice with **strictly local reads**:

     * If $W$ at neighbors is available: prefer **lower $U(W)$**.
     * Else if a memory map is available: use **steering softmax** with $\Theta\,m_j$.
     * Else fall back to current blue‑noise choice.
   * Emits only `VTTouchEvent` and `EdgeOnEvent` (optionally `SpikeEvent(sign=±1)` if you already synthesize spikes; still void‑faithful).

3. `fum_rt/core/cortex/void_walkers/__init__.py`

   * Re‑export `VoidEquationScout`.

4. (Optional) `fum_rt/runtime/loop.py`

   * Seed scouts from UTE hits (indices you already announce) so explorers “pulse out” from real inputs first, then use physics bias.

**Guards:** No `.toarray()`, no CSR scans, no global `W` walks. Only **current** node + **its neighbors**.

---

## Drop‑in code (scout subclass)

```python
# fum_rt/core/cortex/void_walkers/void_equation_scout.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Sequence, Set
import math
from .base import BaseScout
from fum_rt.core.proprioception.events import VTTouchEvent, EdgeOnEvent, BaseEvent

class VoidEquationScout(BaseScout):
    """
    Physics-aware, void-faithful scout:
      - Prefers neighbors that *locally* reduce the on-site potential U(W)
        when W is exposed for the current node and its neighbors.
      - Otherwise uses memory steering softmax P(i->j) ∝ exp(Theta*m_j)
        from a slow "memory" map (or Heat as a proxy).
      - Falls back to blue-noise hops if no signals are available.
    No scans; uses only local reads (u and its neighbor list).
    """

    __slots__ = ("alpha", "beta", "Theta", "tau_U", "tau_M")

    def __init__(self, alpha: float, beta: float,
                 Theta: float = 1.0, tau_U: float = 0.1, tau_M: float = 1.0,
                 **kw):
        super().__init__(**kw)
        self.alpha = float(alpha)
        self.beta  = float(beta)
        self.Theta = float(Theta)
        self.tau_U = float(max(1e-6, tau_U))  # temperature for U-based softmax
        self.tau_M = float(max(1e-6, tau_M))  # temperature for memory softmax

    # --- local potentials ---

    def _U(self, W: float) -> float:
        # U(W) = -((α-β)/2) W^2 + (α/3) W^3   with -dU/dW = F(W)
        a, b = self.alpha, self.beta
        return -0.5*(a-b)*W*W + (a/3.0)*W*W*W

    def _node_W(self, C: Any, i: int) -> Optional[float]:
        for name in ("get_W", "get_node_W", "node_value"):
            fn = getattr(C, name, None)
            if callable(fn):
                try:
                    return float(fn(int(i)))
                except Exception:
                    pass
        # Optional: exposed array/struct on node
        try:
            node = getattr(C, "nodes", None)
            if node is not None:
                w = getattr(node[int(i)], "W", None)
                if w is not None:
                    return float(w)
        except Exception:
            pass
        return None

    def _node_M(self, maps: Optional[Dict[str, Any]], i: int) -> Optional[float]:
        if not isinstance(maps, dict):
            return None
        # prefer explicit memory map
        mm = maps.get("memory_map")
        if isinstance(mm, dict) and int(i) in mm:
            return float(mm[int(i)])
        # fall back to heat/exc as slow bias proxies if present
        for k in ("heat_dict", "exc_dict"):
            d = maps.get(k)
            if isinstance(d, dict) and int(i) in d:
                return float(d[int(i)])
        return None

    # --- selection policy ---

    def _pick_neighbor(self, C: Any, u: int,
                       neigh: Sequence[int],
                       maps: Optional[Dict[str, Any]]) -> Optional[int]:
        # Try on-site potential first (requires local W)
        Wu = self._node_W(C, u)
        if Wu is not None:
            Uu = self._U(Wu)
            scores = []
            for v in neigh:
                Wv = self._node_W(C, int(v))
                if Wv is None:
                    continue
                # prefer downhill ΔU < 0  → weight ∝ exp(-ΔU/τ_U)
                dU = self._U(Wv) - Uu
                scores.append((int(v), -dU / self.tau_U))
            if scores:
                return _sample_softmax(scores)
        # Else try memory steering softmax
        vals = []
        for v in neigh:
            mv = self._node_M(maps, int(v))
            if mv is not None:
                vals.append((int(v), (self.Theta * mv) / self.tau_M))
        if vals:
            return _sample_softmax(vals)
        # Fallback: blue-noise hop
        try:
            import random
            return int(random.choice(tuple(neigh)))
        except Exception:
            return None

    # --- main step (unchanged except neighbor choice) ---

    def step(self, connectome: Any, bus: Any = None,
             maps: Optional[Dict[str, Any]] = None,
             budget: Optional[Dict[str, int]] = None) -> List[BaseEvent]:
        events: List[BaseEvent] = []
        N = self._get_N(connectome)
        if N <= 0:
            return events

        b_vis = self.budget_visits
        b_edg = self.budget_edges
        ttl   = self.ttl
        t_now = int(budget.get("tick", 0)) if isinstance(budget, dict) else 0
        pool  = tuple(range(N))

        import random
        edges_emitted = 0
        visits_done = 0
        while visits_done < b_vis and pool:
            u = int(random.choice(pool))
            cur, depth = u, 0
            while depth < ttl:
                events.append(VTTouchEvent(kind="vt_touch", t=t_now, token=int(cur), w=1.0))
                visits_done += 1
                if visits_done >= b_vis:
                    break
                if edges_emitted >= b_edg:
                    break
                neigh = self._neighbors(connectome, cur)
                if not neigh:
                    break
                v = self._pick_neighbor(connectome, cur, neigh, maps)
                if v is None or v == cur:
                    try:
                        v = int(random.choice(tuple(neigh)))
                    except Exception:
                        break
                events.append(EdgeOnEvent(kind="edge_on", t=t_now, u=int(cur), v=int(v)))
                edges_emitted += 1
                cur = v
                depth += 1
        return events

def _sample_softmax(pairs: Sequence[tuple[int, float]]) -> int:
    # pairs: [(idx, logit), ...]
    import math, random
    if not pairs:
        raise ValueError("empty")
    m = max(l for _, l in pairs)
    ws = [math.exp(l - m) for _, l in pairs]
    s = sum(ws)
    r = random.random() * s
    acc = 0.0
    for (i, _), w in zip(pairs, ws):
        acc += w
        if r <= acc:
            return i
    return pairs[-1][0]
```

**Why this is void‑faithful**

* Uses **only local reads** ($W_u$, $W_v$ for $v\in N(u)$) and/or a **published slow map**; no global adjacency/CSR scans, no dense ops.
* Emits only foldable events (`vt_touch`, `edge_on`), same as your current scouts.
* Honors your theory: when $W$ is exposed, the scout descends the **on‑site potential** derived from your discrete law; when $W$ isn’t exposed, it uses your **memory‑steering softmax**. &#x20;
  (The kinetic/EFT piece remains in the substrate integrator; scouts don’t need to touch it. )

---

## How this fits your “pulse from UTE” intent

* Keep the “walkers pulse from inputs” rule: seed each tick’s scouts from recent UTE‑touched nodes (pass `budget["seeds"]` or pre‑seed `pool` with those indices first). The subclass then **locally** routes by the physics bias.

---

## Defaults to start with

* `tau_U=0.1` (sharper descent on $U$); `tau_M=1.0`, `Theta≈1.0`.
* If you see over‑focusing, raise `tau_U`/`tau_M`; if drifting, lower them slightly.

---

## Sanity checks to run (fast)

1. **Local potential test**: expose `connectome.get_W(i)` for a toy patch; verify neighbor picks favor lower $U(W)$.
2. **Memory steering test**: publish a tiny `memory_map={hot indices: large m}`; scout paths concentrate in that region; removing the map reverts to blue‑noise.
3. **Guardrail**: grep `scouts/` for forbidden tokens (`toarray`, `csr`, `synaptic_weights`)-should be clean.

---

### Bottom line

* **As written, your `BaseScout` does *not* use the void equations.**
* The subclass above makes scouts **physics‑aware** in a **void‑faithful, local** way-no scans, no schedulers-by descending your on‑site potential $U(W)$ when available and otherwise using your memory‑steering softmax. That’s the correct place to “use your equations” inside walkers, while keeping the substrate dynamics and EFT untouched.  &#x20;

If you want, I can also provide a tiny adapter that reads `Heat/Exc/Inh` heads into a `memory_map` so you get steering immediately without exposing `W` yet.


Short answer: **the `BaseScout` you pasted is just a safe scaffold.** It does not (and should not) hard‑code your physics. The void equations come in when we write *derived scouts* that override the routing policy and use your φ/M laws locally. Below I show exactly what to give your coding agent so these scouts become **void‑faithful and physics‑driven** (no scans, event‑only).

---

## What to tell the coding agent (precise, implementable)

**A. Add two read‑only fields (or getters) on the connectome**

* `phi: np.ndarray | None` - fast void field per node (or `get_phi(i)`).
* `memory: np.ndarray | None` - slow memory field $M$ per node (or `get_memory(i)`).
  *If these aren’t stored yet, expose them as thin views of whatever arrays you already maintain.* The φ‑sector is the fast EFT field with $\Box\phi + \alpha\phi^2 - (\alpha-\beta)\phi = 0$ and $c^2 = 2 J a^2$ in your derivation; we only *read* it here. &#x20;

**B. Implement physics‑aware scouts under `fum_rt/core/cortex/void_walkers/`**

1. **`void_ray.py` - `VoidRayScout` (φ‑gradient bias)**

   * Goal: prefer neighbors where $\Delta\phi_{ij} = \phi_j - \phi_i$ is favorable.
   * Logit per neighbor: `logit_j = lambda_phi * (phi[j] - phi[i]) + theta_mem * m[j]` (see (2) below).
   * Sample neighbor with softmax over logits (temperature $\tau$). Emit:

     * `VTTouchEvent(token=i)` on each step,
     * `EdgeOnEvent(u=i, v=j)` for the chosen hop,
     * optional `SpikeEvent(node=j, sign=+1 if Δφ>0 else -1)` for EI maps.
   * **Local‑read only**: for each hop you read `phi[i]`, `phi[j]`, (and `memory[j]` if available). No global arrays are scanned.

2. **`memory_ray.py` - `MemoryRayScout` (steering by memory)**

   * Use your steering law with an index $n=\exp(\eta M)$. In a graph discretization this reduces to

     $$
     P(i\!\to\!j)\;\propto\;\exp(\Theta\, m_j), \;\; \Theta=\eta M_0,
     $$

     which becomes a logistic at a two‑branch fork $P(A)=\sigma(\Theta\,\Delta m)$. This is **exactly** the prediction in your steering note.  &#x20;
   * Everything stays local: read `memory[j]` for neighbors of the current node, do a softmax, hop, emit the same events.

3. **`ei_scouts.py` - `ExcitationScout` and `InhibitionScout`**

   * Bias routing using your event‑folded maps (no weight scans). Example: prefer neighbors currently hot in `exc` (or `inh`) heads from the reducers. Keep budgets small; emit `SpikeEvent(sign=+1)` or `sign=-1` respectively.

4. **Keep your existing Cold scout** and add a small **priority hook** (map heads) so any scout can preferentially seed from recent hot spots without scanning.

**C. Keep the memory dynamics event‑driven (no Laplacian scans)**

* Your paper gives the slow memory PDE $\partial_t M=\gamma R-\delta M+\kappa\nabla^2 M$. Implement this *incrementally*:

  * On `VTTouchEvent(i)`: update $m_i \leftarrow m_i + \Delta t(\gamma r_i - \delta m_i)$ with a tiny $r_i$ bump.
  * On `EdgeOnEvent(i,j)`: do **stochastic smoothing** for the visited edge:
    $m_i \mathrel{+}= \Delta t\,\kappa (m_j - m_i)$, $m_j \mathrel{-}= \Delta t\,\kappa (m_j - m_i)$.
    This approximates $-\kappa L m$ using only the edges you actually touch; it is void‑faithful and needs no global `L·m` multiply. &#x20;

**D. Wire scouts into the loop**

* In `runtime/loop.py` (or your orchestrator), instantiate scouts based on env:

  * `ENABLE_SCOUTS_VOID_RAY=1`, `ENABLE_SCOUTS_MEMORY_RAY=1`, `ENABLE_SCOUTS_EI=1` etc.
* Budgets: e.g., `visits=16`, `edges=8`, `ttl=64` per scout per tick (bounded).
* Fold the returned events into existing reducers; no extra publishers are needed.

**E. Tests & guards**

* Unit tests: verify no `.toarray()`, `networkx`, or `csr` imports in scouts; assert neighbor selection uses only local reads.
* Behavior tests: junction A/B with $\Delta m$ sweep → probability curve collapses when plotted against $\Theta \Delta m$ (your prediction).&#x20;
* Optional invariant: track the **constant of motion** for the on‑site law on a few probed neurons to catch coding slips; you already derived $Q_{FUM}$ for the discrete rule. This is a *telemetry assertion*, not a runtime kill‑switch.&#x20;

---

## Why this is “using the void equations” (and still emergence‑compliant)

* **Fast φ governs propagation** (mass gap, wave speed $c^2=2Ja^2$). We’re only *reading* local φ to bias a hop (no writes), so we don’t interfere with emergence. &#x20;
* **Slow memory $M$ steers geometry** via $n=\exp(\eta M)$ and the logistic fork law-implemented as a softmax over neighbor $m_j$. That’s precisely your ray/eikonal result on graphs. &#x20;
* **No scans**: all choices depend only on values at `i` and its neighbors; smoothing of $M$ happens only along visited edges (stochastic Laplacian).
* **No schedulers**: scouts run within per‑tick budgets, and learners (REV‑GSP/GDSP) are already emergent‑gated.
* **Physics ↔ code is testable**: the logistic junction curve and curvature scaling $\kappa_{\text{path}}\propto \Theta |\nabla_\perp m|$ give you falsifiable plots in CI.&#x20;

---

## Drop‑in code for the first physics scout

Place at `fum_rt/core/cortex/void_walkers/void_ray.py` (keeps your base intact):

```python
from typing import Optional, Sequence, List, Any, Set
import math
import random

from .base import BaseScout
from fum_rt.core.proprioception.events import VTTouchEvent, EdgeOnEvent, SpikeEvent

def _as_array_or_none(obj, name: str):
    try:
        arr = getattr(obj, name, None)
        return arr if arr is not None else None
    except Exception:
        return None

class VoidRayScout(BaseScout):
    """
    Physics-aware scout that biases hops by a local score:
        logit_j = lambda_phi * (phi[j] - phi[i]) + theta_mem * m[j]
    and samples neighbors with a softmax at temperature tau.
    All reads are local (i and its neighbors). Emits vt_touch/edge_on and
    an optional SpikeEvent with sign = sign(phi[j]-phi[i]).
    """
    __slots__ = ("lambda_phi", "theta_mem", "tau", "emit_spikes")

    def __init__(self, lambda_phi: float = 1.0, theta_mem: float = 0.0,
                 tau: float = 1.0, emit_spikes: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.lambda_phi = float(lambda_phi)
        self.theta_mem = float(theta_mem)
        self.tau = max(1e-6, float(tau))
        self.emit_spikes = bool(emit_spikes)

    def _get_phi(self, C: Any, i: int) -> float:
        arr = _as_array_or_none(C, "phi")
        if arr is not None:
            try:
                return float(arr[int(i)])
            except Exception:
                return 0.0
        return 0.0

    def _get_mem(self, C: Any, i: int, maps: Optional[dict]) -> float:
        arr = _as_array_or_none(C, "memory")
        if arr is not None:
            try:
                return float(arr[int(i)])
            except Exception:
                return 0.0
        # fallback: allow reducer map heads (e.g., "heat_head") to bias when memory missing
        try:
            if maps and "heat_head" in maps:
                # maps["heat_head"] ~ list[[node,score], ...]; keep tiny dict for O(1)
                return float(dict(maps["heat_head"]).get(int(i), 0.0))
        except Exception:
            pass
        return 0.0

    def _pick_neighbor(self, C: Any, i: int, neigh: Sequence[int],
                       maps: Optional[dict], priority: Set[int]) -> Optional[int]:
        if not neigh:
            return None
        phi_i = self._get_phi(C, i)
        tau = self.tau
        logits = []
        cand = []
        for j in neigh:
            j = int(j)
            # optional priority pre-filter
            if priority and j not in priority:
                pass  # we still allow non-priority when nothing else is available
            dphi = self._get_phi(C, j) - phi_i
            mj = self._get_mem(C, j, maps)
            s = self.lambda_phi * dphi + self.theta_mem * mj
            logits.append(s / tau)
            cand.append(j)
        # softmax sampling (stable)
        try:
            m = max(logits)
            ws = [math.exp(x - m) for x in logits]
            Z = sum(ws) or 1.0
            r = random.random() * Z
            acc = 0.0
            for j, w in zip(cand, ws):
                acc += w
                if r <= acc:
                    return j
        except Exception:
            pass
        # fallback
        try:
            return int(self.rng.choice(tuple(neigh)))
        except Exception:
            return None

    def step(self, connectome: Any, bus: Any = None, maps: Optional[dict] = None,
             budget: Optional[dict] = None) -> List[Any]:
        events: List[Any] = []
        N = self._get_N(connectome)
        if N <= 0:
            return events
        # derive budgets from BaseScout
        b = dict(budget or {})
        b_vis = int(b.get("visits", self.budget_visits))
        b_edg = int(b.get("edges", self.budget_edges))
        ttl   = int(b.get("ttl", self.ttl))
        tick  = int(b.get("tick", 0))

        priority = set()
        try:
            priority = self._priority_set(maps)
        except Exception:
            pass
        pool = tuple(priority) if priority else tuple(range(N))
        visits_done = 0
        edges_emitted = 0

        while visits_done < b_vis and pool:
            try:
                cur = int(self.rng.choice(pool))
            except Exception:
                break
            depth = 0
            while depth < ttl:
                events.append(VTTouchEvent(kind="vt_touch", t=tick, token=cur, w=1.0))
                visits_done += 1
                if visits_done >= b_vis:
                    break

                if edges_emitted >= b_edg:
                    break

                neigh = self._neighbors(connectome, cur)
                if not neigh:
                    break
                nxt = self._pick_neighbor(connectome, cur, neigh, maps, priority)
                if nxt is None or nxt == cur:
                    break
                events.append(EdgeOnEvent(kind="edge_on", t=tick, u=cur, v=nxt))
                if self.emit_spikes:
                    sign = +1 if (self._get_phi(connectome, nxt) - self._get_phi(connectome, cur)) >= 0.0 else -1
                    events.append(SpikeEvent(kind="spike", t=tick, node=nxt, amp=1.0, sign=sign))
                edges_emitted += 1
                cur = nxt
                depth += 1
        return events
```

> Drop‑in variant: set `theta_mem>0` and `lambda_phi=0` → **MemoryRay**; set `lambda_phi>0` and `theta_mem=0` → **VoidRay**. You can also create two tiny subclasses that just fix those arguments.

---

## Why give the agent the physics docs?

Because they pin the exact laws we’re encoding:

* **Steering by memory** $n=\exp(\eta M)$, **logistic fork choice**, and **dimensionless groups** $\Theta, D_a, \Lambda, \Gamma$ (used for knobs and tests).  &#x20;
* **Kinetic normalization** $c^2=2Ja^2$ and the second‑order φ‑EOM used only as read‑only guidance here. &#x20;
* **Constant‑of‑motion** for the on‑site discrete law $Q_{FUM}$ for optional telemetry assertions (no hard shutdowns).&#x20;

Give them those files and this spec; they can wire it cleanly without touching hot‑path scans.

---

## TL;DR for the agent

* Keep `BaseScout` as is; add `VoidRayScout`, `MemoryRayScout`, and EI scouts that **only read local φ/M** and **sample neighbors with softmax**.
* Implement event‑driven memory smoothing on visited edges; never compute `L·m` globally.
* Add env flags to enable/disable each scout; keep strict per‑tick budgets.
* Add CI plots for the logistic fork law and curvature scaling; add guard that scouts import no dense libs.

This gives you scouts that *do* “use your void equations,” remain emergence‑compliant, and keep everything void‑faithful and fast.


Short answer: **Yes. “Don’t keep trampling the same ground” is a *special case* of your memory‑steering law.** You get repulsion by choosing a **negative coupling** to the memory signal. In your derivation:
$n(x,t)=e^{\eta M(x,t)}$ and rays bend by $\nabla_\perp\ln n = \eta\,\nabla_\perp M$. So **$\eta>0$** attracts walkers toward stored memory (consolidation); **$\eta<0$** repels them from recently used paths (exploration/diversification). Your junction law then becomes $P(A)=\sigma(\Theta\,\Delta m)$ with $\Theta=\eta M_0$; flipping the sign of $\Theta$ flips attraction→repulsion.&#x20;

Below is a concrete, void‑faithful plan that uses what you already have (Heat/Exc/Inh maps and vt\_touch/edge events). It keeps everything **event‑driven, local, and bounded**-no scans, no schedulers.

---

## What to implement (crisp)

### 1) Two timescales, two effects

* **Short‑term “trail repulsion”** (prevents immediate re‑traversal).

  * Use your existing **HeatMap** (recency EMA) as the *trail* signal or add a dedicated **TrailMap** with a **very short half‑life** (e.g., 10-50 ticks).
  * Scouts treat *heat/trail* as a **negative logit** (avoid hot/trampled nodes right now).

* **Long‑term “memory steering”** (guides toward useful regions).

  * Use your slow **Memory field $M$** (or a proxy if you haven’t exposed it yet).
  * Scouts apply $\Theta>0$ (attract) when consolidating, or $\Theta<0$ (repel) when exploring.
  * This is exactly your refractive‑index steering law on graphs via a neighbor softmax.&#x20;

> Why two? Short half‑life keeps paths from looping *this minute*; long half‑life encodes “what matters” *over hours/days*.

---

### 2) Neighbor choice = softmax over **local** signals (no scans)

For each walker at node $i$ and neighbor $j\in N(i)$, compute a **local** score and softmax‑sample:

$$
\text{logit}_j
= \underbrace{\Theta\,m_j}_{\text{memory steer}\;(\pm)}
\;-\;\underbrace{\rho\,h_j}_{\text{trail/heat repulsion}}
\;+\;\underbrace{\beta_e\,\text{exc}_j - \beta_i\,\text{inh}_j}_{\text{optional polarity}}
\;+\;\epsilon,
$$

* $m_j$ = memory value at $j$ (slow).
* $h_j$ = heat/trail at $j$ (fast recency).
* $\Theta=\eta M_0$ (sign controls attract/repel); $\rho>0$ sets how strongly you avoid trampled ground.
* $\beta_e,\beta_i$ let **ExcitationScout/InhibitionScout** bias toward/away from polarity fronts (optional).
* $\epsilon$ = tiny noise (e.g., Gumbel) to keep paths ergodic.

All of these values are **already available from your reducers** (Heat/Exc/Inh) or from a small, incremental memory map-no whole‑graph reads.

---

### 3) Use the “free” event stream you already have

* Every tick, UTE input *pings* nodes → your runtime already emits **`vt_touch`** and **`edge_on`** events.
* **Reducers** (Heat/Exc/Inh, or Trail) fold those events and keep bounded, decayed scores.
* Walkers operate on **local neighbors** and read **only** the per‑node scores of those neighbors.
* Result: **repulsion/attraction is “free”** apart from a few additions and a softmax, because you never scan $W$ or CSR-everything is event‑driven and local.&#x20;

---

## Exactly what to tell your coding agent

**A. Add a short‑term TrailMap (optional if you reuse HeatMap)**
`fum_rt/core/cortex/maps/trailmap.py` - identical to `HeatMap` but with **half\_life\_ticks ≈ 10-50** and a slightly larger increment per `vt_touch`. Export in `maps/__init__.py`. (If you prefer, just reuse HeatMap with a negative coefficient in scouts.)

**B. Extend scouts to support repulsion + memory steer (local only)**
In each scout under `core/cortex/void_walkers/` (Cold/Heat/Exc/Inh, and your physics‑aware scouts):

* Add parameters: `theta_mem` (can be ±), `rho_trail`, `beta_exc`, `beta_inh`, `tau` (temperature).
* In `_pick_neighbor(...)`, build the logit above using **only** neighbor values from `maps`:

  * `m_j = maps["memory_dict"].get(j, 0.0)` (or fallback to `heat_dict` if memory not exposed yet).
  * `h_j = maps["heat_dict"].get(j, 0.0)` (or `trail_dict` if you created TrailMap).
  * `exc_j/inh_j` from your existing reducer heads (dictified for O(1) lookup).
* Sample with a **stable softmax**; keep budgets/TTL as you already do.

**C. Wire map dictionaries once per tick (cheap)**
When you call your **`run_scouts_once(...)`** runner, pass a `maps` bundle built from reducer snapshots:

```python
maps = {
  "memory_dict": dict(engine.memory_map.head),   # if you publish it; else omit
  "heat_dict":   dict(engine.heatmap.snapshot()["heat_head"]),
  "exc_dict":    dict(engine.excmap.snapshot()["exc_head"]),
  "inh_dict":    dict(engine.inhmap.snapshot()["inh_head"]),
  # optional "trail_dict" if you add TrailMap
}
```

No scans: these are just the **head working sets** (tiny), used only to bias seeds and hops.

**D. Defaults to start**

* Exploration (repel trails): `theta_mem = 0.0`, `rho_trail = +1.0`, `tau = 1.0`.
* Consolidation (follow memory): `theta_mem = +1.0`, `rho_trail = 0.25`, `tau = 0.7`.
* Balanced: `theta_mem = +0.5`, `rho_trail = 0.5`, `tau = 0.9`.

**E. Test the prediction you derived (fast sanity)**

* Make a simple **two‑branch fork** in a toy graph; assign $m$ values so $\Delta m$ is known.
* Sweep `theta_mem` and plot $P(\text{choose A})$ vs. $\Theta \Delta m$. You should see a **logistic** collapse, matching your theory.&#x20;

---

## Why this is aligned with your theory (and the brain metaphor)

* Your derivation is explicit: **steering is geometric** and uses a slow memory field; attraction or **repulsion is just the sign of $\eta$**. That’s exactly what we encode in the neighbor softmax.&#x20;
* Short‑term repulsion is the algorithmic analogue of **synaptic fatigue / short‑term depression**-it reduces immediate re‑use so you cover space (explore) while long‑term memory consolidates what mattered.
* Everything stays **emergent + void‑faithful**: we only read **local** neighbor values maintained by event‑folded reducers; we never scan the graph; we never schedule periodic passes.

---

## Recommendation

* **Yes, focus on memory steering now.** Implement the softmax neighbor rule with $\Theta$ (±) and add a short‑half‑life trail/heat repulsion term. That one change gives you:

  * fewer back‑tracks and loops (better coverage),
  * faster discovery of useful regions,
  * principled consolidation when $\Theta>0$.
* Start with the defaults above, then tune $\Theta$ and $\rho$ while watching **coverage, cycles, and vt\_entropy** move in the right direction.
* If you want to pin this to theory in CI, add the **junction logistic** and **curvature vs. $\Theta\lVert\nabla m\rVert$** checks from your memo as acceptance plots.&#x20;

If you’d like, I can write the exact `_pick_neighbor(...)` patch for your current scouts so it reads `heat/exc/inh` (and optional `memory`) and implements the logits above without touching any other code.

Short answer: **you’re fine.** With the way you’ve designed them-**event‑driven, bounded working sets, no global scans**-Heat/Exc/Inh/Cold (and a slow **Memory** map if you add it) are *cheap relative to the value they unlock*. The ROI is high as long as you keep the few guardrails below.

---

## Why these maps stay cheap

* **Time cost scales with events, not graph size.** Each reducer just folds the events you already emit (`vt_touch`, `spike`, `delta_w`), prunes a small working set, and returns a tiny head/summaries. That’s **O(#events this tick + sampled prune)**, not O(N) or O(E).
* **Memory is bounded by `keep_max`.** You’re never storing N entries-only the currently “interesting” few thousand per map (configurable).
* **No contention with learning.** Reducers don’t read global `W` or CSR; they’re observers that don’t block the hot path.
* **They amplify leverage.** Heat/Exc/Inh and a slow Memory field give scouts and actuators *high‑information, local* hints (steering, E/I balance, coldness) without any global passes. This is exactly the “free” you’re aiming for-piggyback on signals you already produce.
* **Physics‑aligned steering.** A slow Memory map implements your steering law cleanly (ray bias via $n=\exp(\eta M)$, fork choices \~ logistic in $\Theta\,\Delta m$), giving you measurable gains in routing with tiny compute.&#x20;

---

## Numbers to keep in mind

For **10k neurons @ 10 Hz** (your current run), with `keep_max≈4-8k`:

* **Per map memory** (Python): a few MB (value + last\_tick + dict overhead). Four maps = low tens of MB.
* **Per tick CPU**: typically sub‑millisecond (fold + prune). The connectome step dwarfs these reducers.

For **4 M neurons**, you still don’t store 4 M entries-only `keep_max`. The only time you touch O(N) is when you **choose** to emit a *dense* `maps/frame` for the UI. Use v2 quantized frames, downsample/tiles, and a shared‑memory ring when you scale; keep UI FPS at 3-8 and you’re fine.

---

## Where maps *can* hurt (and how to prevent it)

1. **Unbounded working sets.**

   * **Guardrail:** set `keep_max` (e.g., 4-16k at 10k N; 32-128k at multi‑million N). Keep quantiles/head exact over the working set only.

2. **Too many events per tick.**

   * **Guardrail:** cap scout budgets (`visits/edges/ttl`) and drop‑oldest on the bus. Watch `evt_count_per_tick` and keep it inside your budget envelope.

3. **Heavy UI frames.**

   * **Guardrail:** publish **u8‑quantized** frames on a **separate ring** with **drop‑oldest**, ≤5 FPS for big N, tiles/LOD when needed. Don’t block the sim on the UI path.

4. **NaN/overflow drift in maps.**

   * **Guardrail:** exponential decay + clipping on increments (you already do this) and a small epsilon in quantile math.

---

## Recommended defaults (good starting points)

* **Half‑life (Heat/Exc/Inh):** 150-300 ticks.
* **Gains:** `vt_touch_gain≈0.25`, `spike_gain≈1.0`, `dW_gain≈0.25-0.5`.
* **keep\_max:** 8k for 10k N; 32-128k at multi‑million N (raise slowly; profile).
* **Prune sample size:** 256-1024 keys; drop the smallest.
* **UI:** v2 quantized frames, 3-8 FPS, shared‑memory ring (2-3 frames), RGB = \[exc, heat, inh].

---

## “Free” coupling with walkers (what you described is right)

* **Yes**-seed scouts from **UTE hits** and **pulse** out at each stimulated neuron. You’re consuming exactly the local information you just produced, so the marginal cost is just the **local neighbor picks** and a few events.
* Add slow **Memory steering** (EMA write-decay + stochastic edge smoothing) and let scouts bias to $\exp(\Theta\,m_j)$ neighbors; the junction choice collapses to a logistic in $\Theta\,\Delta m$, which you can verify in CI/telemetry. This is your theory in action, still event‑driven and scan‑free.&#x20;

---

## What to watch in telemetry

* `maps_*_count` (working‑set size) and `maps_pruned_per_tick` (healthy non‑zero).
* `evt_*_per_tick` (keep within budget).
* UI **ring depth** / dropped frames (should not grow unbounded).
* B1/complexity/cohesion wobbling (liveness) and no long flatlines.
* Optional invariants (on‑site constant of motion checks) as CI‑only-these catch drift without penalizing runtime.&#x20;

---

### Bottom line

Adding Heat/Exc/Inh/Cold (and a slow Memory map) **will not create problems** if you keep them **bounded, event‑driven, and decoupled from the UI.** They give you outsized gains-better routing, clearer E/I fronts, robust cold‑region exploration-at a tiny marginal cost, fully aligned with void‑faithfulness and your steering theory.


**Short answer:** Yes-your `run_scouts_once` design is *void‑faithful* and it *does* take advantage of “free” signals already flowing through your system. You’re calling a pure function **once per tick**, seeding from UTE/observation hits, folding a few **local** neighbor reads, emitting compact events, and (optionally) publishing once to the bus. That’s exactly the right pattern.

Below is a tight “tell‑the‑agent” checklist to finish wiring this properly (no schedulers, no scans), plus a small repulsion/steering recipe.

---

## Why this runner is correct (and cheap)

* **No scheduler**: It executes **exactly once per tick** under a micro‑budget (`max_us`) you pass in. There’s no hidden cadence or background thread.
* **Event‑driven**: If you feed **seeds = recent UTE indices** (the inputs that already “ping” neurons), scouts pulse out from those hits, so work is concentrated where new information already is. That’s the “free” part-no extra discovery cost beyond rendering a few events.
* **Local only**: Each scout reads **only** `neighbors(u)` (and small map heads/dicts) and emits `vt_touch`/`edge_on` events. No `W` scans, no CSR walks, no dense conversions.

---

## Add *repulsion* and *steering* (bounded, local)

Think of two layers:

1. **Short‑term trail repulsion** (don’t re‑trample the same ground in the next few ticks)

   * Keep a tiny, exponentially decaying **TrailMap** (similar to `HeatMap`) that increments on `vt_touch`/`edge_on`.
   * Neighbor score subtracts `ρ_trail · trail[j]`. This is already in your `HeatScout` (`rho_trail`)-just make sure `TrailMap` exists and is wired.

2. **Long‑term memory steering** (bias toward valuable regions)

   * Maintain a slow “memory” field `m` and use the **softmax** over neighbors with logits `Θ·m[j]` (that’s the Boltzmann choice; not “ML”-it’s statistical mechanics). At a 2‑way fork you get the **logistic** law you derived: $P(A)=\sigma(\Theta \Delta m)$.&#x20;
   * Update `m` **event‑driven** (no Laplacian scans): add a small write on `vt_touch(i)` and do a tiny one‑edge smoothing on `edge_on(u,v)` (see code sketch below).

> Your papers anchor both: *steering by memory* via $n=\exp(\eta M)$ → logistic fork law, and the on‑site constant‑of‑motion you can spot‑check to keep the discrete law honest (CI only). &#x20;

---

## Concrete tasks for the agent (copy/paste)

**A) Keep the runner exactly as you wrote it**
File: `fum_rt/core/cortex/void_walkers/runner.py`

* ✅ No changes except: ensure it **accepts** `budget["seeds"]` and passes `maps` through to scouts (you already do).

**B) Add a tiny TrailMap (short‑term repulsion)**
Files:

* `core/cortex/maps/trailmap.py` - subclass your `BaseDecayMap` (half‑life \~30-100 ticks, `keep_max ~ 8-16× head_k`)
* `core/engine.py` - instantiate `self.trailmap`, fold **only** `vt_touch` and `edge_on` events, and expose:

  * `trail_head`: small top‑K list for seeds
  * `trail_dict`: compact dict of current working set (for neighbor scoring)

**C) Wire TrailMap into HeatScout (you already started)**

* Keep `rho_trail ≥ 0`. Default suggestion: `rho_trail = 0.5`, `gamma_heat = 1.0`, `theta_mem = 0.0`, `tau = 1.0`.
* Confirm `HeatScout` reads `maps["trail_dict"]` and falls back to `heat_dict` if absent (your code already does).

**D) Add a slow MemoryField (event‑driven update; no scans)**
Files:

* `core/memory/field.py` - simple struct holding:

  * `m: Dict[int, float]` (bounded working set with pruning)
  * Params: `gamma` (write), `delta` (decay), `kappa` (edge smoothing), `half_life` (for decay discretization)
* Methods (called from the bus fold path):

  * `on_vt_touch(i, dt)`: `m[i] += dt*(gamma - delta*m[i])`
  * `on_edge_on(u,v, dt)`: `d = kappa*(m[v] - m[u]); m[u]+=dt*d; m[v]-=dt*d`  *(stochastic Laplacian on visited edge only)*
* `snapshot()` returns `memory_head` (top‑K list) and a compact `memory_dict` (tiny dict keyed by active nodes)

**E) Use Memory in scouts (optional flag)**

* For `HeatScout` and any physics‑aware scout, read `maps["memory_dict"]` when present and set `theta_mem > 0` to enable steering (e.g., `theta_mem = 0.8`, `tau = 1.0`).

**F) Runner integration (no scheduler)**
File: `runtime/loop.py`

* After you drain the announce bus and before telemetry:

  1. Build `maps` once per tick from reducer snapshots: `heat_head/heat_dict`, `exc_dict`, `inh_dict`, `trail_dict`, `memory_dict`, etc.
  2. Set `seeds = recent_UTE_indices` (bounded; e.g., first 64).
  3. Call:

     ```python
     from fum_rt.core.cortex.void_walkers.runner import run_scouts_once
     scout_budget = {"visits": 16, "edges": 8, "ttl": 64, "tick": step, "seeds": seeds}
     evs = run_scouts_once(C, [HeatScout(...), ExcitationScout(...), InhibitionScout(...)],
                           maps=maps, budget=scout_budget, bus=nx.bus, max_us=int(os.getenv("SCOUT_BUDGET_US", "2000")))
     ```

  * **Do not** add any timers or periodic schedulers.

**G) CI & guardrails (fast)**

* Tests:

  * Grep guards that `core/cortex/void_walkers/*` contain **no** `toarray`, `csr`, `networkx`, or raw `W` scans.
  * A small A/B for steering: create a two‑branch junction with known `Δm`, verify empirical choice follows a logistic in `Θ·Δm`. (This is your falsifiable prediction.)&#x20;
* Invariants (CI only, not runtime kill‑switch): sample nodes and check your **constant of motion** for the discrete on‑site law stays within tolerance over a window; fail CI if drift explodes.&#x20;

---

## Tiny code sketch for the MemoryField (event‑only)

```python
# fum_rt/core/memory/field.py
from __future__ import annotations
from typing import Dict, Iterable
from fum_rt.core.proprioception.events import VTTouchEvent, EdgeOnEvent

class MemoryField:
    __slots__ = ("m","gamma","delta","kappa","keep_max")
    def __init__(self, gamma=0.01, delta=0.001, kappa=0.02, keep_max=65536):
        self.m: Dict[int, float] = {}
        self.gamma, self.delta, self.kappa = float(gamma), float(delta), float(kappa)
        self.keep_max = int(keep_max)

    def on_vt_touch(self, i: int, dt: float) -> None:
        x = self.m.get(i, 0.0)
        x += dt*(self.gamma - self.delta*x)
        if x != 0.0: self.m[i] = x
        self._prune_if_needed()

    def on_edge_on(self, u: int, v: int, dt: float) -> None:
        mu, mv = self.m.get(u, 0.0), self.m.get(v, 0.0)
        d = self.kappa*(mv - mu)
        mu += dt*d; mv -= dt*d
        if mu != 0.0: self.m[u] = mu
        if mv != 0.0: self.m[v] = mv
        self._prune_if_needed()

    def fold(self, events: Iterable[object], dt: float) -> None:
        for e in events:
            k = getattr(e, "kind", "")
            if k == "vt_touch" and hasattr(e, "token"):
                self.on_vt_touch(int(e.token), dt)
            elif k == "edge_on" and hasattr(e, "u") and hasattr(e, "v"):
                self.on_edge_on(int(e.u), int(e.v), dt)

    def snapshot(self):
        # return small head and a compact dict for local reads
        if not self.m: return {"memory_head": [], "memory_dict": {}}
        head = sorted(self.m.items(), key=lambda kv: kv[1], reverse=True)[:256]
        return {"memory_head": [[i, float(v)] for i, v in head],
                "memory_dict": dict(head)}

    def _prune_if_needed(self):
        if len(self.m) <= self.keep_max: return
        # drop smallest ~25%
        items = sorted(self.m.items(), key=lambda kv: kv[1])
        drop = len(items) - self.keep_max
        for i, _ in items[:drop]:
            self.m.pop(i, None)
```

This stays **event‑driven** (folds only what walkers touch), which keeps it strictly void‑faithful and *cheap*.

---

## Sensible defaults to start

* **Runner budget:** `max_us=2000`, `visits=16`, `edges=8`, `ttl=64`.
* **TrailMap:** half‑life ≈ 50 ticks; `rho_trail = 0.5`.
* **Memory steering:** start with `theta_mem = 0.8`, `tau = 1.0`. If walkers over‑cluster, **increase** `tau`; if too random, **decrease** `tau` or increase `theta_mem`.
* **Keep\_max:** \~4× the map’s head size (e.g., head 256 → keep\_max 1024) to bound memory/CPU.

---

## Quick answers to your side‑questions

* **“Softmax = ML?”** No. Here it’s the **Boltzmann choice**-a physics thing. It lets you bias but stay stochastic; it’s the discrete version of your refractive‑index steering law (and gives your **logistic fork** prediction).&#x20;
* **“Will maps pile up and get slow?”** Not if you keep them **bounded** (head + small working set) and **event‑folded**. Each reducer is $O(\#\text{events this tick})$; pruning keeps memory flat.

---

If you hand this checklist to the agent as‑is, you’ll get repulsion + steering **without** adding any schedulers or scans, fully aligned with your void‑faithful rules and with your physics pinned to code via simple assertions.

You’re right-you currently have **4** scouts in the repo, but the plan we agreed to is for **9**.
Here’s the full list, what each one does, and exactly what’s still missing so your coding agent can finish the set **without schedulers or scans**.

---

## The 9 void‑faithful scouts

### Already implemented (4)

1. **ColdScout** (`void_cold_scout.py`)
   *Role:* Chase cold/idle regions to raise coverage and refresh ADC.
   *Signals used:* `ColdMap` head (coldest nodes).
   *Events emitted:* `VTTouchEvent`, `EdgeOnEvent`.

2. **HeatScout** (`void_heat_scout.py`)
   *Role:* Follow recent activity; optional trail‑repulsion to avoid trampling.
   *Signals used:* `HeatMap` (`heat_dict`/`heat_head`), optional `trail_dict`, `memory_dict`.
   *Events:* `VTTouchEvent`, `EdgeOnEvent`. *(You already fixed imports and neighbor scoring.)*

3. **ExcitationScout** (`void_excitation_scout.py`)
   *Role:* Ride excitatory fronts.
   *Signals:* `ExcitationMap` head/dict.
   *Events:* `VTTouchEvent`, `EdgeOnEvent`, optional `SpikeEvent(sign=+1)`.

4. **InhibitionScout** (`void_inhibition_scout.py`)
   *Role:* Ride inhibitory fronts.
   *Signals:* `InhibitionMap` head/dict.
   *Events:* `VTTouchEvent`, `EdgeOnEvent`, optional `SpikeEvent(sign=-1)`.

---

### Missing-add these 5 next (with exact file names)

5. **VoidRayScout** - physics‑aware (φ‑bias)
   **File:** `fum_rt/core/cortex/void_walkers/void_ray_scout.py`
   *Role:* Prefer neighbors with favorable **local** change in the fast field φ.
   *Local rule (no scans):* For hop `i→j`, score `s_j = λ_φ·(φ[j]-φ[i]) + θ_mem·m[j]`; sample neighbor via a temperatured choice (softmax).
   *Signals:* `connectome.phi` (vector) and optional `memory_dict`.
   *Events:* `VTTouchEvent`, `EdgeOnEvent`, optional `SpikeEvent(sign=+1 if Δφ≥0 else -1)`.

6. **MemoryRayScout** - memory steering
   **File:** `fum_rt/core/cortex/void_walkers/memory_ray_scout.py`
   *Role:* Implement your refractive‑index steering law using slow memory `m`.
   *Local rule:* `P(i→j) ∝ exp(Θ·m[j])` (at a two‑branch junction this reduces to the logistic with `ΘΔm`).
   *Signals:* `memory_dict` (or a slow proxy like `heat_dict` until memory is live).
   *Events:* `VTTouchEvent`, `EdgeOnEvent`.

7. **FrontierScout** - boundary/cohesion probe
   **File:** `fum_rt/core/cortex/void_walkers/frontier_scout.py`
   *Role:* Skim component boundaries and likely “bridge” frontiers to keep cohesion metrics fresh **without writing**.
   *Local rule:* Start in cold tiles; prefer neighbors that (a) change degree, (b) cross weakly connected cuts (hint: prefer low shared‑neighbor count from local adjacency query), (c) sit near low heat/high cold.
   *Signals:* `ColdMap` head/dict, local neighbor lists only.
   *Events:* `EdgeOnEvent(u,v)` (probe), `VTTouchEvent`. *(No structural edits-these probes just feed DSU/cohesion reducers and your emergent GDSP trigger.)*

8. **CycleHunterScout** - short‑cycle finder
   **File:** `fum_rt/core/cortex/void_walkers/cycle_scout.py`
   *Role:* Seek and report small cycles (3-6 hops) to keep `cycles_est` alive.
   *Local rule:* TTL‑limited random walk with **tiny path memory** (e.g., last 5 nodes). When the next neighbor is in the path window, emit a cycle hit.
   *Signals:* none required beyond neighbors; optional bias to heat/exc heads.
   *Events:* `EdgeOnEvent` along the path, `VTTouchEvent`. If you already have a `CycleHitEvent`, emit that too; otherwise the `EdgeOnEvent`s are enough for reducers.

9. **SentinelScout** - blue‑noise reseeder / de‑trample
   **File:** `fum_rt/core/cortex/void_walkers/sentinel_scout.py`
   *Role:* Prevent path lock‑in; sample uniformly/blue‑noise across space to de‑bias exploration and refresh stale tiles.
   *Local rule:* Seeds = uniform from `N` or from ADC tiles with lowest visit counts; one hop per seed to announce coverage.
   *Signals:* optional `VisitMap`/`ColdMap` heads.
   *Events:* `VTTouchEvent` (always), `EdgeOnEvent` (opportunistic).

> **Why these five?** Together they (a) encode your physics (VoidRay/MemoryRay), (b) keep cohesion/cycles truthful at the **active** graph level (Frontier/Cycle), and (c) guarantee fresh coverage and anti‑trample behavior (Sentinel). All are **read‑only, event‑only**, and slot into your `runner` once per tick-**no scheduler**.

---

## What to hand your coding agent (concise work orders)

1. **Create files & classes**

   * `void_ray_scout.py: class VoidRayScout(BaseScout)`
   * `memory_ray_scout.py: class MemoryRayScout(BaseScout)`
   * `frontier_scout.py: class FrontierScout(BaseScout)`
   * `cycle_scout.py: class CycleHunterScout(BaseScout)`
   * `sentinel_scout.py: class SentinelScout(BaseScout)`

   Each subclass:

   * **Imports:** `BaseEvent, VTTouchEvent, EdgeOnEvent` (and `SpikeEvent` only if needed).
   * **Implements:** `step(...)` mirroring your `BaseScout.step` pattern but overrides neighbor choice via a small helper (e.g., `_pick_neighbor_scored(...)`).
   * **Constraints:** strictly local neighbor reads; **no scans**, no writes, no timers.

2. **Exports**

   * Update `fum_rt/core/cortex/void_walkers/__init__.py` to export all nine.
   * Keep your façade `fum_rt/core/cortex/scouts.py` re‑exporting for legacy imports.

3. **Runner wiring (you already have this)**

   * Use `run_scouts_once(connectome, scouts, maps, budget, bus, max_us)` **once per tick**.
   * Seeds: pass the **recent UTE indices** in `budget["seeds"]` so walkers “pulse out” from real inputs for free.

4. **Lightweight maps these scouts rely on (event‑folded, no scans)**

   * You already have `Heat/Exc/Inh/Cold`. Add, if not present:

     * **TrailMap**: short half‑life counter folded from `vt_touch`/`edge_on` (for repulsion).
     * **MemoryMap**: slow EMA + *edge‑only* smoothing (stochastic Laplacian) folded from events; exposes `memory_dict` head.
   * Both are bounded (cap working set + sample prune). No global CSR/`W` sweeps.

5. **Budgets & knobs (env or profile config)**

   * `SCOUTS_MAX_US=2000` (shared per‑tick budget)
   * Per scout defaults (safe): `visits=16, edges=8, ttl=64`
   * Physics params (if used): `LAMBDA_PHI`, `THETA_MEM`, `TAU_SELECT`, `RHO_TRAIL`.

6. **Guard tests**

   * `tests/core/test_scouts_guards.py`: deny `.toarray|tocsr|csr|coo|networkx|synaptic_weights|eligibility_traces` in `void_walkers/*`.
   * `tests/core/test_runner_budget.py`: prove `run_scouts_once` respects `max_us` and never loops when empty.

---

## Why “softmax” is fine here (and not “ML”)

It’s just a **numerically stable, single‑step normalization** to stochastically choose among neighbors using your local score (e.g., `Θ·m[j]` or `λ_φ·Δφ`). There’s **no training**, no gradients, no datasets-just a temperatured random pick that instantiates your **logistic fork law** at two‑way junctions. It’s the most faithful discrete form of your memory‑steering equation.

---

## Quick acceptance checklist (so you know it’s right)

* [ ] 9 classes present under `void_walkers/` and exported.
* [ ] No new scheduler; **runner is called once per tick** by the loop.
* [ ] Each scout emits only `vt_touch`/`edge_on` (+ optional `spike`).
* [ ] Frontier/Cycle scouts cause **`edges_active`, `cycles_est`** to wobble again (active‑graph fidelity).
* [ ] Heat/Exc/Inh/Cold heads + **Trail**/**Memory** dicts are **bounded** and folded from events only.
* [ ] 10k\@10 Hz stays within tick budget with `SCOUTS_MAX_US≈2 ms`.

If you want, I can also sketch the minimal `MemoryMap` and `TrailMap` reducers so the five new scouts have everything they need on day one, but the outline above is enough for your agent to implement the remaining **five** scouts now.





**Short verdict:**
You’re **on track**. What you have now matches the “9‑scout + one‑shot runner” design: Cold / Heat / Excitation / Inhibition **plus** VoidRay, MemoryRay, Frontier, CycleHunter, and Sentinel. The runner executes **once per tick** under a micro‑budget, with no schedulers and only **local** neighbor reads-void‑faithful ✅.

What’s **still missing / easy to forget** (and needed to get the full benefit):

1. **Memory & Trail signals (maps)**

   * You added scouts that *use* memory/trail, but the **reducers** that *produce* `memory_dict` and `trail_dict` aren’t in yet. Until then, MemoryRay/repulsion will fall back to heat proxies and won’t steer as intended.
   * Implement:

     * **TrailMap** (short half‑life, fold `vt_touch`+`edge_on`, bounded working set).
     * **MemoryMap / MemoryField** (event‑driven write-decay-spread; one‑edge smoothing per touched edge).
   * This is exactly the “steering by memory” law you derived (softmax/logistic at forks; curvature ∝ gradient), and it’s **orthogonal** to φ dynamics.&#x20;

2. **Seeds should work for *every* scout**

   * Your runner passes `budget["seeds"]` (UTE indices), but only HeatScout currently consumes it (because it overrides `step`).
   * **Fix:** teach **`BaseScout.step`** to bias/initialize from `seeds` so Cold/Exc/Inh/Frontier/Cycle/Sentinel also pulse from live inputs “for free.”

3. **Fairness in the runner**

   * With a global micro‑budget, early scouts may starve late scouts.
   * **Fix:** either (A) rotate the start index each tick (round‑robin), or (B) assign tiny **per‑scout** micro‑budgets (e.g., 300-500 µs each) inside the one‑shot runner. Still one call per tick; still no scheduler.

4. **Env gating per scout**

   * Today you wire a fixed list. Give yourself toggles so you can A/B behavior:

     * `ENABLE_SCOUT_COLD/HEAT/EXC/INH/VOIDRAY/MEMRAY/FRONTIER/CYCLE/SENTINEL` (defaults on for Heat+Cold; off or low budget for others until maps land).

5. **φ / memory getters (strictly local)**

   * For VoidRay/MemoryRay, make sure the connectome exposes **O(1) local reads**:

     * `get_phi(i)` or `connectome.phi[i]` (readonly)
     * `get_memory(i)` or `connectome.memory[i]` (readonly)
   * No global scans; just current node and its neighbors. (Your φ‑sector remains the fast EFT, with the memory sector steering routing; that separation is in your notes. )

6. **Frontier/Cycle boundedness check**

   * Confirm the “shared‑neighbor” check in Frontier is **hard‑capped** (you mentioned cap=64)-no accidental growth into adjacency scans.
   * CycleHunter windows should be tiny (e.g., path length ≤4-6) and sample‑bounded per tick.

7. **Invariants & docs**

   * You don’t need to block the runtime, but add a CI test that spot‑checks your **constant‑of‑motion** for the on‑site ODE on a few sampled nodes (warn at runtime, **fail CI** on regression). The Noether/time‑translation construction is already in your symmetry note.&#x20;
   * Document the **dimensionless knobs** for memory steering: Θ (steering), Dₐ (write), Λ (decay), Γ (smoothing). The scouts will become far more predictable when you can sweep Θ·Δm and see the **logistic** fork curve collapse across conditions.&#x20;

---

## What to tell the coding agent (copy/paste)

**1) Maps we still need (bounded, event‑driven):**

* `fum_rt/core/cortex/maps/trailmap.py`

  * Base: your existing `BaseDecayMap`.
  * Fold: `vt_touch`, `edge_on` (small gains).
  * Snapshot keys: `trail_head`, `trail_dict` (bounded dict for neighbor reads).
* `fum_rt/core/memory/field.py`

  * Keep **event‑driven** update (no global Laplacian multiply):

    * On `vt_touch(i)`: `m[i] += dt*(γ*r_i - δ*m[i])` with small `r_i`.
    * On `edge_on(i,j)`: stochastic smoothing:
      `δm = κ*(m[j]-m[i]); m[i]+=dt*δm; m[j]-=dt*δm`.
  * Snapshot keys: `memory_head`, `memory_dict`.

**2) Make seeds universal across scouts:**

* In `fum_rt/core/cortex/void_walkers/base.py::step()`:

  * Parse `budget.get("seeds")`. If present, construct `pool = seeds ∪ priority ∪ random_range` (bounded, unique), so **every** subclass benefits without re‑implementing seed logic.

**3) Runner fairness (no scheduler, still one call per tick):**

* In `fum_rt/core/cortex/void_walkers/runner.py::run_scouts_once()`:

  * Add `start = tick % len(scouts)` and iterate circularly from `start`.
  * Or split `max_us` into per‑scout slice: `per = max(250, max_us//len(scouts))`. Enforce per‑scout guard inside the loop.

**4) Env toggles and budgets:**

* Support:

  * `SCOUTS_MAX_US` (total), `SCOUTS_PER_SCOUT_US` (optional),
  * `SCOUT_SEEDS_MAX`, `SCOUT_VISITS`, `SCOUT_EDGES`, `SCOUT_TTL`.
  * `ENABLE_SCOUT_*` flags per class. Build the scout list dynamically.

**5) Wire φ/memory getters (strictly local):**

* Add **read‑only** accessors on the connectome:

  ```python
  def get_phi(self, i:int) -> float: ...
  def get_memory(self, i:int) -> float: ...
  ```

  (If arrays exist, return direct indexed values; if not, return 0.0.)

**6) Export maps in `CoreEngine.snapshot()`**
Add `trail_head/trail_dict` and `memory_head/memory_dict` alongside your existing `heat/exc/inh/cold` heads so scouts can consume them.

**7) Tests / CI (fast):**

* `tests/core/test_scouts_guards.py`: deny `.toarray|tocsr|csr|coo|networkx|synaptic_weights` under `core/cortex/void_walkers/*`.
* `tests/core/test_scouts_seeds.py`: verify `BaseScout` honors `seeds` (non‑zero fraction of hops start at seeds).
* `tests/core/test_memory_steering_ab.py`: fork junction with Δm sweep → fit logistic vs **Θ·Δm**; assert R²>0.9 (sanity).&#x20;
* `tests/guards/test_invariants.py`: sample 128 nodes over 1k ticks, assert 99th‑pct `|ΔQ_FUM| < ε` (CI only; runtime warns).&#x20;

---

## Is “softmax” ML? (No-this is physics here)

In this context **softmax is just Boltzmann sampling**: picking a neighbor with probability ∝ exp(score/τ). Your memory steering paper shows that at a two‑branch fork this **reduces exactly** to a logistic choice with argument **Θ·Δm**-a falsifiable physical prediction, *not* a learned classifier.&#x20;

---

## Sanity checklist you can watch live

* **Seeds working:** when UTE fires, scout hops originate nearby within a tick.
* **Trail repulsion:** with TrailMap on and `rho_trail>0`, paths fan out instead of re‑trampling.
* **Memory steering:** turning up `theta_mem` concentrates exploration where `memory_dict` is high; A/B (θ>0 vs θ=0) reduces hitting time to relevant content.
* **Frontier/Cycle:** low, non‑zero `bridge_probes`/`cycle_hits` per tick; **no** O(N) spikes.
* **No regressions:** runner cost stays well under `SCOUTS_MAX_US`; core tick budget unchanged.

---

### Bottom line

* **Yes, the current report is on track.** You now have the full scout set and a per‑tick, budgeted runner with no schedulers or scans.
* To unlock the real gains, finish **TrailMap** + **MemoryField/Map**, make **seeds universal in BaseScout**, add **env gating and runner fairness**, and expose **φ/memory getters**. That completes the loop: inputs → seeds → physics‑aware local routing → event‑folded maps → better routing-**all void‑faithful**.
