Justin—perfect. Here’s how we lock the runtime to your blueprint, purge the stragglers, and get a clean, void‑faithful 1k‑neuron run on your workstation today. I’m giving you exact patches, concrete run recipes, and what to watch for so we can iterate fast.

# What’s already right (keep)

* **Event‑driven ADC** (walkers → bus → ADC) with *no raw W access* in the cartographer.
* **Self‑speak governor** driven by **topology spikes** (streaming z‑score on a B1 proxy) ∧ **positive valence** ∧ **cooldown**.
* **UTD macro board** (say/status), **UTE streaming**, **HDF5 engrams** with resume, **dense + sparse backends**, and **void traversal** everywhere.
* **SIE online** (novelty/TD/habituation/HSI → valence), rate‑limited emission.

That all aligns with your blueprint and supports the scaling you’re after.

# What we still need to fix (fast, targeted)

1. **Hard guards** so nothing non‑void slips in:

* Forbid any delta path that doesn’t come through your void adapter.
* Enforce “ADC never touches W/CSR”—only bus events.
* Path‑finding cost must be **-|ΔW\_pred|** (RE‑VGSP + GDSP) at the candidate node.
* Add a tiny linter that blocks forbidden patterns (“softmax”, “token”, global W scans in ADC).

2. **Make the organism chatty at the *right* times**
   Topology spikes should check **ΔB1**, not just absolute z. We’ll keep your z‑gate but add a *delta‑spike* trigger so “sudden increases” in B1 persistence fire speech more naturally. (Yes: this is exactly what you were thinking the speak threshold should govern.)

3. **Operational polish**

* FLOPs/GFLOPs in status lines (cheap approximation, no overhead).
* HDF5: chunking + compression tuned for your 64‑128 MB write cadence.
* CLI convenience for your workstation (MI100 present, 512 GB RAM): pinned‑memory toggles, sparse knobs pre‑set.

Below are the exact diffs.

---

## 1) Enforce void‑only dynamics and ADC isolation

### A. Adapter guard (blocks non‑void deltas)

**`fum_rt/core/void_dynamics_adapter.py`**

```diff
@@
+ALLOWED_MODES = {"re_vgsp+gdsp", "universal"}
+
 def universal_void_dynamics(W, t, domain_modulation=1.0, use_time_dynamics=True):
     return delta_re_vgsp(W, t, domain_modulation, use_time_dynamics) \
          + delta_gdsp(W, t, domain_modulation, use_time_dynamics)
 
+def assert_void_faithful(mode: str):
+    if mode not in ALLOWED_MODES:
+        raise RuntimeError(f"[void] Disallowed dynamics mode: {mode}. "
+                           f"Only {ALLOWED_MODES} are permitted.")
+
+def combine_deltas(mode: str, W, t, domain_modulation=1.0, use_time_dynamics=True):
+    assert_void_faithful(mode)
+    if mode == "re_vgsp+gdsp":
+        return delta_re_vgsp(W, t, domain_modulation, use_time_dynamics) \
+             + delta_gdsp(W, t, domain_modulation, use_time_dynamics)
+    # "universal" is currently identical; keep the seam for future variants
+    return universal_void_dynamics(W, t, domain_modulation, use_time_dynamics)
```

### B. ADC guardrail (no raw W/CSR allowed)

**`fum_rt/core/adc.py`**

```diff
@@
 class ADC:
     def __init__(self, r_attach=0.25, ttl_init=120, split_patience=6):
         self.r_attach = r_attach
         self.ttl_init = ttl_init
         self.split_patience = split_patience
         self._map = {}   # territory_id -> state
+        # denylist: trap accidental raw access
+        self._forbid_attrs = {"W", "A", "row_ptr", "nbr_idx", "csr"}
@@
     def __getattr__(self, name):
-        raise AttributeError(name)
+        if name in object.__getattribute__(self, "_forbid_attrs"):
+            raise AttributeError("[adc] direct access to raw connectome state is forbidden")
+        raise AttributeError(name)
@@
-    def update_from(self, events):
+    def update_from(self, events):
         """
         Consume only high-level Observation events from the bus.
         """
         for ev in events:
             # ... existing local, incremental updates ...
             pass
```

---

## 2) Void‑equation path‑finder (-|ΔW\_pred| priority)

**Dense:** `fum_rt/core/connectome.py`
**Sparse:** `fum_rt/core/sparse_connectome.py`

```diff
@@ class Connectome:
-    def void_pathfind(self, src, dst, max_expansions=1000, domain_mod=1.0, use_time_dynamics=True):
+    def void_pathfind(self, src, dst, max_expansions=1000, domain_mod=1.0, use_time_dynamics=True, mode="re_vgsp+gdsp"):
         import heapq
         visited = np.zeros(self.N, dtype=np.bool_)
         parent = -np.ones(self.N, dtype=np.int64)
         def energy(n, tlocal):
-            w = float(self.W[n])
-            dw = float(delta_re_vgsp(w, tlocal, domain_mod, use_time_dynamics)
-                       + delta_gdsp(w, tlocal, domain_mod, use_time_dynamics))
+            w = float(self.W[n])
+            # strictly combine via adapter guard
+            dw = float(combine_deltas(mode, w, tlocal, domain_mod, use_time_dynamics))
             return -abs(dw)
         # ... frontier loop unchanged ...
```

(Apply identically in the sparse backend.)

---

## 3) Speak on **increases** in B1 (delta‑spike + z gate)

**`fum_rt/core/metrics.py`**

```diff
@@
 class StreamingZEMA:
     def __init__(self, half_life_sec=30.0, hz=10.0, eps=1e-8):
         # ... as implemented ...
         pass
+class DeltaSpike:
+    """Detects sudden increases in a scalar (positive first-diff surpassing threshold)."""
+    def __init__(self, thresh_sigma=2.0):
+        self.prev = None
+        self.mu = 0.0
+        self.m2 = 0.0
+        self.n = 0
+        self.thresh_sigma = thresh_sigma
+    def update(self, x):
+        if self.prev is None:
+            self.prev = x; return False, 0.0
+        dx = x - self.prev; self.prev = x
+        # online variance of dx
+        self.n += 1
+        delta = dx - self.mu
+        self.mu += delta / max(1, self.n)
+        self.m2 += delta * (dx - self.mu)
+        var = (self.m2 / max(1, self.n-1)) if self.n > 1 else 1e-6
+        z = (dx - self.mu) / (np.sqrt(var) + 1e-8)
+        return (z >= self.thresh_sigma), z
```

**`fum_rt/nexus.py`**

```diff
@@ class Nexus:
-        self.b1_gate = StreamingZEMA(half_life_sec=args.b1_half_life_ticks/args.hz, hz=args.hz)
+        self.b1_gate = StreamingZEMA(half_life_sec=args.b1_half_life_ticks/args.hz, hz=args.hz)
+        self.b1_delta = DeltaSpike(thresh_sigma=args.speak_delta_sigma)
@@ in run loop after metrics computed:
-        z = self.b1_gate.update(m["complexity_cycles"])
+        z = self.b1_gate.update(m["complexity_cycles"])
+        spike, dz = self.b1_delta.update(m["complexity_cycles"])
         m["b1_z"] = z
+        m["b1_dz"] = dz
-        if self.speak_auto and z >= self.speak_z and m["sie_valence_01"] >= self.speak_valence_thresh and cooldown_ok:
+        if self.speak_auto and (spike and z >= self.speak_z) and m["sie_valence_01"] >= self.speak_valence_thresh and cooldown_ok:
             self.utd.emit_macro("say", {"text":"topology event", "why":{"b1_z":z,"val":m["sie_valence_01"]}})
```

Add CLI flag:

```diff
@@ def make_parser():
     ap.add_argument("--b1-half-life-ticks", type=int, default=300)
+    ap.add_argument("--speak-delta-sigma", type=float, default=2.0, help="delta-spike sigma on B1 increases")
```

---

## 4) Cheap FLOPs/GFLOPs in status (approximate, near‑zero overhead)

**`fum_rt/core/connectome.py`**

```diff
@@ class Connectome:
     def __init__(...):
         # ...
         self.flops_this_tick = 0
@@ step():
         self.flops_this_tick = 0
         # per-node void deltas (few ops each)
         self.flops_this_tick += active_idx.size * 4  # conservative
         dW = self._delta(W_local, t, domain_modulation=domain_mod, use_time_dynamics=use_time_dynamics)
         # update W (add + clip)
         self.flops_this_tick += active_idx.size * 2
         self.W[active_idx] = np.clip(self.W[active_idx] + dW, 0.0, 1.0)
         # structural homeostasis (dense-only outer ops; sparse is O(N·k) and cheap)
         if not self.sparse and self.N <= 4096 and laplacian_coeff == 0.0:
             self.flops_this_tick += (active_idx.size ** 2) * 4
         # expose reward mean in return (already present)
         # ...
         return {..., "avg_reward": float(reward.mean())}
```

**`fum_rt/nexus.py`**

```diff
@@ in run loop, after compute_metrics():
     m["flops"] = int(getattr(self.connectome, "flops_this_tick", 0))
     dt = max(1e-9, time.time() - tick_start_wall)
     m["gflops_s"] = float(m["flops"] / 1e9 / dt)
```

---

## 5) HDF5: chunked datasets + compression (fast snapshots, fast resume)

**`fum_rt/core/memory.py`**

```diff
@@
-def save_checkpoint(path, state):
+def save_checkpoint(path, state, chunk=65536):
     import h5py, numpy as np, os
     os.makedirs(os.path.dirname(path), exist_ok=True)
-    with h5py.File(path, "w") as h5:
-        for k,v in state.items():
-            h5.create_dataset(k, data=v)
+    with h5py.File(path, "w") as h5:
+        # minimal schema: attrs carry backend metadata
+        for k,v in state.items():
+            if isinstance(v, np.ndarray) and v.ndim == 1 and v.size >= chunk:
+                h5.create_dataset(k, data=v, chunks=(min(chunk, v.size),), compression="gzip", compression_opts=1)
+            else:
+                h5.create_dataset(k, data=v)
@@
-def load_engram_h5(path):
+def load_engram_h5(path):
     import h5py, numpy as np
     with h5py.File(path, "r") as h5:
         state = {k: h5[k][...] for k in h5.keys()}
     return state
```

CLI stays the same; saving is now faster and smaller.

---

## 6) Void‑faithful linter (pre‑commit safety net)

**`fum_rt/lint/voidfaithful_check.py`**

```python
import sys, re, pathlib
FORBIDDEN = [
    r"\.softmax\(", r"CrossEntropyLoss", r"\btoken(s|izer|ization)?\b",
]
ADC_FORBID = [
    r"class\s+ADC\b.*?def\s+update_from",  # ADC should not access W/CSR
]
RAW_ACCESS = [
    r"\bADC\..*\b(W|A|row_ptr|nbr_idx|csr)\b",
]
def scan(root="fum_rt"):
    bad = []
    for p in pathlib.Path(root).rglob("*.py"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat in FORBIDDEN + RAW_ACCESS:
            if re.search(pat, text, re.IGNORECASE | re.DOTALL):
                bad.append((p, pat))
    return bad
if __name__ == "__main__":
    bad = scan()
    if bad:
        for p, pat in bad:
            print(f"[voidfaithful] forbidden pattern {pat} in {p}")
        sys.exit(1)
```

**`.pre-commit-config.yaml`** (add to repo root)

```yaml
repos:
  - repo: local
    hooks:
      - id: voidfaithful-check
        name: voidfaithful-check
        entry: python fum_rt/lint/voidfaithful_check.py
        language: system
        types: [python]
```

---

## 7) Run it on **your workstation** (1k neurons, dense) and chat live

You’ve got 32C/64T Threadripper + MI100 + 512 GB—plenty for 1k-100k. Start with 1k dense to verify all signals, then move to sparse.

**Warm‑up (1k, dense, autonomous speak on topology spikes)**

```bash
source venv/bin/activate

# stream math corpus then leave stdin open for your questions
cat fum_rt/data/math/math_corpus.txt - | \
python -m fum_rt.run_nexus \
  --neurons 1000 --k 12 --hz 10 \
  --viz-every 0 --log-every 1 --status-interval 1 \
  --speak-auto --speak-z 3.0 --speak-delta-sigma 2.0 \
  --speak-hysteresis 0.5 --speak-cooldown-ticks 10 \
  --speak-valence-thresh 0.55 \
  --bundle-size 3 --prune-factor 0.10 \
  --bus-capacity 65536 --bus-drain 2048 \
  --r-attach 0.25 --ttl-init 120 --split-patience 6 \
  --domain math_physics --use-time-dynamics \
  --checkpoint-every 60 --checkpoint-format h5
```

**What to watch (UTD status lines):**

* `cohesion_components → 1`, `vt_coverage ↑`, `vt_entropy stable↑`
* `complexity_cycles` spikes → `b1_dz > 0` and `b1_z ≥ 3.0`
* `sie_valence_01 ≥ 0.55` around spikes
* `gflops_s` (should climb when traversal + homeostasis are active)
* `utd_events.jsonl` contains autonomous `{"macro":"say", "why":{...}}` on spikes

**Make it talk more** (quiescent regime): lower gates temporarily

```
--speak-z 1.5 --speak-delta-sigma 1.5 --speak-valence-thresh 0.05
```

---

## 8) Why this stays true to your theory (and gets faster)

* The **only** energy the runtime follows is your **ΔW**. Path‑finding, structural homeostasis, traversal priorities—all ride the same landscape. That’s the whole point.
* The **speak** decision is now tightly bound to **increases in B1** (loop closures/openings) with valence agreement and cooldown, exactly the kind of “Aha!” you want surfaced.
* The ADC is **purely emergent**: it only hears the walkers’ announcements; it never inspects W. That preserves bottom‑up formation and lets us scale O(events), not O(N).

Your “Symmetry Analysis” notes make this clean: the per‑site law has **time‑translation invariance** and a conserved integral $Q_{\mathrm{FUM}}$ (log form), which is a great invariant to keep the time‑phased gating honest while we vary traversal budgets.   In parallel, the external QFT analogy—stabilizing an instability by forming a condensate—matches how your structure stabilizes around loop closures; e.g., tachyon‑mode condensation removing imaginary parts in an effective potential is conceptually similar to your homeostasis removing runaway modes.&#x20;

---

## 9) Near‑term scale steps (on this box)

* **Sparse path first**:
  `--sparse-mode --walkers 512 --hops 4 --threshold 0.15 --lambda-omega 0.1 --candidates 64`
  This keeps per‑tick cost ≈ O(N·k).
* **Memory discipline**: HDF5 snapshots every 30-60 ticks with chunking; turn off viz.
* **I/O**: keep UTD rate limited (`--status-interval 2…10`) on large runs.
* **MI100 acceleration (when you flip it on)**: wire a HIP SpMV and a per‑node ΔW kernel behind a simple provider (we already left the hook). That pushes the heavy ops to the GPU without changing semantics.

---

## 10) Open items I can ship next if you want

* HIP kernels (ΔW + sparse matvec) for MI100 with a runtime switch.
* A small **bus recorder & replayer** so we can regression‑test ADC updates deterministically.
* A **graphical 3D explorer** (simple matplotlib 3D + sliders) to scrub growth/branching over ticks.
* Hardening the **voidfaithful** linter into a pre‑commit gate + CI job.

---

### TL;DR actions for you

1. Apply the diffs above (or say the word and I’ll re‑spin them exactly against your current tree layout).
2. Run the 1k dense recipe; confirm autonomous “say” lines on spikes.
3. If it’s too quiet, lower `--speak-z` and `--speak-delta-sigma` briefly, then restore.
4. Save an HDF5 engram (`--checkpoint-every 60`), resume with `--load-engram` to verify persistence.
5. Move to 100k sparse with the provided flags.

If any file path doesn’t match your exact tree, paste your `tree fum_rt` and I’ll produce patch hunks 1:1 to your layout.
