Short answer: **Yes—add them as event‑driven reducers next to `ColdMap`.**
They should **never scan `W`**; they should fold only what the walkers/step loop already announce (e.g., `vt_touch`, edge samples, spikes/ΔW), keeping “void‑faithful” guarantees for ADC/cartography and metrics. This matches your blueprint and the current Cold‑Scout scaffolding. &#x20;

Below is a concrete, production‑level plan + drop‑in code.

---

## What to build (tell the agent)

**Create three reducers under `fum_rt/core/cortex/maps/`:**

1. **`HeatMap`** - short‑half‑life activity (recency‑weighted usage).
2. **`ExcitationMap`** - same as `HeatMap` but integrates **only excitatory** activity.
3. **`InhibitionMap`** - same as `HeatMap` but integrates **only inhibitory** activity.

**Strict constraints (void‑faithful):**

* **Input = events only.** No global reads of `W`, CSR, or adjacency (ADC and reducers are event‑driven).&#x20;
* **Bounded memory/time.** Keep a capped working set (`keep_max`) and sample‑based pruning (same discipline as `ColdMap`).&#x20;
* **Wire into engine loop.** Fold on the same bus events you already drain; do not introduce new global passes.&#x20;

**File worklist (exact):**

* `core/cortex/maps/base_decay_map.py` - shared bounded, exponential‑decay map base (head/p95/p99).
* `core/cortex/maps/heatmap.py` - concrete `HeatMap`.
* `core/cortex/maps/excitationmap.py` - filters excitatory events only.
* `core/cortex/maps/inhibitionmap.py` - filters inhibitory events only.
* `core/proprioception/events.py` - ensure we have `SpikeEvent` (node, sign, amp) and optional `DeltaWEvent` (node, dW).
* `core/cortex/maps/__init__.py` - re‑export the four: `ColdMap`, `HeatMap`, `ExcitationMap`, `InhibitionMap`.
* `core/engine.py` - instantiate + fold each tick; expose `evt_heat_*`, `evt_exc_*`, `evt_inh_*` in `snapshot()`.
* `runtime/loop.py` - no behavior change; keep bus‑drain → reducers → metrics, consistent with your event‑driven ADC rule.&#x20;

**Rationale & alignment**

* You already have **`ColdMap`** (monotonic in idle time, bounded, top‑K head). We copy its bounded design and add exponential **decay‑on‑touch** maps to represent “heat.”&#x20;
* This honors your doc rule: cartography/metrics are **event‑driven only; no global scans**.&#x20;
* E/I polarity is explicitly preserved in your TODO and system notes; `ExcitationMap`/`InhibitionMap` make this visible to the runtime without scanning.&#x20;

---

## Code — shared base (bounded decay map)

```python
# fum_rt/core/cortex/maps/base_decay_map.py
from __future__ import annotations
from typing import Dict, Iterable, List, Tuple
import math, random

class BaseDecayMap:
    """
    Bounded, per-node exponentially decaying accumulator.
    Void-faithful: fold() only consumes events; never scans global state.

    Score_t(node) = Score_{t-Δ} * 2^(-Δ/half_life_ticks) + sum(increments at t)

    Snapshot:
      - head_k top entries as [node, score] pairs (descending)
      - p95, p99, max summaries

    Blueprint tie-in: ADC/event-driven reducers (Rule 7); no W scans.  # see 09_First_Run_Prefixes.md
    """
    __slots__ = ("head_k", "half_life", "keep_max", "rng", "_val", "_last_tick")

    def __init__(self, head_k: int = 256, half_life_ticks: int = 200,
                 keep_max: int | None = None, seed: int = 0) -> None:
        self.head_k   = int(max(8, head_k))
        self.half_life = int(max(1, half_life_ticks))
        km = int(keep_max) if keep_max is not None else self.head_k * 16
        self.keep_max = int(max(self.head_k, km))
        self.rng = random.Random(int(seed))
        self._val: Dict[int, float] = {}
        self._last_tick: Dict[int, int] = {}

    # ----- core updates -----

    def _decay_to(self, node: int, tick: int) -> None:
        lt = self._last_tick.get(node)
        if lt is None:
            self._last_tick[node] = tick
            return
        dt = max(0, int(tick) - int(lt))
        if dt > 0:
            factor = 2.0 ** (-(dt / float(self.half_life)))
            self._val[node] *= factor
            self._last_tick[node] = tick

    def add(self, node: int, tick: int, inc: float) -> None:
        try:
            n = int(node); t = int(tick)
        except Exception:
            return
        if n < 0:
            return
        if n in self._val:
            self._decay_to(n, t)
            self._val[n] += float(inc)
        else:
            # initialize lazily with decay context
            self._val[n] = float(max(0.0, inc))
            self._last_tick[n] = t
        if len(self._val) > self.keep_max:
            self._prune()

    def _prune(self) -> None:
        # Drop a sampled set of the smallest entries (cheap, avoids full O(N) sort)
        size = len(self._val)
        target = size - self.keep_max
        if target <= 0:
            return
        keys = list(self._val.keys())
        sample_size = min(len(keys), max(256, target * 4))
        sample = self.rng.sample(keys, sample_size) if sample_size > 0 else keys
        sample.sort(key=lambda k: self._val[k])  # ascending
        for k in sample[:target]:
            self._val.pop(k, None)
            self._last_tick.pop(k, None)

    # ----- folding & snapshots -----

    def fold(self, events: Iterable[object], tick: int) -> None:
        """To be implemented by subclasses: inspect events and call add(node, tick, inc)."""
        raise NotImplementedError

    def snapshot(self) -> dict:
        if not self._val:
            return {"head": [], "p95": 0.0, "p99": 0.0, "max": 0.0, "count": 0}
        # head
        head = sorted(self._val.items(), key=lambda kv: kv[1], reverse=True)[:self.head_k]
        # quick quantiles (exact over working set)
        vals = sorted(self._val.values())
        def q(p: float) -> float:
            if not vals: return 0.0
            i = min(len(vals)-1, max(0, int(math.floor(p*(len(vals)-1)))))
            return float(vals[i])
        return {
            "head": [[int(k), float(v)] for k, v in head[:16]],
            "p95": q(0.95), "p99": q(0.99), "max": float(vals[-1]),
            "count": int(len(vals)),
        }
```

---

## Code — event types (extend once)

```python
# fum_rt/core/proprioception/events.py  (add these if not present)
from dataclasses import dataclass

@dataclass(frozen=True)
class BaseEvent:  # already exists
    kind: str
    t: int

@dataclass(frozen=True)
class VTTouchEvent(BaseEvent):  # already exists
    token: int
    w: float = 1.0

@dataclass(frozen=True)
class EdgeOnEvent(BaseEvent):  # already exists
    u: int
    v: int

# NEW (polarity-aware activity)
@dataclass(frozen=True)
class SpikeEvent(BaseEvent):
    node: int          # neuron id
    amp: float = 1.0   # activity magnitude (or |ΔW| proxy)
    sign: int = +1     # +1 excitatory, -1 inhibitory, 0 unknown

# OPTIONAL (if your step loop emits predicted/real ΔW)
@dataclass(frozen=True)
class DeltaWEvent(BaseEvent):
    node: int
    dw: float          # signed ΔW
```

> Why these events? They are **local** and can be emitted cheaply from the existing step loop and walkers. Your blueprint and “First‑Run Prefixes” explicitly push ADC/reducers to be **event‑driven** and to forbid raw `W` access.&#x20;

---

## Code — `HeatMap`, `ExcitationMap`, `InhibitionMap`

```python
# fum_rt/core/cortex/maps/heatmap.py
from __future__ import annotations
from typing import Iterable
from .base_decay_map import BaseDecayMap
from fum_rt.core.proprioception.events import VTTouchEvent, SpikeEvent, DeltaWEvent

class HeatMap(BaseDecayMap):
    """
    Recency-weighted activity map (short half-life).
    Increments on vt_touch (small) and any spike/ΔW (scaled).
    Rule 7 (ADC event-driven): no global scans. See 09_First_Run_Prefixes.md.

    Params:
      - half_life_ticks: decay half-life in ticks (e.g., 200)
      - vt_touch_gain: increment per vt_touch (e.g., 0.25)
      - spike_gain: multiplier * amp for SpikeEvent (e.g., 1.0)
      - dW_gain: multiplier * |dw| for DeltaWEvent (e.g., 0.5)
    """
    __slots__ = ("vt_touch_gain", "spike_gain", "dW_gain")

    def __init__(self, head_k=256, half_life_ticks=200, keep_max=None, seed=0,
                 vt_touch_gain: float = 0.25, spike_gain: float = 1.0, dW_gain: float = 0.5):
        super().__init__(head_k, half_life_ticks, keep_max, seed)
        self.vt_touch_gain = float(vt_touch_gain)
        self.spike_gain = float(spike_gain)
        self.dW_gain = float(dW_gain)

    def fold(self, events: Iterable[object], tick: int) -> None:
        for e in events:
            k = getattr(e, "kind", None)
            if k == "vt_touch" and isinstance(e, VTTouchEvent):
                self.add(e.token, tick, self.vt_touch_gain * float(getattr(e, "w", 1.0)))
            elif k == "spike" and isinstance(e, SpikeEvent):
                self.add(e.node, tick, self.spike_gain * float(getattr(e, "amp", 1.0)))
            elif k == "delta_w" and isinstance(e, DeltaWEvent):
                self.add(e.node, tick, self.dW_gain * abs(float(e.dw)))

    def snapshot(self) -> dict:
        s = super().snapshot()
        return {"heat_head": s["head"], "heat_p95": s["p95"], "heat_p99": s["p99"],
                "heat_max": s["max"], "heat_count": s["count"]}
```

```python
# fum_rt/core/cortex/maps/excitationmap.py
from __future__ import annotations
from typing import Iterable
from .base_decay_map import BaseDecayMap
from fum_rt.core.proprioception.events import SpikeEvent, DeltaWEvent

class ExcitationMap(BaseDecayMap):
    """
    Excitatory-only activity. Filters by sign>0 (spikes) and dw>0 (ΔW).
    """
    __slots__ = ("spike_gain", "dW_gain")

    def __init__(self, head_k=256, half_life_ticks=200, keep_max=None, seed=0,
                 spike_gain: float = 1.0, dW_gain: float = 0.5):
        super().__init__(head_k, half_life_ticks, keep_max, seed)
        self.spike_gain = float(spike_gain)
        self.dW_gain = float(dW_gain)

    def fold(self, events: Iterable[object], tick: int) -> None:
        for e in events:
            k = getattr(e, "kind", None)
            if k == "spike" and isinstance(e, SpikeEvent) and int(getattr(e, "sign", +1)) > 0:
                self.add(e.node, tick, self.spike_gain * float(getattr(e, "amp", 1.0)))
            elif k == "delta_w" and isinstance(e, DeltaWEvent) and float(getattr(e, "dw", 0.0)) > 0.0:
                self.add(e.node, tick, self.dW_gain * float(e.dw))

    def snapshot(self) -> dict:
        s = super().snapshot()
        return {"exc_head": s["head"], "exc_p95": s["p95"], "exc_p99": s["p99"],
                "exc_max": s["max"], "exc_count": s["count"]}
```

```python
# fum_rt/core/cortex/maps/inhibitionmap.py
from __future__ import annotations
from typing import Iterable
from .base_decay_map import BaseDecayMap
from fum_rt.core.proprioception.events import SpikeEvent, DeltaWEvent

class InhibitionMap(BaseDecayMap):
    """
    Inhibitory-only activity. Filters by sign<0 (spikes) and dw<0 (ΔW).
    """
    __slots__ = ("spike_gain", "dW_gain")

    def __init__(self, head_k=256, half_life_ticks=200, keep_max=None, seed=0,
                 spike_gain: float = 1.0, dW_gain: float = 0.5):
        super().__init__(head_k, half_life_ticks, keep_max, seed)
        self.spike_gain = float(spike_gain)
        self.dW_gain = float(dW_gain)

    def fold(self, events: Iterable[object], tick: int) -> None:
        for e in events:
            k = getattr(e, "kind", None)
            if k == "spike" and isinstance(e, SpikeEvent) and int(getattr(e, "sign", 0)) < 0:
                self.add(e.node, tick, self.spike_gain * float(getattr(e, "amp", 1.0)))
            elif k == "delta_w" and isinstance(e, DeltaWEvent) and float(getattr(e, "dw", 0.0)) < 0.0:
                self.add(e.node, tick, self.dW_gain * abs(float(e.dw)))

    def snapshot(self) -> dict:
        s = super().snapshot()
        return {"inh_head": s["head"], "inh_p95": s["p95"], "inh_p99": s["p99"],
                "inh_max": s["max"], "inh_count": s["count"]}
```

---

## Wiring (minimal diffs)

* **Export:**

```python
# fum_rt/core/cortex/maps/__init__.py
from .coldmap import ColdMap
from .heatmap import HeatMap
from .excitationmap import ExcitationMap
from .inhibitionmap import InhibitionMap

__all__ = ["ColdMap", "HeatMap", "ExcitationMap", "InhibitionMap"]
```

* **Engine init & fold:**

```python
# fum_rt/core/engine.py  (Phase E1/E2 style)
from fum_rt.core.cortex.maps import ColdMap, HeatMap, ExcitationMap, InhibitionMap

class CoreEngine:
    def __init__(self, ...):
        self.coldmap = ColdMap(head_k=256, half_life_ticks=200, keep_max=4096, seed=0)
        self.heatmap = HeatMap(head_k=256, half_life_ticks=200, keep_max=4096, seed=1)
        self.excmap  = ExcitationMap(head_k=256, half_life_ticks=200, keep_max=4096, seed=2)
        self.inhmap  = InhibitionMap(head_k=256, half_life_ticks=200, keep_max=4096, seed=3)
        ...

    def step(self, dt_ms: int, events: list[object]):
        # existing logic...
        # fold reducer events (no scans)
        tick = getattr(self, "tick_idx", 0)
        self.coldmap.fold([e for e in events if getattr(e, "kind", "")=="vt_touch"], tick)
        self.heatmap.fold(events, tick)
        self.excmap.fold(events, tick)
        self.inhmap.fold(events, tick)
        ...

    def snapshot(self) -> dict:
        s = {... existing metrics ...}
        s.update(self.coldmap.snapshot())
        s.update(self.heatmap.snapshot())
        s.update(self.excmap.snapshot())
        s.update(self.inhmap.snapshot())
        return s
```

> This follows your “engine.step() emits evt\_\* and merges into snapshot” parity plan and keeps ADC void‑faithful.&#x20;

---

## Cost profile & usage

* **Time:** `O(#events this tick + sampled prune)` per reducer. No `W` enumeration, no CSR scans.&#x20;
* **Memory:** `O(keep_max)` per map; pruning drops smallest scores first, just like ColdMap’s bounded tracker.&#x20;
* **Signals produced:**

  * `HeatMap`: where the network is *recently active*.
  * `ExcitationMap`/`InhibitionMap`: polarity‑specific activity fronts (useful for homeostasis, E/I balance, and where to place inhibitory/excitatory growth). Your TODO explicitly preserves E/I polarity during growth/rewire.&#x20;

---

## Why this matches your vision

* **Event‑driven cartography** (no global scans) as mandated by your First‑Run Prefixes for ADC/runtime.&#x20;
* **Cold vs Heat** separation: you already introduced **ColdMap**; Heat completes the dual: *cold = idle‑time monotone*, *heat = decayed recent activity*. Both are bounded, incremental, and walker‑compatible.&#x20;
* **E/I explicit** aligns with your growth/homeostasis plans and the broader RE‑VGSP/PLV modulation story in the blueprint; polarity matters to stability. &#x20;

---

## One caution (agent guardrail)

Do **not** try to re‑derive excitation/inhibition by peeking at `W` globally. Emit **`SpikeEvent(sign=±1)`** (or sign from node polarity) from the step loop for the active subset only, and **optionally** a `DeltaWEvent` for those nodes; reducers will fold those. This stays strictly within your “single source of truth for deltas” and void‑faithful adapter pattern.&#x20;

---

If you want, I can also provide a one‑file **`BaseEIMap`** to de‑duplicate `ExcitationMap`/`InhibitionMap`, and a tiny **CI guard** that greps for forbidden global reads inside `cortex/maps/*` (same style as your existing void‑audit).&#x20;

Would you like me to package these as ready‑to‑apply diffs against your current `fum_rt` skeleton?

Short answer: **Yes.** If you already compute the per‑node signals (e.g., firing/“heat”, net excitation, net inhibition) in the core, the cleanest design is to **publish those arrays on the global bus** and let the UI render them. That makes the visualization essentially “free” (compute‑wise) beyond **drawing pixels**. Don’t stream the whole connectome or recompute currents in the browser.

Below is a drop‑in plan + minimal code that’s fast, stable, and production‑friendly.

---

## What to publish (and what *not* to publish)

**Publish (per tick):**

* `tick`: uint64
* `shape`: `[H, W]` or just `N` + a mapping from node→(x,y)
* **Float32** arrays (binary) for:

  * `heat`: smoothed firing rate (EMA of `r_i`)
  * `exc`: net excitatory drive (already computed in core)
  * `inh`: net inhibitory drive (already computed in core; positive magnitude)
* Optional: `min/max` for each channel (pre‑computed in core to avoid per‑frame scans in UI)
* Optional derived: `b1_prob`, `novelty`, `plv` (phase‑locking), etc., if you want additional overlays

**Do *not* publish:**

* Full edge lists / weight matrices (N²/nnz is too heavy)
* Anything that forces the UI to re‑integrate the model

> If you don’t already compute `exc`/`inh` in core, add two **O(nnz)** streaming accumulators during your step to produce
> `E_i = Σ_j max(W_ij, 0)·r_j` and `I_i = Σ_j max(-W_ij, 0)·r_j`.
> That’s one sparse sweep you’re already doing for dynamics; expose the row sums.

---

## Wire format (stable and cheap)

**Frame header (JSON, \~200B):**

```json
{
  "topic": "maps/frame",
  "tick": 123456789,
  "n": 65536,
  "shape": [256, 256],
  "channels": ["heat","exc","inh"],
  "dtype": "f32",
  "endianness": "LE",
  "stats": {
    "heat": {"min":0.0,"max":1.3},
    "exc":  {"min":0.0,"max":0.8},
    "inh":  {"min":0.0,"max":0.7}
  }
}
```

**Binary payload (follow header):**

```
Float32Array heat  (n elements)
Float32Array exc   (n elements)
Float32Array inh   (n elements)
```

For 65,536 nodes this is \~256 KB per channel → \~768 KB per frame. At 10 fps that’s \~7.5 MB/s—fine over local websockets. If you need <2 MB/s, (a) lower fps to 5-8, (b) send **downsampled tiles** (e.g., 128×128), or (c) gzip/deflate (browser‑side pako).

---

## Server publisher (Python, asyncio websockets)

```python
# server/publish_maps.py
import asyncio, json, struct
import websockets

# Assume you already have these NumPy arrays per tick:
# heat, exc, inh: shape (N,), dtype float32
# shape: (H, W)

async def publish_maps(stream):
    async with websockets.serve(stream, "0.0.0.0", 8765, max_size=None):
        await asyncio.Future()

async def stream(websocket):
    # Simple broadcast loop — replace with your engine’s tick hook
    tick = 0
    while True:
        heat, exc, inh, shape = get_maps_from_core()  # <- your hook
        n = heat.size

        # Precompute stats (or pull from core if already logged there)
        def stats(a):
            return {"min": float(a.min()), "max": float(a.max())}
        header = {
            "topic": "maps/frame",
            "tick": tick,
            "n": int(n),
            "shape": list(shape),
            "channels": ["heat","exc","inh"],
            "dtype": "f32",
            "endianness": "LE",
            "stats": {
                "heat": stats(heat),
                "exc":  stats(exc),
                "inh":  stats(inh)
            }
        }
        # Send header
        await websocket.send(json.dumps(header))

        # Send binary payload (little-endian Float32)
        # Ensure .tobytes(order='C') and float32 dtype
        payload = heat.tobytes() + exc.tobytes() + inh.tobytes()
        await websocket.send(payload)

        tick += 1
        await asyncio.sleep(0.1)  # ~10 fps

if __name__ == "__main__":
    asyncio.run(publish_maps(stream))
```

**Notes**

* Keep arrays **contiguous** and `float32`.
* If you multiplex many subscribers, put frames on a broadcast queue.
* Add back‑pressure (drop oldest frame) to avoid UI stutter under load.

---

## Browser consumer (TypeScript) + Canvas renderer

```ts
// ui/maps.ts
type MapHeader = {
  topic: "maps/frame";
  tick: number;
  n: number;
  shape: [number, number];
  channels: string[]; // ["heat","exc","inh"]
  dtype: "f32";
  endianness: "LE";
  stats: Record<string,{min:number,max:number}>;
};

const ws = new WebSocket("ws://localhost:8765");
ws.binaryType = "arraybuffer";

let pendingHeader: MapHeader | null = null;

ws.onmessage = (evt) => {
  if (typeof evt.data === "string") {
    pendingHeader = JSON.parse(evt.data) as MapHeader;
    return;
  }
  if (!pendingHeader) return;

  const { n, shape, stats } = pendingHeader;
  const buf = evt.data as ArrayBuffer;

  // payload layout: heat[n], exc[n], inh[n] as Float32
  const f32 = new Float32Array(buf);
  const heat = f32.subarray(0, n);
  const exc  = f32.subarray(n, 2*n);
  const inh  = f32.subarray(2*n, 3*n);

  drawComposite(shape, heat, exc, inh, stats);

  pendingHeader = null;
};

const canvas = document.getElementById("map") as HTMLCanvasElement;
const ctx = canvas.getContext("2d", { alpha: false })!;

function norm(val: number, min: number, max: number) {
  if (max <= min) return 0;
  const t = (val - min) / (max - min);
  return Math.min(1, Math.max(0, t));
}

// Example visualization: RGB = [exc, heat, inh]
function drawComposite(
  shape: [number, number],
  heat: Float32Array,
  exc: Float32Array,
  inh: Float32Array,
  stats: Record<string,{min:number,max:number}>
) {
  const [H, W] = shape;
  canvas.width = W;
  canvas.height = H;

  const img = ctx.createImageData(W, H);
  const data = img.data;

  const sh = stats["heat"], se = stats["exc"], si = stats["inh"];

  for (let i = 0; i < heat.length; i++) {
    const r = Math.round(255 * norm(exc[i],  se.min, se.max));
    const g = Math.round(255 * norm(heat[i], sh.min, sh.max));
    const b = Math.round(255 * norm(inh[i],  si.min, si.max));
    const o = i * 4;
    data[o] = r; data[o+1] = g; data[o+2] = b; data[o+3] = 255;
  }
  ctx.putImageData(img, 0, 0);
}
```

**Why this works well**

* Zero copies: `Float32Array` views directly over the websocket buffer.
* **O(N)** pixel write; no expensive per‑frame scans (you shipped `min/max`).
* Color mapping is simple and composable (you can switch to colormaps or legends easily).

---

## Legend & layers (no surprises for users)

* Add a fixed legend explaining channel mapping. Example:

  * **Red**: Excitation (higher = stronger excitatory drive)
  * **Green**: Heat (smoothed firing)
  * **Blue**: Inhibition (higher = stronger inhibitory drive)
* Provide toggles: `[✓] Heat [✓] Exc [✓] Inh` and sliders for dynamic range (override `min/max` per channel).
* Optionally render **isolines** or contours for a single channel (cheap marching‑squares over a downsampled grid).

---

## Performance & scaling

* 256×256 at 10 fps: **<10% CPU** in a modern browser tab.
* For **>1M nodes**, publish a **quadtree pyramid**: {256², 512², 1024² tiles}; the UI requests LOD based on zoom.
* Use a **ring buffer** on the server (capacity 2-3 frames). If subscriber lags, **drop** the oldest.

---

## Action checklist for your agent

1. **Bus topics**

   * `maps/frame` (header JSON) + binary payload (Float32 LE).
   * Optional per‑channel topics if you want independent rates: `maps/heat`, `maps/exc`, `maps/inh`.

2. **Core emitters**

   * During `engine.step`, accumulate `E_i` and `I_i` (net excit/inh currents).
   * Maintain EMA heat: `heat_i ← (1-λ)·heat_i + λ·r_i`.

3. **Telemetry builder**

   * Pack stats (min/max) server‑side.
   * Write broadcast with drop‑oldest policy.

4. **UI**

   * Add the WebSocket consumer above.
   * Implement channel toggles + legend + range sliders.
   * (Optional) A “per‑node probe” tooltip showing `[i, heat, exc, inh]`.

5. **Safeguards**

   * Type checks (`float32`, little‑endian).
   * Rate limiter (e.g., 5-15 fps).
   * Back‑pressure: skip frames when the UI is busy.

---

## Bottom line

* **Yes**—reading **per‑node arrays** from the global bus and assembling the maps in the UI is the right move. It keeps the core hot path pure and makes the visualization cost **O(N) pixel writes** per frame.
* Avoid shipping edges or recomputing currents client‑side. Push **aggregated** signals the core already has.

If you want, I can adapt the schema to your existing event bus and fold the publisher into your `telemetry.py`/runtime loop so this is live in one pass.

Short answer: **budget \~1-16 MiB per active map view**, depending on resolution and buffering. Here’s the concrete breakdown and what I’d set as defaults.

---

## Rule‑of‑thumb (works every time)

You hold **3 channels** (heat/exc/inh) as `Float32` (4 B each) and render to one `RGBA` canvas (1 B per channel). Per pixel that’s:

* Payload: `3 × 4 B = 12 B`
* Canvas buffer: `4 B`
* **Total base** = `16 B` per pixel

So the **resident memory** per view is:

**Base MiB ≈ (H × W) / 65 536**

> Double‑buffering or a small frame ring multiplies that by the number of extra buffers you keep.

### Concrete sizes

| Grid      | Pixels (N) | Base (payload + one RGBA) | With double‑buffer |
| --------- | ---------: | ------------------------: | -----------------: |
| 128×128   |     16 384 |              **0.25 MiB** |           0.50 MiB |
| 256×256   |     65 536 |               **1.0 MiB** |            2.0 MiB |
| 512×512   |    262 144 |               **4.0 MiB** |            8.0 MiB |
| 1024×1024 |  1 048 576 |              **16.0 MiB** |           32.0 MiB |

If you show **three separate panels** (heat, exc, inh) **from the same payload**, you only add two extra RGBA canvases (not more payload), so **1.5× the base** (e.g., 512² → 6 MiB instead of 4 MiB; 1024² → 24 MiB instead of 16 MiB).

---

## Recommended caps (browser/UI)

* **Default desktop:** 512×512, single payload + single canvas, **\~4 MiB per map view**.
  If you need buttery playback, allow a 2‑frame buffer: **\~8 MiB**.
* **Mobile/low‑end:** 256×256, **\~1-2 MiB**.
* **High‑detail bursts (zoom/inspect):** 1024×1024 for the focused view only, **16-32 MiB**. Don’t keep multiple 1024² canvases alive.

If you routinely keep **three panels visible**, target **≤ 18 MiB** total at 512² (shared payload + 3 RGBA canvases, double‑buffered payload).

---

## How to stay inside budget (practical knobs)

1. **Share one payload across panels.**
   Keep **one** `Float32Array` payload (3 channels interleaved or adjacent). Each panel owns only its **RGBA** canvas buffer (4N bytes).

2. **Avoid persistent frame rings unless you need scrubbing.**
   For live playback, **0-1 extra payload buffer** is enough. If you need a scrubber, cap the ring at **≤ 3 frames** and store **compressed** (see #4).

3. **Pre‑allocate and reuse buffers.**

   * Reuse one `ImageData` for the canvas.
   * Reuse typed arrays; don’t allocate per frame.
   * Release the websocket `ArrayBuffer` after you’ve filled the RGBA.

4. **Optional quantization (2× savings end‑to‑end).**
   Send channels as **`Uint16`** with per‑frame `{min,max}` in the header. On the client:

   ```
   value = min + (u16 / 65535) * (max - min)
   ```

   Memory per pixel becomes `3×2B + 4B = 10B` → **Base MiB ≈ (H×W) / 104 858**
   (e.g., 512² ≈ 2.5 MiB; 1024² ≈ 10 MiB). This also halves network bandwidth.

5. **Composite by default.**
   For the overview, render **RGB = \[exc, heat, inh]** to **one** canvas (1 RGBA buffer). Only materialize separate panels when toggled.

6. **WebGL note (if you go GPU):**

   * Use **RGBA8** textures for display (4 B/pixel) and upload normalized data; avoid **RGBA32F** unless you truly need it (it’s **16 B/pixel** GPU‑side).
   * One 1024² RGBA8 texture ≈ **4 MiB** on the GPU.

7. **Back‑pressure:**
   If the UI is busy, **drop the oldest frame**. Don’t let frames queue; it only grows memory and increases latency.

---

## Server‑side sanity (publisher)

* Keep **one** payload in a broadcast queue (12N bytes) and **drop‑oldest**.
  At 512² that’s **\~3 MiB** resident; at 1024² **\~12 MiB**.
* If multiple subscribers, don’t duplicate payloads per client—fan out the same buffer.

---

## Quick budget calculator (paste into your UI)

```ts
// Estimate resident memory for maps (MiB)
function mapMemMiB(
  w: number, h: number,
  opts: { channels?: number; bytesPerVal?: number; canvases?: number; payloadBuffers?: number } = {}
) {
  const N = w * h;
  const channels = opts.channels ?? 3;         // heat/exc/inh
  const bytesPerVal = opts.bytesPerVal ?? 4;   // 4=Float32, 2=Uint16
  const canvases = opts.canvases ?? 1;         // number of RGBA canvases alive
  const payloadBuffers = opts.payloadBuffers ?? 1; // e.g., 2 if double-buffered

  const payloadBytes = N * channels * bytesPerVal * payloadBuffers; // 12N for Float32
  const rgbaBytes = N * 4 * canvases; // 4N per canvas
  return (payloadBytes + rgbaBytes) / (1024 * 1024);
}

// Examples:
mapMemMiB(512,512)                        // ~4.0 MiB (Float32, 1 canvas, 1 payload)
mapMemMiB(512,512,{payloadBuffers:2})    // ~8.0 MiB (double-buffered)
mapMemMiB(512,512,{canvases:3})          // ~6.0 MiB (3 panels, shared payload)
mapMemMiB(1024,1024,{bytesPerVal:2})     // ~10.0 MiB (Uint16 quantized)
```

---

## Bottom line

* **Ship a 512² composite view by default → \~4-8 MiB per viewer.**
* **Only escalate to 1024² on demand for a single focused view → 16-32 MiB.**
* If you need to shave memory/bandwidth further, **quantize to `Uint16`** and keep at most **one extra payload buffer**.

That keeps the visualization essentially “free” computationally, and the memory footprint predictable and small—even with heat/excitation/inhibition all live.

Got it. You don’t want a cron‑like pass that “does GDSP every N ticks.” You want **structural growth to fire only when the system itself exposes a local need**—i.e., emergent from events, budgets, and void‑debt signals. Here’s a tight, production‑oriented plan to make that true and verifiable.

---

## What “emergent GDSP” means (contract)

**Never** run GDSP on a timer or fixed cadence.
**Only** run GDSP when *opportunities* appear on the bus (cold gaps, failed routing, E/I imbalance, reward‑modulated void debt).
**Always** cap work by a small, per‑tick **budget** minted from reward/void‑debt (no O(nnz) scans).
**Only** touch a small **territory** around the triggering site (radius, K‑nearest), never global scans.

This matches your two‑rule split: RE‑VGSP = continuous resonance learning (“Alpha”), GDSP = sparse structural edits (“Omega”), both modulated by the same universal constants; GDSP shouldn’t be a scheduler pass. &#x20;

---

## Tell the agent exactly what to do

### 1) Kill all scheduled invocations

* **Remove/disable** any `every_n_ticks`, `schedule_*`, or “phase pass” that calls GDSP.
* In `runtime/loop.py` / orchestrator: **no direct calls** to GDSP except via events (below).
* Add a **CI grep guard** that fails the build if `gdsp` is invoked from anywhere outside the engine’s *opportunity* handler.

**Guard test (example):**

* Assert: no calls to `GDSPActuator.run_epoch|step|scheduled` in the codebase.
* Assert: only allowed entrypoint is `GDSPActuator.consider(opportunity, …)`.

### 2) Introduce a first‑class **opportunity event**

Add to `core/proprioception/events.py`:

```python
@dataclass(frozen=True)
class GDSPOpportunity(BaseEvent):
    kind: str = "gdsp_opportunity"
    node: int = -1              # focal node / seed
    territory_id: int | None = None
    reason: str = ""            # "cold_gap" | "route_fail" | "ei_imbalance" | "novelty"
    debt: float = 0.0           # void-debt or deficit score
    budget_hint: int = 1        # proposed work units
    radius: int = 2             # territory scope in hops
```

### 3) Emit opportunities **from events**, not timers

In `core/engine.py` (inside your existing folding path), synthesize `GDSPOpportunity` **only** from live reducers/signals:

* **Cold gap:** top‑K items from `ColdMap` with very low heat near them → `reason="cold_gap"`, `radius=R`.
* **Route fail:** repeated b1/route failure at node i (your b1 detector) → `reason="route_fail"`.
* **E/I imbalance:** from `ExcitationMap`/`InhibitionMap` divergence (local instability) → `reason="ei_imbalance"`.
* **Novelty / demand:** composer/telemetry novelty spike (telemetry‑only) → `reason="novelty"`.

All four are **event‑driven reducers** you already planned; no scans over `W`.

### 4) Mint a **small budget** from reward/void‑debt (no schedule)

Define a pure function:

```python
def mint_gdsp_budget(total_reward: float, void_debt: float) -> int:
    # Example: 0-3 edits per tick, monotone in both signals
    # void_debt from your universal modulation (β/α) style ratios
    base = 1 if abs(total_reward) > 1e-6 else 0
    extra = 0
    if void_debt > 0.2: extra += 1
    if void_debt > 0.4: extra += 1
    return min(3, base + extra)
```

> Use your **VoidDebtModulation** math to derive `void_debt` / thresholds—this keeps it principled rather than ad‑hoc.&#x20;

### 5) Make GDSP an **actuator** that only reacts to opportunities

In `core/neuroplasticity/gdsp.py` implement:

```python
class GDSPActuator:
    def __init__(self, rng, max_pairs=64, territory_k=256):
        self.rng = rng
        self.max_pairs = max_pairs
        self.territory_k = territory_k

    def consider(self, opp: GDSPOpportunity, substrate, rng) -> int:
        """
        Returns how many edits were actually applied (<= opp.budget_hint).
        Only samples within opp.radius/territory. No global scans.
        """
        if opp.budget_hint <= 0: return 0

        # 1) Build a tiny local frontier (radius hops from opp.node)
        nodes = territory_view(substrate, center=opp.node, radius=opp.radius, k=self.territory_k)

        # 2) Sample a few candidate pairs (or source->target via scouts/cold edges)
        pairs = self._sample_pairs(nodes, limit=min(self.max_pairs, 8*opp.budget_hint))

        # 3) Score pairs with your **goal‑directed** criterion (no global read):
        #    e.g., close cold gaps, improve reachability, respect polarity, plv gates.
        scored = self._score_pairs(substrate, pairs)

        # 4) Apply up to budget_hint edits with small initial weights; log reasons.
        applied = 0
        for (u,v,score) in top_k(scored, k=opp.budget_hint):
            if self._safe_to_link(substrate, u, v):
                self._add_or_strengthen_edge(substrate, u, v, w0=small_init(u,v,score))
                applied += 1

        return applied
```

Key properties:

* **No epoch/loop** inside `GDSPActuator`. It **never runs** unless `engine.step` passes an opportunity.
* **Bounded territory** (`radius`, `k`) and **bounded pairs** (`max_pairs`).
* **PLV/valence gating** and polarity are **local** multipliers, not global scans (consistent with your RE‑VGSP/PLV story).&#x20;

### 6) Wire it in the engine (replace any scheduler)

In `CoreEngine.step`:

```python
budget = mint_gdsp_budget(total_reward, void_debt)
for opp in gdsp_opportunities_this_tick:
    if budget <= 0: break
    opp_budget = min(opp.budget_hint, budget)
    used = self.gdsp.consider(opp, self.substrate, self.rng)
    budget -= used
    self.telemetry.emit("gdsp_apply", reason=opp.reason, used=used, node=opp.node)
```

> **Zero scheduler.** If no opportunities, **no GDSP**. If budget is 0, **no GDSP**. If both exist, **tiny local edits** only.

### 7) Observability & proofs that it’s emergent

* Telemetry fields: `evt_gdsp_apply{tick, node, reason, used}`, and counters per reason.
* Add a **runtime assert**: if last call site to GDSP was not via `consider()`, raise.
* CI test: run 2-3k ticks with **no opportunities** → assert 0 GDSP applies; inject synthetic cold gaps → assert applies appear only then.
* Docs: “GDSP is emergent; there is no scheduler or cadence.”

---

## Why this is better (and aligned with your math)

* **Alpha/Omega split** is respected: RE‑VGSP runs continuously (alpha), GDSP edits are sparse, *only when needed* (omega), with the same universal constants controlling magnitude/timing.&#x20;
* **Void‑debt budget** provides principled throttling; you already have a formal derivation of domain‑modulation & debt ratios—use it to mint tiny per‑tick budgets.&#x20;
* **Event‑driven** is void‑faithful: opportunities come from your reducers (Cold/Heat/Exc/Inh, b1, novelty), not global scans or timers.
* **No epochs.** Learning is indefinite/online; this removes the last “epoch‑ish” artifact (a scheduled structural pass).

---

## Quick “do this now” checklist

1. **Delete/disable** any GDSP scheduler hooks.
2. **Add `GDSPOpportunity`** event + emitters in engine from Cold/route/EI/novelty.
3. **Implement `GDSPActuator.consider()`** (no loops/epochs inside).
4. **Mint budget** from reward/void‑debt and call `consider()` opportunistically.
5. **Add CI guards** banning scheduled GDSP entrypoints.
6. **Expose telemetry** proving calls are reasoned & bounded.

If you paste the files where GDSP is currently scheduled, I’ll point to the exact lines to rip out and give you a concrete diff.

Short answer: **Yes.** Making GDSP **emergent** (triggered by local evidence + budgets) instead of **scheduled** global passes is *strictly* more efficient and scales better—latency, throughput, and cache behavior all improve. It also matches your “alpha/omega” split (RE‑VGSP = learning; GDSP = slow structural closure) where updates arise from the dynamics themselves, not from a timer.&#x20;

---

## Why emergent wins (engineering facts)

1. **Asymptotic cost**

   * **Scheduled:** $O(\text{nnz})$ or $O(N)$ every sweep—even if nothing interesting happened.
   * **Emergent:** $O(\#\text{events this tick} \times k_{\text{local}})$ with bounded sampling/pruning. When activity is sparse (the usual case), you’re doing **orders of magnitude** less work.

2. **Tail‑latency & cache locality**
   Local, event‑scoped updates stay hot in L1/L2 and avoid blowing caches with full CSR walks.

3. **Back‑pressure & stability**
   Token‑bucket budgets per tick/per territory keep GDSP from starving the fast path. You get smooth degradation under bursts, no stutters.

4. **Void‑faithful discipline**
   Structural changes occur **only** where the system reveals persistent “debt” (cold gaps under active flow), not where a clock says “it’s time.” That’s consistent with your void dynamics story (ALPHA drives resonance learning; BETA closes structure slowly).&#x20;

5. **Observability**
   Event‑driven reducers (Cold/Heat/Exc/Inh) already summarize *where* to act without global scans; folding those events is $O(\#\text{events})$ and bounded memory.&#x20;

6. **Domain modulation**
   If you need different behavior by regime, apply your **void‑debt modulation** factor once to budgets/thresholds—no schedulers required.&#x20;

---

## Back‑of‑envelope (why the numbers favor you)

* Suppose $N=10^5$ nodes, $\text{nnz}=10^7$ edges.
* **Scheduled GDSP @ 5 Hz:** $\approx 5 \times 10^7$ edge touches/s (plus memory traffic).
* **Emergent:** 50k meaningful events/s × $k_{\text{local}} \le 32$ candidates ≈ **1.6 M** local touches/s.
  That’s **\~30× less work** in the steady state, with lower variance.

---

## What to tell the agent (concrete, minimal changes)

**1) Remove all timers/schedulers for GDSP.**

* Delete/disable any `schedule_gdsp()` or cron‑like hooks from the orchestrator/loop.

**2) Make GDSP a *local actuator* that fires on evidence:**

* **Triggers:** when a node/territory accrues *void debt* (e.g., high ColdMap with sustained flow around it, or repeated `vt_touch` misses), enqueue a **local** GDSP action for that territory.
* **Budgeting:** per‑tick **token bucket** (global) + per‑territory micro‑budget. If either is empty, **skip** (no backlogs).
* **Scope:** candidates come **only** from the local neighborhood (territory head, frontier of ColdMap, recent Exc/Inh peaks). Never scan `W` globally.

**3) Keep it void‑faithful & bounded:**

* No CSR/adjacency scans. Fold **only events** you already emit (vt\_touch, spike, ΔW)—the same pattern you used for Heat/Exc/Inh maps.&#x20;
* Cap working sets (`keep_max`) and use sample‑prune (as you did for maps).

**4) Optional: modulate budgets by domain**

* Multiply per‑territory GDSP budget or trigger thresholds by your universal **domain\_modulation** factor when you change operating regimes.&#x20;

---

## Drop‑in actuator sketch (illustrative)

```python
class GDSPActuator:
    def __init__(self, tok_per_tick=200, territory_budget=8, seed=0):
        self.tokens = tok_per_tick
        self.tok_per_tick = tok_per_tick
        self.terr_budget = territory_budget
        self.rng = random.Random(seed)

    def replenish(self):  # call each tick
        self.tokens = self.tok_per_tick

    def maybe_act(self, territory, events, maps, W):
        # Bail if no global budget
        if self.tokens <= 0: 
            return 0

        # Cheap local trigger: cold gap with nearby activity
        debt = maps.cold.score(territory.id) - 0.5*maps.heat.score(territory.id)
        if debt <= territory.theta: 
            return 0

        # Per-territory cap
        acts = 0
        for _ in range(min(self.terr_budget, self.tokens)):
            u = self._pick_frontier_node(territory, maps)
            v = self._sample_neighbor_candidate(u, maps, W)  # local only, no scans
            if v is None: 
                break
            self._apply_gdsp_update(u, v, W)                # sparse, CSR-safe
            acts += 1
            self.tokens -= 1
            if self.tokens == 0: 
                break
        return acts
```

* `_pick_frontier_node`: pick from **ColdMap head** ∩ recent **Exc/Heat** fringe.
* `_sample_neighbor_candidate`: bounded random/sample‑top‑K from `N(u)` or adjacent territories; **never** enumerate whole graph.
* `_apply_gdsp_update`: your REV‑/GDSP micro‑rule (PLV gated if available), **sparse‑safe** arithmetic only.

---

## Guardrails you should add

* **CI budget test:** assert average GDSP actions/tick ≤ configured cap; fail if exceeded.
* **No‑scan grep:** unit test that forbids `for i in range(N)` or `for e in csr` in GDSP paths.
* **Telemetry counters:** `gdsp_acts`, `gdsp_skips_budget`, `gdsp_skips_evidence`; alert when skips>0 for 95th percentile ticks.

---

## Bottom line

You’re right: **emergent GDSP** is both **truer to the model** and **far more efficient**. Keep structural growth strictly **event‑driven + budgeted**, and you’ll get big CPU wins without sacrificing learning quality—exactly the ALPHA (RE‑VGSP) / BETA (GDSP) synergy you designed.  &#x20;









Below is a **fully rewritten plan** that folds in **Heat/Excitation/Inhibition scouts** alongside Cold, and it incorporates your answers on emergence, void‑faithfulness, memory budgets, and CI. It’s written as *instructions for your coding agent* (file paths, invariants, tests, knobs). I’ve also tied each physics check to your derivations and locked where CI should enforce vs. where runtime just logs.

---

## Rewritten, consolidated plan (agent‑ready)

### 0) Guiding constraints (don’t violate)

* **Void‑faithful hot path**: no global scans; reducers fold **only events**.
* **Emergent‑only structural learning**: GDSP/RevGSP trigger on *signals*, never on fixed cadence.
* **Scouts are read‑only**: traverse, measure, announce; no writes.
* **Performance guard**: all new features are budgeted; back‑pressure and drop‑oldest where needed.

---

## 1) Turn proofs → runtime assertions & CI (lock theory ↔ code)

**What & why (short):** Tie your runtime to the math you’ve derived—this prevents silent regressions and *improves* emergence by keeping dynamics inside the stable band you proved (wave speed, mass gap, invariant).

* Continuum EOM & kinetic normalization: $\partial_t^2\phi - c^2\nabla^2\phi + V'(\phi)=0,\ c^2=2Ja^2$.&#x20;
* Discrete↔continuum potential mapping (nonlinear terms): $\Box\phi + \alpha\phi^2 - (\alpha-\beta)\phi=0$.&#x20;
* On‑site **constant of motion** $Q_{\rm FUM}$ from time‑translation symmetry.&#x20;
* Units/physical scaling map when needed.&#x20;

**Agent tasks**

* **New module** `fum_rt/core/phys_guard.py`:

  * `assert_wave_speed(J, a, measured_c, tol_rel=0.1)` — compare measured pulse speed vs. $c=\sqrt{2Ja^2}$. **Runtime:** warn; **CI:** fail test beyond tolerance.&#x20;
  * `assert_mass_gap(alpha, beta, measured_m_eff, tol_rel=0.1)` — check $m_{\rm eff}^2 \approx \alpha-\beta$. **Runtime:** warn; **CI:** fail.&#x20;
  * `sample_Q_FUM(nodes, alpha, beta)` — compute $Q_{\rm FUM}=t-\frac{1}{\alpha-\beta}\ln\!\big|\frac{W}{(\alpha-\beta)-\alpha W}\big|$ for K sampled nodes; ensure d/dt ≈ 0 within ε. **Runtime:** log; **CI:** fail if median drift > ε.&#x20;
* **Control‑impact metric** (engineering): add `control_impact = ||Δstate_non_emergent||₁ / ||Δstate_total||₁`.

  * **Runtime:** record only (never halt).
  * **CI:** fail if moving average > 1e‑5 on golden scenario. (This is a *guardrail*, not physics law.)

**Clarifications to your questions**

* **1a)** Yes—tying to the math *improves* stability and performance by preventing the engine from drifting out of the proven regime (c, m\_eff, invariant).
* **1b)** “Fail CI” = fail tests; **never** hard‑stop the runtime. Simulations are a feature; runtime continues with warnings.
* **1d)** Control‑impact is the limit we track to ensure emergent control dominates; it’s not a physics axiom but a discipline metric.

---

## 2) Versioned **maps/frame** + **atlas** placement (indices, coords, counts, free to assemble)

Your model is self‑organizing; we’ll let neurons own their coordinates/tiles and publish **atlas** updates *event‑driven*. Walkers can announce changes; the UI never scans.

**Agent tasks**

* **New topic** `maps/atlas:v1` (JSON, occasional):

  * `{tick, n, shape:[H,W] | null, tiling:{tile_size, scheme}, coords?:"tile|xy", moved:[ [id,new_tile], ... ]}`
  * Emitted on topology/placement changes and at start.
* **Freeze** `maps/frame:v1` (current):
  `{topic:"maps/frame", ver:1, tick, n, shape, channels:["heat","exc","inh"], dtype:"f32", endianness:"LE", stats{min,max}}` + payload Float32 LE: `heat[n]|exc[n]|inh[n]`. (Already implemented per your summary.)
* **Where**: build buffers in `core/engine.py`; publish in `runtime/telemetry.py`. (Keep it void‑faithful: fill only known entries from reducer working sets; others default 0.)

---

## 3) Emergent‑only GDSP/RevGSP triggers (no schedulers)

Nothing changes from your redline except we **codify** the trigger table + optional scout assist.

**Triggers (any):**

* B1 spike event
* $|\mathrm{td\_signal}| \ge {\tt GDSP\_TD\_THRESH}$ (default 0.2)
* `cohesion_components > 1`

**If trigger fires but territory indices insufficient:** emit a **`bias_hint`** (see §5) to pull local scouts into that region for 1-2 ticks, then re‑attempt. (Still emergent; no cadence.)

---

## 4) Territories & indices hand‑off, strictly void‑faithful

We keep territory detection **event‑folded** (Union‑Find on `edge_on/off`, `probe_edge`) and expose a **bounded** set of member indices when GDSP needs them.

**Agent tasks**

* `core/proprioception/territory.py`:

  * UF fold API: `fold(events)`; `components_count()`; `sample_indices(component_id, k)`
  * Emits `evt_cohesion_components` (already used) and serves a **bounded** index set for actuators.
* `runtime/loop._maybe_run_gdsp()`:

  * When triggers hit: request `sample_indices` for affected components; if empty, publish a `bias_hint(region=component_id, ttl=2)` (see §5), then skip this tick.

---

## 5) **Scout completeness** (Cold, Heat, Excitation, Inhibition)

Scouts are **read‑only walkers**. They consume maps & hints, explore within a budget, and **announce**. No writes, no scans. This replaces expensive dense passes with targeted local probes.

**Scouts to implement**

* **ColdScout** — chases **ColdMap** maxima (stale regions).
* **HeatScout** — rides **HeatMap** ridges (active flows); good for recency coverage.
* **ExcitationScout** — follows **ExcitationMap** peaks (E‑fronts, stability/homeostasis instrument).
* **InhibitionScout** — follows **InhibitionMap** peaks (I‑fronts; balance instrument).

**Events they emit (bus)**

* `probe_visit(tile, sample_ids:[...])`
* `probe_edge(u,v)` — boundary cohesion measurements
* `probe_frontier(tile, neighbor_tile)`
* `vt_touch(token)` — if they poke a VT token during traversal
* **New:** `bias_hint(region|tile, ttl)` — small TTL hint a scheduler can respect to spawn/redirect scouts *locally* when a GDSP trigger lacked indices.

**Agent tasks**

* **Files**

  * `core/cortex/scouts/base.py` — TTL, budget, seeded RNG, step policy.
  * `core/cortex/scouts/{cold,heat,exc,inh}_scout.py` — policies:

    * seed from map.head K
    * neighbor choice = softmax over local gradient (map score deltas)
    * budgeted: max\_steps, max\_events/tick
  * `core/cortex/scouts/__init__.py` + `runtime/phase.py` wiring.
* **Config knobs**

  * `SCOUT_BUDGET_US`, `SCOUT_K`, `SCOUT_TTL`
  * `ENABLE_{COLD,HEAT,EXC,INH}_SCOUTS=1`
* **Scheduler (budgeted)**

  * At `engine.step`: allocate a small step budget (e.g., ≤1-3% tick time) across active scout types.
  * Respect `bias_hint` to prioritize tiles/regions *this tick only*.
* **Acceptance**

  * Assert **no writes** to connectome; scouts only publish probe events.
  * P50/P99 tick time unchanged ±2%.

> Heat/Exc/Inh scouts use the **event‑folded** maps you already built; they never scan. This keeps ADC/cartography void‑faithful. (Derivations anchor the φ‑dynamics separately; maps are telemetry/steering signals.)

---

## 6) Memory & transport budgets (4M neurons case)

**Numbers**

* One channel (float32) for N=4,000,000 = **\~16 MB**. Three channels (heat/exc/inh) = **\~48 MB/frame**.
* At 10 fps this is \~480 MB/s—too heavy for a single websocket and too heavy to sit on the same FIFO bus.

**Design**
How do 3D massive multiplayer games render to millions of users? The short answer is: **games don’t stream pixels; they stream tiny amounts of state and render everything locally on the GPU.** Your current plan pushes **entire 4 M×3‑channel arrays** through a CPU→bus→JS→GPU path every frame, which is a bandwidth and copies problem, not a “rendering is hard” problem.

Here’s the breakdown and the fix.

---

## Why games feel “free” and your heatmap doesn’t

**What games do**

* **Network:** send a few KB per entity per tick (positions, inputs, IDs). No pixels.
* **CPU→GPU:** most scene data lives on the GPU. Each frame the CPU updates a **small** constant buffer (camera, a few transforms).
* **GPU:** rasterizes millions of triangles/points at hundreds of GB/s of **on‑card** bandwidth with nearly zero CPU involvement.
* **Culling/LOD:** draw only what matters; coarse when far, detailed when close.

**What your 4 M heatmap does (naïvely)**

* **CPU computes 3 full arrays** (heat/exc/inh) = `4e6 * 3 * 4 B ≈ 48 MB` per frame.
* **Ships 48 MB/frame** to the UI; at 10 fps that’s **\~480 MB/s** of copies just to hand pixels around.
* **JS loops** over 4 M elements to pack into `ImageData` (slow).
* **Uploads** to GPU as a texture every frame (another big copy).

That’s why it stutters: you’re doing the **worst‑case** path (full‑frame CPU work + large transfers), while games keep state **resident on the GPU** and only send **small deltas**.

---

## Make it “game‑style”: keep maps on the GPU and update sparsely

Design this like a particle system / render target:

### 1) Represent your maps as a GPU texture once

* Use a **2048×2048** texture (≈4.19 M texels).
* Pack channels as:

  * **WebGL2:** `RGBA8` (8‑bit) with RGB = (exc, heat, inh), A unused → **\~16 MB** per texture.
    If you truly need floats, `RGBA16F` is \~32 MB; `RGBA32F` is \~64 MB.
  * **WebGPU:** `rgba8unorm` (or `rgba16float` if needed).

Keep **two copies** (ping‑pong) to apply decay without reading back → **32-64 MB** total for 8‑bit.

### 2) Apply decay on‑GPU each frame

* Fullscreen pass: `outTex = decay * inTex` (exponential half‑life).
* This is a single draw call, entirely on the GPU.

### 3) Add sparse event updates (“splat” the changes) on‑GPU

* From your bus, collect only the **K updates** this tick (node index + Δexc/Δheat/Δinh). K is usually ≪ N.
* Upload **just those K updates** (e.g., a SSBO/vertex buffer with `(x, y, dExc, dHeat, dInh)`), typically a few KB-MB.
* Draw **K point sprites** into the map FBO with **additive blending** (`ONE, ONE`) so each event increments its pixel.

  * Vertex shader converts node index → (x, y) → NDC.
  * Fragment color = (Δexc, Δheat, Δinh, 0).

No full‑frame copies, no per‑pixel JS loops.

### 4) Composite for display

* Either show the map directly (RGB = Exc/Heat/Inh) or run a tiny shader to apply colormaps/toggles/legend.

### 5) Level of Detail (LOD) for zoom and bandwidth

* When zoomed out, sample **lower mip levels** (free downsampling on GPU).
* For remote viewers, stream **tiles/LODs**; local UI doesn’t need network at all.

---

## Numbers (so you can sanity‑check)

* **Resident map memory (8‑bit):**
  2048×2048×4 B ≈ 16 MB. Ping‑pong = 32 MB. Add one staging buffer for events (say 1 MB). **Well under 64 MB**.
* **Per‑frame CPU→GPU uploads:**

  * **Decay:** none (shader)
  * **Events:** `K * (position+Δ)`; e.g., K=50 k → \~50 k × 20 B ≈ **1 MB**/frame.
  * **Compare to 48 MB**/frame (full array): \~**50× less** bandwidth.
* **GPU work:** drawing 4 M pixels per frame is trivial for modern GPUs if texels already live on‑card. The bottleneck was your **transfers**, not fill‑rate.

---

## Action plan for your agent (WebGL2; WebGPU mirrors this)

**Files**

* `ui/gl/maps_renderer.ts` - WebGL2 renderer (init + three passes below)
* `ui/gl/shaders/` - `decay.fs`, `splat_vs.glsl`, `splat_fs.glsl`, `composite.fs`
* `ui/state/maps_stream.ts` - subscribes to **events**, batches `(idx, dExc, dHeat, dInh)` each tick

**Initialization**

1. Create `gl` with `alpha:false, antialias:false, premultipliedAlpha:false`.
2. Allocate two `RGBA8` 2048×2048 **FBO‑backed textures** (`texA`, `texB`).
3. Build programs:

   * **Decay pass**: fullscreen quad; uniforms `decayFactor = 2^(-Δt/halfLifeTicks)`.
   * **Splat pass**: instanced points; VBO layout = `u32 idx` (or `vec2 x,y`), `vec3 delta`.
   * **Composite pass**: sample current map → to screen; apply toggles/scales.

**Per frame**

```ts
// 1) DECAY (ping → pong)
bindFBO(texB);
bindProgram(decay);
bindTex(0, texA);
setUniform(decayFactor, f);
drawFullScreenQuad();

// 2) SPLAT sparse updates into pong
bindFBO(texB);
bindProgram(splat);
bindTex(0, texB); // if you read-modify-write, do a separate target or ensure blending only writes deltas
enable(ADDITIVE_BLENDING); // ONE, ONE
uploadOrUpdateVBO(eventsThisTick); // K instances
drawInstancedPoints(K);

// 3) SWAP
swap(texA, texB);

// 4) COMPOSITE to canvas
bindDefaultFramebuffer();
bindProgram(composite);
bindTex(0, texA);
drawFullScreenQuad();
```

**Node→pixel mapping**

* If each neuron “knows” its `(x,y)` (as you want), stream that once (or derive on UI).
* If you only have an index, precompute a 2D layout (e.g., row‑major, Hilbert curve) and store in a **static** 2048×2048 RG texture with coordinates; the splat VS fetches `(x,y)` by index via `texelFetch`.

**Quality/precision**

* Start with **8‑bit** maps. If you need dynamic range, expose per‑channel min/max in uniforms and do `normalize(val)` in the composite shader.
* Only move to `16F/32F` if diagnostics demand it.

**Threading**

* Use **OffscreenCanvas** + a **Worker** so uploads/draws don’t block the main thread.

---

## If you absolutely must keep CPU arrays

* **Quantize to `Uint8`** on the producer and send `RGB` (12 MB/frame instead of 48 MB).
* **Tile + delta encode**: send only changed tiles; compress with permessage‑deflate.
* Still worse than the event‑driven GPU path above, but acceptable for prototypes.

---

## Bottom line

* The “hard” part was pushing **huge arrays** around, not drawing them.
* Treat the heat/exc/inh maps like a **GPU‑resident render target**; update with **sparse events** (your void‑faithful bus already produces them), apply **decay in a shader**, composite for display.
* That’s exactly how games achieve “near‑zero‑latency” visuals: **small deltas in, GPU does the heavy lifting**.


---

## 7) Security stubs (localhost for now)

* `io/websocket_server.py` — auth stub + origin check; default allow `127.0.0.1`.
* Toggle: `WS_ALLOW_ORIGIN` (comma‑sep), `WS_MAX_CONN`.

---

## 8) Telemetry layering (no interference with dynamics)

* Keep `engine.snapshot()` numbers only; maps are staged separately and transported via the ring.
* Ensure maps building **never** enumerates `W` or CSR—fill from reducer working sets only; missing nodes default `0`.

---

## 9) Tests & CI (fast, surgical)

* **Physics guards** (`tests/core/test_phys_guard.py`):

  * wave speed within 10% (measured vs. $\sqrt{2Ja^2}$).&#x20;
  * mass gap within 10% ($m_{\rm eff}^2$ vs. $\alpha-\beta$).&#x20;
  * $Q_{\rm FUM}$ drift < ε on K nodes.&#x20;
* **Void‑faithful checks** (`tests/void/test_no_scans.py`):

  * AST/grep deny list inside `core/cortex/maps/*`, `core/engine.py` maps section.
* **Maps contract** (`tests/core/test_maps_contract.py`):

  * header `ver:1`, `channels:["heat","exc","inh"]`, `dtype:"f32"`, `endianness:"LE"`.
* **Scouts** (`tests/cortex/test_scouts.py`):

  * prove no writes to graph; budget respected; events emitted.
* **Control‑impact** (`tests/accept/test_control_impact.py`):

  * golden scenario moving‑avg < 1e‑5 (CI only).

---

## 10) Memory‑steering layer (keep if it helps performance)

This is **not** a heavy “physics sim”; it’s a light, dimensionless law to bias routing using slowly‑stored structure $M$. It improves exploration efficiency, fork choice, and curvature scaling—useful for scouts and walkers.

* Steering law (dimensionless): paths bend with $\mathbf r'' \propto \nabla_\perp M$.
* Memory PDE (write‑decay‑spread): $\partial_t M=\gamma R-\delta M+\kappa\nabla^2M$.
* Clean graph discretization included already in your notes; we keep it optional and **budgeted**.&#x20;

**Agent tasks (optional module, off by default)**

* `core/memory_steering.py`

  * `update_memory(m, r, L, gamma, delta, kappa, dt)`
  * `transition_probs(i, neighbors, m, theta)`
* **Flags:** `ENABLE_MEMORY_STEERING=0` by default; when on, allow scouts to use `transition_probs` for neighbor choice.
* **Why keep it:** It measurably reduces steps‑to‑useful‑coverage in sparse/cold regions without touching the core φ‑dynamics. (φ‑sector invariants remain governed by your EFT mapping.)

---

## 11) Bus/event schema (adds for completeness)

* **Existing**: `vt_touch`, `edge_on/off`, `spike(sign, amp)`, `delta_w(dw)`, `delta(b1, td, …)`.
* **Add**:

  * `probe_visit`, `probe_edge`, `probe_frontier` (scouts)
  * `bias_hint(region|tile, ttl)` (light nudge for scouts when GDSP trigger lacks indices)
  * `maps/atlas:v1` (occasional JSON)
  * `maps/frame:v1` (binary frame via ring + websocket)

---

## 12) File worklist (exact diffs for the agent)

**Core**

* `core/phys_guard.py` (new) — physics assertions & helpers.
* `core/proprioception/territory.py` (new) — UF, components, bounded sampling.
* `core/cortex/scouts/{base,cold,heat,exc,inh}_scout.py` (new)
* `core/cortex/scouts/__init__.py` (export)
* `core/engine.py` — init scouts, fold events, step budgets, build maps (no scans).

**Runtime**

* `runtime/loop.py` — emergent GDSP trigger + `bias_hint` handling.
* `runtime/telemetry.py` — publish `maps/frame:v1`; forward `maps/atlas:v1` when coords change.

**IO/Transport**

* `io/maps_ring.py` (new) — shared‑memory ring for frames (2-3 slots).
* `io/websocket_server.py` (new) — bounded, drop‑oldest, localhost default.

**Tests**

* `tests/core/test_phys_guard.py`
* `tests/void/test_no_scans.py`
* `tests/core/test_maps_contract.py`
* `tests/cortex/test_scouts.py`
* `tests/accept/test_control_impact.py`

---

## 13) Knobs (sane defaults)

```ini
# emergence & learning
ENABLE_GDSP=1
ENABLE_REVGSP=1
GDSP_TD_THRESH=0.2

# scouts
ENABLE_COLD_SCOUTS=1
ENABLE_HEAT_SCOUTS=1
ENABLE_EXC_SCOUTS=1
ENABLE_INH_SCOUTS=1
SCOUT_BUDGET_US=3000
SCOUT_K=64
SCOUT_TTL=100

# maps transport
MAPS_FPS=8
MAPS_RING=3
MAPS_TILE=none   # or 256 for 256x256 downsampling

# optional steering
ENABLE_MEMORY_STEERING=0
```

---

## 14) Why this aligns with your vision (void‑faithful + emergent)

* **No schedulers**: learning fires only on real signals (B1, TD, cohesion).
* **No scans**: all cartography and scouts use **event‑folded** maps or bounded heads.
* **Exploration by scouts, not scans**: cold + (heat/exc/inh) scouts give you a *radar* of the network for free, driven by maps you already fold.
* **Physics‑anchored**: c‑normalization, mass gap, and $Q_{\rm FUM}$ are checked continuously (warn in runtime, enforce in CI)—this increases stability, not burden.
* **Units‑ready**: when you need GeV‑rigor, the scaling map is already specified.&#x20;
* **Optional steering**: a lightweight memory layer can improve routing efficiency when enabled; otherwise it stays off.&#x20;

---

You’re right—and I’m going to keep anchoring every change to **void‑faithfulness** and **high‑leverage performance**. Below is a clean, production‑oriented work order that prioritizes the GPU/tiling pipeline, event‑only cartography, and emergent learning—no global scans, no cron‑like schedulers. I’ve included acceptance checks and CI guards so the system can’t drift away from your design principles.

---

## North star (summarized in one line)

**Everything is event‑folded, never scans `W`, and all heavy visualization work is done by a tile/LOD GPU path fed by a separate maps transport, not the announce bus.**
(This is consistent with your discrete law → EFT mapping and “kinetic is fixed; no hidden scans,” which we can also test at runtime.  )

---

## WORK ORDERS FOR THE CODING AGENT

### A) Zero‑copy, void‑faithful visualization path (GPU + tiles)

**Goal:** Render 1-4M neurons at 5-15 fps with near‑zero main‑thread load and no back‑pressure on the announce bus.

1. **Separate transport**

   * Create `fum_rt/io/maps_ring.py` — fixed‑capacity (2-3 frames) shared‑memory ring for **maps frames**.
   * Create `fum_rt/io/websocket_server.py` — forwards **only** maps frames (header JSON + binary) with **drop‑oldest**.
   * The announce bus remains for compact events only.

2. **Message formats (frozen)**

   * **Full frame (u8, 3 channels)**

     ```json
     { "topic":"maps/frame.v2",
       "tick": <int>, "n": <int>, "shape":[H,W],
       "channels":["exc","heat","inh"], "dtype":"u8", "endianness":"LE",
       "quant": {"exc": [min,max], "heat": [min,max], "inh": [min,max]},
       "tiling": {"mode":"none"} }
     ```

     Payload: `uint8` planar blocks: `exc[n] | heat[n] | inh[n]`.
     **Why u8?** 4M nodes → **12 MB/frame** (vs 48 MB with f32). At 10 fps this is 120 MB/s and feasible over localhost.
   * **Sparse tiles (u8, 128×128)**

     ```json
     { "topic":"maps/tiles.v1",
       "tick": <int>, "shape":[H,W],
       "tile": {"size":128, "grid":[Gh,Gw]},
       "channels":["exc","heat","inh"], "dtype":"u8", "endianness":"LE" }
     ```

     Then a stream of tiles:

     ```
     <tile_header: u32 tile_id, u16 h, u16 w, u8 has_exc, u8 has_heat, u8 has_inh, pad>
     <optional quant triples per present channel: 2×f32 (min,max)>
     <payload bytes for present channels, tightly packed>
     ```

     Only changed tiles are sent. Delta mode caps bandwidth to **O(#changed\_tiles)**.

3. **Server‑side quantization (no scans)**

   * In `core/engine.py` maps builder, **do not** sweep the whole array. Use each reducer’s **working set** to update rolling per‑channel `(min,max)` and **write zeros elsewhere**. (No global W reads; still void‑faithful.)
   * Quantize to `u8` per channel using the rolling `(min,max)`.
     *Note:* A fixed LUT with soft‑clamp for robust color (e.g., clip at P99) is allowed—computed from reducer values only.

4. **Browser renderer (WebGL2 or WebGPU)**

   * Provide `ui/maps_renderer.ts` with:

     * One `WebGL2` texture per channel (R8). Composite in a fragment shader to RGB (R=exc, G=heat, B=inh).
     * **Fast path**: Upload whole planes for frame.v2; for tiles.v1, use `texSubImage2D` per changed tile.
     * Toggles for per‑channel visibility and range override (for debugging).

5. **Acceptance (performance)**

   * 4M nodes, 10 fps, CPU main thread <15% on a 2020+ laptop (local).
   * End‑to‑end latency ≤ 2 frames (ring depth ≤ 3).

---

### B) Event‑only reducers **and** matching scouts (Cold, Heat, Exc, Inh)

**Goal:** Keep cartography pure and event‑driven. **No scans.** Provide mirror scouts so exploration follows the maps.

1. **Reducers (already scaffolded)**

   * `ColdMap` (idle‑time monotone), `HeatMap` (short half‑life), `ExcitationMap`, `InhibitionMap`.
   * Fold only `vt_touch`, `spike(sign,amp)`, `delta_w(dw)`—**never** peek at `W`. (You’ve documented this separation; keep it. )

2. **Scouts**

   * Implement four read‑only walker species that **subscribe** to the same maps (no scans), each with a small per‑tick step budget:

     * **ColdScout**: climb **coldness** gradient (find stale/idle regions).
     * **HeatScout**: climb **heat** gradient (trace active fronts).
     * **ExcitationScout**: chase **exc** peaks (useful for growth target context).
     * **InhibitionScout**: chase **inh** peaks (useful for homeostasis/inhibitory balance).
   * All scouts **emit only** probe/visit/edge events into the bus (and nothing mutative).
   * Budget knobs: `SCOUT_K` (count), `SCOUT_TTL`, `SCOUT_BUDGET_US`. “Self‑leveling” mode adjusts K so the queue drains each tick.

3. **Acceptance (void‑faithful)**

   * Grep/AST CI guard: no `toarray/tocsr/csr/coo/adj/synaptic_weights` in `core/cortex/maps/*.py` or scouts.
   * With scouts on, **canonical metrics unchanged** (telemetry‑only outputs get richer).

---

### C) Emergent‑only learning gates (GDSP/RevGSP)—no schedulers

**Goal:** Structural learning runs **only** when reality demands it.

* Keep **emergent triggers**: `b1_spike ∨ |td|≥τ ∨ cohesion_components>1`. No `STRUCT_EVERY`.
* Territory input must come from **bounded** APIs (e.g., “give me K indices from active territories”), never from whole‑graph passes.
* If a trigger fires but territory indices are thin, **bias the scouts** toward that region next tick; don’t promote a scan.

(These choices align with the discrete → continuum discipline you’ve written, where dynamics and invariants live in the local law—not in periodic control planes.  )

---

### D) Runtime proofs as **assertions**, not shackles

**Goal:** Tie code to your theory without blocking experiments.

* **Q\_FUM onsite invariant checker (sampled)**
  Each tick, sample K nodes and check the closed‑form constant of motion from your symmetry note. Log z‑scores; **do not abort**—flag & count. (We treat it as a diagnostic, not a hard gate.)&#x20;
* **Kinetic normalization sanity**
  Track measured propagation speed vs. `c^2=2Ja^2` (your kinetic derivation). Alert if drift > ε for T seconds; again, **no abort**—just telemetry.&#x20;
* **Control‑impact metric**
  Keep it as an **engineering hygiene** number, not a blocker. Target is “near‑zero” external control. We log and graph it; nothing hard‑fails unless explicitly configured.

---

### E) Memory‑steering (optional, but performance‑relevant)

**Goal:** Improve routing/performance, not simulate physics for its own sake.

* Add the **slow memory field M(x,t)** with the minimal PDE (write/decay/spread) and use it only for **routing bias** (softmax over neighbor memory values). This can reduce exploration cost and speed convergence. It’s orthogonal to φ‑dynamics and respects your void‑faithful separation (fast φ vs. slow M).&#x20;
* Guardrail: the M‑layer must consume **existing usage/spike events**; no scans, no extra passes.

---

## WHY THIS STAYS VOID‑FAITHFUL (with your math)

* The **kinetic structure** and “no hidden scans” ethos are exactly what you formalized: `𝓛_K = ½(∂_t φ)^2 - J a^2(∇φ)^2`, with `c^2=2Ja^2` set by units—not by hidden global work. The render path is a **consumer** of reducer outputs, not a producer of dynamics.&#x20;
* Your **discrete on‑site law** and its EFT mapping remain the only sources of state change; scouts and maps observe and bias exploration (when enabled) but never write.&#x20;
* The optional **memory steering** is a slow, external index that shapes path choice without altering on‑site evolution—exactly how you framed it.&#x20;

---

## Concrete task checklist (copy/paste for the agent)

**Transport & GPU**

* [ ] `io/maps_ring.py`: SHM ring (2-3 frames), push/pop, drop‑oldest on full.
* [ ] `runtime/telemetry.py`: write `frame.v2` (u8) into ring each tick (or `tiles.v1` when enabled).
* [ ] `io/websocket_server.py`: forward header JSON + bytes; rate limit to 5-15 fps; drop‑oldest.
* [ ] `ui/maps_renderer.ts`: WebGL2 renderer, R8 textures per channel, tile sub‑updates, RGB composite shader, range sliders/toggles.

**Reducers & Scouts**

* [ ] Ensure `HeatMap`, `ExcitationMap`, `InhibitionMap` are folding only events; export snapshots without scans.
* [ ] Implement `ColdScout`, `HeatScout`, `ExcitationScout`, `InhibitionScout` with per‑tick budget; emit probe events only.
* [ ] Self‑leveling K: keep queue empty; manual override env‑vars for tests.

**Learning Gates**

* [ ] `_maybe_run_gdsp()` and `_maybe_run_revgsp()` keep **emergent only** triggers (no cadence).
* [ ] Add “territory indices” bounded API; if thin, bias scouts rather than scan.

**Assertions & CI (non‑blocking by default)**

* [ ] `assertions/q_fum.py`: sample K nodes; compute/log invariant error (z‑score); no abort.&#x20;
* [ ] `assertions/kinetic_norm.py`: measure φ pulse speed vs `2Ja^2`; log drift.&#x20;
* [ ] `tests/void_faithful_guards.py`: denylist scans in `core/cortex/maps/*` and scouts.
* [ ] `tests/maps_transport.py`: throughput tests for 4M nodes, 10 fps, CPU budget.

**Config defaults**

* [ ] `MAPS_MODE=frame_v2_u8` (or `tiles_v1_u8` for huge N)
* [ ] `SCOUTS_SELF_LEVEL=1`, `SCOUT_K_MAX=…`, `SCOUT_BUDGET_US=…`
* [ ] `ENABLE_GDSP=1`, `ENABLE_REVGSP=1`, no `STRUCT_EVERY` anywhere.

---

## Memory & bandwidth recap (4M neurons)

* **u8, 3 channels:** \~12 MB/frame; 10 fps → \~120 MB/s (localhost OK).
* **Tiles (128×128):** update only changed tiles; typical frames << full‑frame size.
* **Ring depth 3:** \~36 MB (frame mode) or \~a few MB (tiles) resident.
* **Announce bus unaffected** (maps ride a separate transport).

---

## Bottom line

This plan **prioritizes massive, practical improvements** (GPU + tiles + u8 quantization) while keeping the **void‑faithful** guarantees: **event‑only** inputs, **emergent** learners, **no scans**, and math‑backed invariants logged—not shackles on exploration. It will make your system faster, cleaner, and harder to regress away from your vision.



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
   * Emergent triggers only (no fixed cadences) for GDSP/RevGSP—already aligned with your direction.
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
2. **Publish `adc_territories_detail`**: for each territory: head size, churn rate, cohesion, exemplar tokens—no scans.

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
* **Steering by memory** gives the system a *principled* way to prefer useful regions—this boosts competence, not just correctness, and comes with testable predictions (junction choice, curvature).&#x20;
* **Unbounded territories** + **event‑driven scouts** let domains proliferate naturally as evidence appears—exactly what you want for “masters all domains.”
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

     * `_node_W(connectome, i) -> Optional[float]`  — try `connectome.get_W(i)` or `connectome.nodes[i].W` if exposed; else `None`.
     * `_node_M(maps, i) -> Optional[float]` — read from `maps.get("memory", {})` or fall back to `heat_head` score map (void‑faithful proxies).
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
3. **Guardrail**: grep `scouts/` for forbidden tokens (`toarray`, `csr`, `synaptic_weights`)—should be clean.

---

### Bottom line

* **As written, your `BaseScout` does *not* use the void equations.**
* The subclass above makes scouts **physics‑aware** in a **void‑faithful, local** way—no scans, no schedulers—by descending your on‑site potential $U(W)$ when available and otherwise using your memory‑steering softmax. That’s the correct place to “use your equations” inside walkers, while keeping the substrate dynamics and EFT untouched.  &#x20;

If you want, I can also provide a tiny adapter that reads `Heat/Exc/Inh` heads into a `memory_map` so you get steering immediately without exposing `W` yet.


Short answer: **the `BaseScout` you pasted is just a safe scaffold.** It does not (and should not) hard‑code your physics. The void equations come in when we write *derived scouts* that override the routing policy and use your φ/M laws locally. Below I show exactly what to give your coding agent so these scouts become **void‑faithful and physics‑driven** (no scans, event‑only).

---

## What to tell the coding agent (precise, implementable)

**A. Add two read‑only fields (or getters) on the connectome**

* `phi: np.ndarray | None` — fast void field per node (or `get_phi(i)`).
* `memory: np.ndarray | None` — slow memory field $M$ per node (or `get_memory(i)`).
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
* **Slow memory $M$ steers geometry** via $n=\exp(\eta M)$ and the logistic fork law—implemented as a softmax over neighbor $m_j$. That’s precisely your ray/eikonal result on graphs. &#x20;
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
   * Emergent triggers only (no fixed cadences) for GDSP/RevGSP—already aligned with your direction.
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
2. **Publish `adc_territories_detail`**: for each territory: head size, churn rate, cohesion, exemplar tokens—no scans.

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
* **Steering by memory** gives the system a *principled* way to prefer useful regions—this boosts competence, not just correctness, and comes with testable predictions (junction choice, curvature).&#x20;
* **Unbounded territories** + **event‑driven scouts** let domains proliferate naturally as evidence appears—exactly what you want for “masters all domains.”
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

     * `_node_W(connectome, i) -> Optional[float]`  — try `connectome.get_W(i)` or `connectome.nodes[i].W` if exposed; else `None`.
     * `_node_M(maps, i) -> Optional[float]` — read from `maps.get("memory", {})` or fall back to `heat_head` score map (void‑faithful proxies).
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
3. **Guardrail**: grep `scouts/` for forbidden tokens (`toarray`, `csr`, `synaptic_weights`)—should be clean.

---

### Bottom line

* **As written, your `BaseScout` does *not* use the void equations.**
* The subclass above makes scouts **physics‑aware** in a **void‑faithful, local** way—no scans, no schedulers—by descending your on‑site potential $U(W)$ when available and otherwise using your memory‑steering softmax. That’s the correct place to “use your equations” inside walkers, while keeping the substrate dynamics and EFT untouched.  &#x20;

If you want, I can also provide a tiny adapter that reads `Heat/Exc/Inh` heads into a `memory_map` so you get steering immediately without exposing `W` yet.


Short answer: **the `BaseScout` you pasted is just a safe scaffold.** It does not (and should not) hard‑code your physics. The void equations come in when we write *derived scouts* that override the routing policy and use your φ/M laws locally. Below I show exactly what to give your coding agent so these scouts become **void‑faithful and physics‑driven** (no scans, event‑only).

---

## What to tell the coding agent (precise, implementable)

**A. Add two read‑only fields (or getters) on the connectome**

* `phi: np.ndarray | None` — fast void field per node (or `get_phi(i)`).
* `memory: np.ndarray | None` — slow memory field $M$ per node (or `get_memory(i)`).
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
* **Slow memory $M$ steers geometry** via $n=\exp(\eta M)$ and the logistic fork law—implemented as a softmax over neighbor $m_j$. That’s precisely your ray/eikonal result on graphs. &#x20;
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

Below is a concrete, void‑faithful plan that uses what you already have (Heat/Exc/Inh maps and vt\_touch/edge events). It keeps everything **event‑driven, local, and bounded**—no scans, no schedulers.

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

All of these values are **already available from your reducers** (Heat/Exc/Inh) or from a small, incremental memory map—no whole‑graph reads.

---

### 3) Use the “free” event stream you already have

* Every tick, UTE input *pings* nodes → your runtime already emits **`vt_touch`** and **`edge_on`** events.
* **Reducers** (Heat/Exc/Inh, or Trail) fold those events and keep bounded, decayed scores.
* Walkers operate on **local neighbors** and read **only** the per‑node scores of those neighbors.
* Result: **repulsion/attraction is “free”** apart from a few additions and a softmax, because you never scan $W$ or CSR—everything is event‑driven and local.&#x20;

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
* Short‑term repulsion is the algorithmic analogue of **synaptic fatigue / short‑term depression**—it reduces immediate re‑use so you cover space (explore) while long‑term memory consolidates what mattered.
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

Short answer: **you’re fine.** With the way you’ve designed them—**event‑driven, bounded working sets, no global scans**—Heat/Exc/Inh/Cold (and a slow **Memory** map if you add it) are *cheap relative to the value they unlock*. The ROI is high as long as you keep the few guardrails below.

---

## Why these maps stay cheap

* **Time cost scales with events, not graph size.** Each reducer just folds the events you already emit (`vt_touch`, `spike`, `delta_w`), prunes a small working set, and returns a tiny head/summaries. That’s **O(#events this tick + sampled prune)**, not O(N) or O(E).
* **Memory is bounded by `keep_max`.** You’re never storing N entries—only the currently “interesting” few thousand per map (configurable).
* **No contention with learning.** Reducers don’t read global `W` or CSR; they’re observers that don’t block the hot path.
* **They amplify leverage.** Heat/Exc/Inh and a slow Memory field give scouts and actuators *high‑information, local* hints (steering, E/I balance, coldness) without any global passes. This is exactly the “free” you’re aiming for—piggyback on signals you already produce.
* **Physics‑aligned steering.** A slow Memory map implements your steering law cleanly (ray bias via $n=\exp(\eta M)$, fork choices \~ logistic in $\Theta\,\Delta m$), giving you measurable gains in routing with tiny compute.&#x20;

---

## Numbers to keep in mind

For **10k neurons @ 10 Hz** (your current run), with `keep_max≈4-8k`:

* **Per map memory** (Python): a few MB (value + last\_tick + dict overhead). Four maps = low tens of MB.
* **Per tick CPU**: typically sub‑millisecond (fold + prune). The connectome step dwarfs these reducers.

For **4 M neurons**, you still don’t store 4 M entries—only `keep_max`. The only time you touch O(N) is when you **choose** to emit a *dense* `maps/frame` for the UI. Use v2 quantized frames, downsample/tiles, and a shared‑memory ring when you scale; keep UI FPS at 3-8 and you’re fine.

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

* **Yes**—seed scouts from **UTE hits** and **pulse** out at each stimulated neuron. You’re consuming exactly the local information you just produced, so the marginal cost is just the **local neighbor picks** and a few events.
* Add slow **Memory steering** (EMA write-decay + stochastic edge smoothing) and let scouts bias to $\exp(\Theta\,m_j)$ neighbors; the junction choice collapses to a logistic in $\Theta\,\Delta m$, which you can verify in CI/telemetry. This is your theory in action, still event‑driven and scan‑free.&#x20;

---

## What to watch in telemetry

* `maps_*_count` (working‑set size) and `maps_pruned_per_tick` (healthy non‑zero).
* `evt_*_per_tick` (keep within budget).
* UI **ring depth** / dropped frames (should not grow unbounded).
* B1/complexity/cohesion wobbling (liveness) and no long flatlines.
* Optional invariants (on‑site constant of motion checks) as CI‑only—these catch drift without penalizing runtime.&#x20;

---

### Bottom line

Adding Heat/Exc/Inh/Cold (and a slow Memory map) **will not create problems** if you keep them **bounded, event‑driven, and decoupled from the UI.** They give you outsized gains—better routing, clearer E/I fronts, robust cold‑region exploration—at a tiny marginal cost, fully aligned with void‑faithfulness and your steering theory.


**Short answer:** Yes—your `run_scouts_once` design is *void‑faithful* and it *does* take advantage of “free” signals already flowing through your system. You’re calling a pure function **once per tick**, seeding from UTE/observation hits, folding a few **local** neighbor reads, emitting compact events, and (optionally) publishing once to the bus. That’s exactly the right pattern.

Below is a tight “tell‑the‑agent” checklist to finish wiring this properly (no schedulers, no scans), plus a small repulsion/steering recipe.

---

## Why this runner is correct (and cheap)

* **No scheduler**: It executes **exactly once per tick** under a micro‑budget (`max_us`) you pass in. There’s no hidden cadence or background thread.
* **Event‑driven**: If you feed **seeds = recent UTE indices** (the inputs that already “ping” neurons), scouts pulse out from those hits, so work is concentrated where new information already is. That’s the “free” part—no extra discovery cost beyond rendering a few events.
* **Local only**: Each scout reads **only** `neighbors(u)` (and small map heads/dicts) and emits `vt_touch`/`edge_on` events. No `W` scans, no CSR walks, no dense conversions.

---

## Add *repulsion* and *steering* (bounded, local)

Think of two layers:

1. **Short‑term trail repulsion** (don’t re‑trample the same ground in the next few ticks)

   * Keep a tiny, exponentially decaying **TrailMap** (similar to `HeatMap`) that increments on `vt_touch`/`edge_on`.
   * Neighbor score subtracts `ρ_trail · trail[j]`. This is already in your `HeatScout` (`rho_trail`)—just make sure `TrailMap` exists and is wired.

2. **Long‑term memory steering** (bias toward valuable regions)

   * Maintain a slow “memory” field `m` and use the **softmax** over neighbors with logits `Θ·m[j]` (that’s the Boltzmann choice; not “ML”—it’s statistical mechanics). At a 2‑way fork you get the **logistic** law you derived: $P(A)=\sigma(\Theta \Delta m)$.&#x20;
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

* **“Softmax = ML?”** No. Here it’s the **Boltzmann choice**—a physics thing. It lets you bias but stay stochastic; it’s the discrete version of your refractive‑index steering law (and gives your **logistic fork** prediction).&#x20;
* **“Will maps pile up and get slow?”** Not if you keep them **bounded** (head + small working set) and **event‑folded**. Each reducer is $O(\#\text{events this tick})$; pruning keeps memory flat.

---

If you hand this checklist to the agent as‑is, you’ll get repulsion + steering **without** adding any schedulers or scans, fully aligned with your void‑faithful rules and with your physics pinned to code via simple assertions.

You’re right—you currently have **4** scouts in the repo, but the plan we agreed to is for **9**.
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

### Missing—add these 5 next (with exact file names)

5. **VoidRayScout** — physics‑aware (φ‑bias)
   **File:** `fum_rt/core/cortex/void_walkers/void_ray_scout.py`
   *Role:* Prefer neighbors with favorable **local** change in the fast field φ.
   *Local rule (no scans):* For hop `i→j`, score `s_j = λ_φ·(φ[j]-φ[i]) + θ_mem·m[j]`; sample neighbor via a temperatured choice (softmax).
   *Signals:* `connectome.phi` (vector) and optional `memory_dict`.
   *Events:* `VTTouchEvent`, `EdgeOnEvent`, optional `SpikeEvent(sign=+1 if Δφ≥0 else -1)`.

6. **MemoryRayScout** — memory steering
   **File:** `fum_rt/core/cortex/void_walkers/memory_ray_scout.py`
   *Role:* Implement your refractive‑index steering law using slow memory `m`.
   *Local rule:* `P(i→j) ∝ exp(Θ·m[j])` (at a two‑branch junction this reduces to the logistic with `ΘΔm`).
   *Signals:* `memory_dict` (or a slow proxy like `heat_dict` until memory is live).
   *Events:* `VTTouchEvent`, `EdgeOnEvent`.

7. **FrontierScout** — boundary/cohesion probe
   **File:** `fum_rt/core/cortex/void_walkers/frontier_scout.py`
   *Role:* Skim component boundaries and likely “bridge” frontiers to keep cohesion metrics fresh **without writing**.
   *Local rule:* Start in cold tiles; prefer neighbors that (a) change degree, (b) cross weakly connected cuts (hint: prefer low shared‑neighbor count from local adjacency query), (c) sit near low heat/high cold.
   *Signals:* `ColdMap` head/dict, local neighbor lists only.
   *Events:* `EdgeOnEvent(u,v)` (probe), `VTTouchEvent`. *(No structural edits—these probes just feed DSU/cohesion reducers and your emergent GDSP trigger.)*

8. **CycleHunterScout** — short‑cycle finder
   **File:** `fum_rt/core/cortex/void_walkers/cycle_scout.py`
   *Role:* Seek and report small cycles (3-6 hops) to keep `cycles_est` alive.
   *Local rule:* TTL‑limited random walk with **tiny path memory** (e.g., last 5 nodes). When the next neighbor is in the path window, emit a cycle hit.
   *Signals:* none required beyond neighbors; optional bias to heat/exc heads.
   *Events:* `EdgeOnEvent` along the path, `VTTouchEvent`. If you already have a `CycleHitEvent`, emit that too; otherwise the `EdgeOnEvent`s are enough for reducers.

9. **SentinelScout** — blue‑noise reseeder / de‑trample
   **File:** `fum_rt/core/cortex/void_walkers/sentinel_scout.py`
   *Role:* Prevent path lock‑in; sample uniformly/blue‑noise across space to de‑bias exploration and refresh stale tiles.
   *Local rule:* Seeds = uniform from `N` or from ADC tiles with lowest visit counts; one hop per seed to announce coverage.
   *Signals:* optional `VisitMap`/`ColdMap` heads.
   *Events:* `VTTouchEvent` (always), `EdgeOnEvent` (opportunistic).

> **Why these five?** Together they (a) encode your physics (VoidRay/MemoryRay), (b) keep cohesion/cycles truthful at the **active** graph level (Frontier/Cycle), and (c) guarantee fresh coverage and anti‑trample behavior (Sentinel). All are **read‑only, event‑only**, and slot into your `runner` once per tick—**no scheduler**.

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

It’s just a **numerically stable, single‑step normalization** to stochastically choose among neighbors using your local score (e.g., `Θ·m[j]` or `λ_φ·Δφ`). There’s **no training**, no gradients, no datasets—just a temperatured random pick that instantiates your **logistic fork law** at two‑way junctions. It’s the most faithful discrete form of your memory‑steering equation.

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
You’re **on track**. What you have now matches the “9‑scout + one‑shot runner” design: Cold / Heat / Excitation / Inhibition **plus** VoidRay, MemoryRay, Frontier, CycleHunter, and Sentinel. The runner executes **once per tick** under a micro‑budget, with no schedulers and only **local** neighbor reads—void‑faithful ✅.

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

   * Confirm the “shared‑neighbor” check in Frontier is **hard‑capped** (you mentioned cap=64)—no accidental growth into adjacency scans.
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

## Is “softmax” ML? (No—this is physics here)

In this context **softmax is just Boltzmann sampling**: picking a neighbor with probability ∝ exp(score/τ). Your memory steering paper shows that at a two‑branch fork this **reduces exactly** to a logistic choice with argument **Θ·Δm**—a falsifiable physical prediction, *not* a learned classifier.&#x20;

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
* To unlock the real gains, finish **TrailMap** + **MemoryField/Map**, make **seeds universal in BaseScout**, add **env gating and runner fairness**, and expose **φ/memory getters**. That completes the loop: inputs → seeds → physics‑aware local routing → event‑folded maps → better routing—**all void‑faithful**.
