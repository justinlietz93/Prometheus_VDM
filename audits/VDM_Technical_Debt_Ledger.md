# VDM Technical-Debt Ledger (Read-Only)

## 1) Repo Map & Conventions

**Module tree (≤3 levels)**
- `fum_rt/` - real-time runtime scaffold (loop, telemetry, orchestration) with CLI entrypoint and helper seams.【F:README.md†L62-L101】
  - `runtime/` - tick loop, telemetry packagers, retention/state helpers.【F:README.md†L66-L99】
  - `core/` - connectome, metrics, visualizer, memory, signals, void adapters.【F:README.md†L74-L99】
- `derivation/` - theoretical papers, acceptance plans, and physics prototypes informing runtime.【F:derivation/README_PUBLIC.md†L1-L46】
- `tools/` - repo-specific hygiene and analytics scripts such as `md_hygiene_check.py` (Markdown gate) and the standalone dependency analyzer toolchain.【F:tools/md_hygiene_check.py†L1-L120】【F:tools/dependency_analyzer/README.md†L1-L23】

**Language & framework mix**
- Python dominates (runtime, tools, derivations) with Dash/Plotly front-end launched via `fum_live.py`.【F:README.md†L8-L26】【F:fum_live.py†L6-L26】
- Requirements emphasize NumPy, NetworkX, Matplotlib, Torch, SciPy/TDA stacks, Redis, and Dash for telemetry/visualization.【F:requirements.txt†L1-L25】

**Build/CI & conventions**
- No dedicated CI scripts; repo relies on custom tools like `tools/md_hygiene_check.py` and `tools/dependency_analyzer` for linting/coverage gating.【F:tools/md_hygiene_check.py†L1-L120】【F:tools/dependency_analyzer/README.md†L1-L23】
- Code style unstated; no formatter configs discovered (no `pyproject.toml`/`setup.cfg`). Manual guardrails documented via tests under `fum_rt/tests`.【F:fum_rt/tests/core/test_runner_budget.py†L1-L40】

## 2) Duplicate & Near-Duplicate Code

Command used:
```bash
python - <<'PY'
import os, hashlib
root='.'
files=[]
for dirpath, _, filenames in os.walk(root):
    if '.git' in dirpath.split(os.sep):
        continue
    for fn in filenames:
        if fn.endswith('.py'):
            path=os.path.join(dirpath, fn)
            with open(path,'r',encoding='utf-8',errors='ignore') as f:
                data=f.read()
            tokens=''.join(data.split())
            files.append((hashlib.md5(tokens.encode()).hexdigest(), path))
from collections import defaultdict
clusters=defaultdict(list)
for h,path in files:
    clusters[h].append(path)
for h,paths in clusters.items():
    if len(paths)>1:
        print(h)
        for p in paths:
            print(' ',p)
        print()
PY
```
【11dd49†L1-L33】

| cluster_id | files | similarity% | notes |
| --- | --- | --- | --- |
| md5:4dc162a5 | `derivation/code/FUM_Void_Equations.py`; `derivation/code/computational_toy_proofs/FUM_Void_Equations.py`; `fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Equations.py` | 100 | Identical void dynamics (Δα/Δω) implementations repeated across derivation/runtime.【F:derivation/code/FUM_Void_Equations.py†L35-L112】【F:fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Equations.py†L35-L112】 |
| md5:e6ad008d | `derivation/code/FUM_Void_Debt_Modulation.py`; `derivation/code/computational_toy_proofs/FUM_Void_Debt_Modulation.py`; `fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Debt_Modulation.py` | 100 | Domain modulation tables duplicated verbatim.【F:fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Debt_Modulation.py†L1-L133】 |
| md5:6e6bce7b | `derivation/code/physics/memory_steering/memory_steering.py`; `fum_rt/physics/memory_steering/memory_steering.py` | 100 | Memory steering PDE + sampling API copied directly, drifting only in package path.【F:fum_rt/physics/memory_steering/memory_steering.py†L8-L198】 |
| md5:e66aadae | `fum_rt/io/sensors/{somatosensory,vision,auditory,symbols}.py`; `fum_rt/io/actuators/{visualize,vocalizer,symbols}.py` | 100 | All eight files contain only boilerplate license docstrings (no code), indicating unused scaffolding duplication.【F:fum_rt/io/sensors/vision.py†L1-L7】 |
| md5:d41d8cd9 | Multiple `__init__.py` stubs (empty files) across API/io packages | 100 | Empty placeholders offer no functionality; consolidation possible.【F:fum_rt/io/__init__.py†L1-L1】 |

Drift example: `derivation/.../void_functions.py` mirrors Δα/Δω logic but with altered docstrings while maintaining identical computations, risking divergence if constants change.【F:derivation/code/computational_toy_proofs/void_functions.py†L10-L79】

## 3) Redundant Implementations (same capability, different modules)

| capability | candidates (file:line) | preferred? | rationale |
| --- | --- | --- | --- |
| Void dynamics equations | `fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Equations.py:35-119`; `derivation/code/FUM_Void_Equations.py:35-119` | Yes → keep runtime copy | Centralize runtime to one authoritative module; derivation copies should import to avoid divergence.【F:fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Equations.py†L35-L119】 |
| Domain modulation factors | `fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Debt_Modulation.py:12-133`; `derivation/code/FUM_Void_Debt_Modulation.py:12-133` | Yes → keep runtime copy | Triple maintenance burdens updates; prefer runtime export for both theoretical and production consumers.【F:fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Debt_Modulation.py†L12-L133】 |
| Memory steering PDE utilities | `fum_rt/physics/memory_steering/memory_steering.py:73-198`; `derivation/code/physics/memory_steering/memory_steering.py:73-198` | Prefer runtime (`fum_rt`) | Identical APIs; consolidating avoids drift and simplifies test targeting.【F:fum_rt/physics/memory_steering/memory_steering.py†L73-L198】 |
| Graph coarse-graining | `fum_rt/fum_advanced_math/graph/coarse_grain_graph.py:12-48` vs runtime connectome heuristics | Prefer integrate into `core` or drop | Standalone coarse-grain helper not referenced; overlaps structural homeostasis logic.【F:fum_rt/fum_advanced_math/graph/coarse_grain_graph.py†L12-L47】 |

## 4) Dead/Unused Code Paths

| symbol | file:line | last-modified | refcount evidence | severity | effort |
| --- | --- | --- | --- | --- | --- |
| `fum_rt.io.sensors.*` stubs | `fum_rt/io/sensors/vision.py:1-7` (similar for others) | Unknown | No references found via `rg "io\.sensors\.vision" -n` (empty).【F:fum_rt/io/sensors/vision.py†L1-L7】【bf3bfb†L1-L1】 | Low | S |
| `fum_rt.io.actuators.*` stubs | `fum_rt/io/actuators/visualize.py:1-7` | Unknown | No imports or calls detected (`rg "io\.actuators"` shows none).【F:fum_rt/io/actuators/visualize.py†L1-L7】【8a5664†L1-L1】 | Low | S |
| `fum_rt/io/__init__.py` | `fum_rt/io/__init__.py:1` | Unknown | Empty file; packages already discovered via namespace packages. | Low | S |

## 5) Single-Writer Violations & Hidden Side-Effects

| file:line | op | kind | via_GDSP? | severity | effort |
| --- | --- | --- | --- | --- | --- |
| `fum_rt/fum_advanced_math/structural_plasticity/apply_structural_plasticity.py:37-52` | `graph.remove_edge/add_edge` | Topology mutations on arbitrary `nx.Graph` | N | Med | M | External structural plasticity rewires graphs using global RNG without runtime budgeting, bypassing GDSP gating.【F:fum_rt/fum_advanced_math/structural_plasticity/apply_structural_plasticity.py†L37-L52】 |
| `fum_rt/core/connectome.py:299-327` | `A_new` dense rebuild + assignment | Topology/weights reset each tick | N (internal loop) | High | L | Dense `np.zeros` rebuilds adjacency outside GDSP budget; no guard for large N sparse expectations.【F:fum_rt/core/connectome.py†L295-L327】 |
| `fum_rt/runtime/loop/main.py:347-355` | `setattr(C, "bus", b)` | State mutation of connectome/bus linkage | N | Low | S | Hidden side effect attaches bus every loop without logging; failure swallowed.【F:fum_rt/runtime/loop/main.py†L347-L355】 |

## 6) Dense-Scan & Hot-Path Anti-Patterns

| file:line | pattern | path | severity | effort |
| --- | --- | --- | --- | --- |
| `fum_rt/core/connectome.py:299-327` | `np.zeros((N,N))` + dense top-k search | Tick loop | High | L | O(N²) allocation per step contradicts sparse policy for large N.【F:fum_rt/core/connectome.py†L295-L327】 |
| `fum_rt/core/connectome.py:398-402` | `nx.from_numpy_array` on dense mask | Viz path (per viz tick) | Med | M | Materializes full adjacency mask, heavy for >10k nodes.【F:fum_rt/core/connectome.py†L398-L402】 |
| `fum_rt/frontend/plugins/fum_visualizer_v1/fum_visualizer.py:150-198` | `W.toarray()` / `.cpu().numpy()` | Frontend tick viz | Med | M | Forces dense conversions and Python loops each frame; unsuitable for large runtime graphs.【F:fum_rt/frontend/plugins/fum_visualizer_v1/fum_visualizer.py†L150-L198】 |

## 7) RNG & Reproducibility Drift

| file:line | issue | impact | suggested single source | severity | effort |
| --- | --- | --- | --- | --- | --- |
| `fum_rt/core/void_dynamics_adapter.py:23-43` | Fallback Δα/Δω use `np.random.uniform` (global RNG) | Breaks reproducibility even with CLI `--seed` | Expose seeded RNG (pass from connectome) | Med | M【F:fum_rt/core/void_dynamics_adapter.py†L23-L43】 |
| `fum_rt/io/cognition/composer.py:43-84` | Reseeds emergent text generator with `seed=int(step)` each call | Deterministic repeating outputs, no global RNG linkage | Use shared RNG seeded at run start | Low | S【F:fum_rt/io/cognition/composer.py†L43-L84】 |
| `fum_rt/fum_advanced_math/structural_plasticity/apply_structural_plasticity.py:37-47` | Uses `np.random.rand/choice` without seed plumbing | Structural rewiring nondeterministic | Accept RNG from caller or runtime seed | Med | M【F:fum_rt/fum_advanced_math/structural_plasticity/apply_structural_plasticity.py†L37-L47】 |

## 8) Config & Flag Sprawl

| flag/param | sources | conflict? | notes | severity | effort |
| --- | --- | --- | --- | --- | --- |
| `ENABLE_GDSP` | `fum_rt/runtime/loop/main.py:163-280`; planning docs【2d7fd3†L15-L31】 | Yes | Env gate toggles actuator while CLI lacks parallel flag; silent failure when enabled due to swallowed exceptions.【F:fum_rt/runtime/loop/main.py†L163-L280】 | High | M |
| `ENABLE_COLD_SCOUTS` vs `ENABLE_SCOUT_*` | `fum_rt/runtime/loop/main.py:295-602` | Yes | Overlapping env gates for scouts; defaults conflict (`ENABLE_COLD_SCOUTS` + per-scout toggles).【F:fum_rt/runtime/loop/main.py†L295-L602】 | Med | M |
| `use_time_dynamics` | CLI flag (`fum_rt/cli/args.py:25-27`), frontend profiles (`fum_rt/frontend/utilities/profiles.py:48-117`), runtime stepper default (`fum_rt/runtime/stepper.py:89`) | Potential drift | Multiple layers maintain defaults; absence of central config may desync CLI vs UI defaults. | Low | M |
| Redis outputs | `fum_rt/runtime/helpers/redis_out.py:64-137` | Partial | Requires ENABLE_REDIS_* env but no CLI/doc mapping; missing failure logs. | Low | S |

## 9) Logging & Telemetry Gaps

| signal | present? | where | how to enable | missing_consumer? | severity |
| --- | --- | --- | --- | --- | --- |
| GDSP actuator success/fail | N | `_run_gdsp` silently returns on exception.【F:fum_rt/runtime/loop/main.py†L269-L280】 | `ENABLE_GDSP=1` | No log means operators can’t detect failures. | High |
| Dense fallback usage | N | `connectome` raises at import but no runtime counter/log for dense rebuild fallback.【F:fum_rt/core/connectome.py†L11-L15】 | `FORCE_DENSE=1` (env) | Lack of telemetry when dense forced. | Med |
| Event metrics gating | Y | `runtime/loop/main.py` attaches `_evt_metrics` when enabled.【F:fum_rt/runtime/loop/main.py†L316-L334】 | `ENABLE_EVENT_METRICS` | No downstream consumer verification. | Low |
| Viz errors | Partial | `helpers/viz.py` logs info if logger exists.【F:fum_rt/runtime/helpers/viz.py†L18-L31】 | `viz_every` | Lacks counter for skipped renders. | Low |

## 10) Tests & Safety Nets

| area | tests present? | files | coverage notes | severity |
| --- | --- | --- | --- | --- |
| GDSP actuator | N | — | `rg "GDSP" fum_rt/tests` returned none.【2b40c3†L1-L2】 Critical logic untested. | High |
| Gate hysteresis (speak/B1) | N | — | `rg "hysteresis" fum_rt/tests` empty.【a89eb5†L1-L2】 | Med |
| Locality guard / adjacency budget | N | — | `rg "locality" fum_rt/tests` empty.【4c88a4†L1-L2】 | Med |
| ADC updates & announcements | N | — | `rg "ADC" fum_rt/tests` empty.【335d4f†L1-L2】 | Med |
| Void walker runner budget | Y | `fum_rt/tests/core/test_runner_budget.py` enforces one-shot & time budget.【F:fum_rt/tests/core/test_runner_budget.py†L6-L106】 | - | Low |

## 11) Viz & Tooling Debt

| file:line | anti-pattern | suggested move | severity | effort |
| --- | --- | --- | --- | --- |
| `fum_rt/core/visualizer.py:73-88` | `nx.spring_layout` every snapshot (O(N³) worst-case) | Cache layout offline; precompute positions per run. | Med | M |
| `fum_rt/runtime/helpers/viz.py:18-31` | Synchronous plotting inside tick with `history` slicing | Move to async/offline worker to avoid tick stalls. | Med | M |
| `fum_rt/frontend/plugins/fum_visualizer_v1/fum_visualizer.py:150-198` | Dense conversions + Matplotlib drawing per frame | Provide downsampled tiles or WebGL/tiled backend. | High | L |

## 12) Security/Robustness Odds & Ends

| file:line | issue | severity | quick hardening note |
| --- | --- | --- | --- |
| `fum_rt/runtime/helpers/status_http.py:36-188` | In-process HTTP server lacks auth/TLS; exposed host configurable via env | Med | Bind to localhost only by default (already) and add optional token auth/logging.【F:fum_rt/runtime/helpers/status_http.py†L36-L188】 |
| `fum_rt/runtime/loop/main.py:269-280` | `except Exception: return` hides GDSP failures | High | Log exception and trip STRICT gate to fail fast when `VOID_STRICT=1`.【F:fum_rt/runtime/loop/main.py†L269-L283】 |
| `fum_rt/run_nexus.py:20-43` | Directory scanning for checkpoints swallows filesystem errors silently | Low | Emit warning so operators know fallback used.【F:fum_rt/run_nexus.py†L20-L44】 |
| `fum_rt/core/visualizer.py:15-70` | File writes without exception logging; potential silent failure to persist dashboards | Low | Wrap with logger error to surface disk/permission issues.【F:fum_rt/core/visualizer.py†L15-L70】 |

## 13) Consolidated Ledger & Prioritized Actions

**Top-10 debt items (Severity×ROI/Effort)**
1. Dense connectome rebuild each tick — `fum_rt/core/connectome.py` — O(N²) tick cost blocks scale — Effort: L — Owner: Core Runtime
2. GDSP actuator silent failure — `fum_rt/runtime/loop/main.py` — Actuator can’t be trusted without logs — Effort: M — Owner: Runtime Loop
3. Duplicate void dynamics libraries — multiple files — Risk of drift in physics constants — Effort: M — Owner: Advanced Math
4. Memory steering duplication — `fum_rt/physics/...` & `derivation/...` — Double maintenance, inconsistent fixes — Effort: M — Owner: Physics Team
5. RNG fallback noise in void adapter — `fum_rt/core/void_dynamics_adapter.py` — Breaks reproducibility baseline — Effort: M — Owner: Core Runtime
6. Scout flag sprawl — `fum_rt/runtime/loop/main.py` — Hard to audit runtime behavior toggles — Effort: M — Owner: Runtime Loop
7. Frontend visualizer dense conversions — `fum_rt/frontend/plugins/.../fum_visualizer.py` — UI stalls large runs — Effort: L — Owner: Viz Team
8. Structural plasticity RNG w/out seed — `fum_rt/fum_advanced_math/.../apply_structural_plasticity.py` — Non-deterministic experiments — Effort: M — Owner: Advanced Math
9. Status HTTP unauthenticated — `fum_rt/runtime/helpers/status_http.py` — Potential data leak if exposed — Effort: S — Owner: Runtime Ops
10. Missing GDSP tests — `fum_rt/tests` — Actuator regressions undetected — Effort: M — Owner: QA

**Merge candidates**
- Collapse void dynamics & domain modulation into `fum_rt/fum_advanced_math/void_dynamics/` and import from derivation notebooks to avoid triple maintenance.【F:fum_rt/fum_advanced_math/void_dynamics/FUM_Void_Equations.py†L35-L119】
- Deduplicate memory steering by exporting runtime module to derivation namespace (or vice versa).【F:fum_rt/physics/memory_steering/memory_steering.py†L73-L198】

**Kill switches to add immediately**
- `NO_DENSE_CONNECTOME=1` env gate that asserts if dense path allocates beyond threshold, complementing existing FORCE_DENSE guard.【F:fum_rt/core/connectome.py†L11-L15】
- `STRICT_GDSP=1` to elevate `_run_gdsp` exceptions instead of silent returns when debugging.【F:fum_rt/runtime/loop/main.py†L269-L283】

**One-week plan (clean foundation)**
1. Refactor connectome step to sparse adjacency structure (reuse `SparseConnectome`) and profile tick latency.
2. Wire centralized RNG/seed plumbing (runtime seed → void dynamics, structural plasticity, composer).
3. Consolidate void dynamics & memory steering modules; update derivation imports.
4. Implement GDSP telemetry + regression tests covering enable/disable flows.
5. Audit env flags; document in README and add validation for mutually exclusive toggles.

