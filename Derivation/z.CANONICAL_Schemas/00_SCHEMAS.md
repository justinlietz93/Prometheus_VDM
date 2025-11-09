<!-- DOC-GUARD: CANONICAL -->
<!-- RULES for maintaining this file are here: /mnt/ironwolf/git/Prometheus_VDM/prompts/schemas_maintenance.md -->
<!-- markdownlint-disable MD033 -->
# VDM Schemas (Auto-compiled)

**Last updated**: 2025-11-05
**Last commit**: HEAD
**Scope:** Single source of truth for message/record/state/config schemas used in this repository.  
**Rules:** Paste schema definitions from source; document fields. Link to equations/constants/symbols/units/algorithms.  
**MathJax:** Inline `$...$` only in descriptions (no display math or LaTeX environments).

---

## Configs & CLI/ENV

### Run Profile Configuration  <a id="schema-run-profile"></a>

**Kind:** config  
**Versioning (if present):** none  
**Defined at:** `run_profiles/*.json` • `6b63a5e`

**Definition (verbatim snippet from source):**

```json
{
  "neurons": 1000,
  "k": 12,
  "hz": 100,
  "domain": "math_physics",
  "use_time_dynamics": true,
  "sparse_mode": false,
  "threshold": 0.15,
  "lambda_omega": 0.1,
  "candidates": 64,
  "walkers": 256,
  "hops": 3,
  "status_interval": 1,
  "bundle_size": 3,
  "prune_factor": 0.1,
  "stim_group_size": 8,
  "stim_amp": 0.08,
  "stim_decay": 0.92,
  "stim_max_symbols": 128,
  "speak_auto": true,
  "speak_z": 3.0,
  "speak_hysteresis": 0.5,
  "speak_cooldown_ticks": 10,
  "speak_valence_thresh": 0.55,
  "b1_half_life_ticks": 50,
  "viz_every": 100,
  "log_every": 1,
  "checkpoint_every": 60,
  "checkpoint_keep": 5,
  "duration": null
}
```

**Fields (expand from source; do not invent):**

| Field                   | Type      | Required | Default | Units/Normalization | Description (lifted)                              | Source                             |
| ----------------------- | --------- | :------: | ------- | ------------------- | ------------------------------------------------- | ---------------------------------- |
| `neurons`               | `int`     |    Y     | n/a     | count               | Number of neurons in the substrate                | `run_profiles/*.json`              |
| `k`                     | `int`     |    Y     | n/a     | count               | Connectivity parameter                            | `run_profiles/*.json`              |
| `hz`                    | `int`     |    Y     | n/a     | Hz                  | Update frequency                                  | `run_profiles/*.json`              |
| `domain`                | `string`  |    Y     | n/a     | n/a                 | Domain identifier (e.g., "math_physics")          | `run_profiles/*.json`              |
| `use_time_dynamics`     | `bool`    |    Y     | n/a     | n/a                 | Enable time-based dynamics                        | `run_profiles/*.json`              |
| `sparse_mode`           | `bool`    |    Y     | n/a     | n/a                 | Enable sparse connectivity mode                   | `run_profiles/*.json`              |
| `threshold`             | `float`   |    Y     | n/a     | normalized          | Activation threshold                              | `run_profiles/*.json`              |
| `lambda_omega`          | `float`   |    Y     | n/a     | normalized          | Omega lambda parameter                            | `run_profiles/*.json`              |
| `candidates`            | `int`     |    Y     | n/a     | count               | Number of candidates                              | `run_profiles/*.json`              |
| `walkers`               | `int`     |    Y     | n/a     | count               | Number of walker agents                           | `run_profiles/*.json`              |
| `hops`                  | `int`     |    Y     | n/a     | count               | Walker hop count                                  | `run_profiles/*.json`              |
| `status_interval`       | `int`     |    Y     | n/a     | ticks               | Status reporting interval                         | `run_profiles/*.json`              |
| `bundle_size`           | `int`     |    Y     | n/a     | count               | Bundle size parameter                             | `run_profiles/*.json`              |
| `prune_factor`          | `float`   |    Y     | n/a     | normalized          | Pruning factor                                    | `run_profiles/*.json`              |
| `stim_group_size`       | `int`     |    Y     | n/a     | count               | Stimulus group size                               | `run_profiles/*.json`              |
| `stim_amp`              | `float`   |    Y     | n/a     | normalized          | Stimulus amplitude                                | `run_profiles/*.json`              |
| `stim_decay`            | `float`   |    Y     | n/a     | normalized          | Stimulus decay rate                               | `run_profiles/*.json`              |
| `stim_max_symbols`      | `int`     |    Y     | n/a     | count               | Maximum stimulus symbols                          | `run_profiles/*.json`              |
| `speak_auto`            | `bool`    |    Y     | n/a     | n/a                 | Enable automatic speaking                         | `run_profiles/*.json`              |
| `speak_z`               | `float`   |    Y     | n/a     | normalized          | Speaking Z-score threshold                        | `run_profiles/*.json`              |
| `speak_hysteresis`      | `float`   |    Y     | n/a     | normalized          | Speaking hysteresis threshold                     | `run_profiles/*.json`              |
| `speak_cooldown_ticks`  | `int`     |    Y     | n/a     | ticks               | Speaking cooldown period                          | `run_profiles/*.json`              |
| `speak_valence_thresh`  | `float`   |    Y     | n/a     | normalized          | Speaking valence threshold                        | `run_profiles/*.json`              |
| `b1_half_life_ticks`    | `int`     |    Y     | n/a     | ticks               | B1 half-life in ticks                             | `run_profiles/*.json`              |
| `viz_every`             | `int`     |    Y     | n/a     | ticks               | Visualization interval (0 disables)               | `run_profiles/*.json`              |
| `log_every`             | `int`     |    Y     | n/a     | ticks               | Logging interval                                  | `run_profiles/*.json`              |
| `checkpoint_every`      | `int`     |    Y     | n/a     | ticks               | Checkpoint save interval                          | `run_profiles/*.json`              |
| `checkpoint_keep`       | `int`     |    Y     | n/a     | count               | Number of checkpoints to retain                   | `run_profiles/*.json`              |
| `duration`              | `int|null` |   Y     | null    | ticks               | Total simulation duration (null for indefinite)   | `run_profiles/*.json`              |

**Producers/Consumers:** Used by main runtime orchestrator  
**Related equations (anchors only):** TODO: missing anchor (see Derivation/EQUATIONS.md)  
**Related symbols/constants:** TODO: missing anchor (see Derivation/SYMBOLS.md, Derivation/CONSTANTS.md)  
**Examples (if present):** `run_profiles/02_vdm_viz100_20250811.json`, `run_profiles/10kN_viz.json`, `run_profiles/00_vdm_20250810.json`  
**Invariants/Validation rules:** All numeric fields must be >= 0; `neurons`, `k`, `hz` > 0; `duration` may be null  
**Notes:** Multiple run profile variants exist with different scale parameters (100, 1k, 10k neurons)

---

#### LBMConfig  <a id="schema-lbmconfig"></a>

**Kind:** config  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:119-135` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class LBMConfig:
    nx: int = 256
    ny: int = 256
    tau: float = 0.8               # relaxation time; nu = CS2 * (tau - 0.5)
    forcing: tuple[float, float] = (0.0, 0.0)  # body force (fx, fy)
    periodic_x: bool = True
    periodic_y: bool = True
    # VDM void dynamics coupling (bounded stabilizer)
    void_enabled: bool = True
    void_domain: str = "standard_model"
    void_gain: float = 0.5
    void_use_modulation: bool = False
    rho_floor: float = 1e-9
    u_clamp: float | None = None   # e.g., 0.1 to keep Ma≲0.1; None disables
```

**Fields (expand from source; do not invent):**

| Field                | Type              | Required | Default            | Units/Normalization | Description (lifted)                                       | Source                                                            |
| -------------------- | ----------------- | :------: | ------------------ | ------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------- |
| `nx`                 | `int`             |    N     | `256`              | lattice units       | Grid points in x-direction                                 | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:120`      |
| `ny`                 | `int`             |    N     | `256`              | lattice units       | Grid points in y-direction                                 | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:121`      |
| `tau`                | `float`           |    N     | `0.8`              | normalized          | Relaxation time; $\nu = c_s^2 (\tau - 0.5)$               | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:122`      |
| `forcing`            | `tuple[float, float]` |    N | `(0.0, 0.0)`       | lattice force units | Body force $(f_x, f_y)$                                    | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:123`      |
| `periodic_x`         | `bool`            |    N     | `True`             | n/a                 | Enable periodic boundaries in x                            | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:124`      |
| `periodic_y`         | `bool`            |    N     | `True`             | n/a                 | Enable periodic boundaries in y                            | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:125`      |
| `void_enabled`       | `bool`            |    N     | `True`             | n/a                 | VDM void dynamics coupling (bounded stabilizer)          | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:127`      |
| `void_domain`        | `str`             |    N     | `"standard_model"` | n/a                 | Void domain identifier                                     | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:128`      |
| `void_gain`          | `float`           |    N     | `0.5`              | normalized          | Void coupling gain                                         | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:129`      |
| `void_use_modulation`| `bool`            |    N     | `False`            | n/a                 | Enable void debt modulation                                | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:130`      |
| `rho_floor`          | `float`           |    N     | `1e-9`             | lattice density     | Minimum density floor                                      | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:131`      |
| `u_clamp`            | `float | None`    |    N     | `None`             | lattice velocity    | Velocity clamp to keep $Ma \lesssim 0.1$; None disables   | `Derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:132`      |

**Producers/Consumers:** Used by LBM2D solver in fluid dynamics benchmarks → TODO: link `ALGORITHMS.md#vdm-a-lbm-bgk`  
**Related equations (anchors only):** TODO: missing anchor for BGK collision operator (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for $c_s$ (see `Derivation/SYMBOLS.md`)  
**Examples (if present):** `Derivation/code/physics/fluid_dynamics/benchmarks/taylor_green_benchmark.py`, `Derivation/code/physics/fluid_dynamics/benchmarks/lid_cavity_benchmark.py`  
**Invariants/Validation rules:** `nx, ny > 0`; `tau > 0.5` (for stability); `rho_floor > 0`; if `u_clamp` is not None, must be > 0  
**Notes:** Integrates VDM void dynamics as a bounded stabilizer when `void_enabled=True`

---

#### GeometryRunConfig  <a id="schema-geometryrunconfig"></a>

**Kind:** config  
**Versioning (if present):** none  
**Defined at:** `tools/geom_bundle_builder.py:109-143` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class GeometryRunConfig:
    storage_root: Path
    concepts: Sequence[str]
    layers: Sequence[str]
    steps: Sequence[int]
    batch_size: int = 1
    max_bundle_mb: int = 1500
    allow_dirty: bool = False
    probe_mode: str = "eval_no_dropout"
    seeds: Sequence[int] = field(default_factory=list)
    adapter_path: Optional[str] = None
    create_thumbs: bool = False

    @classmethod
    def from_json(cls, data: Mapping[str, object], default_storage_root: Path) -> "GeometryRunConfig":
        storage_root = Path(data.get("storage_root", default_storage_root)).expanduser().resolve()
        concepts = list(data.get("concepts", []))
        layers = list(data.get("layers", []))
        steps = list(data.get("steps", []))
        if not concepts or not layers or not steps:
            raise ValueError("Concepts, layers, and steps must be provided in the config.")
        return cls(
            storage_root=storage_root,
            concepts=concepts,
            layers=layers,
            steps=[int(s) for s in steps],
            batch_size=int(data.get("batch_size", 1)),
            max_bundle_mb=int(data.get("max_bundle_mb", 1500)),
            allow_dirty=bool(data.get("allow_dirty", False)),
            probe_mode=str(data.get("probe_mode", "eval_no_dropout")),
            seeds=[int(v) for v in data.get("seeds", [])],
            adapter_path=str(data.get("adapter_path")) if data.get("adapter_path") else None,
            create_thumbs=bool(data.get("create_thumbs", False)),
        )
```

**Fields (expand from source; do not invent):**

| Field            | Type             | Required | Default                 | Units/Normalization | Description (lifted)                              | Source                              |
| ---------------- | ---------------- | :------: | ----------------------- | ------------------- | ------------------------------------------------- | ----------------------------------- |
| `storage_root`   | `Path`           |    Y     | n/a                     | filesystem path     | Root directory for geometry bundle storage        | `tools/geom_bundle_builder.py:111`  |
| `concepts`       | `Sequence[str]`  |    Y     | n/a                     | n/a                 | List of concepts to capture activations for       | `tools/geom_bundle_builder.py:112`  |
| `layers`         | `Sequence[str]`  |    Y     | n/a                     | n/a                 | List of layer names to probe                      | `tools/geom_bundle_builder.py:113`  |
| `steps`          | `Sequence[int]`  |    Y     | n/a                     | checkpoint steps    | Training checkpoint steps to load                 | `tools/geom_bundle_builder.py:114`  |
| `batch_size`     | `int`            |    N     | `1`                     | count               | Batch size for activation capture                 | `tools/geom_bundle_builder.py:115`  |
| `max_bundle_mb`  | `int`            |    N     | `1500`                  | MB                  | Maximum bundle size in megabytes                  | `tools/geom_bundle_builder.py:116`  |
| `allow_dirty`    | `bool`           |    N     | `False`                 | n/a                 | Allow dirty git working tree                      | `tools/geom_bundle_builder.py:117`  |
| `probe_mode`     | `str`            |    N     | `"eval_no_dropout"`     | n/a                 | Model evaluation mode                             | `tools/geom_bundle_builder.py:118`  |
| `seeds`          | `Sequence[int]`  |    N     | `[]`                    | n/a                 | Random seeds for reproducibility                  | `tools/geom_bundle_builder.py:119`  |
| `adapter_path`   | `str | None`     |    N     | `None`                  | n/a                 | Python import path to adapter (module:ClassName)  | `tools/geom_bundle_builder.py:120`  |
| `create_thumbs`  | `bool`           |    N     | `False`                 | n/a                 | Generate thumbnail visualizations                 | `tools/geom_bundle_builder.py:121`  |

**Producers/Consumers:** Consumed by `tools/geom_bundle_builder.py` workflow  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** TODO: add example config  
**Invariants/Validation rules:** `concepts`, `layers`, and `steps` must be non-empty; `batch_size > 0`; `max_bundle_mb > 0`  
**Notes:** Loaded via `from_json` classmethod; adapter_path format is `module:ClassName`

---

#### VDM Corner Config (YAML)  <a id="schema-vdm-corner-config"></a>

**Kind:** config  
**Versioning (if present):** v0.1 (draft)  
**Defined at:** `Derivation/notebooks/VDM_corner_config.yaml:1-40` • `6b63a5e`

**Definition (verbatim snippet from source):**

```yaml
# VDM Corner Testbed - baseline vs VDM-regularized (draft v0.1)
# Geometry
H: 1.0              # inlet height (non-dimensional units)
L_in: 3.0           # inlet straight length (multiples of H)
L_out: 5.0          # outlet straight length (multiples of H)
rc: 0.00            # inner fillet radius; set to 0.0 to recover a sharp corner

# Fluid
rho: 1.0            # density
nu: 1e-3            # kinematic viscosity (ν)

# Inlet profile
U0: 1.0             # characteristic inlet speed

# Numerics
Nx: 256             # grid points x-direction
Ny: 256             # grid points y-direction
dt: 1e-3            # time step
t_end: 2.0          # simulation end time

# Baseline boundary conditions
walls: no-slip      # no-penetration + no-slip
inlet: dirichlet    # fixed ux=U0, uy=0
outlet: neumann     # zero-grad (pressure/velocity, depending on solver)

# VDM regularizer (Void Debt Modulation)
regularizer:
  enabled: true
  beta: 0.6         # coupling of 'debt' to advective transport limiter (1/(1 + beta*D))
  tau_r: 0.5        # debt relaxation time (D decays like -D/tau_r)
  kappa: 1e-3       # diffusion of D (smooth spread)
  alpha: 1.0        # source strength from strain rate |∇u|^2
  tau_u: 0.1        # velocity smoothing timescale
  tau_g: 0.5        # global valence accumulation window

# Outputs
save_streamlines: true
save_vorticity: true
save_maxspeed_scan: true
```

**Fields (expand from source; do not invent):**

| Field                      | Type    | Required | Default     | Units/Normalization | Description (lifted)                                       | Source                                          |
| -------------------------- | ------- | :------: | ----------- | ------------------- | ---------------------------------------------------------- | ----------------------------------------------- |
| `H`                        | `float` |    Y     | n/a         | non-dimensional     | Inlet height                                               | `Derivation/notebooks/VDM_corner_config.yaml:3` |
| `L_in`                     | `float` |    Y     | n/a         | multiples of H      | Inlet straight length                                      | `Derivation/notebooks/VDM_corner_config.yaml:4` |
| `L_out`                    | `float` |    Y     | n/a         | multiples of H      | Outlet straight length                                     | `Derivation/notebooks/VDM_corner_config.yaml:5` |
| `rc`                       | `float` |    Y     | n/a         | non-dimensional     | Inner fillet radius; 0.0 for sharp corner                  | `Derivation/notebooks/VDM_corner_config.yaml:6` |
| `rho`                      | `float` |    Y     | n/a         | density units       | Fluid density                                              | `Derivation/notebooks/VDM_corner_config.yaml:9` |
| `nu`                       | `float` |    Y     | n/a         | kinematic viscosity | Kinematic viscosity $\nu$                                  | `Derivation/notebooks/VDM_corner_config.yaml:10`|
| `U0`                       | `float` |    Y     | n/a         | velocity units      | Characteristic inlet speed                                 | `Derivation/notebooks/VDM_corner_config.yaml:13`|
| `Nx`                       | `int`   |    Y     | n/a         | count               | Grid points in x-direction                                 | `Derivation/notebooks/VDM_corner_config.yaml:16`|
| `Ny`                       | `int`   |    Y     | n/a         | count               | Grid points in y-direction                                 | `Derivation/notebooks/VDM_corner_config.yaml:17`|
| `dt`                       | `float` |    Y     | n/a         | time units          | Time step                                                  | `Derivation/notebooks/VDM_corner_config.yaml:18`|
| `t_end`                    | `float` |    Y     | n/a         | time units          | Simulation end time                                        | `Derivation/notebooks/VDM_corner_config.yaml:19`|
| `walls`                    | `str`   |    Y     | n/a         | n/a                 | Wall boundary condition type                               | `Derivation/notebooks/VDM_corner_config.yaml:22`|
| `inlet`                    | `str`   |    Y     | n/a         | n/a                 | Inlet boundary condition type                              | `Derivation/notebooks/VDM_corner_config.yaml:23`|
| `outlet`                   | `str`   |    Y     | n/a         | n/a                 | Outlet boundary condition type                             | `Derivation/notebooks/VDM_corner_config.yaml:24`|
| `regularizer.enabled`      | `bool`  |    Y     | n/a         | n/a                 | Enable VDM regularizer                                     | `Derivation/notebooks/VDM_corner_config.yaml:28`|
| `regularizer.beta`         | `float` |    Y     | n/a         | normalized          | Coupling of debt to advective transport limiter            | `Derivation/notebooks/VDM_corner_config.yaml:29`|
| `regularizer.tau_r`        | `float` |    Y     | n/a         | time units          | Debt relaxation time                                       | `Derivation/notebooks/VDM_corner_config.yaml:30`|
| `regularizer.kappa`        | `float` |    Y     | n/a         | diffusion coeff     | Diffusion of debt field $D$                                | `Derivation/notebooks/VDM_corner_config.yaml:31`|
| `regularizer.alpha`        | `float` |    Y     | n/a         | normalized          | Source strength from strain rate $\|\nabla u\|^2$          | `Derivation/notebooks/VDM_corner_config.yaml:32`|
| `regularizer.tau_u`        | `float` |    Y     | n/a         | time units          | Velocity smoothing timescale                               | `Derivation/notebooks/VDM_corner_config.yaml:33`|
| `regularizer.tau_g`        | `float` |    Y     | n/a         | time units          | Global valence accumulation window                         | `Derivation/notebooks/VDM_corner_config.yaml:34`|
| `save_streamlines`         | `bool`  |    Y     | n/a         | n/a                 | Save streamline visualizations                             | `Derivation/notebooks/VDM_corner_config.yaml:37`|
| `save_vorticity`           | `bool`  |    Y     | n/a         | n/a                 | Save vorticity field outputs                               | `Derivation/notebooks/VDM_corner_config.yaml:38`|
| `save_maxspeed_scan`       | `bool`  |    Y     | n/a         | n/a                 | Save maximum speed scan results                            | `Derivation/notebooks/VDM_corner_config.yaml:39`|

**Producers/Consumers:** Used by VDM corner flow benchmarks in notebooks  
**Related equations (anchors only):** TODO: missing anchor for Navier-Stokes and VDM regularization terms (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for $\nu$, $D$ (see `Derivation/SYMBOLS.md`)  
**Examples (if present):** `Derivation/notebooks/VDM_corner_config.yaml`  
**Invariants/Validation rules:** `H, rho, U0 > 0`; `nu > 0`; `Nx, Ny > 0`; `dt, t_end > 0`; `rc >= 0`  
**Notes:** Draft v0.1; VDM regularizer implements Void Debt Modulation for flow stability

---

## State Snapshots & Checkpoints

#### RunMetrics  <a id="schema-runmetrics"></a>

**Kind:** record  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/conservation_law/qfum_validate.py:133-143` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class RunMetrics:
    r: float
    u: float
    solver: str
    dt: float
    T: float
    W0: float
    delta_Q_max: float
    W_min: float
    W_max: float
```

**Fields (expand from source; do not invent):**

| Field          | Type    | Required | Default | Units/Normalization | Description (lifted)                                      | Source                                                              |
| -------------- | ------- | :------: | ------- | ------------------- | --------------------------------------------------------- | ------------------------------------------------------------------- |
| `r`            | `float` |    Y     | n/a     | rate                | Logistic growth rate parameter                            | `Derivation/code/physics/conservation_law/qfum_validate.py:134`     |
| `u`            | `float` |    Y     | n/a     | rate                | Logistic carrying capacity coefficient                    | `Derivation/code/physics/conservation_law/qfum_validate.py:135`     |
| `solver`       | `str`   |    Y     | n/a     | n/a                 | ODE solver identifier (e.g., "rk4", "euler")              | `Derivation/code/physics/conservation_law/qfum_validate.py:136`     |
| `dt`           | `float` |    Y     | n/a     | time units          | Time step size                                            | `Derivation/code/physics/conservation_law/qfum_validate.py:137`     |
| `T`            | `float` |    Y     | n/a     | time units          | Total integration time                                    | `Derivation/code/physics/conservation_law/qfum_validate.py:138`     |
| `W0`           | `float` |    Y     | n/a     | state variable      | Initial condition for $W$                                 | `Derivation/code/physics/conservation_law/qfum_validate.py:139`     |
| `delta_Q_max`  | `float` |    Y     | n/a     | normalized          | Maximum invariant drift $\|Q(t) - Q(0)\|$                | `Derivation/code/physics/conservation_law/qfum_validate.py:140`     |
| `W_min`        | `float` |    Y     | n/a     | state variable      | Minimum $W$ value observed                                | `Derivation/code/physics/conservation_law/qfum_validate.py:141`     |
| `W_max`        | `float` |    Y     | n/a     | state variable      | Maximum $W$ value observed                                | `Derivation/code/physics/conservation_law/qfum_validate.py:142`     |

**Producers/Consumers:** Produced by `qfum_validate.py` validation script; serialized to JSON  
**Related equations (anchors only):** TODO: missing anchor for $Q(W,t) = \ln(W/(r - uW)) - rt$ (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for $W$, $Q$ (see `Derivation/SYMBOLS.md`)  
**Examples (if present):** `Derivation/code/outputs/logs/conservation_law/*_qfum_metrics.json`  
**Invariants/Validation rules:** `r, u, dt, T > 0`; `W0 > 0`; `delta_Q_max >= 0`  
**Notes:** Used to verify Q_FUM logarithmic first integral conservation

---

#### ConvergenceMetrics  <a id="schema-convergencemetrics"></a>

**Kind:** record  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/conservation_law/qfum_validate.py:146-155` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class ConvergenceMetrics:
    r: float
    u: float
    solver: str
    dts: List[float]
    delta_Q_max_list: List[float]
    slope: float
    intercept: float
    r2: float
```

**Fields (expand from source; do not invent):**

| Field              | Type          | Required | Default | Units/Normalization | Description (lifted)                                 | Source                                                              |
| ------------------ | ------------- | :------: | ------- | ------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| `r`                | `float`       |    Y     | n/a     | rate                | Logistic growth rate parameter                       | `Derivation/code/physics/conservation_law/qfum_validate.py:147`     |
| `u`                | `float`       |    Y     | n/a     | rate                | Logistic carrying capacity coefficient               | `Derivation/code/physics/conservation_law/qfum_validate.py:148`     |
| `solver`           | `str`         |    Y     | n/a     | n/a                 | ODE solver identifier                                | `Derivation/code/physics/conservation_law/qfum_validate.py:149`     |
| `dts`              | `List[float]` |    Y     | n/a     | time units          | List of time step sizes tested                       | `Derivation/code/physics/conservation_law/qfum_validate.py:150`     |
| `delta_Q_max_list` | `List[float]` |    Y     | n/a     | normalized          | Maximum invariant drifts for each dt                 | `Derivation/code/physics/conservation_law/qfum_validate.py:151`     |
| `slope`            | `float`       |    Y     | n/a     | log-log slope       | Convergence rate from log-log fit                    | `Derivation/code/physics/conservation_law/qfum_validate.py:152`     |
| `intercept`        | `float`       |    Y     | n/a     | log-log intercept   | Intercept from log-log fit                           | `Derivation/code/physics/conservation_law/qfum_validate.py:153`     |
| `r2`               | `float`       |    Y     | n/a     | normalized          | $R^2$ coefficient of determination                   | `Derivation/code/physics/conservation_law/qfum_validate.py:154`     |

**Producers/Consumers:** Produced by `qfum_validate.py` convergence study; serialized to JSON  
**Related equations (anchors only):** TODO: missing anchor for convergence analysis (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** `Derivation/code/outputs/logs/conservation_law/*_qfum_metrics.json`  
**Invariants/Validation rules:** `r, u > 0`; `dts` and `delta_Q_max_list` must have same length; `r2 in [0,1]`  
**Notes:** Slope should be ≈4 for RK4 solver; tests temporal convergence order

---

## Buses & Messages

#### Petition  <a id="schema-petition"></a>

**Kind:** message  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:11-17` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class Petition:
    kind: str        # 'div', 'swirl', 'shear'
    value: float
    x: float
    y: float
    t: int
```

**Fields (expand from source; do not invent):**

| Field   | Type    | Required | Default | Units/Normalization | Description (lifted)                      | Source                                                                 |
| ------- | ------- | :------: | ------- | ------------------- | ----------------------------------------- | ---------------------------------------------------------------------- |
| `kind`  | `str`   |    Y     | n/a     | n/a                 | Petition type: 'div', 'swirl', or 'shear' | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:12`       |
| `value` | `float` |    Y     | n/a     | varies by kind      | Measured scalar value                     | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:13`       |
| `x`     | `float` |    Y     | n/a     | spatial coord       | X coordinate of measurement               | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:14`       |
| `y`     | `float` |    Y     | n/a     | spatial coord       | Y coordinate of measurement               | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:15`       |
| `t`     | `int`   |    Y     | n/a     | timestep            | Timestep of measurement                   | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:16`       |

**Producers/Consumers:** Produced by Walker agents; posted to Bus; consumed by Reducer → TODO: link `ALGORITHMS.md#vdm-a-walker`  
**Related equations (anchors only):** TODO: missing anchor for divergence, vorticity, shear (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** Emitted by walkers in `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:112-125`  
**Invariants/Validation rules:** `kind` must be one of `['div', 'swirl', 'shear']`; `t >= 0`  
**Notes:** Read-only measurement message; does not modify simulation state

---

#### PolicyBounds  <a id="schema-policybounds"></a>

**Kind:** config/record  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:43-49` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class PolicyBounds:
    tau_min: float = 0.51
    tau_max: float = 1.95
    U_min: float = 1e-8
    U_max: float = 0.2
    uclamp_min: float = 1e-6
    uclamp_max: float = 0.1
```

**Fields (expand from source; do not invent):**

| Field         | Type    | Required | Default | Units/Normalization | Description (lifted)                      | Source                                                                 |
| ------------- | ------- | :------: | ------- | ------------------- | ----------------------------------------- | ---------------------------------------------------------------------- |
| `tau_min`     | `float` |    N     | `0.51`  | normalized          | Minimum relaxation time $\tau$            | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:44`       |
| `tau_max`     | `float` |    N     | `1.95`  | normalized          | Maximum relaxation time $\tau$            | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:45`       |
| `U_min`       | `float` |    N     | `1e-8`  | velocity units      | Minimum characteristic velocity           | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:46`       |
| `U_max`       | `float` |    N     | `0.2`   | velocity units      | Maximum characteristic velocity           | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:47`       |
| `uclamp_min`  | `float` |    N     | `1e-6`  | velocity units      | Minimum velocity clamp                    | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:48`       |
| `uclamp_max`  | `float` |    N     | `0.1`   | velocity units      | Maximum velocity clamp                    | `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:49`       |

**Producers/Consumers:** Used by AdvisoryPolicy in fluid dynamics telemetry  
**Related equations (anchors only):** TODO: missing anchor for LBM stability criteria (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for $\tau$ (see `Derivation/SYMBOLS.md`)  
**Examples (if present):** Instantiated in `Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:51`  
**Invariants/Validation rules:** `tau_min > 0.5` (stability); `tau_max > tau_min`; `U_max > U_min > 0`; `uclamp_max > uclamp_min > 0`  
**Notes:** Advisory policy bounds; numeric parameters only, no forcing

---

#### Observation  <a id="schema-observation"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/announce.py:33-62` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class Observation:
    tick: int
    kind: str  # "region_stat" | "boundary_probe" | "cycle_hit" | "novel_frontier"
    nodes: List[int] = field(default_factory=list)
    centroid: Optional[Tuple[float, float, float]] = None
    w_mean: float = 0.0
    w_var: float = 0.0
    s_mean: float = 0.0
    cut_strength: float = 0.0
    loop_len: int = 0
    loop_gain: float = 0.0
    coverage_id: int = 0
    domain_hint: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
```

**Fields (expand from source; do not invent):**

| Field          | Type                                 | Required | Default | Units/Normalization | Description (lifted)                                          | Source                         |
| -------------- | ------------------------------------ | :------: | ------- | ------------------- | ------------------------------------------------------------- | ------------------------------ |
| `tick`         | `int`                                |    Y     | n/a     | timestep            | Simulation tick when observation was made                     | `fum_rt/core/announce.py:35`   |
| `kind`         | `str`                                |    Y     | n/a     | n/a                 | One of: "region_stat", "boundary_probe", "cycle_hit", "novel_frontier" | `fum_rt/core/announce.py:36` |
| `nodes`        | `List[int]`                          |    N     | `[]`    | node IDs            | Small representative subset of visited node IDs               | `fum_rt/core/announce.py:38`   |
| `centroid`     | `Optional[Tuple[float, float, float]]` |  N     | `None`  | embedding space     | Optional centroid in embedding space                          | `fum_rt/core/announce.py:41`   |
| `w_mean`       | `float`                              |    N     | `0.0`   | state variable      | Mean $W$ over visited set                                     | `fum_rt/core/announce.py:44`   |
| `w_var`        | `float`                              |    N     | `0.0`   | state variable      | Variance of $W$ over visited set                              | `fum_rt/core/announce.py:45`   |
| `s_mean`       | `float`                              |    N     | `0.0`   | coupling strength   | Mean positive coupling during walk                            | `fum_rt/core/announce.py:46`   |
| `cut_strength` | `float`                              |    N     | `0.0`   | normalized          | Strength of cut across boundary sample                        | `fum_rt/core/announce.py:49`   |
| `loop_len`     | `int`                                |    N     | `0`     | count               | Length of detected loop (for cycle_hit)                       | `fum_rt/core/announce.py:52`   |
| `loop_gain`    | `float`                              |    N     | `0.0`   | accumulated weight  | Accumulated positive transition weights along loop            | `fum_rt/core/announce.py:53`   |
| `coverage_id`  | `int`                                |    N     | `0`     | bin ID              | Coverage bin for ADC scheduling                               | `fum_rt/core/announce.py:56`   |
| `domain_hint`  | `str`                                |    N     | `""`    | n/a                 | Optional domain hint from cartographer                        | `fum_rt/core/announce.py:59`   |
| `meta`         | `Dict[str, Any]`                     |    N     | `{}`    | n/a                 | Extra metadata (JSON-serializable only)                       | `fum_rt/core/announce.py:62`   |

**Producers/Consumers:** Produced by void-walker agents; published to announcement bus; consumed by Active Domain Cartography (ADC)  
**Related equations (anchors only):** TODO: missing anchor for RE-VGSP/GDSP deltas (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for $W$, $S_{ij}$ (see `Derivation/SYMBOLS.md`)  
**Examples (if present):** Validated by `fum_rt/core/announce.py:65-75`  
**Invariants/Validation rules:** `tick >= 0`; `kind` must be one of the four allowed values; `len(nodes) <= 256`; `loop_len >= 0`  
**Notes:** Event schema for void-walker announcement bus; kept compact for efficient ADC processing

---

#### BaseEvent  <a id="schema-baseevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:49-52` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class BaseEvent:
    kind: str
    t: Optional[int] = None
```

**Fields (expand from source; do not invent):**

| Field  | Type           | Required | Default | Units/Normalization | Description (lifted)      | Source                                         |
| ------ | -------------- | :------: | ------- | ------------------- | ------------------------- | ---------------------------------------------- |
| `kind` | `str`          |    Y     | n/a     | n/a                 | Event kind identifier     | `fum_rt/core/proprioception/events.py:51`      |
| `t`    | `Optional[int]`|    N     | `None`  | timestep            | Optional simulation tick  | `fum_rt/core/proprioception/events.py:52`      |

**Producers/Consumers:** Base class for all event-driven metrics events  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** Subclassed by DeltaEvent, VTTouchEvent, EdgeOnEvent, etc.  
**Invariants/Validation rules:** Immutable (frozen dataclass)  
**Notes:** Frozen dataclass; base for event hierarchy in event-driven metrics system

---

#### DeltaEvent  <a id="schema-deltaevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:55-71` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class DeltaEvent(BaseEvent):
    """
    Local structural/learning delta.
    Fields:
      - b1: contribution to B1-like topology signal (float)
      - novelty: novelty component in [0, +inf)
      - hab: habituation component in [0, +inf)
      - td: temporal-difference-like component (float)
      - hsi: homeostatic stability/instability component (float)
    """
    b1: float = 0.0
    novelty: float = 0.0
    hab: float = 0.0
    td: float = 0.0
    hsi: float = 0.0
```

**Fields (expand from source; do not invent):**

| Field     | Type    | Required | Default | Units/Normalization | Description (lifted)                                  | Source                                         |
| --------- | ------- | :------: | ------- | ------------------- | ----------------------------------------------------- | ---------------------------------------------- |
| `b1`      | `float` |    N     | `0.0`   | normalized          | Contribution to B1-like topology signal               | `fum_rt/core/proprioception/events.py:66`      |
| `novelty` | `float` |    N     | `0.0`   | $[0, +\infty)$      | Novelty component                                     | `fum_rt/core/proprioception/events.py:67`      |
| `hab`     | `float` |    N     | `0.0`   | $[0, +\infty)$      | Habituation component                                 | `fum_rt/core/proprioception/events.py:68`      |
| `td`      | `float` |    N     | `0.0`   | normalized          | Temporal-difference-like component                    | `fum_rt/core/proprioception/events.py:69`      |
| `hsi`     | `float` |    N     | `0.0`   | normalized          | Homeostatic stability/instability component           | `fum_rt/core/proprioception/events.py:70`      |

**Producers/Consumers:** Produced by connectome/walker learning updates; consumed by EventDrivenMetrics  
**Related equations (anchors only):** TODO: missing anchor for B1 topology, TD learning (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** Emitted during structural plasticity events  
**Invariants/Validation rules:** Immutable (frozen); `novelty, hab >= 0`  
**Notes:** Inherits from BaseEvent; captures local structural/learning delta

---

#### VTTouchEvent  <a id="schema-vttouchevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:73-83` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class VTTouchEvent(BaseEvent):
    """
    Vocabulary/feature touch (used for VT coverage/entropy approximations).
    Fields:
      - token: hashable token id or string
      - w: optional weight (float, default 1.0)
    """
    token: Any = ""
    w: float = 1.0
```

**Fields (expand from source; do not invent):**

| Field   | Type    | Required | Default | Units/Normalization | Description (lifted)                          | Source                                         |
| ------- | ------- | :------: | ------- | ------------------- | --------------------------------------------- | ---------------------------------------------- |
| `token` | `Any`   |    N     | `""`    | n/a                 | Hashable token ID or string                   | `fum_rt/core/proprioception/events.py:81`      |
| `w`     | `float` |    N     | `1.0`   | weight              | Optional weight                               | `fum_rt/core/proprioception/events.py:82`      |

**Producers/Consumers:** Produced on vocabulary/feature access; consumed by EventDrivenMetrics for coverage/entropy approximation  
**Related equations (anchors only):** TODO: missing anchor for vocabulary coverage and entropy (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** Used in VT coverage tracking  
**Invariants/Validation rules:** Immutable (frozen); `w` typically > 0  
**Notes:** Inherits from BaseEvent; used for VT coverage/entropy approximations via Count-Min Sketch

---

#### EdgeOnEvent / EdgeOffEvent  <a id="schema-edgeevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:85-94` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class EdgeOnEvent(BaseEvent):
    u: int = 0
    v: int = 0

@dataclass(frozen=True)
class EdgeOffEvent(BaseEvent):
    u: int = 0
    v: int = 0
```

**Fields (expand from source; do not invent):**

| Field | Type  | Required | Default | Units/Normalization | Description (lifted)  | Source                                         |
| ----- | ----- | :------: | ------- | ------------------- | --------------------- | ---------------------------------------------- |
| `u`   | `int` |    N     | `0`     | node ID             | Source node ID        | `fum_rt/core/proprioception/events.py:87,92`   |
| `v`   | `int` |    N     | `0`     | node ID             | Target node ID        | `fum_rt/core/proprioception/events.py:88,93`   |

**Producers/Consumers:** Produced by structural plasticity; EdgeOn consumed by UnionFindCohesion; EdgeOff marks dirty for reconciliation  
**Related equations (anchors only):** TODO: missing anchor for cohesion metric (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** Emitted during edge creation/deletion  
**Invariants/Validation rules:** Immutable (frozen); `u, v >= 0`  
**Notes:** EdgeOffEvent is marked dirty; low-cadence auditor reconciles connectivity

---

#### SpikeEvent  <a id="schema-spikeevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:97-103` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class SpikeEvent(BaseEvent):
    node: int = 0       # neuron id
    amp: float = 1.0    # activity magnitude (or |ΔW| proxy)
    sign: int = +1      # +1 excitatory, -1 inhibitory, 0 unknown
```

**Fields (expand from source; do not invent):**

| Field  | Type    | Required | Default | Units/Normalization | Description (lifted)                               | Source                                         |
| ------ | ------- | :------: | ------- | ------------------- | -------------------------------------------------- | ---------------------------------------------- |
| `node` | `int`   |    N     | `0`     | neuron ID           | Neuron ID                                          | `fum_rt/core/proprioception/events.py:100`     |
| `amp`  | `float` |    N     | `1.0`   | activity magnitude  | Activity magnitude or $\|\Delta W\|$ proxy         | `fum_rt/core/proprioception/events.py:101`     |
| `sign` | `int`   |    N     | `+1`    | polarity            | +1 excitatory, -1 inhibitory, 0 unknown            | `fum_rt/core/proprioception/events.py:102`     |

**Producers/Consumers:** Produced by neurons during activity; consumed by EventDrivenMetrics  
**Related equations (anchors only):** TODO: missing anchor for void-faithful polarity (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** Emitted during neuron activation  
**Invariants/Validation rules:** Immutable (frozen); `node >= 0`; `sign in [-1, 0, +1]`; `amp >= 0`  
**Notes:** Polarity-aware activity/spike event; void-faithful, event-driven only

---

#### DeltaWEvent  <a id="schema-deltawevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:106-110` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class DeltaWEvent(BaseEvent):
    node: int = 0
    dw: float = 0.0
```

**Fields (expand from source; do not invent):**

| Field  | Type    | Required | Default | Units/Normalization | Description (lifted)           | Source                                         |
| ------ | ------- | :------: | ------- | ------------------- | ------------------------------ | ---------------------------------------------- |
| `node` | `int`   |    N     | `0`     | neuron ID           | Node ID for weight update      | `fum_rt/core/proprioception/events.py:108`     |
| `dw`   | `float` |    N     | `0.0`   | weight delta        | Signed weight delta $\Delta W$ | `fum_rt/core/proprioception/events.py:109`     |

**Producers/Consumers:** Produced by local learning updates; consumed by EventDrivenMetrics  
**Related equations (anchors only):** TODO: missing anchor for weight update rules (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for $W$ (see `Derivation/SYMBOLS.md`)  
**Examples (if present):** Emitted during synaptic weight updates  
**Invariants/Validation rules:** Immutable (frozen); `node >= 0`  
**Notes:** Optional signed weight delta event for local learning updates

---

#### MotifEnterEvent / MotifExitEvent  <a id="schema-motifevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:112-120` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class MotifEnterEvent(BaseEvent):
    motif_id: int = 0

@dataclass(frozen=True)
class MotifExitEvent(BaseEvent):
    motif_id: int = 0
```

**Fields (expand from source; do not invent):**

| Field      | Type  | Required | Default | Units/Normalization | Description (lifted)    | Source                                              |
| ---------- | ----- | :------: | ------- | ------------------- | ----------------------- | --------------------------------------------------- |
| `motif_id` | `int` |    N     | `0`     | motif identifier    | Motif identifier        | `fum_rt/core/proprioception/events.py:114,119`      |

**Producers/Consumers:** Produced by motif detection; consumed by EventDrivenMetrics  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** Emitted when walker enters/exits a detected motif  
**Invariants/Validation rules:** Immutable (frozen); `motif_id >= 0`  
**Notes:** Used for tracking motif traversal patterns

---

#### ADCEvent  <a id="schema-adcevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:122-134` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class ADCEvent(BaseEvent):
    """
    ADC estimator readout event (fold metrics in place of reading raw structures).
    Suggested fields (all optional, numeric):
      - adc_territories
      - adc_boundaries
      - adc_cycle_hits
    """
    adc_territories: Optional[int] = None
    adc_boundaries: Optional[int] = None
    adc_cycle_hits: Optional[float] = None
```

**Fields (expand from source; do not invent):**

| Field             | Type             | Required | Default | Units/Normalization | Description (lifted)           | Source                                         |
| ----------------- | ---------------- | :------: | ------- | ------------------- | ------------------------------ | ---------------------------------------------- |
| `adc_territories` | `Optional[int]`  |    N     | `None`  | count               | Number of ADC territories      | `fum_rt/core/proprioception/events.py:131`     |
| `adc_boundaries`  | `Optional[int]`  |    N     | `None`  | count               | Number of ADC boundaries       | `fum_rt/core/proprioception/events.py:132`     |
| `adc_cycle_hits`  | `Optional[float]`|    N     | `None`  | count/rate          | ADC cycle hits metric          | `fum_rt/core/proprioception/events.py:133`     |

**Producers/Consumers:** Produced by Active Domain Cartography (ADC) estimator; consumed by telemetry  
**Related equations (anchors only):** TODO: missing anchor for ADC algorithm (see `Derivation/ALGORITHMS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** ADC readout snapshots  
**Invariants/Validation rules:** Immutable (frozen); all fields optional; if present, numeric values >= 0  
**Notes:** Fold metrics in place of reading raw structures

---

#### BiasHintEvent  <a id="schema-biashintevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/proprioception/events.py:137-149` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class BiasHintEvent(BaseEvent):
    """
    Hint to bias exploration or actuation to a region/tile for a short TTL.
    - region: free-form label (e.g., "unknown", "tile:3,4")
    - nodes: bounded set of indices to hint (tuple for immutability)
    - ttl:   time-to-live in ticks (downstream consumer-managed)
    Note: EventDrivenMetrics ignores this; it travels on the bus for optional consumers.
    """
    region: str = "unknown"
    nodes: Tuple[int, ...] = tuple()
    ttl: int = 2
```

**Fields (expand from source; do not invent):**

| Field    | Type              | Required | Default     | Units/Normalization | Description (lifted)                                  | Source                                         |
| -------- | ----------------- | :------: | ----------- | ------------------- | ----------------------------------------------------- | ---------------------------------------------- |
| `region` | `str`             |    N     | `"unknown"` | n/a                 | Free-form label (e.g., "unknown", "tile:3,4")         | `fum_rt/core/proprioception/events.py:146`     |
| `nodes`  | `Tuple[int, ...]` |    N     | `tuple()`   | node IDs            | Bounded set of node indices to hint (immutable tuple) | `fum_rt/core/proprioception/events.py:147`     |
| `ttl`    | `int`             |    N     | `2`         | ticks               | Time-to-live in ticks (downstream consumer-managed)   | `fum_rt/core/proprioception/events.py:148`     |

**Producers/Consumers:** Produced by exploration heuristics; travels on bus for optional consumers (EventDrivenMetrics ignores)  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** Exploration bias hints  
**Invariants/Validation rules:** Immutable (frozen); `ttl > 0`  
**Notes:** Hint for biasing exploration/actuation; not folded by metrics

---

#### HorizonActivityEvent  <a id="schema-horizonactivityevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/cosmology/events.py:26-62` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class HorizonActivityEvent(BaseEvent):
    """Local horizon activity routed through the cosmology event bus."""

    kind: str = "horizon_activity"
    t: int = 0
    x: Tuple[float, ...] = field(default_factory=tuple)
    dotA: float = 0.0
    horizon_id: str = ""
    dt_ret: float = 0.0
```

**Fields (expand from source; do not invent):**

| Field        | Type               | Required | Default              | Units/Normalization | Description (lifted)                           | Source                                    |
| ------------ | ------------------ | :------: | -------------------- | ------------------- | ---------------------------------------------- | ----------------------------------------- |
| `kind`       | `str`              |    N     | `"horizon_activity"` | n/a                 | Event kind identifier                          | `fum_rt/core/cosmology/events.py:30`      |
| `t`          | `int`              |    N     | `0`                  | timestep            | Simulation tick                                | `fum_rt/core/cosmology/events.py:31`      |
| `x`          | `Tuple[float, ...]`|    N     | `tuple()`            | local coordinates   | Local coordinates (≤4 dimensions)              | `fum_rt/core/cosmology/events.py:32`      |
| `dotA`       | `float`            |    N     | `0.0`                | rate                | Observable production rate $\dot{A}$           | `fum_rt/core/cosmology/events.py:33`      |
| `horizon_id` | `str`              |    N     | `""`                 | n/a                 | Non-empty horizon identifier                   | `fum_rt/core/cosmology/events.py:34`      |
| `dt_ret`     | `float`            |    N     | `0.0`                | time units          | Strictly retarded window duration              | `fum_rt/core/cosmology/events.py:35`      |

**Producers/Consumers:** Produced by horizon activity detection; routed through cosmology event bus  
**Related equations (anchors only):** TODO: missing anchor for retarded kernel and horizon activity (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for $\dot{A}$ (see `Derivation/SYMBOLS.md`)  
**Examples (if present):** Cosmology router events  
**Invariants/Validation rules:** Immutable (frozen); `t >= 0`; `x` must contain 1-4 finite coordinates; `dt_ret > 0`; `dotA != 0`; `horizon_id` non-empty  
**Notes:** Post-init validation ensures all constraints; used in cosmology router feature

---

#### RouterSplitEvent  <a id="schema-routersplitevent"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/cosmology/events.py:64-94` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class RouterSplitEvent(BaseEvent):
    """Budget split instruction for the cosmology router channels."""

    kind: str = "router_split"
    energy_budget: float = 0.0
    f_vac: float = 0.0
    f_grain: float = 0.0
    f_gw: float = 0.0
```

**Fields (expand from source; do not invent):**

| Field           | Type    | Required | Default          | Units/Normalization | Description (lifted)                  | Source                                    |
| --------------- | ------- | :------: | ---------------- | ------------------- | ------------------------------------- | ----------------------------------------- |
| `kind`          | `str`   |    N     | `"router_split"` | n/a                 | Event kind identifier                 | `fum_rt/core/cosmology/events.py:68`      |
| `energy_budget` | `float` |    N     | `0.0`            | energy units        | Total energy budget                   | `fum_rt/core/cosmology/events.py:69`      |
| `f_vac`         | `float` |    N     | `0.0`            | fraction $[0,1]$    | Fraction for vacuum channel           | `fum_rt/core/cosmology/events.py:70`      |
| `f_grain`       | `float` |    N     | `0.0`            | fraction $[0,1]$    | Fraction for grain channel            | `fum_rt/core/cosmology/events.py:71`      |
| `f_gw`          | `float` |    N     | `0.0`            | fraction $[0,1]$    | Fraction for gravitational wave channel | `fum_rt/core/cosmology/events.py:72`    |

**Producers/Consumers:** Produced by cosmology router; consumed by energy partition subsystem  
**Related equations (anchors only):** TODO: missing anchor for energy routing (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** n/a  
**Examples (if present):** Router budget split instructions  
**Invariants/Validation rules:** Immutable (frozen); `energy_budget >= 0`; `f_vac, f_grain, f_gw in [0,1]`; `f_vac + f_grain + f_gw = 1.0` (within 1e-9 tolerance)  
**Notes:** Post-init validation ensures fraction sum equals 1; property accessor `fractions` returns tuple

---

#### BudgetTick  <a id="schema-budgettick"></a>

**Kind:** event  
**Versioning (if present):** none  
**Defined at:** `fum_rt/core/cosmology/events.py:96-127` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass(frozen=True)
class BudgetTick(BaseEvent):
    """Tick-scoped budget guard used to bound router processing."""

    kind: str = "budget_tick"
    tick: int = 0
    max_ops: int = 0
    max_emits: int = 0
    ttl: int = 1
```

**Fields (expand from source; do not invent):**

| Field       | Type  | Required | Default         | Units/Normalization | Description (lifted)              | Source                                    |
| ----------- | ----- | :------: | --------------- | ------------------- | --------------------------------- | ----------------------------------------- |
| `kind`      | `str` |    N     | `"budget_tick"` | n/a                 | Event kind identifier             | `fum_rt/core/cosmology/events.py:100`     |
| `tick`      | `int` |    N     | `0`             | timestep            | Current tick                      | `fum_rt/core/cosmology/events.py:101`     |
| `max_ops`   | `int` |    N     | `0`             | count               | Maximum operations allowed        | `fum_rt/core/cosmology/events.py:102`     |
| `max_emits` | `int` |    N     | `0`             | count               | Maximum emissions allowed         | `fum_rt/core/cosmology/events.py:103`     |
| `ttl`       | `int` |    N     | `1`             | ticks               | Time-to-live (must be >= 1)       | `fum_rt/core/cosmology/events.py:104`     |

**Producers/Consumers:** Produced by budget system; guard method raises `BudgetExceededError` when limits exceeded  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** Router processing budget guards  
**Invariants/Validation rules:** Immutable (frozen); `tick >= 0`; `max_ops, max_emits >= 0`; `ttl >= 1`  
**Notes:** Post-init validation; `guard(ops_used, emits_used, elapsed_ticks)` method raises `BudgetExceededError` when any budget exhausted

---

## Diagnostics & Logs

#### QFUM Metrics JSON Output  <a id="schema-qfum-metrics-json"></a>

**Kind:** file  
**Versioning (if present):** version field = "1.0"  
**Defined at:** `Derivation/code/outputs/logs/conservation_law/*_qfum_metrics.json` • `6b63a5e`

**Definition (verbatim snippet from source):**

```json
{
  "version": "1.0",
  "timestamp_utc": "20250826T142459Z",
  "params": {
    "r": 0.15,
    "u": 0.25,
    "T": 10.0,
    "solver": "rk4",
    "W0_list": [0.12],
    "dt_list": [0.002, 0.001, 0.0005]
  },
  "runs": [
    {
      "r": 0.15,
      "u": 0.25,
      "solver": "rk4",
      "dt": 0.002,
      "T": 10.0,
      "W0": 0.12,
      "delta_Q_max": 1.5e-13,
      "W_min": 0.12,
      "W_max": 0.36
    }
  ],
  "convergence": {
    "r": 0.15,
    "u": 0.25,
    "solver": "rk4",
    "dts": [0.002, 0.001, 0.0005],
    "delta_Q_max_list": [1.5e-13, 8.4e-15, 3.1e-15],
    "slope": 3.95,
    "intercept": -11.2,
    "r2": 0.998
  },
  "acceptance": {
    "drift_ok": true,
    "drift_gate": 1e-08,
    "convergence_ok": true,
    "convergence_expected_order": 4,
    "convergence_r2_min": 0.98,
    "order_tol": 0.4,
    "passed": true
  }
}
```

**Fields (expand from source; do not invent):**

| Field                                    | Type          | Required | Default | Units/Normalization | Description (lifted)                              | Source                                              |
| ---------------------------------------- | ------------- | :------: | ------- | ------------------- | ------------------------------------------------- | --------------------------------------------------- |
| `version`                                | `str`         |    Y     | n/a     | n/a                 | Schema version                                    | `Derivation/code/outputs/logs/conservation_law/*.json:2` |
| `timestamp_utc`                          | `str`         |    Y     | n/a     | ISO 8601            | UTC timestamp of run                              | `Derivation/code/outputs/logs/conservation_law/*.json:3` |
| `params.r`                               | `float`       |    Y     | n/a     | rate                | Logistic growth rate                              | `Derivation/code/outputs/logs/conservation_law/*.json:5` |
| `params.u`                               | `float`       |    Y     | n/a     | rate                | Logistic carrying capacity coefficient            | `Derivation/code/outputs/logs/conservation_law/*.json:6` |
| `params.T`                               | `float`       |    Y     | n/a     | time units          | Total integration time                            | `Derivation/code/outputs/logs/conservation_law/*.json:7` |
| `params.solver`                          | `str`         |    Y     | n/a     | n/a                 | ODE solver name                                   | `Derivation/code/outputs/logs/conservation_law/*.json:8` |
| `params.W0_list`                         | `List[float]` |    Y     | n/a     | state variable      | List of initial conditions tested                 | `Derivation/code/outputs/logs/conservation_law/*.json:9` |
| `params.dt_list`                         | `List[float]` |    Y     | n/a     | time units          | List of time steps tested                         | `Derivation/code/outputs/logs/conservation_law/*.json:10` |
| `runs`                                   | `List[object]`|    Y     | n/a     | n/a                 | Array of RunMetrics objects (see schema-runmetrics) | `Derivation/code/outputs/logs/conservation_law/*.json:12` |
| `convergence`                            | `object`      |    Y     | n/a     | n/a                 | ConvergenceMetrics object (see schema-convergencemetrics) | `Derivation/code/outputs/logs/conservation_law/*.json:24` |
| `acceptance.drift_ok`                    | `bool`        |    Y     | n/a     | n/a                 | Whether drift test passed                         | `Derivation/code/outputs/logs/conservation_law/*.json:34` |
| `acceptance.drift_gate`                  | `float`       |    Y     | n/a     | threshold           | Drift acceptance threshold                        | `Derivation/code/outputs/logs/conservation_law/*.json:35` |
| `acceptance.convergence_ok`              | `bool`        |    Y     | n/a     | n/a                 | Whether convergence test passed                   | `Derivation/code/outputs/logs/conservation_law/*.json:36` |
| `acceptance.convergence_expected_order`  | `int`         |    Y     | n/a     | order               | Expected convergence order                        | `Derivation/code/outputs/logs/conservation_law/*.json:37` |
| `acceptance.convergence_r2_min`          | `float`       |    Y     | n/a     | threshold           | Minimum $R^2$ for convergence fit                 | `Derivation/code/outputs/logs/conservation_law/*.json:38` |
| `acceptance.order_tol`                   | `float`       |    Y     | n/a     | tolerance           | Tolerance for order match                         | `Derivation/code/outputs/logs/conservation_law/*.json:39` |
| `acceptance.passed`                      | `bool`        |    Y     | n/a     | n/a                 | Overall acceptance gate                           | `Derivation/code/outputs/logs/conservation_law/*.json:40` |

**Producers/Consumers:** Produced by `Derivation/code/physics/conservation_law/qfum_validate.py`; consumed by validation gates  
**Related equations (anchors only):** TODO: missing anchor for Q_FUM invariant (see `Derivation/EQUATIONS.md`)  
**Related symbols/constants:** TODO: missing anchor for drift_gate, order thresholds (see `Derivation/CONSTANTS.md`)  
**Examples (if present):** `Derivation/code/outputs/logs/conservation_law/20250826_110546_qfum_metrics.json`  
**Invariants/Validation rules:** version must be "1.0"; all numeric params > 0; acceptance.passed is conjunction of sub-gates  
**Notes:** arXiv-ready validation metrics for Q_FUM conservation law

---

#### Tube Spectrum Summary (tachyonic_condensation)  <a id="schema-tube-spectrum-summary"></a>

**Kind:** file (JSON summary)  
**Versioning (if present):** metrics_version = "v2-phys-aware"  
**Defined at:** `Derivation/code/physics/tachyonic_condensation/schemas/tube-spectrum-summary-v1.schema.json` • 09f871a

**Definition (verbatim snippet from source):**

```json
{
  "tag": "tube-spectrum-v1",
  "metrics_version": "v2-phys-aware",
  "coverage_phys": 1.0,
  "coverage_raw": 0.5481,
  "attempts": 74,
  "attempts_phys": 74,
  "attempts_raw": 135,
  "successes": 74,
  "csv": "/.../tube_spectrum_roots__tube-spectrum-v1.csv",
  "figure": "/.../tube_spectrum_overview__tube-spectrum-v1.png",
  "heatmap": "/.../tube_spectrum_heatmap__tube-spectrum-v1.png",
  "max_residual": 0.709,
  "passed": true
}
```

**Fields (expand from source; do not invent):**

| Field             | Type      | Required | Default | Units/Normalization | Description                                                   | Source |
| ----------------- | --------- | :------: | ------- | ------------------- | -------------------------------------------------------------- | ------ |
| `tag`             | `string`  |    Y     | n/a     | n/a                 | Tag identifier                                                 | schema |
| `metrics_version` | `string`  |    Y     | n/a     | n/a                 | Version of KPI computation                                     | schema |
| `coverage`        | `number`  |    N     | alias   | fraction [0,1]      | Alias of `coverage_phys` (back-compat)                         | schema |
| `coverage_phys`   | `number`  |    Y     | n/a     | fraction [0,1]      | Primary KPI: successes/attempts over physically admissible set | schema |
| `coverage_raw`    | `number`  |    Y     | n/a     | fraction [0,1]      | Transparency KPI: successes over total R×ell pairs             | schema |
| `attempts`        | `integer` |    Y     | n/a     | count               | Physically admissible attempts                                 | schema |
| `attempts_phys`   | `integer` |    Y     | n/a     | count               | Equals `attempts`                                              | schema |
| `attempts_raw`    | `integer` |    Y     | n/a     | count               | Total R×ell pairs                                              | schema |
| `successes`       | `integer` |    Y     | n/a     | count               | Number of roots found (lowest per ell per R)                   | schema |
| `csv`             | `string`  |    Y     | n/a     | path                | Absolute path to roots CSV                                     | schema |
| `figure`          | `string|null` | N    | n/a     | path                | Absolute path to overview PNG (optional)                        | schema |
| `heatmap`         | `string|null` | N    | n/a     | path                | Absolute path to diagnostic heatmap PNG (optional)             | schema |
| `max_residual`    | `number|null` | N    | n/a     | residual units      | Max absolute secular residual (informational v1)               | schema |
| `passed`          | `boolean` |    Y     | n/a     | n/a                 | Overall acceptance: `coverage_phys >= 0.95`                    | schema |

**Producers/Consumers:** Produced by `run_tachyon_tube.py --mode spectrum`; consumed by RESULTS and gates.  
**Related equations (anchors only):** see `EQUATIONS.md#vdm-e-095` (tube secular), `VALIDATION_METRICS.md#kpi-tube-cov-phys`.  
**Related symbols/constants:** see `SYMBOLS.md` entries for $\kappa, \ell, R$.  
**Examples (if present):** `Derivation/code/outputs/logs/tachyonic_condensation/*_tube_spectrum_summary__tube-spectrum-v1.json`  
**Invariants/Validation rules:** `0 <= coverage_phys, coverage_raw <= 1`; `attempts_raw = |R_sweep| (ell_max+1)`; `coverage = coverage_phys`.

---

#### Tube Condensation Summary (tachyonic_condensation)  <a id="schema-tube-condensation-summary"></a>

**Kind:** file (JSON summary)  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/tachyonic_condensation/schemas/tube-condensation-summary-v1.schema.json` • 09f871a

**Definition (verbatim snippet from source):**

```json
{
  "tag": "tube-condensation-v1",
  "finite_fraction": 1.0,
  "min_R": 1.35,
  "min_E": 11.98996,
  "curvature_ok": true,
  "fit_coeffs": [1.8109, -4.9177, 15.3284],
  "csv": "/.../tube_energy_scan__tube-condensation-v1.csv",
  "figure": "/.../tube_energy_scan__tube-condensation-v1.png",
  "passed": true
}
```

**Fields (expand from source; do not invent):**

| Field             | Type             | Required | Default | Units/Normalization | Description                                         | Source |
| ----------------- | ---------------- | :------: | ------- | ------------------- | -------------------------------------------------- | ------ |
| `tag`             | `string`         |    Y     | n/a     | n/a                 | Tag identifier                                     | schema |
| `finite_fraction` | `number`         |    Y     | n/a     | fraction [0,1]      | Fraction of finite E(R) values over scan grid      | schema |
| `min_R`           | `number|null`    |    Y     | n/a     | radius units        | Radius at minimum energy (if finite)               | schema |
| `min_E`           | `number|null`    |    Y     | n/a     | energy units        | Minimum energy value (if finite)                   | schema |
| `curvature_ok`    | `boolean`        |    Y     | n/a     | n/a                 | True if local convexity near minimum is verified   | schema |
| `fit_coeffs`      | `array|null`     |    N     | n/a     | coefficients        | [a, b, c] quadratic fit near minimum (if computed) | schema |
| `csv`             | `string`         |    Y     | n/a     | path                | Absolute path to energy scan CSV                   | schema |
| `figure`          | `string`         |    Y     | n/a     | path                | Absolute path to energy scan PNG                   | schema |
| `passed`          | `boolean`        |    Y     | n/a     | n/a                 | Overall acceptance gate                            | schema |

**Producers/Consumers:** Produced by `run_tachyon_tube.py --mode condensation`; consumed by RESULTS and gates.  
**Related equations (anchors only):** see `EQUATIONS.md#vdm-e-097` (quadratic fit).  
**Related symbols/constants:** `SYMBOLS.md` entries for $E(R)$.  
**Examples (if present):** `Derivation/code/outputs/logs/tachyonic_condensation/*_tube_condensation_summary__tube-condensation-v1.json`  
**Invariants/Validation rules:** `finite_fraction in [0,1]`; `passed = (finite_fraction >= 0.80) and curvature_ok`.

---

#### KG Energy Oscillation Summary (metriplectic)  <a id="schema-kg-energy-osc"></a>

**Kind:** file (JSON summary)  
**Versioning (if present):** tag = "KG-energy-osc-v1"  
**Defined at:** `Derivation/code/physics/metriplectic/schemas/KG-energy-osc-v1.schema.json`

**Definition (verbatim snippet from source):**

```json
{
  "tag": "KG-energy-osc-v1",
  "dt_list": [1.0e-2, 5.0e-3, 2.5e-3],
  "AH": [ ... ],
  "rel_AH": [ ... ],
  "fit": { "p": 1.9999, "R2": 0.999999 },
  "e_rev": 2.9e-16,
  "checkpoints": [100, 200, 300],
  "hashes": ["sha256:...", "sha256:...", "sha256:..."],
  "env_audit": { "threads": 1, "fft_determinism": true },
  "figure": "/.../kg_energy_osc_scaling__KG-energy-osc-v1.png",
  "csv": "/.../kg_energy_osc_scaling__KG-energy-osc-v1.csv",
  "gate": { "notes": "Acceptance gates per VALIDATION_METRICS (KG)" },
  "passed": true
}
```

**Fields (expand from source; do not invent):**

| Field           | Type              | Required | Default | Units/Normalization | Description                                                  | Source                                                                 |
| ----------------| ----------------- | :------: | ------- | ------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------- |
| `tag`           | `string`          |    Y     | n/a     | n/a                 | Tag identifier (must equal `"KG-energy-osc-v1"`)             | `Derivation/code/physics/metriplectic/schemas/KG-energy-osc-v1.schema.json` |
| `grid`          | `object`          |    N     | n/a     | n/a                 | Grid specification (shape, spacing, BCs)                     | schema                                                                  |
| `params`        | `object`          |    N     | n/a     | n/a                 | Physical/numerical parameters used                           | schema                                                                  |
| `dt_list`       | `array<number>`   |    Y     | n/a     | time step           | Time step ladder used for scaling study (values ≥ 0)         | schema                                                                  |
| `AH`            | `array<number>`   |    Y     | n/a     | energy units        | Median energy oscillation amplitude per `dt` (half peak–peak) | schema                                                                  |
| `rel_AH`        | `array<number>`   |    N     | n/a     | normalized          | Median relative amplitude per `dt` (`AH / mean(H)`)          | schema                                                                  |
| `fit.p`         | `number`          |    Y     | n/a     | log–log slope       | Fitted scaling exponent for `AH ~ dt^p`                       | schema                                                                  |
| `fit.R2`        | `number`          |    Y     | n/a     | [0,1]               | Coefficient of determination for the log–log fit             | schema                                                                  |
| `e_rev`         | `number`          |    Y     | n/a     | sup-norm error      | Max time-reversal error across seeds (≥ 0)                   | schema                                                                  |
| `checkpoints`   | `array<integer>`  |    N     | n/a     | step index          | Step indices for checkpoint hashing                          | schema                                                                  |
| `hashes`        | `array<string>`   |    N     | n/a     | SHA-256             | Hashes of raw buffers at checkpoints                         | schema                                                                  |
| `env_audit`     | `object`          |    N     | n/a     | n/a                 | Environment audit (threads, deterministic kernels, etc.)     | schema                                                                  |
| `figure`        | `string`          |    N     | n/a     | path                | Absolute path to scaling plot PNG                            | schema                                                                  |
| `csv`           | `string`          |    N     | n/a     | path                | Absolute path to scaling CSV                                 | schema                                                                  |
| `gate`          | `object`          |    N     | n/a     | n/a                 | Gate parameters snapshot (for transparency)                  | schema                                                                  |
| `passed`        | `boolean`         |    Y     | n/a     | n/a                 | Overall acceptance flag (per VALIDATION_METRICS KG gates)    | schema                                                                  |

**Producers/Consumers:** Produced by `Derivation/code/physics/metriplectic/run_kg_energy_oscillation.py`; consumed by RESULTS and canon gates.  
**Related equations (anchors only):** see `VALIDATION_METRICS.md` (KG energy-osc KPIs).  
**Related symbols/constants:** see `SYMBOLS.md`/`CONSTANTS.md` entries for Klein–Gordon normalization and step-size scaling.  
**Examples (if present):** `Derivation/code/outputs/logs/metriplectic/*_KG-energy-osc-v1.json`  
**Invariants/Validation rules:** `len(dt_list) == len(AH)`; `0 ≤ fit.R2 ≤ 1`; `e_rev ≥ 0`; `passed` reflects conjunction of KG gates defined in canon.  
**Notes:** Validates two conservative-limb invariants: (i) energy oscillation amplitude scaling with log–log slope near 2 for Störmer–Verlet; (ii) strict time-reversal symmetry. Includes determinism receipts via checkpoint buffer hashes and environment audit.

---

## External Interfaces

#### PYTHON_PACKAGE_SCHEMA (TypeScript)  <a id="schema-python-package-schema"></a>

**Kind:** API  
**Versioning (if present):** none  
**Defined at:** `tools/python_utilities_generator/services/geminiService.ts:12-35` • `6b63a5e`

**Definition (verbatim snippet from source):**

```typescript
const PYTHON_PACKAGE_SCHEMA = {
  type: Type.OBJECT,
  properties: {
    files: {
      type: Type.ARRAY,
      description: "An array of generated files for the Python package.",
      items: {
        type: Type.OBJECT,
        properties: {
          fileName: {
            type: Type.STRING,
            description: "The name of the file, e.g., 'main.py', 'README.md', 'config.json'."
          },
          fileContent: {
            type: Type.STRING,
            description: "The complete, raw content of the file."
          }
        },
        required: ["fileName", "fileContent"]
      }
    }
  },
  required: ["files"]
};
```

**Fields (expand from source; do not invent):**

| Field                      | Type     | Required | Default | Units/Normalization | Description (lifted)                              | Source                                                        |
| -------------------------- | -------- | :------: | ------- | ------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| `files`                    | `Array`  |    Y     | n/a     | n/a                 | Array of generated files for the Python package   | `tools/python_utilities_generator/services/geminiService.ts:14` |
| `files[].fileName`         | `string` |    Y     | n/a     | n/a                 | File name (e.g., 'main.py', 'README.md')          | `tools/python_utilities_generator/services/geminiService.ts:21` |
| `files[].fileContent`      | `string` |    Y     | n/a     | n/a                 | Complete, raw content of the file                 | `tools/python_utilities_generator/services/geminiService.ts:25` |

**Producers/Consumers:** Produced by Gemini AI code generation service; consumed by Python utilities generator  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** Used in `tools/python_utilities_generator/services/geminiService.ts:generatePythonPackage`  
**Invariants/Validation rules:** TypeScript Type.OBJECT validation; `files` array required; each item must have `fileName` and `fileContent`  
**Notes:** TypeScript schema for Gemini API response; JSON schema for AI-generated Python packages

---

#### SayRecord  <a id="schema-sayrecord"></a>

**Kind:** record  
**Versioning (if present):** none  
**Defined at:** `tools/extract_say_texts.py:31-39` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
@dataclass
class SayRecord:
    source_path: str
    line_no: int
    text: str
    t: Optional[float] = None
    phase: Optional[int] = None
    score: Optional[float] = None
    why: Optional[Dict] = None
```

**Fields (expand from source; do not invent):**

| Field         | Type             | Required | Default | Units/Normalization | Description (lifted)                   | Source                            |
| ------------- | ---------------- | :------: | ------- | ------------------- | -------------------------------------- | --------------------------------- |
| `source_path` | `str`            |    Y     | n/a     | n/a                 | Source file path                       | `tools/extract_say_texts.py:33`   |
| `line_no`     | `int`            |    Y     | n/a     | line number         | Line number in source                  | `tools/extract_say_texts.py:34`   |
| `text`        | `str`            |    Y     | n/a     | n/a                 | Extracted 'say' text                   | `tools/extract_say_texts.py:35`   |
| `t`           | `Optional[float]`|    N     | `None`  | time/tick           | Optional timestamp                     | `tools/extract_say_texts.py:36`   |
| `phase`       | `Optional[int]`  |    N     | `None`  | phase ID            | Optional phase identifier              | `tools/extract_say_texts.py:37`   |
| `score`       | `Optional[float]`|    N     | `None`  | normalized          | Optional score metric                  | `tools/extract_say_texts.py:38`   |
| `why`         | `Optional[Dict]` |    N     | `None`  | n/a                 | Optional metadata dictionary           | `tools/extract_say_texts.py:39`   |

**Producers/Consumers:** Produced by `tools/extract_say_texts.py` from JSONL logs; exported to CSV/JSONL/text  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** Extracted from JSONL logs with `{"type":"macro","macro":"say","args":{"text":"..."}}`  
**Invariants/Validation rules:** `line_no > 0`; `source_path` non-empty  
**Notes:** Streams JSONL logs to extract 'say' macro events for analysis

---

#### GeometryProbeAdapter (Protocol)  <a id="schema-geometryprobeadapter"></a>

**Kind:** other (Protocol/Interface)  
**Versioning (if present):** none  
**Defined at:** `tools/geom_bundle_builder.py:96-106` • `6b63a5e`

**Definition (verbatim snippet from source):**

```python
class GeometryProbeAdapter(Protocol):
    """Adapter contract for model-specific activation capture."""

    def prepare(self, config: "GeometryRunConfig") -> None:
        """Perform any one-time setup before checkpoints are processed."""

    def load_checkpoint(self, step: int) -> None:
        """Load the checkpoint corresponding to ``step``."""

    def encode_concepts(self, concepts: Sequence[str], layer_name: str) -> np.ndarray:
        """Return a matrix with shape ``(len(concepts), neurons)`` for ``layer_name``."""
```

**Fields (expand from source; do not invent):**

| Method            | Signature                                                      | Required | Description (lifted)                                      | Source                              |
| ----------------- | -------------------------------------------------------------- | :------: | --------------------------------------------------------- | ----------------------------------- |
| `prepare`         | `(self, config: GeometryRunConfig) -> None`                   |    Y     | One-time setup before checkpoints are processed           | `tools/geom_bundle_builder.py:99`   |
| `load_checkpoint` | `(self, step: int) -> None`                                    |    Y     | Load checkpoint corresponding to step                     | `tools/geom_bundle_builder.py:102`  |
| `encode_concepts` | `(self, concepts: Sequence[str], layer_name: str) -> np.ndarray` | Y     | Return activation matrix (concepts × neurons) for layer   | `tools/geom_bundle_builder.py:105`  |

**Producers/Consumers:** Implemented by model-specific adapters; consumed by `tools/geom_bundle_builder.py` workflow  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** Adapter instances loaded via `module:ClassName` format  
**Invariants/Validation rules:** `encode_concepts` must return numpy array with shape `(len(concepts), neurons)`  
**Notes:** Python Protocol defining adapter contract for model-specific activation capture

---

#### KG-Lite Chunk Envelope v1  <a id="schema-kg-lite-chunkenvelope-v1"></a>

**Kind:** file
**Versioning (if present):** `set_version` field
**Defined at:** `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:1-203`

**Definition (verbatim snippet from source):**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "kg-lite.chunkenvelope.v1.schema.json",
  "title": "KG-Lite Chunk Envelope v1",
  "$comment": "Deterministic envelope for KG-Lite branches. Enforce gates in code: (1) content_sha256 equals SHA-256 of canonical JSON of payload; (2) chunk_id == `${set_id}@${set_version}:${chunk_type}`; (3) sharding via part/total_parts.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "set_id",
    "set_version",
    "chunk_type",
    "chunk_id",
    "updated",
    "source",
    "content_sha256",
    "part",
    "total_parts",
    "payload"
  ],
  "properties": {
    "set_id": { "type": "string", "maxLength": 120 },
    "set_version": { "type": "string" },
    "chunk_type": {
      "type": "string",
      "enum": ["index","meta","axes_dimensions","subfactors","signals","edges","retrieval_policy"]
    }
}
```

**Fields (expand from source; do not invent):**

| Field            | Type        | Required | Default | Units/Normalization | Description (lifted) | Source |
| ---------------- | ----------- | :------: | ------- | ------------------- | -------------------- | ------ |
| `set_id`         | `string`    |    Y     | n/a     | n/a                 |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:21` |
| `set_version`    | `string`    |    Y     | n/a     | n/a                 |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:22` |
| `chunk_type`     | `string`    |    Y     | n/a     | enum                |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:23` |
| `chunk_id`       | `string`    |    Y     | n/a     | pattern             |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:27` |
| `scope`          | `string`    |    N     | n/a     | n/a                 |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:31` |
| `updated`        | `string`    |    Y     | n/a     | date-time           |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:32` |
| `source`         | `string`    |    Y     | n/a     | n/a                 |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:33` |
| `content_sha256` | `string`    |    Y     | n/a     | sha256 hex          |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:34` |
| `part`           | `integer`   |    Y     | n/a     | ≥1                  |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:35` |
| `total_parts`    | `integer`   |    Y     | n/a     | ≥1                  |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:36` |
| `tags`           | `string[]`  |    N     | n/a     | n/a                 |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:37` |
| `payload`        | `object`    |    Y     | n/a     | n/a                 |                      | `memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json:38` |

---

#### Metriplectic Assisted Echo Spec (v1)  <a id="schema-echo-spec-v1"></a>

**Kind:** config
**Versioning (if present):** none
**Defined at:** `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:1-36` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$id": "echo_spec-v1.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Metriplectic Assisted Echo Spec (v1)",
  "type": "object",
  "metadata": { "tag": "echo_spec-v1" },
  "required": ["grid", "params", "dt", "steps", "seeds", "lambdas", "budget"],
  "properties": {
    "tag": {"type": ["string", "null"]},
    "grid": {
      "type": "object",
      "required": ["N", "dx"],
      "properties": {
        "N": {"type": "integer", "minimum": 8},
        "dx": {"type": "number", "exclusiveMinimum": 0}
      }
    },
    "params": {
      "type": "object",
      "required": ["c", "m", "D", "m_lap_operator"],
      "properties": {
        "c": {"type": "number"},
        "m": {"type": "number"},
        "D": {"type": "number"},
        "m_lap_operator": {"type": "string", "enum": ["spectral", "stencil"]}
      },
      "additionalProperties": true
    },
    "dt": {"type": "number", "exclusiveMinimum": 0},
    "steps": {"type": "integer", "minimum": 1},
    "seeds": {"type": "array", "items": {"type": "integer"}, "minItems": 1},
    "lambdas": {"type": "array", "items": {"type": "number", "minimum": 0}, "minItems": 1},
    "budget": {"type": "number", "minimum": 0}
  },
  "additionalProperties": false
}
```

**Fields (expand from source; do not invent):**

| Field                 | Type              | Required | Default | Units/Normalization | Description (lifted) | Source                                                             |
| --------------------- | ----------------- | :------: | ------- | ------------------- | -------------------- | ------------------------------------------------------------------ |
| `tag`                 | `string|null`     |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:9`  |
| `grid`                | `object`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:10-17` |
| `grid.N`              | `integer (≥8)`    |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:14` |
| `grid.dx`             | `number (>0)`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:15` |
| `params`              | `object`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:18-28` |
| `params.c`            | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:22` |
| `params.m`            | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:23` |
| `params.D`            | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:24` |
| `params.m_lap_operator` | `string (enum)` |    Y     | n/a     | n/a                 | enum: `spectral` \| `stencil` | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:25` |
| `dt`                  | `number (>0)`     |    Y     | n/a     | time step           |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:29` |
| `steps`               | `integer (≥1)`    |    Y     | n/a     | count               |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:30` |
| `seeds`               | `integer[]`       |    Y     | n/a     | n/a                 | `minItems: 1`        | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:31` |
| `lambdas`             | `number[]`        |    Y     | n/a     | n/a                 | `minItems: 1`, elements `≥0` | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:32` |
| `budget`              | `number (≥0)`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json:33` |

**Producers/Consumers:** n/a
**Related equations (anchors only):** n/a
**Related symbols/constants:** n/a
**Examples (if present):** n/a
**Invariants/Validation rules:** `N ≥ 8`; `dx > 0`; `dt > 0`; `steps ≥ 1`; `lambdas[i] ≥ 0`; `budget ≥ 0`; `seeds` non-empty.

---

#### Metriplectic Assisted Echo Spec (v1b)  <a id="schema-echo-spec-v1b"></a>

**Kind:** config
**Versioning (if present):** none
**Defined at:** `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:1-36` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$id": "echo_spec-v1b.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Metriplectic Assisted Echo Spec (v1b)",
  "type": "object",
  "metadata": { "tag": "echo_spec-v1b" },
  "required": ["grid", "params", "dt", "steps", "seeds", "lambdas", "budget"],
  "properties": {
    "tag": {"type": ["string", "null"]},
    "grid": {
      "type": "object",
      "required": ["N", "dx"],
      "properties": {
        "N": {"type": "integer", "minimum": 8},
        "dx": {"type": "number", "exclusiveMinimum": 0}
      }
    },
    "params": {
      "type": "object",
      "required": ["c", "m", "D", "m_lap_operator"],
      "properties": {
        "c": {"type": "number"},
        "m": {"type": "number"},
        "D": {"type": "number"},
        "m_lap_operator": {"type": "string", "enum": ["spectral", "stencil"]}
      },
      "additionalProperties": true
    },
    "dt": {"type": "number", "exclusiveMinimum": 0},
    "steps": {"type": "integer", "minimum": 1},
    "seeds": {"type": "array", "items": {"type": "integer"}, "minItems": 1},
    "lambdas": {"type": "array", "items": {"type": "number", "minimum": 0}, "minItems": 1},
    "budget": {"type": "number", "minimum": 0}
  },
  "additionalProperties": false
}
```

**Fields (expand from source; do not invent):**

| Field                       | Type              | Required | Default | Units/Normalization | Description (lifted) | Source                                                                |
| --------------------------- | ----------------- | :------: | ------- | ------------------- | -------------------- | --------------------------------------------------------------------- |
| `tag`                       | `string|null`     |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:9`  |
| `grid`                      | `object`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:10-17` |
| `grid.N`                    | `integer (≥8)`    |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:14` |
| `grid.dx`                   | `number (>0)`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:15` |
| `params`                    | `object`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:18-28` |
| `params.c`                  | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:22` |
| `params.m`                  | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:23` |
| `params.D`                  | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:24` |
| `params.m_lap_operator`     | `string (enum)`   |    Y     | n/a     | n/a                 | enum: `spectral` \| `stencil` | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:25` |
| `dt`                        | `number (>0)`     |    Y     | n/a     | time step           |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:29` |
| `steps`                     | `integer (≥1)`    |    Y     | n/a     | count               |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:30` |
| `seeds`                     | `integer[]`       |    Y     | n/a     | n/a                 | `minItems: 1`        | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:31` |
| `lambdas`                   | `number[]`        |    Y     | n/a     | n/a                 | `minItems: 1`, elements `≥0` | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:32` |
| `budget`                    | `number (≥0)`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1b.schema.json:33` |

**Producers/Consumers:** n/a
**Related equations (anchors only):** n/a
**Related symbols/constants:** n/a
**Examples (if present):** n/a
**Invariants/Validation rules:** Same as v1.

---

#### Metriplectic Assisted Echo Spec (v1c)  <a id="schema-echo-spec-v1c"></a>

**Kind:** config
**Versioning (if present):** none
**Defined at:** `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:1-36` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$id": "echo_spec-v1c.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Metriplectic Assisted Echo Spec (v1c)",
  "type": "object",
  "metadata": { "tag": "echo_spec-v1c" },
  "required": ["grid", "params", "dt", "steps", "seeds", "lambdas", "budget"],
  "properties": {
    "tag": {"type": ["string", "null"]},
    "grid": {
      "type": "object",
      "required": ["N", "dx"],
      "properties": {
        "N": {"type": "integer", "minimum": 8},
        "dx": {"type": "number", "exclusiveMinimum": 0}
      }
    },
    "params": {
      "type": "object",
      "required": ["c", "m", "D", "m_lap_operator"],
      "properties": {
        "c": {"type": "number"},
        "m": {"type": "number"},
        "D": {"type": "number"},
        "m_lap_operator": {"type": "string", "enum": ["spectral", "stencil"]}
      },
      "additionalProperties": true
    },
    "dt": {"type": "number", "exclusiveMinimum": 0},
    "steps": {"type": "integer", "minimum": 1},
    "seeds": {"type": "array", "items": {"type": "integer"}, "minItems": 1},
    "lambdas": {"type": "array", "items": {"type": "number", "minimum": 0}, "minItems": 1},
    "budget": {"type": "number", "minimum": 0}
  },
  "additionalProperties": false
}
```

**Fields (expand from source; do not invent):**

| Field                       | Type              | Required | Default | Units/Normalization | Description (lifted) | Source                                                                |
| --------------------------- | ----------------- | :------: | ------- | ------------------- | -------------------- | --------------------------------------------------------------------- |
| `tag`                       | `string|null`     |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:9`  |
| `grid`                      | `object`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:10-17` |
| `grid.N`                    | `integer (≥8)`    |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:14` |
| `grid.dx`                   | `number (>0)`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:15` |
| `params`                    | `object`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:18-28` |
| `params.c`                  | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:22` |
| `params.m`                  | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:23` |
| `params.D`                  | `number`          |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:24` |
| `params.m_lap_operator`     | `string (enum)`   |    Y     | n/a     | n/a                 | enum: `spectral` \| `stencil` | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:25` |
| `dt`                        | `number (>0)`     |    Y     | n/a     | time step           |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:29` |
| `steps`                     | `integer (≥1)`    |    Y     | n/a     | count               |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:30` |
| `seeds`                     | `integer[]`       |    Y     | n/a     | n/a                 | `minItems: 1`        | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:31` |
| `lambdas`                   | `number[]`        |    Y     | n/a     | n/a                 | `minItems: 1`, elements `≥0` | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:32` |
| `budget`                    | `number (≥0)`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_spec-v1c.schema.json:33` |

**Producers/Consumers:** n/a
**Related equations (anchors only):** n/a
**Related symbols/constants:** n/a
**Examples (if present):** n/a
**Invariants/Validation rules:** Same as v1.

---

#### Assisted Echo Artifacts (v1)  <a id="schema-echo-artifacts-v1"></a>

**Kind:** file
**Versioning (if present):** none
**Defined at:** `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:1-30` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$id": "echo_artifacts-v1.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Assisted Echo Artifacts (v1)",
  "type": "object",
  "required": ["seeds", "lambdas", "ceg_summary", "per_seed"],
  "properties": {
    "seeds": {"type": "array", "items": {"type": "integer"}},
    "lambdas": {"type": "array", "items": {"type": "number"}},
    "grid": {"type": "object"},
    "params": {"type": "object"},
    "dt": {"type": "number"},
    "steps": {"type": "integer"},
    "per_seed": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["seed", "baseline_err", "assisted_err", "ceg"],
        "properties": {
          "seed": {"type": "integer"},
          "baseline_err": {"type": "number"},
          "assisted_err": {"type": "object"},
          "ceg": {"type": "object"}
        }
      }
    },
    "ceg_summary": {"type": "object"}
  },
  "additionalProperties": true
}
```

**Fields (expand from source; do not invent):**

| Field                         | Type           | Required | Default | Units/Normalization | Description (lifted) | Source                                                                       |
| ----------------------------- | -------------- | :------: | ------- | ------------------- | -------------------- | ---------------------------------------------------------------------------- |
| `seeds`                       | `integer[]`    |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:8`  |
| `lambdas`                     | `number[]`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:9`  |
| `grid`                        | `object`       |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:10` |
| `params`                      | `object`       |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:11` |
| `dt`                          | `number`       |    N     | n/a     | time step           |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:12` |
| `steps`                       | `integer`      |    N     | n/a     | count               |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:13` |
| `per_seed`                    | `object[]`     |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:14-26` |
| `per_seed[].seed`             | `integer`      |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:20` |
| `per_seed[].baseline_err`     | `number`       |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:21` |
| `per_seed[].assisted_err`     | `object`       |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:22` |
| `per_seed[].ceg`              | `object`       |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:23` |
| `ceg_summary`                 | `object`       |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/echo_artifacts-v1.schema.json:27` |

**Producers/Consumers:** n/a
**Related equations (anchors only):** n/a
**Related symbols/constants:** n/a
**Examples (if present):** n/a
**Invariants/Validation rules:** `per_seed[*]` objects must include `seed`, `baseline_err`, `assisted_err`, `ceg`.

---

#### assisted_echo prereg v1c schema  <a id="schema-assisted-echo-t4-prereg-v1c"></a>

**Kind:** config
**Versioning (if present):** none
**Defined at:** `Derivation/code/physics/metriplectic/schemas/assisted-echo-t4-prereg-v1c.schema.json:1-9` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:metriplectic:assisted-echo-t4-prereg-v1c",
  "title": "assisted_echo prereg v1c schema",
  "type": "object",
  "metadata": { "tag": "assisted-echo-t4-prereg-v1c" },
  "properties": {},
  "required": []
}
```

**Fields (expand from source; do not invent):**

| Field | Type | Required | Default | Units/Normalization | Description (lifted) | Source |
| ----- | ---- | :------: | ------- | ------------------- | -------------------- | ------ |
| —     | —    |    —     | —       | —                   | No fields (empty `properties` and `required`). | `Derivation/code/physics/metriplectic/schemas/assisted-echo-t4-prereg-v1c.schema.json:1-9` |

**Producers/Consumers:** n/a
**Related equations (anchors only):** n/a
**Related symbols/constants:** n/a
**Examples (if present):** n/a
**Invariants/Validation rules:** none specified.

---

#### KG Dispersion Run Log (metriplectic)  <a id="schema-kg-dispersion-v1"></a>

**Kind:** file  
**Versioning (if present):** `version` field  
**Defined at:** `Derivation/code/physics/metriplectic/schemas/KG-dispersion-v1.schema.json:1-14` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KG Dispersion Run Log",
  "version": "1.0.0",
  "type": "object",
  "tag": "KG-dispersion-v1",
  "properties": {
    "params": { "type": "object" },
    "fit": { "type": "object" },
    "gate": { "type": "object" },
    "policy": { "type": "object" }
  },
  "required": ["tag", "type"]
}
```

**Fields (expand from source; do not invent):**

| Field      | Type     | Required | Default | Units/Normalization | Description (lifted) | Source |
| ---------- | -------- | :------: | ------- | ------------------- | -------------------- | ------ |
| `params`   | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-dispersion-v1.schema.json:8` |
| `fit`      | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-dispersion-v1.schema.json:9` |
| `gate`     | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-dispersion-v1.schema.json:10` |
| `policy`   | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-dispersion-v1.schema.json:11` |

**Producers/Consumers:** n/a  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** n/a  
**Invariants/Validation rules:** `required` includes `"tag"` and `"type"`.

---

#### KG Noether Energy/Momentum Invariants Log (v1)  <a id="schema-kg-noether-v1"></a>

**Kind:** file  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:1-35` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KG Noether Energy/Momentum Invariants Log (v1)",
  "tag": "KG-noether-v1",
  "type": "object",
  "properties": {
    "tag": { "type": "string", "const": "KG-noether-v1" },
    "dt": { "type": "number", "minimum": 0 },
    "steps": { "type": "integer", "minimum": 1 },
    "N": { "type": "integer", "minimum": 1 },
    "max_per_step_delta": {
      "type": "object",
      "properties": {
        "E_disc": { "type": "number" },
        "P_disc": { "type": "number" }
      },
      "required": ["E_disc", "P_disc"]
    },
    "passed": {
      "type": "object",
      "properties": {
        "energy": { "type": "boolean" },
        "momentum": { "type": "boolean" },
        "reversibility": { "type": "boolean" }
      },
      "required": ["energy", "momentum", "reversibility"]
    },
    "csv": { "type": "string" },
    "figure": { "type": "string" },
    "grid": { "type": "object" },
    "params": { "type": "object" }
  },
  "required": ["dt", "steps", "N", "max_per_step_delta", "passed" ],
  "additionalProperties": true
}
```

**Fields (expand from source; do not invent):**

| Field                     | Type      | Required | Default | Units/Normalization | Description (lifted) | Source |
| ------------------------- | --------- | :------: | ------- | ------------------- | -------------------- | ------ |
| `tag`                     | `string`  |    N     | n/a     | const               | `"KG-noether-v1"`    | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:7` |
| `dt`                      | `number`  |    Y     | n/a     | ≥0                  |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:8` |
| `steps`                   | `integer` |    Y     | n/a     | ≥1                  |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:9` |
| `N`                       | `integer` |    Y     | n/a     | ≥1                  |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:10` |
| `max_per_step_delta`      | `object`  |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:11-18` |
| `max_per_step_delta.E_disc` | `number`|    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:14` |
| `max_per_step_delta.P_disc` | `number`|    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:15` |
| `passed.energy`           | `boolean` |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:22` |
| `passed.momentum`         | `boolean` |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:23` |
| `passed.reversibility`    | `boolean` |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:24` |
| `csv`                     | `string`  |    N     | n/a     | path                |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:28` |
| `figure`                  | `string`  |    N     | n/a     | path                |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:29` |
| `grid`                    | `object`  |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:30` |
| `params`                  | `object`  |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json:31` |

**Producers/Consumers:** n/a  
**Related equations (anchors only):** `../Derivation/VALIDATION_METRICS.md#` (Noether gates; link to exact anchors when present)  
**Related symbols/constants:** `../Derivation/SYMBOLS.md#` (E, P)  
**Examples (if present):** n/a  
**Invariants/Validation rules:** `dt ≥ 0`; `steps ≥ 1`; `N ≥ 1`; `max_per_step_delta` includes `E_disc` and `P_disc`; `passed` requires all three booleans.

---

#### KG Light Cone Run Log (v1)  <a id="schema-kg-cone-v1"></a>

**Kind:** file  
**Versioning (if present):** `version` field  
**Defined at:** `Derivation/code/physics/metriplectic/schemas/KG-cone-v1.schema.json:1-14` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KG Light Cone Run Log",
  "version": "1.0.0",
  "type": "object",
  "tag": "KG-cone-v1",
  "properties": {
    "params": { "type": "object" },
    "fit": { "type": "object" },
    "gate": { "type": "object" },
    "policy": { "type": "object" }
  },
  "required": ["tag", "type"]
}
```

**Fields (expand from source; do not invent):**

| Field    | Type     | Required | Default | Units/Normalization | Description (lifted) | Source |
| -------- | -------- | :------: | ------- | ------------------- | -------------------- | ------ |
| `params` | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-cone-v1.schema.json:8` |
| `fit`    | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-cone-v1.schema.json:9` |
| `gate`   | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-cone-v1.schema.json:10` |
| `policy` | `object` |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/metriplectic/schemas/KG-cone-v1.schema.json:11` |

**Producers/Consumers:** n/a  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** n/a  
**Invariants/Validation rules:** `required` includes `"tag"` and `"type"`.

---

#### Intelligence Model — Substrate v1 summary  <a id="schema-im-substrate-v1"></a>

**Kind:** file  
**Versioning (if present):** none  
**Defined at:** `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:1-93` • HEAD

**Definition (verbatim snippet from source):**

```json
{
  "tag": "im-substrate-v1",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Intelligence Model — Substrate v1 summary",
  "type": "object",
  "required": [
    "tag",
    "domain",
    "provenance",
    "env",
    "compliance",
    "kpi",
    "artifacts",
    "policy",
    "gate_matrix",
    "status"
  ],
  "properties": {
    "tag": { "type": "string", "const": "im-substrate-v1" },
    "domain": { "type": "string", "const": "intelligence_model" },
    "provenance": {
      "type": "object",
      "required": ["commit_full", "commit"],
      "properties": {
        "commit_full": { "type": "string" },
        "commit": { "type": "string" }
      }
    },
    "env": {
      "type": "object",
      "properties": {
        "threads": { "type": ["integer", "null"] },
        "blas": { "type": ["string", "null"] }
      }
    },
    "compliance": {
      "type": "object",
      "required": [
        "probe_only",
        "real_time",
        "void_faithful",
        "determinism"
      ],
      "properties": {
        "probe_only": { "type": "boolean" },
        "real_time": { "type": "boolean" },
        "void_faithful": { "type": "boolean" },
        "determinism": { "type": "boolean" },
        "determinism_clause": { "type": ["string", "null"] }
      }
    },
    "dimensionless": {
      "type": "object",
      "properties": {
        "Pi_walk": { "type": ["number", "null"] },
        "Pi_step": { "type": ["number", "null"] }
      }
    },
    "kpi": {
      "type": "object",
      "required": ["shared_score_F"],
      "properties": {
        "shared_score_F": {
          "type": "object",
          "required": ["value"],
          "properties": {
            "value": { "type": "number" },
            "note": { "type": ["string", "null"] }
          }
        }
      }
    },
    "artifacts": {
      "type": "object",
      "properties": {
        "figures": { "type": "array", "items": { "type": "string" } },
        "logs": { "type": "array", "items": { "type": "string" } }
      }
    },
    "policy": {
      "type": "object",
      "properties": {
        "approved": { "type": "boolean" },
        "engineering_only": { "type": "boolean" },
        "quarantined": { "type": "boolean" },
        "tag": { "type": "string" },
        "proposal": { "type": ["string", "null"] }
      }
    },
    "gate_matrix": { "type": "object" },
    "status": { "type": "string", "enum": ["success", "failed", "aborted", "pending"] }
  }
}
```

**Fields (expand from source; do not invent):**

| Field                              | Type                 | Required | Default | Units/Normalization | Description (lifted) | Source |
| ---------------------------------- | -------------------- | :------: | ------- | ------------------- | -------------------- | ------ |
| `tag`                              | `string` (const)     |    Y     | n/a     | const               | `"im-substrate-v1"`  | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:19` |
| `domain`                           | `string` (const)     |    Y     | n/a     | const               | `"intelligence_model"` | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:20` |
| `provenance.commit_full`           | `string`             |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:25` |
| `provenance.commit`                | `string`             |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:26` |
| `env.threads`                      | `integer|null`       |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:32` |
| `env.blas`                         | `string|null`        |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:33` |
| `compliance.probe_only`            | `boolean`            |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:45` |
| `compliance.real_time`             | `boolean`            |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:46` |
| `compliance.void_faithful`         | `boolean`            |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:47` |
| `compliance.determinism`           | `boolean`            |    Y     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:48` |
| `compliance.determinism_clause`    | `string|null`        |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:49-50` |
| `dimensionless.Pi_walk`            | `number|null`        |    N     | n/a     | unitless            |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:55` |
| `dimensionless.Pi_step`            | `number|null`        |    N     | n/a     | unitless            |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:56-57` |
| `kpi.shared_score_F.value`         | `number`             |    Y     | n/a     | unitless            |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:67` |
| `kpi.shared_score_F.note`          | `string|null`        |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:68-69` |
| `artifacts.figures[]`              | `string[]`           |    N     | n/a     | paths               |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:76` |
| `artifacts.logs[]`                 | `string[]`           |    N     | n/a     | paths               |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:77-78` |
| `policy.approved`                  | `boolean`            |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:83` |
| `policy.engineering_only`          | `boolean`            |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:84` |
| `policy.quarantined`               | `boolean`            |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:85` |
| `policy.tag`                       | `string`             |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:86` |
| `policy.proposal`                  | `string|null`        |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:87-88` |
| `gate_matrix`                      | `object`             |    N     | n/a     | n/a                 |                      | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:90` |
| `status`                           | `string (enum)`      |    Y     | n/a     | n/a                 | enum: `"success"`, `"failed"`, `"aborted"`, `"pending"` | `Derivation/code/physics/intelligence_model/schemas/im-substrate-v1.schema.json:91-92` |

**Producers/Consumers:** n/a  
**Related equations (anchors only):** n/a  
**Related symbols/constants:** n/a  
**Examples (if present):** n/a  
**Invariants/Validation rules:** All fields listed under top-level `"required"` must be present in documents conforming to this schema.

---
<!-- BEGIN AUTOSECTION: SCHEMAS-INDEX -->
<!-- Tool-maintained list of [Schema](#schema-...) anchors for quick lookup -->

### Schema Index

- [ADCEvent](#schema-adcevent)
- [BaseEvent](#schema-baseevent)
- [BiasHintEvent](#schema-biashintevent)
- [BudgetTick](#schema-budgettick)
- [ConvergenceMetrics](#schema-convergencemetrics)
- [DeltaEvent](#schema-deltaevent)
- [DeltaWEvent](#schema-deltawevent)
- [EdgeOnEvent / EdgeOffEvent](#schema-edgeevent)
- [GeometryProbeAdapter](#schema-geometryprobeadapter)
- [GeometryRunConfig](#schema-geometryrunconfig)
- [HorizonActivityEvent](#schema-horizonactivityevent)
- [LBMConfig](#schema-lbmconfig)
- [MotifEnterEvent / MotifExitEvent](#schema-motifevent)
- [Observation](#schema-observation)
- [Petition](#schema-petition)
- [PolicyBounds](#schema-policybounds)
- [PYTHON_PACKAGE_SCHEMA](#schema-python-package-schema)
- [QFUM Metrics JSON Output](#schema-qfum-metrics-json)
- [Tube Spectrum Summary (tachyonic_condensation)](#schema-tube-spectrum-summary)
- [Tube Condensation Summary (tachyonic_condensation)](#schema-tube-condensation-summary)
- [RouterSplitEvent](#schema-routersplitevent)
- [Run Profile Configuration](#schema-run-profile)
- [RunMetrics](#schema-runmetrics)
- [SayRecord](#schema-sayrecord)
- [SpikeEvent](#schema-spikeevent)
- [VDM Corner Config (YAML)](#schema-vdm-corner-config)
- [VTTouchEvent](#schema-vttouchevent)
- [KG Energy Oscillation Summary (metriplectic)](#schema-kg-energy-osc)
- [KG-Lite Chunk Envelope v1](#schema-kg-lite-chunkenvelope-v1)

<!-- END AUTOSECTION: SCHEMAS-INDEX -->
