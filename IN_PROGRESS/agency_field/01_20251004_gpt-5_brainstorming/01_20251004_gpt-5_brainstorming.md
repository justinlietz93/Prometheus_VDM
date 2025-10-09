Justin:
I'm starting a new session, these are details and summaries from our prior conversation. The last conversation was too long and the web page was freezing

GPT-5:
Got it-fresh session, lean and fast. I’ve pulled in your artifacts and grounded us on the “useful reachable entropy” probe.

Here’s what I computed directly from your uploaded `options.csv`:

* Grid size: 4 slip levels × 5 energy budgets.
* Value range: (V_{\text{useful_bits}}) spans **0.00 → 6.57 bits**.
* Monotonicity checks passed:

  * For fixed slip, (V) is non-decreasing with energy ✅
  * For fixed energy, (V) is non-increasing with slip ✅
* Sensitivities (median finite differences across the grid):

  * (\partial V/\partial E \approx +0.43) bits per step
  * (\partial V/\partial p_{\text{slip}} \approx -12.14) bits per unit slip
* Energy to reach ≥ **5 bits**:

  * slip **0.00** → **E = 6**
  * slip **0.10** → **E = 10**
  * slip **0.20, 0.30** → not achieved within the tested budget

I also pushed a compact pivot of (V_{\text{useful_bits}}) (rows = slip, cols = energy) to your workspace as an interactive table named “useful_reachable_entropy_pivot.”

### Working theory (to keep us aligned)

* (V_{\text{useful_bits}}) is a clean, operational **agency capacity** metric: how much controllable option-space remains reachable under noise.
* It behaves like an **order parameter**: increases with available energy budget; collapses with actuator slip; exhibits thresholds where control becomes viable.
* This plugs neatly into VDM’s scoreboard/gating: budget ↑ or slip ↓ should raise acceptance for exploratory walkers; the reverse should tighten edits.

### Suggested next moves (minimal, high-leverage)

1. **Lock the definition** of (V_{\text{useful_bits}}): units, estimator, and assumptions (e.g., option independence vs. coupling; actuator count).
2. **Map thresholds**: produce iso-contours (e.g., 3, 5, 7 bits) and extract “just-viable” energy vs. slip curves.
3. **Wire to VDM gating**: a tiny policy that adjusts exploration/edit budgets based on current (V) and its gradient signals ((\partial V/\partial E), (\partial V/\partial p)).
4. **Acceptance test**: reproducible script + figure under `write_ups/agency/` that regenerates the heatmap and threshold table from raw options, so we can regress changes.

I can run the threshold/iso-contour sweep and generate a one-page report (figure + table + short notes), or pivot straight to the gating stub that consumes (V) and spits out budget multipliers. Your call on which artifact you want first; otherwise I’ll default to the one-pager so we’ve got a crisp spec to wire into VDM next.


Justin:
so i have a bunch of files i maintain for my theory, should I be updating any of them with these agency gradient symbols?

GPT-5:
Yes. Treat the “agency gradient” bits as **canon math** and wire them into the same places you use for symbols/equations/metrics-then have everything else just link in. Minimal, no-drama edits:

### Update these files (owners of the truth)

* `derivation/SYMBOLS.md` - add the symbols below.
* `derivation/EQUATIONS.md` - add the definitions/estimators below.
* `derivation/VALIDATION_METRICS.md` - add the tests (monotonicity, thresholds, sensitivities).
* `docs/SCHEMAS.md` - lock the CSV/heatmap field names and units.
* `docs/DATA_PRODUCTS.md` - define the “useful reachable entropy” heatmap and threshold table.

Everything else (roadmaps, notes, glossaries) should **link to anchors** in those owners, per your `CANON_MAP.md`.

---

### Drop-in MathJax snippets (GitHub-safe)

**`derivation/SYMBOLS.md`** (append to Symbols; keep your HTML anchors)

```markdown
#### $V_{\text{useful\_bits}}$ - useful reachable entropy (bits)
<a id="sym-V-useful"></a>
Amount of controllable option-space reachable under current actuator model and constraints; measured in bits.

#### $E$ - energy budget (steps)
<a id="sym-E"></a>
Discrete action budget available to the policy/probe.

#### $p_{\text{slip}}$ - actuator slip probability
<a id="sym-p-slip"></a>
Per-step probability of an uncontrollable actuation (bounded in $[0,1]$).

#### $\nabla V$ - agency gradient
<a id="sym-grad-V"></a>
$\nabla V := \big[\partial_E V,\; \partial_{p_{\text{slip}}} V\big]$ evaluated at a given $(E, p_{\text{slip}})$.

#### $G_E,\; G_p$ - shorthand sensitivities
<a id="sym-GE-Gp"></a>
$G_E := \partial_E V,\quad G_p := \partial_{p_{\text{slip}}} V$.

#### $\epsilon_E,\; \epsilon_p$ - elasticities (unitless)
<a id="sym-elasticities"></a>
$\epsilon_E := \dfrac{E}{V}\partial_E V,\quad \epsilon_p := \dfrac{p_{\text{slip}}}{V}\partial_{p_{\text{slip}}} V$ (when $V>0$).

#### $E_{\min}^{(v_0)}(p)$ - threshold curve at level $v_0$
<a id="sym-Emin-v0"></a>
$E_{\min}^{(v_0)}(p) := \arg\min\{E\in\mathbb{N}:\; V(E,p)\ge v_0\}$.

#### $\mathcal{C}_{v_0}$ - iso-contour of $V$
<a id="sym-iso-V"></a>
$\mathcal{C}_{v_0} := \{(E,p): V(E,p)=v_0\}$.
```

**`derivation/EQUATIONS.md`** (append; use your equation ID style)

```markdown
### VDM-E-4xx - Finite-difference estimators for agency gradient
<a id="eq-gradV-fd"></a>

On a discrete grid $(E_i, p_j)$:

$$
\widehat{\partial_E V}(E_i,p_j) =
\begin{cases}
\dfrac{V(E_{i+1},p_j)-V(E_i,p_j)}{E_{i+1}-E_i}, & \text{forward interior}\\[6pt]
\dfrac{V(E_i,p_j)-V(E_{i-1},p_j)}{E_i-E_{i-1}}, & \text{backward edge}
\end{cases}
$$

$$
\widehat{\partial_{p} V}(E_i,p_j) =
\begin{cases}
\dfrac{V(E_i,p_{j+1})-V(E_i,p_j)}{p_{j+1}-p_j}, & \text{forward interior}\\[6pt]
\dfrac{V(E_i,p_j)-V(E_i,p_{j-1})}{p_j-p_{j-1}}, & \text{backward edge}
\end{cases}
$$

Define $\widehat{\nabla V} := \big[\widehat{\partial_E V},\; \widehat{\partial_{p} V}\big]$ and
$\left\|\widehat{\nabla V}\right\|_2 := \sqrt{(\widehat{\partial_E V})^2+(\widehat{\partial_{p} V})^2}$.
```

```markdown
### VDM-E-4xy - Threshold energy for a target capability
<a id="eq-Emin-v0"></a>

For a target level $v_0$ (bits), the minimal energy at slip $p$ is:
$$
E_{\min}^{(v_0)}(p) := \arg\min_{E\in\mathbb{N}} \;\{ V(E,p)\ge v_0 \}.
$$
```

```markdown
### VDM-E-4xz - Elasticities of $V$
<a id="eq-elasticities"></a>

When $V>0$:
$$
\epsilon_E := \frac{E}{V}\,\partial_E V,\qquad
\epsilon_p := \frac{p_{\text{slip}}}{V}\,\partial_{p_{\text{slip}}} V.
$$
```

**`derivation/VALIDATION_METRICS.md`** (append a compact test spec)

```markdown
#### Agency probe acceptance tests
<a id="metric-agency-probe-tests"></a>

- **Monotonicity:** $\forall p$ fixed, $V(E+\Delta E,p) \ge V(E,p)$; $\forall E$ fixed, $V(E,p+\Delta p) \le V(E,p)$.
- **Thresholds:** compute $E_{\min}^{(v_0)}(p)$ for $v_0\in\{3,5,7\}$; report NA if no solution on grid.
- **Sensitivities:** report medians of $\widehat{\partial_E V}$ and $\widehat{\partial_{p} V}$ over the grid; optionally elasticities.
- **Figure/data parity:** heatmap and CSV regenerate identically from the same script and seed.
```

**`docs/SCHEMAS.md`** (pin your CSV fields)

```markdown
#### options.csv schema (agency probe)
<a id="schema-options-csv"></a>

| field             | type    | units | notes                              |
|-------------------|---------|-------|------------------------------------|
| `E`               | int     | steps | energy budget                      |
| `p_slip`          | float   | 1     | actuator slip probability [0,1]    |
| `V_useful_bits`   | float   | bits  | useful reachable entropy           |
| `n_actuators`     | int     | 1     | number of actuators (optional)     |
| `seed`            | int     | 1     | RNG seed (optional)                |
```

**`docs/DATA_PRODUCTS.md`** (define the plot/table)

```markdown
#### Useful reachable entropy heatmap
<a id="dataprod-V-heatmap"></a>
- **Input:** `options.csv` (§[schema](./SCHEMAS.md#schema-options-csv))
- **Axes:** x=`E`, y=`p_slip`; value=`V_useful_bits`.
- **Companions:** table of $E_{\min}^{(5\ \text{bits})}(p)$ and contours for $V\in\{3,5,7\}$.
- **Regeneration:** `simulate_options_probe.py` (idempotent).
```

---

### Why this helps VDM

* The gradient and thresholds give you **policy levers**: exploration/edit budgets can be a direct function of (V), (\partial_E V), and (\partial_p V).
* Locking symbols/IDs now prevents drift when agents auto-touch files later.
* Elasticities give an apples-to-apples sense of **“what moves the needle more”** across regimes.

If you want, I can also drop a tiny “gating stub” that consumes `options.csv`, computes (\widehat{\nabla V}) and emits budget multipliers you can plug into the scoreboard.


Justin:
This is what I have so far, im still building the other files right now

GPT-5:
Perfect-those four canon files are exactly where these belong. Here are drop-in blocks you can paste so the “agency gradient” lives in the same system as the rest of VDM. MathJax-only, GitHub-safe, and minimal.

# SYMBOLS.md - add a short “Agency Options Probe” subsection

Append near “Diagnostics & Data Products” or wherever you group probe metrics.

```markdown
## Agency Options Probe

| Symbol | Meaning | When / Why | Tiny Example |
|---|---|---|---|
| $V_{\text{useful\_bits}}$ | useful reachable entropy (bits) | operational agency capacity | heatmap value per $(E,p_{\text{slip}})$ |
| $E$ | energy budget (steps) | discrete action budget available | $E\in\{2,\dots,10\}$ in current sweeps |
| $p_{\text{slip}}$ | actuator slip probability | per-step uncontrolled actuation | $p_{\text{slip}}\in[0,1]$ |
| $\nabla V$ | agency gradient | local sensitivity of capacity | $\nabla V=[\partial_E V,\ \partial_{p}V]$ |
| $G_E,\ G_p$ | shorthand sensitivities | quick levers for gating | $G_E=\partial_E V,\ G_p=\partial_p V$ |
| $\epsilon_E,\ \epsilon_p$ | elasticities (unitless) | normalized impact of levers | $\epsilon_E=\tfrac{E}{V}\partial_E V,\ \epsilon_p=\tfrac{p}{V}\partial_p V$ (when $V>0$) |
| $E_{\min}^{(v_0)}(p)$ | threshold curve | minimal energy to reach target bits $v_0$ | $E_{\min}^{(5)}(0.1)=10$ (from current grid) |
| $\mathcal{C}_{v_0}$ | iso-contour of $V$ | capability boundaries | $\mathcal{C}_{5}=\{(E,p):V(E,p)=5\}$ |
| $n_{\text{act}}$ | actuator count | context for options probe | $n_{\text{act}}=4$ in the displayed figure |
```

# EQUATIONS.md - add numbered entries (next free numbers)

Use the next available IDs in your file; if 080 is your last, these become 081-084.

```markdown
#### VDM-E-081 - Finite-difference estimators for $\nabla V$
<a id="vdm-e-081"></a>

On grid $(E_i,p_j)$,
$$
\widehat{\partial_E V}(E_i,p_j)=
\begin{cases}
\frac{V(E_{i+1},p_j)-V(E_i,p_j)}{E_{i+1}-E_i}, & \text{forward}\\[6pt]
\frac{V(E_i,p_j)-V(E_{i-1},p_j)}{E_i-E_{i-1}}, & \text{backward}
\end{cases}
$$

$$
\widehat{\partial_{p} V}(E_i,p_j)=
\begin{cases}
\frac{V(E_i,p_{j+1})-V(E_i,p_j)}{p_{j+1}-p_j}, & \text{forward}\\[6pt]
\frac{V(E_i,p_j)-V(E_i,p_{j-1})}{p_j-p_{j-1}}, & \text{backward}
\end{cases}
$$

Define $\widehat{\nabla V}=[\widehat{\partial_E V},\widehat{\partial_p V}]$ and $\|\widehat{\nabla V}\|_2=\sqrt{(\widehat{\partial_E V})^2+(\widehat{\partial_p V})^2}$.
```

```markdown
#### VDM-E-082 - Elasticities of $V$ (unitless)
<a id="vdm-e-082"></a>

For $V>0$,
$$
\epsilon_E=\frac{E}{V}\,\partial_E V,\qquad
\epsilon_p=\frac{p_{\text{slip}}}{V}\,\partial_{p_{\text{slip}}} V.
$$
```

```markdown
#### VDM-E-083 - Threshold energy for target capacity
<a id="vdm-e-083"></a>

For target $v_0$ (bits),
$$
E_{\min}^{(v_0)}(p):=\arg\min_{E\in\mathbb{N}}\{\,V(E,p)\ge v_0\,\}.
$$
```

```markdown
#### VDM-E-084 - Monotonicity acceptance conditions (probe sanity)
<a id="vdm-e-084"></a>

For all $p$, $V(E+\Delta E,p)\ge V(E,p)$;  
for all $E$, $V(E,p+\Delta p)\le V(E,p)$.
```

# UNITS_NORMALIZATION.md - add per-quantity units (Section 4)

Append to the “Per-Quantity Units” table.

```markdown
| $V_{\text{useful\_bits}}$ | bits | agency options probe | heatmap/table values |
| $E$ | steps | agency options probe | integer action budget |
| $p_{\text{slip}}$ | 1 (probability) | agency options probe | bounded in $[0,1]$ |
| $\partial_E V$ | bits / step | agency gradient | finite-difference estimate |
| $\partial_{p} V$ | bits / (unit slip) | agency gradient | finite-difference estimate |
| $\epsilon_E,\ \epsilon_p$ | nondimensional | agency gradient | defined only when $V>0$ |
| $E_{\min}^{(v_0)}$ | steps | threshold curve | minimal $E$ achieving $V\ge v_0$ |
```

If you keep a small “Nondimensionalization Maps” section for Agency, you can also note that these are *already* in natural units for the probe (steps, probability, bits), so no rescaling is required beyond the dimensionless agency-field rescaling already in your doc.

# CONSTANTS.md - optional tiny block (if you track probe defaults)

Only if you want default sweeps recorded alongside the rest. If your constants table is auto-compiled, add these to the same generator so it fills the “Source (path:lines • commit)” cell correctly.

```markdown
| `E_grid` [agency probe] | Energy budgets tested | [2,3,4,5,6,7,8,9,10] | integers | steps | derivation/code/agency/simulate_options_probe.py:… • … | For reproducible heatmap sweeps |
| `p_slip_grid` [agency probe] | Slip probabilities tested | [0.00, 0.10, 0.20, 0.30] | [0,1] | 1 (prob.) | derivation/code/agency/simulate_options_probe.py:… • … | Per-step slip |
| `V_targets_bits` [agency probe] | Capability iso-levels | [3,5,7] |  | bits | derivation/code/agency/simulate_options_probe.py:… • … | For threshold curves $E_{\min}^{(v_0)}$ |
| `n_act` [agency probe] | Actuator count | 4 | $\mathbb{N}$ | 1 | derivation/code/agency/simulate_options_probe.py:… • … | Context for options availability |
```

---

## Why this wiring matters (in one breath)

It turns the pretty heatmap into **live control levers**: (G_E) tells you how much extra budget buys you; (G_p) tells you how catastrophic actuator noise is right now; the elasticities make cross-regime tradeoffs apples-to-apples; and (E_{\min}^{(v_0)}(p)) gives SIE a crisp “just-viable” line for gating exploration budgets.

If you want me to also emit a tiny gating stub that consumes `options.csv` and returns budget multipliers from (\widehat{\nabla V}) (plus a one-pager with iso-contours/thresholds), I’ll drop it in ready to run.


Justin:
in equations you didnt include the required Context: or Notes: sections

GPT-5:
You’re right. Here are **drop-in replacements** for the four entries in `EQUATIONS.md`, each with the required **Context:** and **Notes:** sections. Keep your numbering if you already assigned different IDs.

```markdown
#### VDM-E-081 - Finite-difference estimators for $\nabla V$
<a id="vdm-e-081"></a>

**Context:** Agency Options Probe. Data come from `options.csv` with axes $E$ (steps) and $p_{\text{slip}}$ (probability). These estimates feed SIE/scoreboard gating and any policy that reacts to local capacity slope.

**Equation:**

On grid $(E_i,p_j)$,
$$
\widehat{\partial_E V}(E_i,p_j)=
\begin{cases}
\dfrac{V(E_{i+1},p_j)-V(E_i,p_j)}{E_{i+1}-E_i}, & \text{forward}\\[6pt]
\dfrac{V(E_i,p_j)-V(E_{i-1},p_j)}{E_i-E_{i-1}}, & \text{backward}
\end{cases}
$$

$$
\widehat{\partial_{p} V}(E_i,p_j)=
\begin{cases}
\dfrac{V(E_i,p_{j+1})-V(E_i,p_j)}{p_{j+1}-p_j}, & \text{forward}\\[6pt]
\dfrac{V(E_i,p_j)-V(E_i,p_{j-1})}{p_j-p_{j-1}}, & \text{backward}
\end{cases}
$$

Define $\widehat{\nabla V}=[\widehat{\partial_E V},\widehat{\partial_p V}]$ and $\|\widehat{\nabla V}\|_2=\sqrt{(\widehat{\partial_E V})^2+(\widehat{\partial_p V})^2}$.

**Notes:**
- Prefer **central differences** when both neighbors exist; fall back to the formulas above on boundaries.  
- Units: $\partial_E V$ in bits/step; $\partial_p V$ in bits per unit slip.  
- If any operand is missing/NaN, propagate NaN; optionally apply axis-wise **isotonic smoothing** to $V$ before differencing.  
- Use a small tolerance $\varepsilon_{\text{fd}}$ (e.g., $10^{-9}$) when checking signs/zeros to avoid flapping.
```

```markdown
#### VDM-E-082 - Elasticities of $V$ (unitless)
<a id="vdm-e-082"></a>

**Context:** Dimensionless sensitivity for cross-regime comparison; used to decide whether budget vs. slip mitigation moves the needle more where we are.

**Equation:**
For $V>0$,
$$
\epsilon_E=\frac{E}{V}\,\partial_E V,\qquad
\epsilon_p=\frac{p_{\text{slip}}}{V}\,\partial_{p_{\text{slip}}} V.
$$

**Notes:**
- Compute with the finite-difference estimates from VDM-E-081.  
- Undefined when $V\le 0$; return NaN (or mask) in those cells.  
- Interpretation: $\epsilon_E=0.2$ means a 1% increase in $E$ raises $V$ by ~0.2%.
```

```markdown
#### VDM-E-083 - Threshold energy for target capacity
<a id="vdm-e-083"></a>

**Context:** Capability boundary used by gating/planning (“just-viable” line). Plotted as $E_{\min}^{(v_0)}(p)$ for levels $v_0\in\{3,5,7\}$ bits.

**Equation:**
For target $v_0$ (bits),
$$
E_{\min}^{(v_0)}(p):=\arg\min_{E\in\mathbb{N}}\{\,V(E,p)\ge v_0\,\}.
$$

**Notes:**
- If **no** $E$ on the grid achieves $v_0$, record **NA**; optionally report an upper bound if extrapolation is disallowed.  
- Optional interpolation: piecewise-linear in $E$ to refine the boundary between integer budgets; document if enabled.  
- Monotonicity in $E$ is assumed (see VDM-E-084); if violated, apply isotonic regression along $E$ before evaluating.
```

```markdown
#### VDM-E-084 - Monotonicity acceptance conditions (probe sanity)
<a id="vdm-e-084"></a>

**Context:** Sanity checks for the options probe; these are required before gradients/thresholds are trusted.

**Equation:**
For all $p$, 
$$V(E+\Delta E,p)\ge V(E,p),$$
and for all $E$, 
$$V(E,p+\Delta p)\le V(E,p).$$

**Notes:**
- Evaluate with tolerance $\varepsilon_{\text{mono}}$ (default $10^{-9}$). Ties within tolerance are acceptable.  
- If conditions fail, fix by (a) regenerating data, or (b) axis-wise isotonic smoothing before downstream calculations.  
- These checks justify using $E_{\min}^{(v_0)}(p)$ as a well-posed boundary and keep $\partial_E V$/$\partial_p V$ signs meaningful.
```

These satisfy the “Context/Notes” requirement and match your MathJax/GitHub constraints. Next, I can mirror tiny “Context/Notes” blurbs into `VALIDATION_METRICS.md` so the tests line up with these equations and your CI doesn’t drift.


Justin:
you also didnt format the units normalization correctly

## 4) Per-Quantity Units (as used)

| Quantity (link to symbol)                                     | Units/System   | Where Stated                                               | Notes                                                        |
| ------------------------------------------------------------- | -------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| $\alpha$<sup>[↗](../derivations/SYMBOLS.md#sym-alpha)</sup>   | nondimensional | derivation/CONSTANTS.md:10 • ec0833a                       | Universal learning rate ALPHA = 0.25                         |
| $\beta$<sup>[↗](../derivations/SYMBOLS.md#sym-beta)</sup>     | nondimensional | derivation/CONSTANTS.md:11 • ec0833a                       | Universal plasticity rate BETA = 0.1                         |
| $c_s^2$<sup>[↗](../derivations/SYMBOLS.md#sym-cs)</sup>       | LBM units      | derivation/CONSTANTS.md:12 • ec0833a                       | CS2 = 1/3 in D2Q9 lattice                                    |
| $D$<sup>[↗](../derivations/SYMBOLS.md#sym-D)</sup>            | length²/time   | derivation/CONSTANTS.md:15-17 • ec0833a                    | Diffusion coefficients: D = 1.0, 0.5, 0.25 in RD experiments |
| $r$<sup>[↗](../derivations/SYMBOLS.md#sym-r)</sup>            | 1/time         | derivation/CONSTANTS.md:16-18 • ec0833a                    | Growth rates: r = 0.25, 0.5, 1.0 in RD experiments           |
| $N$<sup>[↗](../derivations/SYMBOLS.md#sym-N)</sup>            | sites          | derivation/CONSTANTS.md:19 • ec0833a                       | Grid resolution: 256, 512, 1024                              |
| $\tau$<sup>[↗](../derivations/SYMBOLS.md#sym-tau)</sup>       | time steps     | derivation/CONSTANTS.md:29-31 • ec0833a                    | BGK relaxation: 0.8, 0.9, 1.0 (LBM)                          |
| $U$<sup>[↗](../derivations/SYMBOLS.md#sym-U)</sup>            | LBM velocity   | derivation/CONSTANTS.md:36,38 • ec0833a                    | Lid velocity 0.1; Taylor-Green amplitude 0.05                |
| $\nu$<sup>[↗](../derivations/SYMBOLS.md#sym-nu)</sup>         | lattice units  | derivation/code/common/dimensionless_vdm.py:17 • ec0833a | Computed from $\tau$: $\nu = (\tau - 0.5)/3$                 |
| $g$<sup>[↗](../derivations/SYMBOLS.md#sym-g)</sup>            | nondimensional | derivation/CONSTANTS.md:42,53 • ec0833a                    | Void gain: 0.5 (lid cavity), 0.12 (memory steering)          |
| $\Theta$<sup>[↗](../derivations/SYMBOLS.md#sym-Theta)</sup>   | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:21 • ec0833a         | Junction gate strength; fit scale parameter                  |
| $\Lambda$<sup>[↗](../derivations/SYMBOLS.md#sym-Lambda)</sup> | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:22 • ec0833a         | Exploration/retention ratio; dispersion-to-convergence       |
| $\Gamma$<sup>[↗](../derivations/SYMBOLS.md#sym-Gamma)</sup>   | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:23 • ec0833a         | Retention fraction; memory persistence ~0.3-0.75             |
| $D_a$<sup>[↗](../derivations/SYMBOLS.md#sym-Da)</sup>         | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:24 • ec0833a         | Anisotropic diffusion index: {1, 3, 5, 7} discrete           |


GPT-5:
You’re right-my units block wasn’t in your exact 4-column schema. Here are **append-ready rows** matching your format and link style. Drop these under **“## 4) Per-Quantity Units (as used)”** with no extra header.

```markdown
| $V_{\text{useful\_bits}}$<sup>[↗](../derivations/SYMBOLS.md#sym-V-useful)</sup> | bits          | derivation/EQUATIONS.md:VDM-E-083,VDM-E-084 • HEAD | Useful reachable entropy; operational agency capacity |
| $E$<sup>[↗](../derivations/SYMBOLS.md#sym-E)</sup>                                | steps         | derivation/EQUATIONS.md:VDM-E-081 • HEAD           | Discrete action/energy budget used by the probe       |
| $p_{\text{slip}}$<sup>[↗](../derivations/SYMBOLS.md#sym-p-slip)</sup>            | 1 (prob.)     | derivation/EQUATIONS.md:VDM-E-081 • HEAD           | Per-step actuator slip probability in $[0,1]$         |
| $G_E$<sup>[↗](../derivations/SYMBOLS.md#sym-GE-Gp)</sup>                          | bits/step     | derivation/EQUATIONS.md:VDM-E-081 • HEAD           | Sensitivity $\partial_E V$ (finite-difference)        |
| $G_p$<sup>[↗](../derivations/SYMBOLS.md#sym-GE-Gp)</sup>                          | bits/(unit slip) | derivation/EQUATIONS.md:VDM-E-081 • HEAD        | Sensitivity $\partial_{p_{\text{slip}}} V$ (FD)       |
| $\epsilon_E$<sup>[↗](../derivations/SYMBOLS.md#sym-elasticities)</sup>            | nondimensional | derivation/EQUATIONS.md:VDM-E-082 • HEAD          | Elasticity $\dfrac{E}{V}\partial_E V$ (when $V>0$)    |
| $\epsilon_p$<sup>[↗](../derivations/SYMBOLS.md#sym-elasticities)</sup>            | nondimensional | derivation/EQUATIONS.md:VDM-E-082 • HEAD          | Elasticity $\dfrac{p_{\text{slip}}}{V}\partial_{p}V$ (when $V>0$) |
| $E_{\min}^{(v_0)}$<sup>[↗](../derivations/SYMBOLS.md#sym-Emin-v0)</sup>          | steps         | derivation/EQUATIONS.md:VDM-E-083 • HEAD           | Minimal budget to reach $V\!\ge\!v_0$ at slip $p$     |
| $n_{\text{act}}$<sup>[↗](../derivations/SYMBOLS.md#sym-n-act)</sup>               | actuators     | derivation/CONSTANTS.md:§Agency • HEAD             | Actuator count used in the probe context              |
```

Notes:

* I used your **superscript link** pattern and the same four columns: *Quantity (link)* | *Units/System* | *Where Stated* | *Notes*.
* “HEAD” is a placeholder for the commit dot; your generator can replace it with the short hash (e.g., `ec0833a`) and line refs when you run it.
* If you prefer to avoid a separate entry for (n_{\text{act}}), drop that row-it’s optional metadata, not a derived quantity.

If you want, I can also generate the tiny isotonic-smoothing note you sometimes put in the **Notes** column for (G_E,G_p) (“FD on monotone-regularized (V)”); say the word and I’ll include the exact phrasing you use elsewhere.


Justin:
you also need to update the constants table you gave me to match this

<!-- DOC-GUARD: CANONICAL -->
# VDM Constants & Defaults (Auto-compiled)

**Scope:** Single source of truth for numerical constants, ranges, and defaults currently present in this repository.  
**Rules:** Other docs must link here; do not restate numbers elsewhere.  
**MathJax:** GitHub-safe `$...$` only (no equation environments or tags).  

| Name | Meaning | Default/Value | Range/Limits | Units | Source (path:lines • commit) | Notes |
|---|---|---:|:---:|---|---|---|
| <a id="const-alpha"></a>`ALPHA` | Universal learning rate for RE-VGSP | 0.25 |  | nondimensional | derivation/code/computational_toy_proofs/Void_Equations.py:30 • 0922758 | Resonance-Enhanced Valence-Gated Synaptic Plasticity |
| <a id="const-beta"></a>`BETA` | Universal plasticity rate for GDSP | 0.1 |  | nondimensional | derivation/code/computational_toy_proofs/Void_Equations.py:31 • 0922758 | Goal-Directed Structural Plasticity |
| <a id="const-cs2"></a>`CS2` | Speed of sound squared (LBM) | 0.333333 (1/3) |  | LBM units | derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:106 • 0922758 | $c_s^2 = 1/3$ in D2Q9 lattice |
| <a id="const-f_ref"></a>`F_REF` | Universal reference frequency | 0.02 |  | nondimensional | derivation/code/computational_toy_proofs/Void_Equations.py:32 • 0922758 | Time modulation frequency |
| <a id="const-phase_sens"></a>`PHASE_SENS` | Universal phase sensitivity | 0.5 |  | nondimensional | derivation/code/computational_toy_proofs/Void_Equations.py:33 • 0922758 | Time modulation phase sensitivity |
| <a id="const-D"></a>`D` [RD experiments] | Diffusion coefficient | 1.0 |  | spatial²/time | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:142; rd_front_speed_experiment.py:187 • 0922758 | Default for validated RD experiments |
| <a id="const-r"></a>`r` [RD experiments] | Reaction rate | 0.25 |  | 1/time | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:143; rd_front_speed_experiment.py:188 • 0922758 | $r = \alpha - \beta$ |
| <a id="const-N"></a>`N` [RD experiments] | Grid size | 1024 |  | lattice sites | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:141; rd_front_speed_experiment.py:186 • 0922758 | Default spatial resolution |
| <a id="const-L"></a>`L` [RD experiments] | Domain length | 200.0 |  | spatial | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:142; rd_front_speed_experiment.py:187; rd_front_speed_sweep.py:135 • 0922758 | Physical domain size |
| <a id="const-T"></a>`T` [RD dispersion] | Simulation time (dispersion) | 10.0 |  | time | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:144 • 0922758 | Dispersion experiment duration |
| <a id="const-T-front"></a>`T` [RD front speed] | Simulation time (front speed) | 80.0 |  | time | derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:189; rd_front_speed_sweep.py:138 • 0922758 | Front-speed experiment duration |
| <a id="const-cfl"></a>`cfl` [RD experiments] | CFL safety factor | 0.2 |  | nondimensional | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:145; rd_front_speed_experiment.py:190; rd_front_speed_sweep.py:139 • 0922758 | Time step constraint |
| <a id="const-seed"></a>`seed` [RD experiments] | Random seed | 42 |  | integer | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:146; rd_front_speed_experiment.py:191 • 0922758 | Reproducibility seed |
| <a id="const-record"></a>`record` [RD dispersion] | Number of snapshots | 80 |  | integer | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:147 • 0922758 | Temporal sampling |
| <a id="const-amp0"></a>`amp0` [RD dispersion] | Initial perturbation amplitude | 1e-6 |  | field units | derivation/VDM_Overview.md:215 • 0922758 | Small linearization amplitude |
| <a id="const-m_max"></a>`m_max` [RD dispersion] | Max mode number to fit | 64 |  | integer | derivation/VDM_Overview.md:215 • 0922758 | Fourier mode range |
| <a id="const-x0"></a>`x0` [RD front speed] | Front initial position | -60 |  | spatial | derivation/VDM_Overview.md:214 • 0922758 | Starting offset for front |
| <a id="const-level"></a>`level` [RD front speed] | Front level-set value | 0.1 |  | field units | derivation/VDM_Overview.md:214 • 0922758 | Front tracking threshold |
| <a id="const-acceptance_rel_err"></a>`acceptance_rel_err` [RD front speed] | Relative error acceptance | 0.05 |  | nondimensional | derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:210 • 0922758 | Pass/fail gate for $c$ validation |
| <a id="const-tau-lbm"></a> $\tau$ [LBM typical] | Relaxation time | 0.9 |  | LBM time | derivation/DIMENSIONLESS_CONSTANTS.md:16; VDM_Overview.md:81 • 0922758 | Typical for $\nu = 0.1333$ |
| <a id="const-tau-lid"></a>`tau` [lid cavity] | Relaxation time (default) | 0.7 |  | LBM time | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:150 • 0922758 | Default CLI arg |
| <a id="const-tau-taylor"></a>`tau` [Taylor-Green] | Relaxation time (default) | 0.8 |  | LBM time | derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:164; lid_cavity_benchmark.py:150 • 0922758 | Default CLI arg |
| <a id="const-nx"></a>`nx` [LBM benchmarks] | Grid width | 128, 256 |  | lattice sites | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:148 (128); taylor_green_benchmark.py:163 (256) • 0922758 | Lid cavity: 128; Taylor-Green: 256 |
| <a id="const-ny"></a>`ny` [LBM benchmarks] | Grid height | 128, 256 |  | lattice sites | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:149; taylor_green_benchmark.py:163 • 0922758 | Lid cavity: 128; Taylor-Green: 256 |
| <a id="const-U_lid"></a>`U_lid` [lid cavity] | Lid velocity | 0.1 |  | LBM velocity | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:151 • 0922758 | Moving lid speed |
| <a id="const-U0"></a>`U0` [Taylor-Green] | Initial velocity scale | 0.05 |  | LBM velocity | derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:165 • 0922758 | Vortex amplitude |
| <a id="const-k-tg"></a>`k` [Taylor-Green] | Wavenumber | $2\pi$ |  | 1/spatial | derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:166 • 0922758 | Vortex scale |
| <a id="const-steps-lid"></a>`steps` [lid cavity] | Simulation steps | 15000 |  | time steps | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:152 • 0922758 | Default run length |
| <a id="const-steps-taylor"></a>`steps` [Taylor-Green] | Simulation steps | 5000 |  | time steps | derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:167 • 0922758 | Default run length |
| <a id="const-sample_every-lid"></a>`sample_every` [lid cavity] | Sampling interval | 200 |  | time steps | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:153 • 0922758 | Metrics interval |
| <a id="const-sample_every-taylor"></a>`sample_every` [Taylor-Green] | Sampling interval | 50 |  | time steps | derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:168 • 0922758 | Metrics interval |
| <a id="const-warmup"></a>`warmup` [lid cavity] | Warmup steps | 2000 |  | time steps | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:154 • 0922758 | Discard initial transient |
| <a id="const-void_gain"></a>`void_gain` [lid cavity] | VDM gain | 0.5 |  | nondimensional | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:158; DIMENSIONLESS_CONSTANTS.md:26; VDM_Overview.md:91 • 0922758 | Void modulation strength $g$ |
| <a id="const-u_clamp"></a>`u_clamp` [lid cavity] | Velocity clamp | 0.05 |  | LBM velocity | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:159 • 0922758 | Mach control cap |
| <a id="const-Ma_max"></a>`Ma_max` [lid cavity] | Max Mach number | 0.10 |  | nondimensional | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:161 • 0922758 | Compressibility cap |
| <a id="const-div_target"></a>`div_target` [lid cavity] | Divergence target | 1e-6 |  | 1/time | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:162 • 0922758 | L2 divergence acceptance |
| <a id="const-stream_density"></a>`stream_density` [lid cavity] | Streamline density | 1.2 |  | nondimensional | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:165 • 0922758 | Plot streamline spacing |
| <a id="const-psi_iters"></a>`psi_iters` [lid cavity] | Poisson max iterations | 400 |  | integer | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:166 • 0922758 | Streamfunction solver |
| <a id="const-psi_tol"></a>`psi_tol` [lid cavity] | Poisson tolerance | 1e-3 |  | nondimensional | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:167 • 0922758 | Streamfunction residual |
| <a id="const-k_Ma"></a>`k_Ma` [lid controller] | Mach control gain | 0.50 |  | nondimensional | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:94 • 0922758 | Lid velocity adaptation rate |
| <a id="const-k_Re"></a>`k_Re` [lid controller] | Reynolds control gain | 0.10 |  | nondimensional | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:95 • 0922758 | $\tau$ adaptation rate |
| <a id="const-tau_min"></a>`tau_min` [lid controller] | Min relaxation time | 0.51 |  | LBM time | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:129 • 0922758 | Lower $\tau$ clamp |
| <a id="const-tau_max"></a>`tau_max` [lid controller] | Max relaxation time | 1.95 |  | LBM time | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:129 • 0922758 | Upper $\tau$ clamp |
| <a id="const-g-ms"></a>`g` [memory steering] | Void gain (memory) | 0.12 |  | nondimensional | derivation/code/physics/memory_steering/memory_steering_acceptance.py:18 • 0922758 | Default exploration/retention gain |
| <a id="const-lam-ms"></a>`lam` [memory steering] | Retention parameter | 0.08 |  | nondimensional | derivation/code/physics/memory_steering/memory_steering_acceptance.py:19 • 0922758 | Memory decay factor |
| <a id="const-steps-ms"></a>`steps` [memory steering] | Time steps | 512 |  | time steps | derivation/code/physics/memory_steering/memory_steering_acceptance.py:17 • 0922758 | Default run length |
| <a id="const-noise_std-ms"></a>`noise_std` [memory steering] | Noise amplitude | 0.0 |  | field units | derivation/code/physics/memory_steering/memory_steering_acceptance.py:20 • 0922758 | Stochastic perturbation |
| <a id="const-MS_LOGISTIC_R2_MIN"></a>`MS_LOGISTIC_R2_MIN` | Junction logistic R² gate | 0.95 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:479 • 0922758 | Fit quality threshold |
| <a id="const-MS_LOGISTIC_X0_ABS_MAX"></a>`MS_LOGISTIC_X0_ABS_MAX` | Junction center max | 0.25 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:480 • 0922758 | Logistic x0 limit |
| <a id="const-MS_CURV_R2_MIN"></a>`MS_CURV_R2_MIN` | Curvature R² gate | 0.65 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:482 • 0922758 | Fit quality threshold |
| <a id="const-MS_CURV_SLOPE_MIN"></a>`MS_CURV_SLOPE_MIN` | Curvature slope gate | 0.0 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:483 • 0922758 | Minimum positive slope |
| <a id="const-MS_CURV_R_MIN"></a>`MS_CURV_R_MIN` | Curvature Pearson R gate | 0.80 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:484 • 0922758 | Correlation threshold |
| <a id="const-MS_SIGNED_PASS_MIN"></a>`MS_SIGNED_PASS_MIN` | Signed invariance gate | 0.70 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:486 • 0922758 | Sign consistency pass rate |
| <a id="const-MS_STAB_DRET_MIN"></a>`MS_STAB_DRET_MIN` | Stability retention delta gate | 0.05 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:488 • 0922758 | Min retention increase |
| <a id="const-MS_STAB_DFID_MIN"></a>`MS_STAB_DFID_MIN` | Stability fidelity delta gate | 0.10 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:489 • 0922758 | Min fidelity increase |
| <a id="const-MS_STAB_FIDSHUF_ABS_MAX"></a>`MS_STAB_FIDSHUF_ABS_MAX` | Fidelity shuffle max | 0.20 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:490 • 0922758 | Control shuffle limit |
| <a id="const-MS_STAB_AUC_ROB_MIN"></a>`MS_STAB_AUC_ROB_MIN` | Stability AUC robust gate | 0.65 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:491 • 0922758 | Robust AUC threshold |
| <a id="const-MS_STAB_SNR_ROB_MIN"></a>`MS_STAB_SNR_ROB_MIN` | Stability SNR robust gate | 0.50 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:492 • 0922758 | Robust SNR threshold |
| <a id="const-MS_STAB_GAMMA_SLICE_DFID_MIN"></a>`MS_STAB_GAMMA_SLICE_DFID_MIN` | Gamma slice fidelity delta gate | 0.10 |  | nondimensional | derivation/code/physics/memory_steering/plot_memory_steering.py:493 • 0922758 | Per-gamma fidelity min |
| <a id="const-FUM_UI_TAIL_CAP_BYTES"></a>`FUM_UI_TAIL_CAP_BYTES` | UI tail initial cap | 1048576 |  | bytes | fum_rt/frontend/utilities/tail.py:50 • 0922758 | 1 MB default window |
| <a id="const-FUM_UI_TAIL_MAX_DELTA_BYTES"></a>`FUM_UI_TAIL_MAX_DELTA_BYTES` | UI tail max delta | 131072 |  | bytes | fum_rt/frontend/utilities/tail.py:51 • 0922758 | 128 KB max per tick |
| <a id="const-FUM_UI_TAIL_MAX_LINES"></a>`FUM_UI_TAIL_MAX_LINES` | UI tail max lines | 600 |  | lines | fum_rt/frontend/utilities/tail.py:52 • 0922758 | Max JSONL parsed/tick |
| <a id="const-neurons"></a>`neurons` [dashboard] | Network size | 1000 |  | integer | fum_rt/frontend/utilities/profiles.py:44 • 0922758 | Default neuron count |
| <a id="const-k-dash"></a>`k` [dashboard] | Connectome degree | 12 |  | integer | fum_rt/frontend/utilities/profiles.py:45 • 0922758 | Average connections per node |
| <a id="const-hz"></a>`hz` [dashboard] | Tick rate | 10 |  | Hz | fum_rt/frontend/utilities/profiles.py:46 • 0922758 | Simulation frequency |
| <a id="const-threshold"></a>`threshold` [dashboard] | Active edge threshold | 0.15 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:50 • 0922758 | Connectome pruning |
| <a id="const-lambda_omega"></a>`lambda_omega` [dashboard] | Void penalty | 0.10 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:51 • 0922758 | Exploration cost |
| <a id="const-candidates"></a>`candidates` [dashboard] | Candidate budget | 64 |  | integer | fum_rt/frontend/utilities/profiles.py:52 • 0922758 | Growth candidates |
| <a id="const-walkers"></a>`walkers` [dashboard] | Walker count | 256 |  | integer | fum_rt/frontend/utilities/profiles.py:53 • 0922758 | Connectome traversal walkers |
| <a id="const-hops"></a>`hops` [dashboard] | Walker hops | 3 |  | integer | fum_rt/frontend/utilities/profiles.py:54 • 0922758 | Traversal depth |
| <a id="const-bundle_size"></a>`bundle_size` [dashboard] | Bundle size | 3 |  | integer | fum_rt/frontend/utilities/profiles.py:55 • 0922758 | Edge bundling |
| <a id="const-prune_factor"></a>`prune_factor` [dashboard] | Prune factor | 0.10 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:56 • 0922758 | Homeostasis pruning |
| <a id="const-speak_z"></a>`speak_z` [dashboard] | Speak Z-score | 3.0 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:61 • 0922758 | B1 detector threshold |
| <a id="const-speak_hysteresis"></a>`speak_hysteresis` [dashboard] | Speak hysteresis | 0.5 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:62 • 0922758 | B1 hysteresis band |
| <a id="const-speak_cooldown_ticks"></a>`speak_cooldown_ticks` [dashboard] | Speak cooldown | 10 |  | ticks | fum_rt/frontend/utilities/profiles.py:63 • 0922758 | Minimum interval |
| <a id="const-speak_valence_thresh"></a>`speak_valence_thresh` [dashboard] | Speak valence threshold | 0.55 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:64 • 0922758 | Valence gate |
| <a id="const-b1_half_life_ticks"></a>`b1_half_life_ticks` [dashboard] | B1 half-life | 50 |  | ticks | fum_rt/frontend/utilities/profiles.py:65 • 0922758 | B1 signal decay |
| <a id="const-stim_group_size"></a>`stim_group_size` [dashboard] | Stimulus group size | 8 |  | integer | fum_rt/frontend/utilities/profiles.py:66 • 0922758 | Neurons per stimulus |
| <a id="const-stim_amp"></a>`stim_amp` [dashboard] | Stimulus amplitude | 0.08 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:67 • 0922758 | Stimulus strength |
| <a id="const-stim_decay"></a>`stim_decay` [dashboard] | Stimulus decay | 0.92 |  | nondimensional | fum_rt/frontend/utilities/profiles.py:68 • 0922758 | Per-tick decay factor |
| <a id="const-stim_max_symbols"></a>`stim_max_symbols` [dashboard] | Max stimulus symbols | 128 |  | integer | fum_rt/frontend/utilities/profiles.py:69 • 0922758 | Symbol vocabulary cap |
| <a id="const-checkpoint_every"></a>`checkpoint_every` [dashboard] | Checkpoint interval | 60 |  | seconds | fum_rt/frontend/utilities/profiles.py:70 • 0922758 | Engram save frequency |
| <a id="const-checkpoint_keep"></a>`checkpoint_keep` [dashboard] | Checkpoint retention | 5 |  | integer | fum_rt/frontend/utilities/profiles.py:71 • 0922758 | Max checkpoints kept |
| <a id="const-speak_z_0"></a>`speak_z` [phase 0] | Speak Z-score (primitives) | 2.0 |  | nondimensional | fum_rt/runtime/phase.py:34 • 0922758 | Phase 0 gate |
| <a id="const-speak_hysteresis_0"></a>`speak_hysteresis` [phase 0] | Speak hysteresis (primitives) | 0.5 |  | nondimensional | fum_rt/runtime/phase.py:34 • 0922758 | Phase 0 band |
| <a id="const-speak_cooldown_ticks_0"></a>`speak_cooldown_ticks` [phase 0] | Speak cooldown (primitives) | 8 |  | ticks | fum_rt/runtime/phase.py:34 • 0922758 | Phase 0 interval |
| <a id="const-speak_valence_thresh_0"></a>`speak_valence_thresh` [phase 0] | Speak valence (primitives) | 0.10 |  | nondimensional | fum_rt/runtime/phase.py:34 • 0922758 | Phase 0 valence |
| <a id="const-walkers_0"></a>`walkers` [phase 0] | Walkers (primitives) | 128 |  | integer | fum_rt/runtime/phase.py:35 • 0922758 | Phase 0 walkers |
| <a id="const-hops_0"></a>`hops` [phase 0] | Hops (primitives) | 3 |  | integer | fum_rt/runtime/phase.py:35 • 0922758 | Phase 0 depth |
| <a id="const-bundle_size_0"></a>`bundle_size` [phase 0] | Bundle size (primitives) | 3 |  | integer | fum_rt/runtime/phase.py:35 • 0922758 | Phase 0 bundling |
| <a id="const-prune_factor_0"></a>`prune_factor` [phase 0] | Prune factor (primitives) | 0.10 |  | nondimensional | fum_rt/runtime/phase.py:35 • 0922758 | Phase 0 pruning |
| <a id="const-speak_z_1"></a>`speak_z` [phase 1] | Speak Z-score (blocks) | 2.5 |  | nondimensional | fum_rt/runtime/phase.py:40 • 0922758 | Phase 1 gate |
| <a id="const-speak_hysteresis_1"></a>`speak_hysteresis` [phase 1] | Speak hysteresis (blocks) | 0.8 |  | nondimensional | fum_rt/runtime/phase.py:40 • 0922758 | Phase 1 band |
| <a id="const-speak_cooldown_ticks_1"></a>`speak_cooldown_ticks` [phase 1] | Speak cooldown (blocks) | 10 |  | ticks | fum_rt/runtime/phase.py:40 • 0922758 | Phase 1 interval |
| <a id="const-speak_valence_thresh_1"></a>`speak_valence_thresh` [phase 1] | Speak valence (blocks) | 0.20 |  | nondimensional | fum_rt/runtime/phase.py:40 • 0922758 | Phase 1 valence |
| <a id="const-walkers_1"></a>`walkers` [phase 1] | Walkers (blocks) | 256 |  | integer | fum_rt/runtime/phase.py:41 • 0922758 | Phase 1 walkers |
| <a id="const-speak_z_2"></a>`speak_z` [phase 2] | Speak Z-score (structures) | 3.0 |  | nondimensional | fum_rt/runtime/phase.py:45 • 0922758 | Phase 2 gate |
| <a id="const-speak_hysteresis_2"></a>`speak_hysteresis` [phase 2] | Speak hysteresis (structures) | 1.0 |  | nondimensional | fum_rt/runtime/phase.py:45 • 0922758 | Phase 2 band |
| <a id="const-speak_cooldown_ticks_2"></a>`speak_cooldown_ticks` [phase 2] | Speak cooldown (structures) | 10 |  | ticks | fum_rt/runtime/phase.py:45 • 0922758 | Phase 2 interval |
| <a id="const-speak_valence_thresh_2"></a>`speak_valence_thresh` [phase 2] | Speak valence (structures) | 0.35 |  | nondimensional | fum_rt/runtime/phase.py:45 • 0922758 | Phase 2 valence |
| <a id="const-walkers_2"></a>`walkers` [phase 2] | Walkers (structures) | 384 |  | integer | fum_rt/runtime/phase.py:46 • 0922758 | Phase 2 walkers |
| <a id="const-hops_2"></a>`hops` [phase 2] | Hops (structures) | 4 |  | integer | fum_rt/runtime/phase.py:46 • 0922758 | Phase 2 depth |
| <a id="const-speak_z_3"></a>`speak_z` [phase 3] | Speak Z-score (questions) | 3.0 |  | nondimensional | fum_rt/runtime/phase.py:50 • 0922758 | Phase 3 gate |
| <a id="const-speak_hysteresis_3"></a>`speak_hysteresis` [phase 3] | Speak hysteresis (questions) | 1.0 |  | nondimensional | fum_rt/runtime/phase.py:50 • 0922758 | Phase 3 band |
| <a id="const-speak_cooldown_ticks_3"></a>`speak_cooldown_ticks` [phase 3] | Speak cooldown (questions) | 10 |  | ticks | fum_rt/runtime/phase.py:50 • 0922758 | Phase 3 interval |
| <a id="const-speak_valence_thresh_3"></a>`speak_valence_thresh` [phase 3] | Speak valence (questions) | 0.55 |  | nondimensional | fum_rt/runtime/phase.py:50 • 0922758 | Phase 3 valence |
| <a id="const-walkers_3"></a>`walkers` [phase 3] | Walkers (questions) | 512 |  | integer | fum_rt/runtime/phase.py:51 • 0922758 | Phase 3 walkers |
| <a id="const-hops_3"></a>`hops` [phase 3] | Hops (questions) | 4 |  | integer | fum_rt/runtime/phase.py:51 • 0922758 | Phase 3 depth |
| <a id="const-speak_z_4"></a>`speak_z` [phase 4] | Speak Z-score (problem-solving) | 3.5 |  | nondimensional | fum_rt/runtime/phase.py:55 • 0922758 | Phase 4 gate |
| <a id="const-speak_hysteresis_4"></a>`speak_hysteresis` [phase 4] | Speak hysteresis (problem-solving) | 1.2 |  | nondimensional | fum_rt/runtime/phase.py:55 • 0922758 | Phase 4 band |
| <a id="const-speak_cooldown_ticks_4"></a>`speak_cooldown_ticks` [phase 4] | Speak cooldown (problem-solving) | 12 |  | ticks | fum_rt/runtime/phase.py:55 • 0922758 | Phase 4 interval |
| <a id="const-speak_valence_thresh_4"></a>`speak_valence_thresh` [phase 4] | Speak valence (problem-solving) | 0.60 |  | nondimensional | fum_rt/runtime/phase.py:55 • 0922758 | Phase 4 valence |
| <a id="const-walkers_4"></a>`walkers` [phase 4] | Walkers (problem-solving) | 768 |  | integer | fum_rt/runtime/phase.py:56 • 0922758 | Phase 4 walkers |
| <a id="const-hops_4"></a>`hops` [phase 4] | Hops (problem-solving) | 5 |  | integer | fum_rt/runtime/phase.py:56 • 0922758 | Phase 4 depth |
| <a id="const-composer_idf_k"></a>`composer_idf_k` [all phases] | Composer IDF novelty gain | 0.0 |  | nondimensional | fum_rt/runtime/phase.py:37,42,47,52,57 • 0922758 | Discovery weight (safe default 0) |
| <a id="const-nu-typical"></a> $\nu$ [LBM typical] | Kinematic viscosity | 0.1333 |  | LBM units | derivation/DIMENSIONLESS_CONSTANTS.md:16; VDM_Overview.md:81 • 0922758 | $\nu = \frac{1}{3}(\tau - \frac{1}{2})$ for $\tau=0.9$ |
| <a id="const-Re-64"></a>$\mathrm{Re}$ [LBM 64²] | Reynolds number (64²) | 9.6 |  | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:17; VDM_Overview.md:82 • 0922758 | $\mathrm{Re} = UL/\nu$ |
| <a id="const-Re-128"></a>$\mathrm{Re}$ [LBM 128²] | Reynolds number (128²) | 19.2 |  | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:17; VDM_Overview.md:82 • 0922758 | $\mathrm{Re} = UL/\nu$ |
| <a id="const-Ma-low"></a>$\mathrm{Ma}$ [LBM typical] | Mach number range | 0.017-0.035 |  | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:18; VDM_Overview.md:83 • 0922758 | $\mathrm{Ma} = U/\sqrt{1/3}$ (low compressibility) |
| <a id="const-c_star"></a> $c^*$ [RD normalized] | Normalized KPP speed | 0.95-1.0 |  | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:20; VDM_Overview.md:85 • 0922758 | $c^* = c/(2\sqrt{Dr})$ |
| <a id="const-Theta"></a> $\Theta$ [VDM junction] | Junction gating strength | $k \approx 1, b \approx 0$ |  | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:21; VDM_Overview.md:86 • 0922758 | Fit scale in $\Theta \Delta m$ or $\Theta \|\nabla m\|$ |
| <a id="const-Gamma"></a> $\Gamma$ [VDM retention] | Retention fraction | 0.3-0.75 |  | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:23; VDM_Overview.md:88 • 0922758 | Memory persistence (representative avg from plots) |
| <a id="const-D_a"></a> $D_a$ [VDM anisotropic] | Anisotropic diffusion index | {1, 3, 5, 7} |  | nondimensional | derivation/DIMENSIONLESS_CONSTANTS.md:24; VDM_Overview.md:89 • 0922758 | Transport anisotropy discrete values |

<!-- BEGIN AUTOSECTION: CONSTANTS-INDEX -->
<!-- Tool-maintained list of [Name](#const-...) anchors -->
[ALPHA](#const-alpha) • [BETA](#const-beta) • [CS2](#const-cs2) • [F_REF](#const-f_ref) • [PHASE_SENS](#const-phase_sens) • [D](#const-D) • [r](#const-r) • [N](#const-N) • [L](#const-L) • [T](#const-T) • [cfl](#const-cfl) • [seed](#const-seed) • [record](#const-record) • [amp0](#const-amp0) • [m_max](#const-m_max) • [x0](#const-x0) • [level](#const-level) • [acceptance_rel_err](#const-acceptance_rel_err) • [τ](#const-tau-lbm) • [tau (lid)](#const-tau-lid) • [tau (Taylor-Green)](#const-tau-taylor) • [nx](#const-nx) • [ny](#const-ny) • [U_lid](#const-U_lid) • [U0](#const-U0) • [k (Taylor-Green)](#const-k-tg) • [steps (lid)](#const-steps-lid) • [steps (Taylor-Green)](#const-steps-taylor) • [sample_every (lid)](#const-sample_every-lid) • [sample_every (Taylor-Green)](#const-sample_every-taylor) • [warmup](#const-warmup) • [void_gain](#const-void_gain) • [u_clamp](#const-u_clamp) • [Ma_max](#const-Ma_max) • [div_target](#const-div_target) • [stream_density](#const-stream_density) • [psi_iters](#const-psi_iters) • [psi_tol](#const-psi_tol) • [k_Ma](#const-k_Ma) • [k_Re](#const-k_Re) • [tau_min](#const-tau_min) • [tau_max](#const-tau_max) • [g (memory steering)](#const-g-ms) • [lam (memory steering)](#const-lam-ms) • [steps (memory steering)](#const-steps-ms) • [noise_std](#const-noise_std-ms) • [MS_LOGISTIC_R2_MIN](#const-MS_LOGISTIC_R2_MIN) • [MS_LOGISTIC_X0_ABS_MAX](#const-MS_LOGISTIC_X0_ABS_MAX) • [MS_CURV_R2_MIN](#const-MS_CURV_R2_MIN) • [MS_CURV_SLOPE_MIN](#const-MS_CURV_SLOPE_MIN) • [MS_CURV_R_MIN](#const-MS_CURV_R_MIN) • [MS_SIGNED_PASS_MIN](#const-MS_SIGNED_PASS_MIN) • [MS_STAB_DRET_MIN](#const-MS_STAB_DRET_MIN) • [MS_STAB_DFID_MIN](#const-MS_STAB_DFID_MIN) • [MS_STAB_FIDSHUF_ABS_MAX](#const-MS_STAB_FIDSHUF_ABS_MAX) • [MS_STAB_AUC_ROB_MIN](#const-MS_STAB_AUC_ROB_MIN) • [MS_STAB_SNR_ROB_MIN](#const-MS_STAB_SNR_ROB_MIN) • [MS_STAB_GAMMA_SLICE_DFID_MIN](#const-MS_STAB_GAMMA_SLICE_DFID_MIN) • [FUM_UI_TAIL_CAP_BYTES](#const-FUM_UI_TAIL_CAP_BYTES) • [FUM_UI_TAIL_MAX_DELTA_BYTES](#const-FUM_UI_TAIL_MAX_DELTA_BYTES) • [FUM_UI_TAIL_MAX_LINES](#const-FUM_UI_TAIL_MAX_LINES) • [neurons](#const-neurons) • [k (dashboard)](#const-k-dash) • [hz](#const-hz) • [threshold](#const-threshold) • [lambda_omega](#const-lambda_omega) • [candidates](#const-candidates) • [walkers (dashboard)](#const-walkers) • [hops (dashboard)](#const-hops) • [bundle_size (dashboard)](#const-bundle_size) • [prune_factor (dashboard)](#const-prune_factor) • [speak_z (dashboard)](#const-speak_z) • [speak_hysteresis (dashboard)](#const-speak_hysteresis) • [speak_cooldown_ticks (dashboard)](#const-speak_cooldown_ticks) • [speak_valence_thresh (dashboard)](#const-speak_valence_thresh) • [b1_half_life_ticks](#const-b1_half_life_ticks) • [stim_group_size](#const-stim_group_size) • [stim_amp](#const-stim_amp) • [stim_decay](#const-stim_decay) • [stim_max_symbols](#const-stim_max_symbols) • [checkpoint_every](#const-checkpoint_every) • [checkpoint_keep](#const-checkpoint_keep) • [speak_z (phase 0)](#const-speak_z_0) • [speak_hysteresis (phase 0)](#const-speak_hysteresis_0) • [speak_cooldown_ticks (phase 0)](#const-speak_cooldown_ticks_0) • [speak_valence_thresh (phase 0)](#const-speak_valence_thresh_0) • [walkers (phase 0)](#const-walkers_0) • [hops (phase 0)](#const-hops_0) • [bundle_size (phase 0)](#const-bundle_size_0) • [prune_factor (phase 0)](#const-prune_factor_0) • [speak_z (phase 1)](#const-speak_z_1) • [speak_hysteresis (phase 1)](#const-speak_hysteresis_1) • [speak_cooldown_ticks (phase 1)](#const-speak_cooldown_ticks_1) • [speak_valence_thresh (phase 1)](#const-speak_valence_thresh_1) • [walkers (phase 1)](#const-walkers_1) • [speak_z (phase 2)](#const-speak_z_2) • [speak_hysteresis (phase 2)](#const-speak_hysteresis_2) • [speak_cooldown_ticks (phase 2)](#const-speak_cooldown_ticks_2) • [speak_valence_thresh (phase 2)](#const-speak_valence_thresh_2) • [walkers (phase 2)](#const-walkers_2) • [hops (phase 2)](#const-hops_2) • [speak_z (phase 3)](#const-speak_z_3) • [speak_hysteresis (phase 3)](#const-speak_hysteresis_3) • [speak_cooldown_ticks (phase 3)](#const-speak_cooldown_ticks_3) • [speak_valence_thresh (phase 3)](#const-speak_valence_thresh_3) • [walkers (phase 3)](#const-walkers_3) • [hops (phase 3)](#const-hops_3) • [speak_z (phase 4)](#const-speak_z_4) • [speak_hysteresis (phase 4)](#const-speak_hysteresis_4) • [speak_cooldown_ticks (phase 4)](#const-speak_cooldown_ticks_4) • [speak_valence_thresh (phase 4)](#const-speak_valence_thresh_4) • [walkers (phase 4)](#const-walkers_4) • [hops (phase 4)](#const-hops_4) • [composer_idf_k](#const-composer_idf_k) • [ν](#const-nu-typical) • [Re (64²)](#const-Re-64) • [Re (128²)](#const-Re-128) • [Ma](#const-Ma-low) • [c*](#const-c_star) • [Θ](#const-Theta) • [Γ](#const-Gamma) • [D_a](#const-D_a)
<!-- END AUTOSECTION: CONSTANTS-INDEX -->


GPT-5:
Totally-here are **append-ready rows** for your **VDM Constants & Defaults (Auto-compiled)** table, matching your exact 7-column schema, anchor style, and bracketed context labels. Paste these under the existing rows.

```markdown
| <a id="const-E_grid-agency"></a>`E_grid` [agency probe] | Energy budgets tested | [2, 3, 4, 5, 6, 7, 8, 9, 10] | integers | steps | derivation/code/agency/simulate_options_probe.py:… • HEAD | Reproducible sweep for useful-entropy heatmap |
| <a id="const-p_slip_grid-agency"></a>`p_slip_grid` [agency probe] | Slip probabilities tested | [0.00, 0.10, 0.20, 0.30] | [0, 1] | nondimensional | derivation/code/agency/simulate_options_probe.py:… • HEAD | Per-step actuator slip |
| <a id="const-V_targets_bits-agency"></a>`V_targets_bits` [agency probe] | Capability iso-levels | [3, 5, 7] |  | bits | derivation/code/agency/simulate_options_probe.py:… • HEAD | For threshold curves $E_{\min}^{(v_0)}(p)$ |
| <a id="const-n_act-agency"></a>`n_act` [agency probe] | Actuator count | 4 |  | integer | derivation/code/agency/simulate_options_probe.py:… • HEAD | Context for options availability |
```

If you want the finite-difference tolerances that the equations reference to live here too, add these two as well:

```markdown
| <a id="const-eps-fd-agency"></a>`EPS_FD` [agency probe] | Finite-diff tolerance | 1e-9 |  | nondimensional | derivation/code/agency/simulate_options_probe.py:… • HEAD | Used in gradient/monotonicity checks |
| <a id="const-eps-mono-agency"></a>`EPS_MONO` [agency probe] | Monotonicity tolerance | 1e-9 |  | nondimensional | derivation/code/agency/simulate_options_probe.py:… • HEAD | Accept ties within tolerance |
```

### Index update (same one-line format)

Add these tokens into the **AUTOSECTION: CONSTANTS-INDEX** block so your anchors are discoverable:

```
• [E_grid (agency)](#const-E_grid-agency) • [p_slip_grid (agency)](#const-p_slip_grid-agency) • [V_targets_bits (agency)](#const-V_targets_bits-agency) • [n_act (agency)](#const-n_act-agency) • [EPS_FD (agency)](#const-eps-fd-agency) • [EPS_MONO (agency)](#const-eps-mono-agency)
```

This keeps agency constants first-class citizens in your canon, so EQUATIONS/SYMBOLS/UNITS can point at a single numeric source and your CI can grep one file to verify drift.


Justin:
Can you take a look and determine if any agency stuff should be added here?



GPT-5:
Short version: the **options-probe** itself is parametric (grid over (E) and (p_{\text{slip}})), so it doesn’t belong in a BC/IC/geometry doc. You’re good there.

Where agency *does* touch this file is when walkers or any “agency field” actually live on a spatial lattice (same grid you already use for `walker_glow`). In that case, adding a couple of BCs and ICs makes your canon complete and prevents future ambiguity about “edge-of-domain behavior.”

Below are **append-ready blocks** that match your current format and stay within the doc’s scope. They reuse your existing `walker-box-2d` geometry, so no duplicate geometry row needed.

---

### Add under **2) Boundary Conditions (by geometry and field/channel)**

##### Absorbing (Dirichlet) boundary for agency walkers  <a id="bc-absorbing-agency-walkers"></a>

**Context:** AGENCY_FIELD_V2.md:§Runtime Walkers • observability/gating runs (agency)
**Field(s):** Walker positions (X); optional agency map (M) (read-only)
**Type:** Absorbing / Dirichlet (out-of-domain removal)
**Definition (quote from source if formula exists):**
Walkers that step outside (\Omega) are removed from the simulation at that step (no re-injection or wrap). If a scalar field (M) is logged, enforce (M|_{\partial\Omega}=0) for visualization.

**Applies on:** All boundaries of [walker-box-2d](#geom-walker-box-2d)
**Parameters:** None
**Implemented at:** - (spec; planned alongside agency walker runtime)
**Notes:** Models “cliff” domains where leaving the workspace terminates control; reduces reachable option-space near walls, which measurably lowers (V_{\text{useful_bits}}) under identical noise.

---

##### Reflecting (specular) boundary for agency walkers  <a id="bc-reflecting-agency-walkers"></a>

**Context:** AGENCY_FIELD_V2.md:§Runtime Walkers • explorative runs (agency)
**Field(s):** Walker positions (X); optional agency map (M) (read-only)
**Type:** Reflecting / Neumann-like (specular reflection)
**Definition (quote from source if formula exists):**
On attempted step (\Delta x) that exits (\Omega), reflect the normal component at the boundary:
(\Delta x_{\perp} \leftarrow -\Delta x_{\perp}), (\Delta x_{\parallel}) unchanged; then apply the reflected step.

**Applies on:** All boundaries of [walker-box-2d](#geom-walker-box-2d)
**Parameters:** None
**Implemented at:** - (spec; planned alongside agency walker runtime)
**Notes:** Preserves mass of walkers; appropriate when physical walls exist but agents can “bounce.” Typically raises reachable option-space vs. absorbing, shifting agency thresholds.

---

### Add under **3) Initial Conditions**

##### Uniform quiescent agency field  <a id="ic-agency-field-quiescent"></a>

**Context:** AGENCY_FIELD_V2.md:§Field Definition • cold-start runs
**Quantity:** Agency map (M(\mathbf{x},0)) (capability/affordance density; read-only for probes)
**Definition (quote from source if formula exists):**
(M(\mathbf{x},0) = 0) on (\Omega).

**Parameters:** None
**Randomization/Seeds:** None (deterministic)
**Applies to Geometry:** [walker-box-2d](#geom-walker-box-2d)
**Notes:** Clean baseline for observing how walkers and constraints imprint structure; pairs with absorbing or reflecting BCs above.

---

##### Seeded walker distribution (Poisson)  <a id="ic-agency-walkers-poisson"></a>

**Context:** AGENCY_FIELD_V2.md:§Runtime Walkers • default seeding
**Quantity:** Walker set ({X_k(0)}_{k=1}^{N_w})
**Definition (quote from source if formula exists):**
Sample (N_w) initial positions i.i.d. uniform on (\Omega) (Poisson disc optional).

**Parameters:** (N_w) (see `walkers` in CONSTANTS.md)
**Randomization/Seeds:** Use `seed`<sup>[↗](CONSTANTS.md#const-seed)</sup> to control RNG for reproducibility
**Applies to Geometry:** [walker-box-2d](#geom-walker-box-2d)
**Notes:** Matches your other ICs: deterministic when seeded; supports side-by-side BC comparisons for agency thresholds.

---

### (Optional) Add under **4) Lattice/Stencil & Neighbor Topology**-only if your agency walkers use 8-neighbors

| <a id="lattice-moore-8"></a>**moore-8** | 2D Moore (8-neighbor) | Neighbors (N(i)={\text{N,S,E,W,NE,NW,SE,SW}}) | (N_y \times N_x), spacing (a) | - (spec) | If agency walkers step diagonally as well as axially |

---

#### What not to add here

* The **options heatmap** and (V_{\text{useful_bits}}) gradients are **parameter-space artifacts**, not spatial fields. Keep them in `DATA_PRODUCTS.md`, `EQUATIONS.md`, and `CONSTANTS.md` (which you already wired). This file should only cover spatial **Ω**, **BC/IC**, and **stencils**.

If you decide to make the agency map (M) dynamic (not just read-only), we can add a flux-form BC block mirroring your RD entry, but for now the four snippets above give you canonical answers to “what happens at the walls?” for agency runs.


Justin:
math here isnt rendering right

**Notes:** Models “cliff” domains where leaving the workspace terminates control; reduces reachable option-space near walls, which measurably lowers (V_{\text{useful_bits}}) under identical noise.

GPT-5:
Yup-two tiny gotchas tripped you:

1. you didn’t wrap the math in `$…$`, and
2. underscores inside `\text{...}` must be escaped (`\_`).

Here’s the single-line fix you wanted:

```markdown
**Notes:** Models “cliff” domains where leaving the workspace terminates control; reduces reachable option-space near walls, which measurably lowers $V_{\text{useful\_bits}}$ under identical noise.
```

If you want literal parentheses in prose, do `($V_{\text{useful\_bits}}$)`.

Bonus: here are the two BC blocks rewritten with **GitHub-safe inline math** (`$...$` everywhere) so everything renders cleanly.

**Absorbing (Dirichlet) boundary for agency walkers**

```markdown
**Definition:** Walkers that step outside $\Omega$ are removed from the simulation at that step (no re-injection or wrap). If a scalar field $M$ is logged, enforce $M\!\mid_{\partial\Omega}=0$ for visualization.

**Notes:** Models “cliff” domains where leaving the workspace terminates control; reduces reachable option-space near walls, which measurably lowers $V_{\text{useful\_bits}}$ under identical noise.
```

**Reflecting (specular) boundary for agency walkers**

```markdown
**Definition:** On attempted step $\Delta x$ that exits $\Omega$, reflect the normal component at the boundary: $\Delta x_{\perp}\leftarrow-\Delta x_{\perp}$, $\Delta x_{\parallel}$ unchanged; then apply the reflected step.

**Notes:** Preserves walker mass; appropriate when physical walls exist but agents can “bounce.” Typically raises reachable option-space vs. absorbing, shifting $E_{\min}^{(v_0)}(p)$ downward for the same $v_0$.
```

Quick lint trick to catch this class of miss:

* Search for `\( *V_` or `V_{\w` not preceded by `$`, and for `\text{.*_.*}` without `\_`.
