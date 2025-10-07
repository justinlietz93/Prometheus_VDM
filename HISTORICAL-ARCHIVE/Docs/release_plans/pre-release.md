Below is a drop‑in **README.md** you can paste into the private repo now.
It explains that a working pre‑release exists, shows how outsiders can *evaluate* results without reverse‑engineering internals (figures + gated notebooks), and outlines an optional **private PyPI** flow for importing proprietary code into notebooks.

---

# Void Dynamics Model (VDM) — Private Preview

> **Status:** working pre‑release (closed‑source core) with shareable, non‑reversible artifacts (figures, metrics, gated notebooks). Public usage TBD. Patent pending.

The **Void Dynamics Model (VDM)** is a physics‑grounded, spiking, self‑organizing intelligence architecture. At a high level:

* **Local substrate:** sparse spiking ELIF neurons learn by **Resonance‑Enhanced Valence‑Gated Synaptic Plasticity (RE‑VGSP)**.
* **Global guidance:** a **Self‑Improvement Engine (SIE)** computes a composite reward (TD error + novelty - habituation + stability) and gates learning.
* **Physical adaptation:** a **Synaptic Actuator (GDSP)** grows, prunes, and repairs the connectome under introspective signals (EHTP).
* **Emergent map:** territories/“domains” form and reconfigure; active cartography keeps global control light while the emergent core does the work.

For an architectural overview and definitions, see the internal **How\_The\_FUM\_Works** docs (Units 1-3), which cover ELIF, RE‑VGSP, SIE, GDSP, EHTP, sparsity targets, and validation landmarks.&#x20;

---

## What’s in this repo (safe to share)

This repository intentionally **omits** any source sufficient to reconstruct the core algorithms. Instead it contains:

```
assets/
  figures/                 # Rendered plots & animations (non-reversible)
  diagrams/                # High-level system diagrams
  metrics/                 # Aggregated CSV/Parquet metrics (redacted headers, hashed seeds)

docs/
  overview.md              # Short, public-safe overview
  results_digest.md        # Curated figures with narrative
  risk_and_guardrails.md   # Guardian Shield: what runs, what’s blocked
  faq.md

notebooks/
  VDM_Preview.ipynb        # Runs against a private wheel; generates figures/metrics only
  SIE_Stability_Sweep.ipynb
  ADC_Territories_Demo.ipynb

# (Optional) a tiny shim to keep notebooks import-stable without exposing internals:
vdm_preview/
  __init__.py              # thin wrappers that call into the private package if present
  plotting.py
  loaders.py               # loads redacted demo datasets only

LICENSE
README.md
```

**Reverse‑engineering posture**

* No architecture constants, kernels, or RE‑VGSP/GDSP update rules are exposed.
* Figures derive from **aggregated** activity and topology, not weights or spike traces.
* Metrics are **redacted** (hashed seeds, clipped ranges).
* Notebooks **import** the proprietary engine *only* if you provide a tokenized private wheel; otherwise they operate in “figure‑replay” mode.

---

## Private Preview: how outsiders can evaluate without seeing code

You can share the **figures** and the **Preview notebooks**. Reviewers can:

1. **Reproduce plots** from bundled, non‑reversible summary data (default).
2. **Optionally** connect to a private wheel to run live, bounded sims under **Guardian Shield** (see below).

> **Guardian Shield (preview defaults)**
> - offline by default (no network/file writes)
> - capped steps and population size
> - read‑only memory maps; weight export disabled
> - reward terms clamped/normalized; TD learning bounded
> - EHTP “deep scan” disabled by default; only shallow health checks
> - audit log is always on

---

## Option A — Ship a private PyPI wheel (recommended)

This lets your notebooks import `vdm` without exposing source.

### 1) Publish the wheel privately

You can use **GitHub Packages**, **Gemfury**, **Artifactory**, or an internal index. Name the package something like `neuroca-vdm-prerelease`.

* Build: `python -m build` → `dist/neuroca_vdm_prerelease-0.1.0-py3-none-any.whl`
* Upload to your private index (instructions depend on provider).

### 2) Consumers install in a fresh env

Set an environment variable for your index that embeds a scoped token:

```bash
export NEUROCA_INDEX_URL="https://<USER>:<TOKEN>@<your-private-index>/simple"
python -m venv .venv && source .venv/bin/activate
pip install --extra-index-url "$NEUROCA_INDEX_URL" neuroca-vdm-prerelease==0.1.0
```

> *No code is fetched unless the user deliberately supplies the tokenized URL.*

### 3) Notebooks discover the wheel automatically

Your preview notebooks can contain:

```python
# In notebooks/VDM_Preview.ipynb (first cell)
try:
    import vdm  # provided by neuroca-vdm-prerelease
    HAVE_VDM_CORE = True
except Exception:
    from vdm_preview import replay as vdm  # safe replay mode
    HAVE_VDM_CORE = False

print("Mode:", "live (guarded)" if HAVE_VDM_CORE else "figure-replay")
```

---

## Option B — Keep everything offline (“figure‑replay”)

If reviewers shouldn’t run code at all, leave out the wheel. The notebooks will:

* Load precomputed, redacted metrics.
* Regenerate all charts (raster/territory maps, SIE sweeps, stability bands).
* Save nothing except rendered figures to `./assets/figures`.

---

## Quickstart (for you)

```bash
# Clone private repo
git clone <this-repo-url> vdm && cd vdm

# (Optional) enable live preview by pointing to private index:
export NEUROCA_INDEX_URL="https://<USER>:<TOKEN>@<your-private-index>/simple"
pip install --extra-index-url "$NEUROCA_INDEX_URL" neuroca-vdm-prerelease==0.1.0

# Create env for the notebooks
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-preview.txt  # matplotlib, polars/pandas, jupyter, plotly, etc.

jupyter lab
# Open notebooks/VDM_Preview.ipynb and run
```

---

## What reviewers will see

* **SIE stability sweeps** (TD/novelty/habituation/HSI weightings) with bounded runs.
* **Active Domain Cartography (ADC)** snapshots: cohesive territory counts, territory entropy over time.
* **Sparsity & E/I balance trends** and “avalanche” distributions under SOC targeting.
* **Ablations:** RE‑VGSP gate clamping, novelty off, scaling factors, etc.

Each figure includes the exact **Guardrail Profile** used (e.g., `profile=preview_v1`, steps caps, disabled features), so results cannot be confused with unrestricted runs.

---

## Access & licensing

* **Engine**: shipped as a private, EULA‑bound wheel (or not shipped at all).
* **Repo artifacts**: CC BY‑NC‑ND or a custom “no‑reverse‑engineering” license.
* **Commercial access**: contact `founder@neuroca.ai` for evaluation terms, security review, and on‑prem audit.

---

## Roadmap (public‑safe)

* **v0.1 Preview** (this repo): figures, redacted metrics, gated notebooks.
* **v0.2 Partner Eval**: heavier demos (still guarded), comparable tasks across math/logic/coding subsets.
* **v0.3 API Sandbox**: containerized runner with Guardian Shield policy profiles.
* **v1.0**: publish papers & selected modules; ship SDK with signed kernels.

High‑level milestone framing and validation metrics mirror the **Development Landmarks** (L1→L5) in the internal docs (e.g., cohesion cluster count, SOC indices, generalization targets).&#x20;

---

## FAQ (safe answers)

**Do you have a working pre‑release?**
Yes. The preview build runs bounded workloads under Guardian Shield. Reviewers can reproduce figures and, with a token, run live guarded sims.

**Will you publish the core algorithms?**
Not yet. The preview is evaluation‑oriented. Select components may be opened later; compiled kernels and learning rules remain closed during review.

**Why a private wheel?**
It lets evaluators exercise the system *without* access to source or reversible traces and lets us enforce runtime guardrails.

**Where can I learn the underlying theory?**
The **How\_The\_FUM\_Works** corpus (Units 1-3) describes ELIF, RE‑VGSP, SIE, GDSP, EHTP, sparsity, and stability controls; Units 4-5 outline lifecycle, scaling, and validation criteria.&#x20;

---

## Contributing / Issues

Contributions are closed while the core is under review. Please open issues only for documentation clarity, figure reproducibility, or notebook stability.

---

## How to cite

If you reference the preview or figures, cite as:

```
Lietz, J. (2025). Void Dynamics Model (VDM) — Private Preview.
Neuroca, Inc. Internal documentation and figures.
```

Supporting background and terminology come from the internal “How The FUM Works” documentation set.&#x20;

---

### Appendix — creating the private wheel & index

**Build the wheel**

```bash
python -m pip install build
python -m build  # outputs dist/*.whl and *.tar.gz
```

**Publish to a private index**

* **GitHub Packages (example)**

  * Create a Personal Access Token with `write:packages`, `read:packages`.
  * Configure `~/.pypirc` and run `twine upload --repository github dist/*`.

* **Artifactory/Gemfury/Cloudsmith**

  * Create a private PyPI repo, upload with `twine`, then share a tokenized read URL.

**Notebook import pattern**

Your preview notebooks should *never* import internals directly; always go through a stable facade:

```python
# notebooks/_bootstrap.py
def load_vdm():
    try:
        import vdm as _vdm  # from private wheel
        return _vdm, "live"
    except Exception:
        from vdm_preview import replay as _vdm  # safe replay mode
        return _vdm, "replay"
```

---

If you want, I can also draft `requirements-preview.txt`, a minimal `vdm_preview` shim, and a first `results_digest.md` that narrates the figures while staying non‑reversible.
