Yes—starting with *primitives first* is exactly the right move, and you don’t need tokens inside the core to do it. Think of Phase‑0 as “teaching the organism the alphabet of reality”: single characters, digits, and a tiny set of logic/math operators, emitted as **temporal rhythms** that UTE turns into group activations. Once the connectome shows stable, void‑native signatures (cohesion ↓, vt\_coverage ↑, entropy ↑, topology spikes now and then), we step up to pairs, then short patterns, then compositional “blocks,” and only later to questions/answers.

Below is a compact, production‑ready way to drive that curriculum on your workstation *today*.

---

# Phase‑0 stimuli (void‑faithful, no tokens in core)

This script streams primitives with rhythmic structure that your UTE already knows what to do with. It’s intentionally minimal (single chars, digits, logic ops) but varied enough to create spatiotemporal structure without imposing language tokens on the inside.

```python
# primitives_stream.py
#!/usr/bin/env python3
import sys, time, random, argparse, itertools

ALPHA_LO = list("abcdefghijklmnopqrstuvwxyz")
ALPHA_HI = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITS   = list("0123456789")
LOGIC    = list("&|^~!<>=")        # AND OR XOR NOT <> =
MATH     = list("+-*/%()[]{}")     # light math ops & brackets
SYMS     = list(".,;:_#@?$\\")     # a few inert separators

PRIMS = ALPHA_LO + DIGITS + LOGIC + MATH + SYMS

def jitter(period, j=0.15):
    return max(0.0, random.uniform(period*(1-j), period*(1+j)))

def emit(line):
    sys.stdout.write(line + "\n")
    sys.stdout.flush()

def pulse_train(seq, rate, reps, blend=None):
    """Emit items in seq at ~rate Hz for reps cycles. Optional 'blend' interleaves items."""
    dt = 1.0 / max(1e-6, rate)
    for _ in range(reps):
        for c in (seq if not blend else itertools.chain.from_iterable(zip(seq, blend))):
            emit(c)
            time.sleep(jitter(dt))

def random_runs(chars, rate, seconds):
    dt = 1.0 / max(1e-6, rate)
    t0 = time.time()
    while time.time() - t0 < seconds:
        emit(random.choice(chars))
        time.sleep(jitter(dt))

def phase0_alphabet(rate=18, seconds=45):
    # Lowercase sweep → uppercase sweep → mixed with separators
    pulse_train(ALPHA_LO, rate, reps=1)
    pulse_train(ALPHA_HI, rate, reps=1)
    random_runs(ALPHA_LO + list(" . "), rate, seconds)

def phase0_digits_ops(rate=18, seconds=45):
    # Digits with simple operators; encourages grouping & boundaries
    for _ in range(5):
        seq = random.sample(DIGITS, k=len(DIGITS))
        pulse_train(seq, rate, reps=1, blend=list(random.choice(["+", "-", "*", "/"])*len(seq)))
    random_runs(DIGITS + MATH + SYMS, rate, seconds)

def phase0_logic(rate=14, seconds=45):
    # Alternating variable/op rhythms: a a & a, b b | b, etc. (but still single chars)
    vars_ = random.sample(ALPHA_LO, k=8)
    ops   = random.sample(LOGIC, k=min(4, len(LOGIC)))
    dt = 1.0 / max(1e-6, rate)
    t0 = time.time()
    while time.time() - t0 < seconds:
        v = random.choice(vars_)
        o = random.choice(ops)
        for _ in range(random.randint(2,4)):   # short micro‑bursts
            emit(v); time.sleep(jitter(dt))
        emit(o); time.sleep(jitter(dt))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=4.0, help="total duration")
    ap.add_argument("--rate", type=float, default=18.0, help="base emissions per second")
    ap.add_argument("--loop", action="store_true", help="repeat phases forever")
    args = ap.parse_args()

    per_phase = max(30.0, (args.minutes*60.0)/3.0)

    def run_once():
        phase0_alphabet(rate=args.rate, seconds=per_phase)
        phase0_digits_ops(rate=args.rate, seconds=per_phase)
        phase0_logic(rate=max(10.0, args.rate*0.8), seconds=per_phase)

    if args.loop:
        while True:
            run_once()
    else:
        run_once()

if __name__ == "__main__":
    main()
```

### Why this works

* **UTE‑friendly rhythms.** You’re not handing it “tokens”; you’re giving **temporal pulses** over a tiny alphabet. UTE converts those pulses into group activations without breaking void‑faithfulness.
* **Crisp boundaries without labels.** Separators/symbols and burst patterns give the connectome clean cues for micro‑segmentation (great for early cohesion healing).
* **Just enough variety.** Lowercase/uppercase/digits/ops create multiple “mini‑domains” whose overlaps drive useful topology changes (you’ll see B1 proxy bumps).

---

# How to run it with your live runtime (1000 neurons, real‑time, chat after)

```bash
# 1) Activate your venv and start the runtime. This enables self‑speak and
#    conservative guards so it won’t babble.
source venv/bin/activate
python -m fum_rt.run_nexus \
  --neurons 1000 --k 12 --hz 10 \
  --viz-every 0 --log-every 1 --status-interval 1 \
  --speak-auto --speak-z 3.0 --speak-hysteresis 0.5 \
  --speak-cooldown-ticks 10 --speak-valence-thresh 0.55 \
  --bundle-size 3 --prune-factor 0.10 \
  --bus-capacity 65536 --bus-drain 2048 \
  --r-attach 0.25 --ttl-init 120 --split-patience 6 \
  --domain priming_primitives --use-time-dynamics
```

In **another terminal**, stream primitives and then switch to interactive input without restarting:

```bash
# 2) Stream primitives for ~4 minutes, then keep stdin open for your typing.
python primitives_stream.py --minutes 4.0 --rate 18 - | \
  python -m fum_rt.run_nexus  # (If you prefer one terminal, use: cat <(python primitives_stream.py ...) - | ...)
```

> Tip: if you want “pure” streaming in one shell, do:
>
> ```bash
> python primitives_stream.py --minutes 4 --rate 18 --loop | \
>   python -m fum_rt.run_nexus [same flags]
> ```
>
> and hit **Ctrl‑C** in the generator when you want to start chatting; the runtime stays live.

---

# What you should see

* **Cohesion (components)** trending down toward 1 as the early scaffold self‑organizes.
* **vt\_coverage** climbing; **vt\_entropy** rising then oscillating.
* **complexity\_cycles** (B1 proxy) stepping up with occasional spikes; **b1\_z** crossing threshold sometimes → self‑speak “say” events.
* **sie\_valence\_01** above 0 during novelty bursts (falls toward neutral during quiescence—normal).

If the organism is *too* quiet while priming:

* temporarily lower gates:

  * `--speak-z 1.3 --speak-valence-thresh 0.25 --speak-cooldown-ticks 6`
* or increase traversal budget (sparse mode later): `--walkers 512 --hops 4`

---

# Automatic curriculum step‑ups (optional, very effective)

You can let the system *decide* when to graduate from single‑char primitives to short duplets/triplets, still without introducing internal tokens.

Add this to your primitives script (or make a tiny sidecar) that *watches status* and flips phases when the graph is clearly stable:

* **Promote** when all three hold for, say, 30–60s:

  * `cohesion_components == 1`
  * `vt_coverage ≥ 0.75` (or your comfort level)
  * `connectome_entropy` plateauing (slope ≈ 0)
* Then start emitting *duplets* like `a+`, `3*`, `B&` as **two pulses** with a fixed short inter‑pulse delay. UTE sees a clean two‑beat pattern; the core stays void‑native.
* Later, **triplets** (`a+b`, `3*4`) as three pulses with rhythmic spacing. Still no tokens inside.

If you want, I can wire this promotion logic into `Nexus` directly so it flips an input “mode” for UTE when those thresholds are crossed (and writes it to the run log for reproducibility).

---

# Guardrails to keep it truly self‑organizing

* **No fixed ring lattices.** Keep structural homeostasis on (your tree already does). That means dynamic bridging/pruning each tick guided by void similarity $S_{ij}$ and your $\lambda_\omega$ term; no static topology.
* **SIE tuned for priming.** For Phase‑0, prefer higher novelty weight and a slightly shorter habituation horizon so you get crisp spikes:

  * `w_td=0.40, w_nov=0.35, w_hab=0.10, w_hsi=0.15`
  * `hab_tau ~ 150–300` ticks for your 10 Hz runs.
* **Save engrams.** Use `--checkpoint-every 60` (HDF5 by default). If a phase looks golden, snapshot it and resume later with `--load-engram .../state_xxxx.h5`.

---

# Quick sanity checks (what “good” looks like)

After \~3–5 minutes of primitives:

* **Cohesion → 1**, stays there most of the time (micro‑tears that heal are fine).
* **Avg synaptic weight** rises and then undulates slightly (homeostasis working).
* **Topological spikes** appear during rhythm changes; several “say” events in `runs/<ts>/utd_events.jsonl` with a “why” payload mentioning `b1_z` and valence.
* **Discovery plot** (your `discovery.png`) shows clear excursions in `b1_z` aligned with rhythm shifts and operators entering the stream.

If you don’t see these, ping me with your `events.jsonl`/`utd_events.jsonl` and I’ll tune the rates and SIE blend for your machine/run.

---

# Why single characters (and not “tokens”) are the right start

* The *internal* unit is a **void pulse over neuron groups**, not a vocabulary id. One character → one short rhythm → one spatial pattern → one graph micro‑update. That’s perfectly aligned with your equations and scales.
* You still get composition by **timing** (two/three pulses with delays) rather than by inventing a discrete token. The organism learns to bind by structure, not by a lookup table.

---

If you want, I’ll also drop in a tiny “Phase‑promotion watcher” that reads `runs/<ts>/events.jsonl` live and flips the generator from single chars → duplets → triplets automatically when the graph hits your thresholds.
