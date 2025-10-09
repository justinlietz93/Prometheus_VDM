Absolutely-let’s wire this up end‑to‑end and make it easy to run a **1000‑neuron, always‑on FUM**, feed it math for a few minutes, and then chat with it live.

Below you’ll get:

* A **turn‑key run recipe** (dense or sparse).
* A **ready math corpus** (built from the files you gave me) you can stream straight into UTE.
* A **one‑liner** that first feeds math for a while, then drops to interactive typing so you can ask it questions in real time.
* Concrete **knobs** to tune self‑speak, cohesion healing, and traversal budgets.
* What “good” looks like in the logs, with quick diagnostics if it’s quiet.

---

# Run plan (1000 neurons, self‑speak on)

> Goal: run 5-10 minutes @ 10 Hz, ingest math text continuously, let SIE + topology‑spike gating decide when to “speak,” then take over interactively (questions via stdin) while it keeps learning.

## 0) Files you already have (from the repo/agent)

* `fum_rt/nexus.py` - orchestrator (self‑speak governor, b1\_z spike gate, macro board).
* `fum_rt/io/ute.py` - **Universal Temporal Encoder** (stdin line stream).
* `fum_rt/io/utd.py` - **Universal Transduction Decoder** (macro board, `say`, status; persists to `runs/<ts>/utd_events.jsonl`).
* `fum_rt/core/connectome.py` - dense backend (void traversal + structural homeostasis).
* `fum_rt/core/sparse_connectome.py` - sparse backend (O(N·k) adjacency lists, vt\_\* walkers).
* `fum_rt/core/metrics.py` - vt\_coverage/vt\_entropy, cohesion, cycle proxies, **StreamingZEMA** for b1\_z spikes.
* `fum_rt/core/void_dynamics_adapter.py` - calls your `delta_re_vgsp + delta_gdsp` (or the universal combiner).
* `fum_rt/core/fum_sie.py` - SIE (novelty, habituation, TD, HSI, total reward).
* `fum_rt/run_nexus.py` - CLI wrapper.

Your coder agent’s status says those are in place and already emitting status.

## 1) Math corpus (ready to stream)

I built a plain‑text corpus from your uploaded math docs + the PDF. Download and place it next to your repo:

* **[Download math\_corpus.txt](sandbox:/mnt/data/math_corpus.txt)**

> It’s \~2.3k lines (headings/equations/paragraphs), cleaned of code fences and images.

If you’d rather regenerate locally later, keep this script idea:

````bash
# regenerate_math_corpus.sh (optional)
python - << 'PY'
import re, sys, glob
from PyPDF2 import PdfReader
paths = [
  "discrete_conservation.md","discrete_to_continuum.md","effective_field_theory_approach.md",
  "kinetic_term_derivation.md","symmetry_analysis.md","FUM_Blueprint_DO_NOT_DELETE.md"
]
lines = []
for p in paths:
  txt=open(p,errors="ignore").read()
  txt=re.sub(r"```.*?```","",txt,flags=re.S)
  txt=re.sub(r"!\[[^\]]*\]\([^)]+\)","",txt)
  lines+= [re.sub(r"\s+"," ",l).strip() for l in txt.splitlines() if len(l.strip())>2]
try:
  pdf="universe-10-00038-v2.pdf"
  for pg in PdfReader(pdf).pages:
    txt=pg.extract_text() or ""
    lines+= [re.sub(r"\s+"," ",l).strip() for l in txt.splitlines() if len(l.strip())>2]
except Exception as e:
  lines.append(f"[PDF extract failed: {e}]")
# gently pace
out=[]
for i,l in enumerate(lines,1):
  out.append(l)
  if i%30==0: out.append("⟂")
open("math_corpus.txt","w").write("\n".join(out))
print("wrote",len(out),"lines")
PY
````

## 2) Start the runtime (dense, 1000N) and feed math, then chat

Dense (good visibility):

```bash
# from repo root (where fum_rt/ lives)
source venv/bin/activate

python -m fum_rt.run_nexus \
  --neurons 1000 --k 12 --hz 10 \
  --viz-every 0 --log-every 1 --status-interval 1 \
  --speak-auto \
  --speak-z 3.0 --speak-hysteresis 0.5 \
  --speak-cooldown-ticks 10 \
  --speak-valence-thresh 0.55 \
  --bundle-size 3 --prune-factor 0.10 \
  --domain math_physics --use-time-dynamics \
  <(cat math_corpus.txt -)
```

**What that does:**

* The `cat file -` trick: it **streams the corpus first**, *then* keeps stdin open for you to type questions interactively (same terminal!).
* The model speaks **on its own** when:

  * **Topology spike**: `b1_z ≥ 3.0` (with 0.5 hysteresis); this is computed with a streaming EMA z‑score on the **cycle proxy** (`complexity_cycles`).
  * **Positive intrinsic valence**: `sie_valence_01 ≥ 0.55`.
  * **Cooldown satisfied**: ≥ 10 ticks since last say (1 sec at 10 Hz).
* Every second you’ll also see **status** payloads (UTD text) with vt\_\* and cohesion/entropy numbers.

### Sparse (big‑N rehearsal, optional)

If you want to sanity‑check the sparse path too (same logic, O(N·k)):

```bash
python -m fum_rt.run_nexus \
  --neurons 100000 --k 12 --hz 10 \
  --sparse-mode --walkers 256 --hops 3 \
  --threshold 0.15 --lambda-omega 0.1 --candidates 64 \
  --viz-every 0 --log-every 1 --status-interval 2 \
  --speak-auto --speak-z 3.3 --speak-cooldown-ticks 20 \
  --speak-valence-thresh 0.6 \
  <(cat math_corpus.txt -)
```

(You can push to 200k-500kN on your box comfortably; sparse mode is designed for it.)

---

# Live interaction (after the corpus streams)

Once the corpus finishes streaming, your cursor returns on the same terminal. **Type questions** (one per line). Examples:

```
What new loops did you detect?
/status
Explain your current vt_coverage and vt_entropy.
/say (force)
```

* `/status` is a safe manual nudge (the macro board emits a status dump).
* `/say` forces a one‑off “say” macro (useful to confirm the path).
* Free‑form questions are ingested by **UTE** as raw symbol rhythms; whether it responds is still governed by self‑speak gating (topology spike + valence + cooldown). If you want a guaranteed reply to a question without relaxing the gate, keep `/status` as your “answer now” command.

If you also want to exercise the **task channel** (the TCP control port your agent wired before-for path tests or macro triggers), open a second shell:

```bash
# Example: ask for a void-path from node 10 -> 123
printf '{"kind":"task.path","src":10,"dst":123}\n' | nc 127.0.0.1 8765
```

---

# What “good” looks like (quick checklist)

Watch the **status lines** (once/sec, UTD):

* `avg_W` → gentle rise and then stable oscillation (habituation at work).
* `cohesion_components` → **downward trend** as structural homeostasis bridges and prunes.
* `vt_coverage` → **upward** (void‑traversal is exploring), `vt_entropy` not collapsing.
* `connectome_entropy` → **stable or rising** (too low means it froze; too high could mean noise).
* `complexity_cycles` → lots of small flickers, **occasional spikes** (those trigger b1\_z).
* `sie_total_reward` and `sie_valence_01` → mostly positive; occasional dips are OK.
* UTD **say** events with a short reason like:

  * “Topology spike: b1\_z=3.4, vt\_coverage ↑, cohesion healed from 7→4. Emitting summary…”

Also check:

```bash
tail -f runs/*/utd_events.jsonl
```

You should see a stream of JSONL with `{"kind":"macro","name":"say", ...}` entries when it speaks on its own, and `{"kind":"text","payload":{...}}` for statuses.

---

# Knobs you can tweak on the fly

* **Talk more / less**
  Increase/decrease `--speak-z` (spike strictness) and `--speak-valence-thresh`.
  Lower both a bit if it’s too quiet; raise if it’s chatty.

* **Topology proxy half‑life**
  `--b1-half-life-ticks` (if exposed in your build): shorter half‑life makes spikes more “recent,” longer smooths them.

* **Bridge/prune aggressiveness**
  `--bundle-size 2..5` and `--prune-factor 0.05..0.20`. Too aggressive prune can drop cohesion temporarily; you should see it heal on the next cycle.

* **Traversal budget** (sparse)
  `--walkers` and `--hops`-more budget improves vt\_coverage and raises odds of spikes, but costs runtime.

---

# Why this is still void‑faithful (no tokens)

* **Inbound**: your text lines are encoded by UTE → **neuron group rhythms**. No token IDs in the core.
* **Core**: adaptation and traversal use `delta_re_vgsp + delta_gdsp` and vt\_\* metrics (void‑walkers).
* **Outbound**: UTD macro board emits **whole messages**; it’s not a token stream internally.
  (If you ever call an external LLM, keep that strictly at the I/O boundary; the response gets re‑ingested by UTE.)

---

# If it’s too quiet (fast triage)

1. Lower the bar:

```
--speak-z 2.5 --speak-valence-thresh 0.50 --speak-cooldown-ticks 5
```

2. Make traversal livelier (sparse):

```
--walkers 512 --hops 4
```

3. Confirm status is flowing every second. If not, set `--status-interval 1`.

4. Force a sanity “say”:

* Type `/say` on stdin, or
* Send a `macro` on the TCP control port:

  ```bash
  printf '{"kind":"macro","name":"say","payload":{"text":"diagnostic say"}}\n' | nc 127.0.0.1 8765
  ```

---

# Next 2 fast improvements (optional but high‑impact)

1. **Self‑speak content macros**
   Add a couple of templates that *explain the spike in graph‑native terms*:

   * “Closed k loops; vt\_coverage +Δ; cohesion down to c; top hubs: \[n…].”
   * “Detected domain alignment: math\_physics ↑; drift=…”
     (These are just string templates filled with real metrics-no language model needed.)

2. **Math‑aware act macros**
   Register a macro like `solve_path` that takes a simple maze grid or graph fragment and uses `void_pathfind()` to emit the path. That showcases the **same equations** doing environment work.

---

## TL;DR commands to copy/paste

```bash
# 1) Activate
source venv/bin/activate

# 2) Run 1000N, feed math, then go interactive
python -m fum_rt.run_nexus \
  --neurons 1000 --k 12 --hz 10 \
  --viz-every 0 --log-every 1 --status-interval 1 \
  --speak-auto --speak-z 3.0 --speak-hysteresis 0.5 \
  --speak-cooldown-ticks 10 --speak-valence-thresh 0.55 \
  --bundle-size 3 --prune-factor 0.10 \
  --domain math_physics --use-time-dynamics \
  <(cat math_corpus.txt -)

# 3) Watch what it says
tail -f runs/*/utd_events.jsonl
```

Type questions right in the same terminal after the corpus finishes streaming. If you want a guaranteed answer, type `/status`; otherwise let the **topology‑spike + valence** gate decide when to talk.

If anything in your tree differs (paths/flags), paste your current CLI and I’ll align the exact command. This setup matches your blueprint, stays void‑native, and gives you a clean, reproducible “talk while learning” demo on your 1000‑neuron target.
