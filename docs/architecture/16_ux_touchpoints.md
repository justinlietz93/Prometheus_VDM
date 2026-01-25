# UX Touchpoints - Product Surface Analysis

**Repository**: Prometheus_VDM  
**Commit**: ae49a391acf2183242e4d96bda49e066beec7680

---

## USER PERSONAS

### 1. **Researcher/Physicist**
- **Goal**: Run VDM simulations, validate theoretical models, publish results
- **Technical Level**: High (Python, physics, math)
- **Primary Interface**: CLI (run_nexus.py) + Jupyter notebooks
- **Pain Points**: Manual setup, no reproducibility guide, derivation validation

### 2. **Developer/Engineer**
- **Goal**: Extend VDM runtime, add physics modules, debug, contribute
- **Technical Level**: High (Python, git, testing)
- **Primary Interface**: IDE, CLI, git
- **Pain Points**: Missing API docs, low test coverage, no local dev guide

### 3. **Operator/SRE**
- **Goal**: Deploy VDM on HPC/cloud, monitor health, manage resources
- **Technical Level**: Medium (ops, containers, monitoring)
- **Primary Interface**: CLI, dashboard, logs
- **Pain Points**: No containerization, no health checks, manual deployment

### 4. **External User (Hypothetical)**
- **Goal**: Use VDM as library/service for own research
- **Technical Level**: Medium (Python, APIs)
- **Primary Interface**: Python API, HTTP API (future)
- **Pain Points**: No pip package, no public API, no SaaS offering

---

## TOUCHPOINT INVENTORY

### 1. Command-Line Interface (CLI)

#### **Entry Point**: `python vdm_rt/run_nexus.py`

**User Journey**:
```bash
# 1. User reads README or --help
python vdm_rt/run_nexus.py --help

# 2. User runs with defaults
python vdm_rt/run_nexus.py --neurons 1000 --hz 10 --duration 60

# 3. User loads profile
python vdm_rt/run_nexus.py --profile run_profiles/05_10k_fuvdm.json

# 4. User resumes from checkpoint
python vdm_rt/run_nexus.py --load-engram runs/20250125_103045/state_1200.h5
```

**Flags (~50 available)**:
- Core: `--neurons`, `--k`, `--hz`, `--domain`, `--seed`
- I/O: `--run-dir`, `--checkpoint-every`, `--viz-every`, `--log-every`
- Physics: `--sparse-mode`, `--threshold`, `--lambda-omega`
- Speak: `--speak-auto`, `--speak-z`, `--speak-cooldown-ticks`
- Advanced: `--b1-half-life-ticks`, `--bundle-size`, `--prune-factor`

**UX Issues**:
- ⚠️ **Flag overload**: 50+ flags → overwhelming
- ⚠️ **No validation**: Invalid values crash at runtime (no argparse checks)
- ⚠️ **No examples**: README lacks common use cases
- ❌ **No shell completion**: No bash/zsh autocomplete

**Improvement Recommendations**:
1. Group flags in `--help` output (Core, I/O, Physics, Advanced)
2. Add default profile: `--profile default` → sensible defaults
3. Generate shell completions (argcomplete)
4. Add CLI examples to README

**CLI UX Score**: **2.5/5** (Functional but overwhelming)

---

### 2. Web Dashboard (vdm_live.py)

#### **Entry Point**: `python vdm_live.py --runs-root runs/`

**User Journey**:
```bash
# 1. Launch dashboard
python vdm_live.py --runs-root runs/

# 2. Open browser → http://127.0.0.1:8060

# 3. Select run from dropdown

# 4. Monitor charts (metrics, events, macros)

# 5. Browse files (workspace tab)

# 6. (Optional) Start/stop subprocess
```

**Features**:
- **Charts**: Real-time Plotly charts (ZEMA, clustering, events)
- **Feed**: Scrolling event log (macros, thoughts)
- **Workspace**: File browser for run artifacts
- **Runtime Controls**: Start/stop Nexus subprocess
- **Config**: View run configuration
- **Performance**: CPU/memory tracking (limited)
- **Chat**: (Placeholder for future user interaction)
- **Engram**: Checkpoint management

**UX Strengths**:
- ✅ Real-time updates (1s polling)
- ✅ Clean layout (responsive design)
- ✅ File browser (navigate runs easily)

**UX Issues**:
- ⚠️ **Read-only**: Cannot modify running simulation
- ⚠️ **No search**: Cannot search events by keyword
- ⚠️ **No filtering**: Cannot filter events by type
- ⚠️ **No alerts**: No notifications for anomalies
- ⚠️ **No export**: Cannot export charts as PNG/CSV
- ❌ **No dark mode**: Single theme only

**Improvement Recommendations**:
1. Add event search/filter (text search + type filter)
2. Add alert thresholds (e.g., notify if ZEMA > 5.0)
3. Add chart export (PNG, CSV)
4. Add dark mode toggle
5. Add pause/resume controls (if subprocess running)

**Dashboard UX Score**: **3.5/5** (Good monitoring; lacks interactivity)

---

### 3. Configuration Files (run_profiles/*.json)

#### **Example**: `run_profiles/05_10k_fuvdm.json`

**User Journey**:
```bash
# 1. Copy existing profile
cp run_profiles/05_10k_fuvdm.json run_profiles/my_experiment.json

# 2. Edit JSON (manually)
vim run_profiles/my_experiment.json

# 3. Run with profile
python vdm_rt/run_nexus.py --profile run_profiles/my_experiment.json
```

**Profile Structure**:
```json
{
  "N": 10000,
  "k": 12,
  "hz": 10,
  "domain": "biology_consciousness",
  "seed": 42,
  "checkpoint_every": 100,
  "viz_every": 10
}
```

**UX Issues**:
- ❌ **No schema**: No JSON Schema for validation
- ❌ **No editor support**: No VSCode schema hints
- ⚠️ **Manual editing**: No GUI editor
- ⚠️ **No versioning**: No `config_version` field
- ⚠️ **No comments**: JSON doesn't support comments (use YAML?)

**Improvement Recommendations**:
1. Add JSON Schema file (`run_profile.schema.json`)
2. Generate VSCode schema hints (`.vscode/settings.json`)
3. Add profile editor in dashboard (future)
4. Migrate to YAML or TOML (support comments)
5. Add `config_version: "1.0.0"` field

**Config UX Score**: **2/5** (Functional but brittle)

---

### 4. Jupyter Notebooks (Derivation/)

#### **Example**: `Derivation/experiments/pta.ipynb`

**User Journey**:
```bash
# 1. Open Jupyter
jupyter notebook Derivation/experiments/pta.ipynb

# 2. Run cells (equations, plots, validation)

# 3. Export results (PNG, LaTeX)
```

**UX Strengths**:
- ✅ Interactive exploration
- ✅ Reproducible (cells + outputs)
- ✅ Rich visualizations (matplotlib, plotly)

**UX Issues**:
- ⚠️ **No Binder link**: Cannot run in cloud (no mybinder.org)
- ⚠️ **No requirements.txt**: Notebook-specific deps unclear
- ⚠️ **No JupyterLab**: Uses classic Jupyter (old UI)

**Improvement Recommendations**:
1. Add Binder badge to README
2. Add `Derivation/requirements-notebooks.txt`
3. Migrate to JupyterLab (modern UI)

**Notebook UX Score**: **3/5** (Good for research; lacks cloud support)

---

### 5. Logs & Telemetry (events.jsonl, macros.jsonl)

#### **Example**: `runs/20250125_103045/events.jsonl`

**User Journey**:
```bash
# 1. Tail logs (real-time)
tail -f runs/20250125_103045/events.jsonl

# 2. Query with jq
cat runs/20250125_103045/events.jsonl | jq 'select(.event_type == "VTTouch")'

# 3. Analyze with pandas
python -c "import pandas as pd; df = pd.read_json('runs/20250125_103045/events.jsonl', lines=True); print(df.describe())"
```

**UX Strengths**:
- ✅ Machine-readable (JSONL)
- ✅ Tail-friendly (newline-delimited)
- ✅ Structured fields (tick, event_type, payload)

**UX Issues**:
- ⚠️ **No log viewer**: Must use command-line tools
- ⚠️ **No log search UI**: Dashboard shows feed but no search
- ❌ **No correlation**: Missing run_id (cannot correlate multi-run)

**Improvement Recommendations**:
1. Add log viewer tab in dashboard (with search/filter)
2. Add correlation ID (run_id) to all events
3. Integrate with Loki or ELK (future)

**Logs UX Score**: **3/5** (Good structure; lacks UI tooling)

---

### 6. Checkpoints (state_N.h5, state_N.npz)

#### **Example**: `runs/20250125_103045/state_1200.h5`

**User Journey**:
```bash
# 1. Resume from checkpoint
python vdm_rt/run_nexus.py --load-engram runs/20250125_103045/state_1200.h5

# 2. Inspect checkpoint (Python)
python -c "
import h5py
with h5py.File('runs/20250125_103045/state_1200.h5', 'r') as f:
    print('Step:', f.attrs['step'])
    print('N:', f.attrs['N'])
    print('Domain:', f.attrs['domain'])
"

# 3. Export checkpoint metadata
python tools/checkpoint_inspector.py runs/20250125_103045/state_1200.h5
```

**UX Issues**:
- ❌ **No inspector tool**: Must write custom Python
- ❌ **No metadata viewer**: Dashboard shows files but no metadata
- ⚠️ **No provenance**: Missing content hash (SHA256)

**Improvement Recommendations**:
1. Add `tools/checkpoint_inspector.py` CLI tool
2. Add metadata viewer in dashboard (Engram tab)
3. Add SHA256 hash to checkpoint metadata

**Checkpoint UX Score**: **2/5** (Works but opaque)

---

### 7. Python API (for developers)

#### **Example**: Programmatic usage

**Current State**: No public API (must import vdm_rt.nexus)

**Hypothetical User Journey**:
```python
from vdm_rt import VDM

# 1. Create VDM instance
vdm = VDM(N=1000, k=12, hz=10, seed=42)

# 2. Run for 60 seconds
vdm.run(duration_s=60)

# 3. Get final state
state = vdm.get_state()
print(state.metrics)

# 4. Export checkpoint
vdm.save_checkpoint('my_checkpoint.h5')
```

**Current Issues**:
- ❌ **No public API**: Must use Nexus class directly (internal API)
- ❌ **No pip package**: Cannot `pip install prometheus-vdm`
- ❌ **No API docs**: No Sphinx/MkDocs documentation

**Improvement Recommendations**:
1. Design public API (`vdm_rt.api.VDM` wrapper)
2. Publish to PyPI (`pip install prometheus-vdm`)
3. Generate API docs (Sphinx + autodoc)
4. Add examples/notebooks for API usage

**API UX Score**: **0/5** (Not implemented)

---

### 8. HTTP API (future)

**Not Implemented**. Recommended for SaaS/service mode:

**Hypothetical Endpoints**:
```
POST /api/v1/runs
  → Create and start run
  → Returns: {"run_id": "...", "status": "running"}

GET /api/v1/runs/{run_id}/status
  → Get current status
  → Returns: {"tick": 1234, "zema": 2.3, ...}

GET /api/v1/runs/{run_id}/events
  → Stream events (Server-Sent Events or WebSocket)

POST /api/v1/runs/{run_id}/stop
  → Gracefully stop run
```

**Future UX Score**: **N/A** (Not implemented)

---

## UX MATURITY MATRIX

| Touchpoint | Discoverability | Usability | Reliability | Documentation | Score |
|------------|-----------------|-----------|-------------|---------------|-------|
| **CLI** | 3/5 | 2/5 | 4/5 | 2/5 | **2.75/5** |
| **Dashboard** | 4/5 | 4/5 | 3/5 | 2/5 | **3.25/5** |
| **Configs** | 3/5 | 2/5 | 3/5 | 1/5 | **2.25/5** |
| **Notebooks** | 3/5 | 4/5 | 3/5 | 2/5 | **3/5** |
| **Logs** | 3/5 | 3/5 | 4/5 | 2/5 | **3/5** |
| **Checkpoints** | 2/5 | 2/5 | 4/5 | 1/5 | **2.25/5** |
| **Python API** | 0/5 | 0/5 | N/A | 0/5 | **0/5** |
| **HTTP API** | N/A | N/A | N/A | N/A | **N/A** |

**Overall UX Score**: **2.5/5** (Functional but requires polishing)

---

## FRICTION POINTS

### 1. **Onboarding** (High Friction)
- No quickstart guide in README
- No "one-liner" install + run
- Must manually install dependencies (unpinned)

**Improvement**:
```bash
# Ideal onboarding
pip install prometheus-vdm
vdm run --profile quickstart  # Pre-configured 10-second demo
vdm dashboard  # Auto-launches browser
```

### 2. **Configuration** (High Friction)
- 50+ CLI flags → overwhelming
- No schema validation → runtime errors
- JSON manual editing → brittle

**Improvement**: Add interactive config wizard
```bash
vdm config wizard  # Guided prompts
```

### 3. **Debugging** (Medium Friction)
- Logs are JSONL → requires jq/pandas
- No correlation IDs → hard to trace
- No log viewer UI

**Improvement**: Add log viewer in dashboard with search/filter

### 4. **Experimentation** (Medium Friction)
- Must manually edit profiles → slow iteration
- No parameter sweep tool → manual loops
- No A/B comparison → manual diffing

**Improvement**: Add parameter sweep CLI
```bash
vdm sweep --param N --values 100,1000,10000 --profile base.json
```

---

## PRODUCT SURFACE RECOMMENDATIONS

### Short-Term (1-2 Months)
1. **Add quickstart guide** to README (5 min onboarding)
2. **Improve CLI help** (group flags, add examples)
3. **Add event search** in dashboard
4. **Add checkpoint inspector** CLI tool
5. **Generate shell completions** (bash, zsh)

### Medium-Term (3-6 Months)
6. **Publish pip package** (`pip install prometheus-vdm`)
7. **Design public API** (VDM wrapper class)
8. **Add config wizard** (interactive prompts)
9. **Add parameter sweep** tool
10. **Generate API docs** (Sphinx)

### Long-Term (6-12 Months)
11. **Build HTTP API** (REST + WebSocket)
12. **SaaS offering** (cloud-hosted VDM)
13. **JupyterHub integration** (Binder + cloud notebooks)
14. **VS Code extension** (run profiles editor, dashboard embed)

---

## CONCLUSION

**UX Maturity**: **Early Stage (2.5/5)**

**Strengths**:
- Dashboard provides good real-time monitoring
- JSONL logs are machine-readable
- Jupyter notebooks support interactive exploration

**Weaknesses**:
- CLI is overwhelming (50+ flags, no grouping)
- No public API or pip package
- High onboarding friction (no quickstart)
- Config management is brittle (manual JSON editing)

**Priority 1**: Reduce onboarding friction (quickstart, pip package, examples)  
**Priority 2**: Improve CLI UX (grouping, wizard, completions)  
**Priority 3**: Build public API (Python + HTTP)
