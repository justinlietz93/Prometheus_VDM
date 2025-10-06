awesome—let’s move one clean step at a time.

# Instruction 1 — Wire **SIE** + **Structure/Morphogenesis** knobs from `phase.json` into the live Nexus (no behavior change, just control)

Goal: your **dashboard** already writes `runs/<ts>/phase.json`. This patch makes the Nexus **consume** new keys and push them directly into the running connectome without restarts:

* `sie`: `{ w_td, w_nov, w_hab, w_hsi, hab_tau, target_var }`
* `structure`: `{ growth_fraction, alias_sampling_rate, b1_persistence_thresh, pruning_low_w_thresh, pruning_T_prune }`
* `schedule`: `{ adc_entropy_alpha, ph_snapshot_interval_sec }`

It’s defensive: if an attribute doesn’t exist on your current `Connectome`, it silently skips (so we don’t break your tree). No changes to update rules yet—this just exposes the controls you asked for.

---

### Apply this patch

**File:** `fum_rt/nexus.py`

```diff
diff --git a/fum_rt/nexus.py b/fum_rt/nexus.py
index 7b1ad1e..94fb2b3 100644
--- a/fum_rt/nexus.py
+++ b/fum_rt/nexus.py
@@ -1,6 +1,7 @@
 import asyncio, json, time, os
 from collections import deque
 from dataclasses import dataclass
+from typing import Any, Dict

 # ... existing imports ...

 class Nexus:
@@
-    def _apply_phase_profile(self, prof):
-        """
-        Called on every tick if runs/<ts>/phase.json changed.
-        Applies speak gates and traversal knobs that Nexus already supports.
-        """
+    def _apply_phase_profile(self, prof: Dict[str, Any]):
+        """
+        Called on every tick if runs/<ts>/phase.json changed.
+        Now also applies SIE and Structure/Morphogenesis knobs to the live connectome.
+        Safe: attributes are set only if present on the connectome.
+        """
         # ==== existing gates you already support ====
         speak = prof.get("speak", {})
         if speak:
             self.speak_auto          = bool(speak.get("speak_auto", getattr(self, "speak_auto", False)))
             self.speak_z             = float(speak.get("speak_z", getattr(self, "speak_z", 2.0)))
             self.speak_hysteresis    = float(speak.get("speak_hysteresis", getattr(self, "speak_hysteresis", 0.5)))
             self.speak_cooldown      = int(speak.get("speak_cooldown_ticks", getattr(self, "speak_cooldown", 20)))
             self.speak_valence_thresh= float(speak.get("speak_valence_thresh", getattr(self, "speak_valence_thresh", 0.0)))

         conn = self.connectome

+        # helper to set nested attrs if they exist
+        def _set(obj, name, value):
+            if obj is None: return False
+            if hasattr(obj, name):
+                setattr(obj, name, value)
+                return True
+            return False
+
+        # ==== SIE knobs ====
+        sie = prof.get("sie")
+        if sie:
+            # accept either connectome.sie.cfg or connectome.sie_cfg (both observed in your trees)
+            sie_obj = getattr(conn, "sie", None)
+            cfg     = getattr(sie_obj, "cfg", None) or getattr(conn, "sie_cfg", None)
+            for k in ("w_td","w_nov","w_hab","w_hsi","hab_tau","target_var"):
+                if k in sie:
+                    if cfg is not None and hasattr(cfg, k):
+                        setattr(cfg, k, float(sie[k]))
+                    else:
+                        _set(conn, k, float(sie[k]))  # last‑ditch: put on connectome if you exposed it there
+
+        # ==== Structure / Morphogenesis knobs ====
+        st = prof.get("structure", {})
+        if st:
+            # growth/sampling
+            _set(conn, "growth_fraction",      float(st.get("growth_fraction",      getattr(conn, "growth_fraction", 0.0))))
+            _set(conn, "alias_sampling_rate",  float(st.get("alias_sampling_rate",  getattr(conn, "alias_sampling_rate", 0.0))))
+            # pruning / topology thresholds
+            _set(conn, "b1_persistence_thresh", float(st.get("b1_persistence_thresh", getattr(conn, "b1_persistence_thresh", 0.0))))
+            _set(conn, "pruning_low_w_thresh",  float(st.get("pruning_low_w_thresh",  getattr(conn, "pruning_low_w_thresh", 0.0))))
+            _set(conn, "pruning_T_prune",       int(  st.get("pruning_T_prune",       getattr(conn, "pruning_T_prune", 0))))
+
+        # ==== Schedules / housekeeping ====
+        sched = prof.get("schedule", {})
+        if sched:
+            _set(self, "adc_entropy_alpha",        float(sched.get("adc_entropy_alpha",        getattr(self, "adc_entropy_alpha", 0.0))))
+            _set(self, "ph_snapshot_interval_sec", float(sched.get("ph_snapshot_interval_sec", getattr(self, "ph_snapshot_interval_sec", 60.0))))
+
+        # Optional: log a compact summary once per change
+        if prof.get("_source") != "NEXUS":
+            try:
+                sie_dbg = {k: getattr(getattr(conn, "sie", None).cfg, k) for k in ("w_td","w_nov","w_hab","w_hsi")} if getattr(conn, "sie", None) else {}
+            except Exception:
+                sie_dbg = {}
+            self.logger.info(f"[NEXUS] phase applied | speak_auto={getattr(self, 'speak_auto', False)} "
+                             f"| SIE={sie_dbg} | structure={{gf:{getattr(conn,'growth_fraction',None)}, "
+                             f"b1:{getattr(conn,'b1_persistence_thresh',None)}, prune_T:{getattr(conn,'pruning_T_prune',None)}}}")
```

> If your `_apply_phase_profile` is named/located slightly differently, drop this block into that method (logic is independent of exact line numbers).

---

### How to test this step

1. Start the runtime the way you already do (Dashboard → **Start Run**).
2. In the **Runtime Controls** (left panel), add a minimal SIE section to the `phase.json` (the dashboard can expose these fields next, but for now you can edit the active file):

```json
{
  "sie": { "w_td": 0.55, "w_nov": 0.25, "w_hab": 0.05, "w_hsi": 0.15, "hab_tau": 800, "target_var": 0.08 },
  "structure": { "growth_fraction": 0.02, "b1_persistence_thresh": 0.12, "pruning_low_w_thresh": 0.01, "pruning_T_prune": 600 }
}
```

3. Within one tick you should see a log line like:

```
[NEXUS] phase applied | speak_auto=... | SIE={'w_td': 0.55,...} | structure={gf:0.02, b1:0.12, prune_T:600}
```

4. (Optional) If your `Connectome.step()` already computes SIE metrics, you’ll also see the numbers in your metrics stream change when you move the sliders and re‑save `phase.json`.

---

### Why this step first

* Your dashboard already writes a validated `phase.json`. Making Nexus ingest **SIE** and **Structure** now unblocks the next two steps (surfacing the sliders on the UI and restoring canonical SIE + void‑driven morphogenesis in the core) without bouncing processes.
* It doesn’t change learning—just gives you live control paths. If any attribute isn’t in your current `Connectome`, it’s skipped (no crashes).

---

If you want me to fire the **next** instruction, say “next step” and I’ll patch `Connectome.step()` to **emit** canonical SIE metrics (`novelty`, `hab_mu`, `hab_var`, `hsi`, `total_reward`) and (if present) your **B1 persistence** so the dashboard can chart them live.
