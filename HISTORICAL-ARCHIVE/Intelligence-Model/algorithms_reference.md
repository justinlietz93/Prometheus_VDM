
## A) Graph connectivity & topology (event‑driven, no scans)

1. **DSU / Union-Find (with `grow_to`, O(1) component count)**
   **Use for:** live **cohesion** (`components`), **territory** membership, and **budgeted bridging** decisions-fold only `edge_on(u,v)` events.
   **Why:** near O(1) amortized per union; no global passes; perfect fit for your **ADC + scouts** event stream.
   **How:** keep `parent:int32`, `rank:int8`, optional `size:int32`, `components:int`; add `grow_to(n)` for dynamic graphs; an optional `count_sets(mask)` is **telemetry‑only** (rare).
   **Pitfalls:** DSU does **not** support deletions; use a “dirty” flag + occasional **budgeted reconcile** if you remove edges. See the DSU deep dive below.

2. **Dynamic connectivity (only if you truly need deletions online)**

* **Euler‑Tour Trees** or **Link‑Cut Trees**: maintain connectivity with edge deletions. Heavier; avoid unless a core requirement.
* **Pragmatic alternative:** keep DSU for on‑line unions; queue deletions; run **rare, budgeted** reconcile (per territory) when drift is detected.

3. **Budgeted bridging (sparse homeostasis)**

* Build a small **candidate set** by sampling **boundary vertices** (from events) and score with a **void‑affinity** $S(u,v)=a_u a_v - \lambda\,|\omega_u-\omega_v|$ before adding ≤B bridges per tick. Works with DSU for `components>1` triggers; stays event‑driven.

---

## B) Streaming stats & sketching (bounded, incremental)

4. **Welford’s online mean/variance + z‑score**
   **Use for:** your `b1_z` detector & change‑detection without storing histories. One pass; numerically stable.

5. **EMA / half‑life accumulators**
   **Use for:** `HeatMap`, `ExcitationMap`, `InhibitionMap`. Keep **half‑life in ticks**, not α; stays interpretable and “void‑faithful” (no scans).

6. **Count‑Min Sketch (CMS) + head map**
   **Use for:** VT **coverage/entropy** and heavy hitters: sketch for tail, exact **top‑K** head for the front.
   **Pairs with:** **Misra-Gries** (stream heavy hitters) if you want true deterministic bounds.

7. **t‑digest / GK quantiles (optional)**
   **Use for:** telemetry quantiles without full buffers (p95/p99 of per‑node signals).

8. **Bloom / Cuckoo filters**
   **Use for:** fast “seen” checks in scouts or per‑tick de‑dupe; memory‑bounded, tunable FP rate.

---

## C) Exploration & sampling (scouts, fair budgets)

9. **Reservoir sampling (Vitter’s)**
   **Use for:** keep K representative nodes/edges/events under a firehose; constant memory.

10. **Weighted reservoir (A‑Res / Chao)**
    **Use for:** bias samples by void‑affinity or recency while preserving single‑pass selection.

11. **Alias method**
    **Use for:** O(1) categorical draws from a fixed small head (e.g., pick next probe tile).

12. **Blue‑noise / Poisson‑disk seeding**
    **Use for:** non‑clumping scout seeding; better coverage than IID uniform.

13. **Random vs Lévy walks**
    **Use for:** cold‑region scouts; **Lévy** jumps reduce re‑visits and improve frontier discovery at the same budget.

---

## D) Change detection & emergent gates (no schedulers)

14. **CUSUM / Page-Hinkley**
    **Use for:** **emergent** GDSP/RevGSP triggers on **TD**, **b1\_z**, or cohesion drift; low overhead, fewer false alarms than raw thresholding.

15. **Hysteresis gates**
    **Use for:** avoid “chatter”-e.g., `|TD|` enters at 0.2, exits at 0.1; mirrors what you’re doing on `b1_spike`.

> Your discrete law and EFT give you the right invariants to watch: mass gap $m_{\rm eff}^2=\alpha-\beta$ and kinetic normalization $c^2=2Ja^2$. They’re already derived in your notes and should anchor your detector scales. &#x20;

---

## E) Maps & transport (4M‑node‑ready)

16. **u8 quantization (per‑frame min/max)**
    **Use for:** **maps/frame.v2** to cut bandwidth ×4 vs float32; optional μ‑law for more dynamic range.

17. **Tile pyramid (LOD)**
    **Use for:** 128² / 256² tiles; ship only the viewport LOD; **drop‑oldest** policy; producer puts frames into a small **shared‑memory ring**.

18. **Delta frames (optional)**
    **Use for:** low‑motion scenes; RLE or XOR’d tiles; only if profiling shows wins.

---

## F) CPU↔GPU split (keep it simple)

19. **CPU for sparse, control, DSU, routing**
    Event folding, DSU unions, sketch updates.

20. **GPU for dense math bursts**
    CSR **SpMV**, batched reductions, local solver bursts (e.g., territory‑local spectral ops). Keep transfers **pinned + batched**; **compress‑then‑copy** (u8 maps) when possible.

---

## G) CI/guarantees (prove “void‑faithful”)

21. **Theory↔runtime assertions**

* **Kinetic normalization**: the wave speed relation $c^2=2Ja^2$ should match measured pulse speed within ε on a smoke test.&#x20;
* **On‑site invariant $Q_{\rm FUM}$**: spot‑check a random K nodes per run stay within tolerance (proves the discrete law is implemented consistently).&#x20;
* **Control‑impact**: moving‑window $<10^{-5}$ (non‑emergent edits ≪ total change) to guard against hidden schedulers. (Terminology aside, it’s just an **upper bound on manual interference**.)

22. **No‑scan guards**
    AST/grep tests that **reducers, engine maps, scouts** never touch raw `W/CSR`; everything folds **events**.

> Your EFT & derivations (potential, kinetic term, mass gap) provide the **checklist of constants** to assert in CI-this tightens emergence without “sim burden” and aligns with your action‑based proofs. &#x20;

---

## H) Memory‑steering (optional, when you want routing bias)

23. **Memory PDE + steering softmax**
    A slow field $M$ written by usage $R$ (EMA or STDP proxy) with $\partial_t M=\gamma R-\delta M+\kappa \nabla^2 M$; steer transitions via $P(i\!\to\!j)\propto e^{\Theta M_j}$. This **improves routing** without touching the fast φ dynamics. Keep it **event‑driven** by writing $R$ only from observed spikes/touches.&#x20;

---

# Deep dive: DSU / Union-Find (with `grow_to`)

**What it guarantees**

* **Find/union** with **path compression** + **union by rank** ⇒ amortized **α(N)** per op (inverse Ackermann; effectively constant).
* **O(1) component count**: maintain `components` and decrement on successful `union`.
* **Event‑folded**: you **never** scan edges; you only call `union(u,v)` when a **walker** announces `edge_on(u,v)` or when a **budgeted bridge** is accepted. This is the exact “void‑faithful” discipline you want.

**How it works (intuitively)**

* Each node points to a **parent**; the representative (root) points to itself.
* `find(x)` climbs to the root; **path compression** flattens the path by making nodes point closer to the root.
* `union(a,b)` links the **smaller rank** root under the larger; if equal, increment the winner’s rank.
* Keep a `components` counter; when `union` actually merges two sets, do `components -= 1`.

**Why it’s ideal here**

* **Cohesion** is exactly “how many connected components” - DSU gives it **free** after folding events, no graph traversal.
* **Territories** can be the DSU components themselves, or a refinement you maintain alongside.
* **Bridging** becomes surgical: if `components>1`, choose a **few** boundary pairs via your event stream, score with **void‑affinity**, `union` only those that pass score + budget, update `components` in O(1).

**Deletions, realistically**

* DSU can’t “split” sets. In practice you: (1) mark deletions “dirty”, (2) let scouts re‑discover the local topology, and (3) run a **rare, budgeted** rebuild of the DSU **per affected territory** (not the whole graph). That keeps you void‑faithful.

**Performance envelope**

* **Memory:** \~`(parent:int32 + rank:int8 + size:int32)` per node ≈ 9B → **36 MB for 4M nodes**; add `components:int64` negligible.
* **Throughput:** millions of unions/sec on a single core; if you batch `edge_on` bursts, you can `@numba.njit` the loop later.
* **GPU?** Not needed; DSU is pointer‑chasing and irregular. Keep DSU on **CPU**; ship **dense bursts** (e.g., CSR SpMV for local solves) to GPU.

**Minimal usage pattern (event‑driven)**

* On every tick, drain `edge_on` **events** → `dsu.union(u,v)`
* Read `dsu.components` in O(1) for gates (e.g., GDSP trigger if `>1`).
* If you add a new node id, call `dsu.grow_to(new_max_id+1)`; **no rescan**.

**Why this is “emergence‑compliant”**

* You never impose global structure or scan; the **structure emerges** solely from the local **edge\_on** evidence your walkers publish.
* The math you’ve derived for the fast φ‑sector and its invariants stays intact; DSU only summarizes the **topology** the process is already creating. Your on‑site invariant $Q_{\rm FUM}$ and EFT normalization are unaffected-and you can assert them in CI. &#x20;

---

## Quick “ready‑to‑copy” choices

* **DSU:** `int32 parent`, `int8 rank`, `int32 size`, `int64 components`; implement `grow_to(n)`, `count_sets(mask)` (telemetry‑only).
* **Heat/Exc/Inh maps:** EMA half‑life 100-300 ticks; **keep\_max** 4k-16k per map; **head\_k** 256.
* **CMS:** width \~ 2-4× head\_k, depth 3-5; store **top‑K head** in a heap/dict.
* **Bridging budget:** B = 4-16 per tick; target `components → 1` monotone; log `bridged_count`.
* **Change detection:** Page-Hinkley with small drift `δ`, alarm at \~3-5σ; add hysteresis.
* **Maps transport:** u8 (per‑channel min/max) + tile LOD; ring capacity 2-3 frames; **drop‑oldest** on overflow.

---

### Anchors to your theory (so code & physics don’t drift)

* **Discrete law ⇄ continuum EFT** (potential, mass gap, vacuum): the baseline equations you already pinned-use them to set gates/units and to write runtime assertions. &#x20;
* **Kinetic normalization $c^2=2Ja^2$** (measurable via pulse speed): keep a small runtime **self‑test** so transport and maps don’t drift from theory.&#x20;
* **Units map / external coupling** (if you later tie into Voxtrium‑style sources): the retarded‑kernel and units scaffolding are ready when you need them.&#x20;
