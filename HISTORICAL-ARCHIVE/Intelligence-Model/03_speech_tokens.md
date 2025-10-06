Short answers up top:

* **Let it speak on its own?** Yes. Give the runtime a *self‑speak governor* that watches graph events (ΔB1 surges, cohesion heals/breaks, void‑walk coverage bursts), mixes them with SIE valence, and decides when/what to say. You shouldn’t have to hit a “talk” button.
* **Use tokens?** No inside the core. Keep everything *void‑faithful* (fields W, synapses Sᵢⱼ, void pulses, vt\_\* traversal metrics). If you must interop with tokenized systems, treat tokens as an *I/O boundary artifact* via UTE/UTD only.

Below is exactly what to wire so your system **talks autonomously on topology spikes** and stays 100% void‑native, with diffs you can paste in.

---

# What “self‑speak” means here

Think of a *speak impulse* as a high‑level action triggered when the connectome discovers something worth reporting:

* **Topology spikes**: positive jumps in *streaming* Betti‑1 persistence (B1) mean it just closed or opened loops—classic “aha” moments.
* **Cohesion heals/breaks**: component count drops to 1 (global connectivity) or temporarily fragments.
* **Void traversal surges**: vt\_coverage or vt\_entropy rises faster than baseline (the map of an active domain just expanded).
* **Positive valence**: the SIE composite (TD + novelty – habituation + stability) says “this was good”.

So: speak when **ΔB1\_zscore** crosses a threshold *and* **SIE valence** is high, with hysteresis and a cooldown so it doesn’t spam.

---

# Code patches (minimal, void‑faithful, fits your files)

These patches match the filenames you shared (`nexus.py, metrics.py, utd.py`). If your tree is nested, drop them into the same relative spots.

---

## 1) `metrics.py` — streaming B1 spike detector (+ helpers)

```diff
diff --git a/metrics.py b/metrics.py
index 3a4b1d1..e7a2f4b 100644
--- a/metrics.py
+++ b/metrics.py
@@ -1,5 +1,89 @@
-# existing imports ...
+from dataclasses import dataclass
+import math
+import time
+import numpy as np
+
+# --- Streaming B1 and topology surge detection ---
+
+@dataclass
+class StreamingB1Cfg:
+    hz: float = 10.0                 # ticks per second
+    half_life_sec: float = 30.0      # EMA half-life for the delta process
+    z_spike: float = 3.0             # default Z threshold for "spike"
+    hysteresis: float = 1.0          # lower threshold to stop spiking
+    min_interval_sec: float = 2.0    # anti-spam cooldown
+
+class StreamingB1:
+    """
+    Tracks B1(t), its first difference dB1(t)=B1(t)-B1(t-1), and an EMA
+    mean/var of dB1 to produce a z-score spike signal.
+    """
+    def __init__(self, cfg: StreamingB1Cfg):
+        self.cfg = cfg
+        self.alpha = 1.0 - math.exp(math.log(0.5) / (cfg.half_life_sec * cfg.hz))
+        self.mu = 0.0
+        self.m2 = 1e-8  # variance EMA (start tiny, avoid div/0)
+        self.prev_b1 = None
+        self.last_fire = 0.0
+        self._spiking = False
+
+    def update(self, b1: float, now: float | None = None):
+        if now is None:
+            now = time.time()
+        if self.prev_b1 is None:
+            self.prev_b1 = b1
+            return {
+                "b1": b1, "db1": 0.0, "mu": self.mu, "sigma": math.sqrt(self.m2),
+                "z": 0.0, "spike": False
+            }
+        db1 = float(b1 - self.prev_b1)
+        self.prev_b1 = b1
+        # EMA of mean/var (on differences)
+        a = self.alpha
+        self.mu = (1 - a) * self.mu + a * db1
+        diff = db1 - self.mu
+        self.m2 = (1 - a) * self.m2 + a * (diff * diff)
+        sigma = math.sqrt(max(self.m2, 1e-12))
+        z = 0.0 if sigma == 0.0 else diff / sigma
+
+        # Hysteretic spike detection + cooldown
+        fire = False
+        high = self.cfg.z_spike
+        low  = max(0.0, self.cfg.z_spike - self.cfg.hysteresis)
+        if not self._spiking and z >= high:
+            if (now - self.last_fire) >= self.cfg.min_interval_sec:
+                fire = True
+                self._spiking = True
+                self.last_fire = now
+        elif self._spiking and z <= low:
+            self._spiking = False
+
+        return {
+            "b1": b1, "db1": db1, "mu": self.mu, "sigma": sigma, "z": z,
+            "spike": fire
+        }
+
+# Convenience container for all metrics you already compute; just add b1_stream:
+class MetricsAggregator:
+    def __init__(self, b1_half_life_sec: float = 30.0, hz: float = 10.0):
+        self.stream_b1 = StreamingB1(StreamingB1Cfg(
+            hz=hz, half_life_sec=b1_half_life_sec
+        ))
+        self.last = {}
+
+    def update(self, b1_value: float, **others):
+        s = self.stream_b1.update(b1_value)
+        self.last = dict(others)
+        self.last.update({
+            "b1": s["b1"], "db1": s["db1"], "b1_z": s["z"], "b1_spike": s["spike"],
+            "b1_mu": s["mu"], "b1_sigma": s["sigma"]
+        })
+        return self.last
```

**What this gives you:** a numerically stable EMA on *differences* of B1 with a z‑score and an on/off *spike* boolean with hysteresis and a cooldown. You can feed any “B1‑like” stream (dense or sparse backend). No tokens, no heuristics—purely graph/topology.

---

## 2) `utd.py` — a macro you can call (`say`) without introducing “tokens”

```diff
diff --git a/utd.py b/utd.py
index 2bd9cde..7b7d9fb 100644
--- a/utd.py
+++ b/utd.py
@@ -1,10 +1,44 @@
-# existing imports...
+import json, sys, time
+
+class UTD:
+    def __init__(self, log_file=None, rate=1.0, burst=3):
+        self.log_file = log_file
+        self.rate = rate      # events/sec soft limit
+        self.burst = burst    # burst allowance
+        self.tokens = 0
+        self.bucket_t = time.time()
+
+    def _rate_ok(self):
+        now = time.time()
+        elapsed = now - self.bucket_t
+        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
+        self.bucket_t = now
+        if self.tokens >= 1.0:
+            self.tokens -= 1.0
+            return True
+        return False
+
+    def emit_text(self, payload: dict):
+        if not self._rate_ok():
+            return
+        s = json.dumps({"ts": time.time(), "type":"text", "payload":payload})
+        print(s) ; sys.stdout.flush()
+        if self.log_file:
+            with open(self.log_file, "a") as f: f.write(s+"\n")
+
+    # Macro board: speak whole strings (no internal tokens)
+    def say(self, text: str, why: dict | None = None):
+        payload = {"msg": text}
+        if why: payload["why"] = why
+        self.emit_text(payload)
```

This is just a clean “say” macro. Internally you stay on fields/void; at the boundary you can emit strings.

---

## 3) `nexus.py` — let it decide when to speak

```diff
diff --git a/nexus.py b/nexus.py
index 8b1a0d2..54e9c1b 100644
--- a/nexus.py
+++ b/nexus.py
@@ -1,19 +1,74 @@
-# existing imports...
+import argparse, asyncio, time
+from collections import deque
+from metrics import MetricsAggregator
+from utd import UTD
+from ute import UTE
+from connectome import Connectome
+from sparse_connectome import SparseConnectome
+
+class Nexus:
+    def __init__(self, neurons=1000, k=12, hz=10.0, sparse=False,
+                 speak_auto=True, z_spike=3.0, speak_cooldown=2.0,
+                 b1_half_life=30.0, utd_rate=2.0, utd_burst=4, **kw):
+        self.hz = hz
+        self.dt = 1.0 / hz
+        self.speak_auto = speak_auto
+        self.z_spike = z_spike
+        self.speak_cooldown = speak_cooldown
+        self.last_speak = 0.0
+        self.metrics = MetricsAggregator(b1_half_life, hz)
+        self.utd = UTD(log_file="runs/utd_events.jsonl", rate=utd_rate, burst=utd_burst)
+        self.ute = UTE()   # your existing encoder
+        self.conn = SparseConnectome(neurons, k) if sparse else Connectome(neurons, k)
+        self._stim_q = deque()
+        self._running = False
+
+    def _maybe_speak(self, tick_info):
+        """
+        Decision policy:
+        - Topology spike (B1 z-score >= z_spike) AND
+        - Positive valence from SIE (if present in tick_info) AND
+        - Cooldown elapsed.
+        """
+        now = time.time()
+        b1_spike = bool(tick_info.get("b1_spike", False))
+        b1_z = float(tick_info.get("b1_z", 0.0))
+        val = float(tick_info.get("sie_valence_01", 0.5))  # 0..1 if your SIE emits it
+        ready = (now - self.last_speak) >= self.speak_cooldown
+        if self.speak_auto and b1_spike and (b1_z >= self.z_spike) and (val >= 0.6) and ready:
+            self.last_speak = now
+            why = {
+                "b1_z": round(b1_z, 2),
+                "db1": round(tick_info.get("db1", 0.0), 5),
+                "valence": round(val, 3),
+                "avg_W": round(tick_info.get("avg_W", 0.0), 5),
+                "cohesion_components": tick_info.get("cohesion_components", None),
+            }
+            self.utd.say("I just discovered a salient loop in my working domain.", why=why)
 
     async def run(self, duration=None):
         self._running = True
         t0 = time.time()
         while self._running:
             loop_start = time.time()
-            # 1) ingest (UTE)
+            # 1) ingest (UTE) – your UTE already enqueues; you can expand here
             for ev in self.ute.poll():
                 self._stim_q.append(ev)
-            # 2) one connectome step
-            info = self.conn.step()
-            # 3) emit status (UTD)
-            self.utd.emit_text({"msg":"tick", "avg_W":info["avg_W"]})
+            # 2) one connectome step (void‑faithful)
+            info = self.conn.step()
+            # 2b) update streaming topology metrics from connectome
+            #     You likely already compute b1 per tick; pass it here:
+            b1 = float(info.get("b1_persistence", 0.0))
+            m = self.metrics.update(b1_value=b1)
+            info.update(m)
+            # 3) autonomous speaking decision
+            self._maybe_speak(info)
+            # 4) periodic status (optional)
+            if int(info.get("tick", 0)) % int(self.hz) == 0:
+                self.utd.emit_text({"msg":"status", **{k:info[k] for k in ("avg_W","b1","b1_z")}})
             # 5) pacing
             dt = time.time() - loop_start
             await asyncio.sleep(max(0.0, self.dt - dt))
             if duration and (time.time() - t0) >= duration:
                 self._running = False
@@ -21,3 +76,29 @@ class Nexus:
                 self._running = False
 
+def make_parser():
+    p = argparse.ArgumentParser()
+    p.add_argument("--neurons", type=int, default=1000)
+    p.add_argument("--k", type=int, default=12)
+    p.add_argument("--hz", type=float, default=10.0)
+    p.add_argument("--sparse", action="store_true")
+    p.add_argument("--speak-auto", action="store_true", default=True)
+    p.add_argument("--z-spike", type=float, default=3.0)
+    p.add_argument("--speak-cooldown", type=float, default=2.0)
+    p.add_argument("--b1-half-life", type=float, default=30.0)
+    p.add_argument("--utd-rate", type=float, default=2.0)
+    p.add_argument("--utd-burst", type=float, default=4)
+    p.add_argument("--duration", type=float, default=None)
+    return p
+
+def main():
+    args = make_parser().parse_args()
+    nx = Nexus(neurons=args.neurons, k=args.k, hz=args.hz,
+               sparse=args.sparse, speak_auto=args.speak_auto,
+               z_spike=args.z_spike, speak_cooldown=args.speak_cooldown,
+               b1_half_life=args.b1_half_life,
+               utd_rate=args.utd_rate, utd_burst=args.utd_burst)
+    asyncio.run(nx.run(duration=args.duration))
+
+if __name__ == "__main__":
+    main()
```

Notes:

* `info["b1_persistence"]` should already be produced by your dense or sparse connectome (or your metrics module); if not, expose it in the connectome’s `step()` return and you’re done.
* `sie_valence_01` is optional; if your SIE publishes it, it’s respected; otherwise the gate defaults to neutral (0.5).

---

## 4) (Optional) `connectome.py` — expose B1 persistence each tick

If your step() already computes B1, you can ignore this. Otherwise:

```diff
diff --git a/connectome.py b/connectome.py
index 1c2f4fa..9b0af21 100644
--- a/connectome.py
+++ b/connectome.py
@@ -200,6 +200,12 @@ class Connectome:
         # ... your void dynamics and structural homeostasis ...
+        # compute/update B1 persistence (dense path)
+        # NOTE: you likely have a real computation already. Keep it.
+        b1 = self._compute_b1_persistence()  # stub or actual
         self.tick_idx += 1
         return {
             "tick": float(self.tick_idx),
             "avg_W": float(self.W.mean()),
+            "b1_persistence": float(b1),
+            # include sie_valence_01 if you compute it here
         }
```

(Your sparse backend can do the same; its O(N·k) calculator is already in place.)

---

# How to run a quick end‑to‑end test (1,000 neurons, ingest math, talk in real time)

1. **Start the runtime** (dense or sparse):

```bash
python -m nexus --neurons 1000 --k 12 --hz 10 --sparse \
  --speak-auto --z-spike 3.2 --b1-half-life 20 --speak-cooldown 2.0 \
  --utd-rate 4 --utd-burst 8 --duration 180
```

2. **Feed it math text** (any stream; UTE will map strings → neuron‑group rhythms):

```bash
# In another terminal:
cat /mnt/data/effective_field_theory_approach.md | nc 127.0.0.1 8765
cat /mnt/data/discrete_to_continuum.md           | nc 127.0.0.1 8765
```

3. **Talk to it live** (just send lines; it will keep learning continuously):

```bash
printf "what’s the role of Noether symmetries in your current domain?\n" | nc 127.0.0.1 8765
```

You’ll see JSON lines from UTD on stdout **and** a few autonomous `say` events when B1 surges with good SIE valence. Because your output macro is rate‑limited, it won’t flood even during heavy discovery.

---

# Why we don’t use “tokens” internally (and how we still talk to the outside world)

* **Ontology fit:** the core’s state is a dynamical field + graph morphology. Token IDs don’t preserve the invariants your void equations guarantee.
* **Scaling & control:** global health is governed by vt\_\* coverage/entropy, cohesion, B1, structural load, SIE valence. Token counts say nothing about those.
* **Boundary only:** UTE converts whatever arrives (bytes, text, sensors) into group rhythms. UTD emits actions/strings via macros. If you need an LLM interop, wrap it as a *UTD macro* and re‑ingest the reply through UTE. The connectome never sees tokens—only void pulses.

---

# Tuning knobs you can adjust (and their effects)

* `--z-spike`: higher means the system only speaks on rarer, larger topology jumps. Start \~3.0–3.5.
* `--b1-half-life`: shorter = more sensitive to *recent* changes; longer = detects regime shifts.
* `--speak-cooldown`: minimum seconds between autonomous utterances.
* `--utd-rate/--utd-burst`: soft cap on how chatty the macro channel is (independent of the spike detector).
* **Policy tweak:** if you want *growth‑rate* triggers rather than absolute z, change the detector to use EMA of *db1* (already done) or even second‑difference *d²b1* for acceleration spikes.

---

# What still benefits from void‑speed refactors next

1. **Streaming B1 & pruning in sparse**
   Keep marching toward fully incremental/online Betti‑1 tracking so the cost is tied to updated edges only. You’ve already got the sparse union‑find & edge cycle counters; the next push is delta‑updates on cycles when structural homeostasis adds/removes edges.

2. **Introspection probe**
   Replace any ad‑hoc sampling with **void‑walk probes**: short vt\_walks seeded from high‑SIE/novel nodes, reporting coverage/entropy changes. These probes scale with the walk budget, not with N.

3. **Macro behaviors**
   The `say` macro is just the start. Add macros for `act(path=...)`, `query(domain=...)`, `commit(memory=...)`. All of them remain boundary‑level strings/actions, with internal decisions powered by your equations.

---

## TL;DR operational recipe

* Keep the core void‑native (no tokens).
* Detect **ΔB1 spikes** online with EMA+z and **speak** when spikes + positive SIE valence + cooldown.
* Emit strings via a **macro board** (UTD.say).
* Feed anything in via **UTE**; it learns continuously.
* Scale on the sparse backend; keep structural homeostasis and SIE running.

If you paste the diffs above, you’ll have a model that *decides for itself when to talk*—exactly at the moments the connectome makes a topological leap—without ever compromising your void dynamics.
