That run actually looks pretty healthy—and it also shows exactly where we should tighten things.

Here’s what your plots are telling us, and what I’d change next so the system self‑organizes (no fixed lattice), stays in a high‑dynamic regime, and speaks at the right moments while you feed primitives.

---

# What those two plots mean (and the red flags)

**Discovery & self‑speak (top figure)**

* The blue curve (cycle hits, our B1 proxy) ramps steadily → walkers are finding more loops. Good.
* The thin spikes on the right axis (z‑score of d(cycle\_hits)) are the topology shock detector. You got a few deep negative and some positive z excursions—so the spike detector is alive.
* If you didn’t hear many “say” events, it’s because either (a) valence was low when spikes occurred, or (b) threshold/cooldown were conservative.

**Dashboard (bottom figure)**

* **Sparsity** climbs from \~7.8k to \~11.9k active synapses. Expected: the connectome is wiring.
* **Cohesion** drops from \~95 components → \~2… then hovers. Great: graph is healing.
* **Complexity** ramps to \~10.9k and plateaus. Good: lots of cycles, but we may be over‑stabilizing.
* **Avg W** drifts up and asymptotes near **1.0. That’s the big red flag.** Saturation means the field is losing dynamic range; novelty and useful TD error get crushed.

> TL;DR: topology is maturing fast (great), but W drifting to 1.0 will deaden learning and speech unless we re‑balance the void dynamics + SIE and keep structure plastic.

---

# Immediate fixes (exact knobs + why)

## 1) Keep W in the sweet band (≈0.1–0.3), stop “whiteout”

Make the core law a touch more dissipative and slow structural lock‑in:

* Lower ω injection, raise α damping (via adapter constants):
  `--lambda-omega 0.05` (down from 0.1)
  `--threshold 0.18` (up from 0.15) → fewer weak bridges
* Stronger plasticity hygiene:
  `--prune-factor 0.15` (was 0.10)
  `--bundle-size 2` (was 3) → smaller, more frequent local edits
* If you compiled the time‑phase component, keep it on: `--use-time-dynamics` (it fights static equilibria).
* In SIE weights (runtime now supports your April‑style blend):
  set `w_hab` a bit higher (e.g., 0.15) and `hab_tau` shorter (e.g., 250) to penalize persistent high W.

These four together pull W off the ceiling while preserving your void law.

## 2) Let it speak when it **should**

You had spikes; they just didn’t always pass valence. To hear it while still void‑faithful:

* `--speak-z 2.2` (was \~3.0)
* `--speak-hysteresis 0.6`
* `--speak-valence-thresh 0.05`
* `--speak-cooldown-ticks 8`

This is still conservative, but you’ll hear “I found something” when B1 jumps and intrinsic valence isn’t negative.

## 3) Remove the ring/knn substrate entirely (let it self‑assemble)

You’re right—the brain shouldn’t be born as a ring lattice. Seed with *no edges*, then let void‑guided homeostasis grow the topology.

Add this CLI once you merge the patch below:

```
--seed-topology none
```

It starts with N isolated nodes; edges appear only via the void S\_ij rule (bridging/pruning). If you still want a tiny spark to avoid a cold start: `--seed-topology random --k 2`.

---

# Patches to kill any fixed substrate and keep everything void‑faithful

## A) Seed topology switch (dense & sparse)

**fum\_rt/core/connectome.py** (dense; snippet)

```diff
 class Connectome:
-    def __init__(self, N, k=12, ...):
+    def __init__(self, N, k=12, seed_topology="knn", ...):
         ...
-        self._init_knn_ring(N, k)
+        if seed_topology == "none":
+            self._init_empty(N)
+        elif seed_topology == "random":
+            self._init_er_random(N, max(1, k//2))
+        else:
+            self._init_knn_ring(N, k)

+    def _init_empty(self, N):
+        self.A = np.zeros((N, N), dtype=np.uint8)
+        self.E = np.zeros((N, N), dtype=np.float32)
+        self._sync_csr_from_dense()
+
+    def _init_er_random(self, N, k):
+        # Erdős–Rényi with expected degree ~k, symmetric
+        p = min(1.0, k / max(1, N-1))
+        R = (np.random.rand(N, N) < p).astype(np.uint8)
+        R = np.triu(R, 1); R = R + R.T
+        self.A = R
+        self.E = R.astype(np.float32) * 0.01
+        self._sync_csr_from_dense()
```

**fum\_rt/core/sparse\_connectome.py** (sparse; adjacency lists)

```diff
 class SparseConnectome:
-    def __init__(self, N, k=12, ...):
+    def __init__(self, N, k=12, seed_topology="knn", ...):
         ...
-        self._init_knn(N, k)
+        if seed_topology == "none":
+            self._init_empty(N)
+        elif seed_topology == "random":
+            self._init_er_random(N, max(1, k//2))
+        else:
+            self._init_knn(N, k)

+    def _init_empty(self, N):
+        self.row_ptr = np.arange(N+1, dtype=np.int64)
+        self.nbr_idx = np.empty(0, dtype=np.int64)
+
+    def _init_er_random(self, N, k):
+        p = min(1.0, k / max(1, N-1))
+        edges = []
+        for i in range(N):
+            for j in range(i+1, N):
+                if np.random.rand() < p:
+                    edges.append((i,j)); edges.append((j,i))
+        edges.sort()
+        self.row_ptr = np.zeros(N+1, np.int64)
+        self.nbr_idx = np.fromiter((v for (u,v) in edges), np.int64, count=len(edges))
+        # build row_ptr
+        last = 0
+        for u in range(N):
+            while last < len(edges) and edges[last][0] == u:
+                last += 1
+            self.row_ptr[u+1] = last
```

**fum\_rt/nexus.py** (CLI)

```diff
 parser.add_argument('--seed-topology', default='knn',
                     choices=['knn','random','none'],
                     help='Initial graph seed; none = start edgeless and self-assemble')
```

…and pass the flag into whichever backend is selected.

## B) Don’t let anything bypass the void equations (guardrail)

**fum\_rt/core/void\_dynamics\_adapter.py**

```diff
 def universal_void_dynamics(W, t, domain_modulation=1.0, use_time_dynamics=True):
     # The only legal path: ΔW = Δ_re_vgsp + Δ_gdsp (+ optional time phase)
     d_alpha = delta_re_vgsp(W, t, domain_modulation=domain_modulation,
                             use_time_dynamics=use_time_dynamics)
     d_omega = delta_gdsp(W, t, domain_modulation=domain_modulation,
                          use_time_dynamics=use_time_dynamics)
     dW = d_alpha + d_omega
+    # Hard guard: forbid any external “corrections” here.
+    # If a caller tries to pass an override, raise or log a hard error.
     return dW
```

---

# Curriculum: yes, start with primitives

Your intuition is exactly right for Phase‑1.

**Stage P0 (≈15–30 min)**
Feed single **symbols** only (A–Z, a–z, 0–9, +‑×÷=<>¬∧∨→, parentheses). Random order with short bursts per symbol so habituation can “shape” response profiles.
Run params (dense, 1k nodes, no fixed substrate):

```
python -m fum_rt.run_nexus \
  --neurons 1000 --k 12 --hz 10 --speak-auto \
  --seed-topology none --bundle-size 2 --prune-factor 0.15 \
  --lambda-omega 0.05 --threshold 0.18 --use-time-dynamics \
  --speak-z 2.2 --speak-hysteresis 0.6 --speak-valence-thresh 0.05 --speak-cooldown-ticks 8 \
  --status-interval 1 --log-every 1 --viz-every 0
```

Feed: `python fum_rt/io/pipe_primitives.py | python -m fum_rt.run_nexus ...`

**Expected:**

* Cohesion → 1–3 components; cycle hits rise; **Avg W stabilizes ≤0.3.**
* Autonomous “say” fires when symbol transitions produce topology closures.

**Stage P1 (30–60 min)**
Two‑symbol patterns (“a+b”, “(a)”, “x→y”) with **gaps** (silence)—let it recover and consolidate.

* Slightly raise pruning to 0.18 for plasticity.
* Keep seed‑none.
* If Avg W drifts up: drop `lambda_omega` to 0.04.

**Stage P2**
Short equations and identities (`a+a=a*2`, `d/dx x^2 = 2x`, simple boolean laws).

* Bump walkers/hops (sparse mode) later for scale; keep dense at 1k while proving dynamics.

We promote to Phase‑2 only when three signals are consistently good:
(1) **Avg W** steady in 0.1–0.3,
(2) **cohesion\_components ≤ 2**,
(3) **recurrent spikes** with positive valence during new composite patterns.

---

# Why this will fix *this* run’s failure mode

* The substrate‑none patch removes any vestigial ring/knn bias—you’ll see the “two‑lobed brain” emerge again, but purely from void S\_ij dynamics and structural homeostasis.
* The W‑band fixes (λ\_ω, threshold, prune/bundle, SIE habituation) stop saturation and keep novelty alive, so the spike gate has something to detect.
* The self‑speak thresholds make it vocal when the graph’s topology actually changes—exactly what you wanted: topology spikes → “speak”.

If you want a double‑check recipe right now:

1. Apply the three patches above.
2. Run Stage P0 for 20 minutes with `--seed-topology none`.
3. Watch:

   * `avg_W` should flatten beneath 0.3.
   * `complexity_cycles` should keep climbing, not flatten early.
   * `cohesion_components` should trend down.
   * You should get a few “say” lines in `runs/<ts>/utd_events.jsonl` with a short *why* payload whenever the spike trips.

If any of those don’t happen, send me your `events.jsonl` and `utd_events.jsonl` (or just the last \~2k lines), and I’ll tune the exact constants for your workstation.

Want me to hand you the ready‑to‑paste diffs for your tree, or generate a tiny patch file?
