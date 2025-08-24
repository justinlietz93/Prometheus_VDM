# Void-announcers for neural networks: passive observability and bounded numeric control

Status: [PLAUSIBLE] with concrete validation plan. Physics conserved (read-only sensing); optional bounded parameter advice does not inject forces.

Purpose
- Map FUVDM “void walker” observability to neural networks (MLP/RNN/attention) as measurement-only sensors.
- Derive a graph Fokker–Planck limit for walker density on a feed-forward graph.
- Define petition taxonomy (sat, grad, shear) and a scalar “void debt” functional.
- Outline a bounded advisory policy to nudge numeric knobs without altering forward dynamics.

Starting Assumptions
- Network f: R^{d_in} -> R^{d_out} with L layers; activations a^{(l)} = φ(z^{(l)}), z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}.
- Nonlinearity φ ∈ {tanh, ReLU, GELU}. We take tanh for smoothness unless stated otherwise.
- “Walker” lives on the bipartite graph of edges (i->j,l): from neuron i at layer l-1 to neuron j at layer l.
- Walkers are read-only: they sample fields and never modify weights/activations.

Discrete Formulation (graph random walk)
- Define local edge saliency S_{i→j}^{(l)} = |W_{ji}^{(l)}| · |a_i^{(l-1)}|.
- Transition probability from node i at layer l-1 to j at layer l:
  p(i→j|l) = S_{i→j}^{(l)} / Σ_k S_{i→k}^{(l)} with ε-jitter for exploration.
- After K hops along layers, each walker emits petitions at its current edge/node:
  sat: σ_sat = 1{|a_j^{(l)}| ≥ a_sat}, grad: g_j^{(l)} = ||∂L/∂z_j^{(l)}|| (if L defined), shear: max{|a_j^{(l)} − a_k^{(l)}|: k∈N(j)}.
- Petitions are tuples (kind, value, node=(l,j), t). A Bus collects them; a Reducer computes robust quantiles and counts per kind.

Continuum Limit (graph Fokker–Planck heuristic)
- Let ρ_l(j,t) be walker density at neuron j, layer l.
- Assume slow variation in “potential” U_l(j) = −log S̄_l(j), where S̄_l(j) = Σ_i S_{i→j}^{(l)}.
- The discrete Markov chain induces, in a continuum limit over wide layers, a drift–diffusion:
  ∂_t ρ_l ≈ ∇_j · (D_l ∇_j ρ_l + ρ_l ∇_j U_l), with reflecting boundary at layer edges and forward drift across layers.
- D_l encodes exploration jitter; ∇_j is graph gradient (e.g., on a kNN graph in activation space).
- This equation is descriptive; walkers remain sampling artifacts and do not back-react.

Void-debt functional (diagnostic)
- Define D_void(t) = α_div · Q_div,99 + α_sat · Q_sat,95 + α_shear · Q_shear,95, where Q_kind,q are bus quantiles at time t.
- Interpretation: large divergence-like signals (compressibility analog), excessive saturation, and high same-layer shear imply “debt.”
- D_void is a ledger for where discretization/representation is near asymptotes (saturation, vanishing/exploding gradients).

Advisory policy (bounded, numeric knobs only)
- Inputs: stats_summary from Reducer, params = {τ (optimizer viscosity), u_clamp (gradient clip), U_in (input scale)}.
- Rules (example): if Q_div,99 > target_div ⇒ tighten u_clamp by ×0.9 and increase τ by +0.02.
  elif Q_swirl,50 < target_swirl and Q_div,99 < 2×target_div ⇒ decrease τ by 0.02 and allow 5% higher U_in.
- Guarantees: params are clipped to safe bounds; no forcing terms are added to forward dynamics.

Mapping table (fluids → nets)
- velocity u ↔ activation flow across layers
- divergence ∇·u ↔ Jacobian trace proxy tr(∂a^{(l)}/∂a^{(l-1)}) or gradient-norm concentration
- vorticity |ω| ↔ curvature/recirculation proxy: local loopiness in feature graph; here we use swirl := robust median |g_j^{(l)}|
- near-wall shear ↔ activation discontinuity between neighboring neurons (graph Laplacian magnitude)

Conservation / Lyapunov structure
- For tanh nets, E = Σ_l ||a^{(l)}||² is bounded; saturation petitions estimate proximity to hard bounds (|a|→1).
- The universal void dynamics W∈[0,1] (if attached per neuron as latent) has stable mean near ≈0.6 in many regimes.
- Without coupling back into forward dynamics, we treat W only as a state reported in telemetry (optional).

Numerical Validation Plan
Objective
- Demonstrate that announcer stats correlate with training instabilities and that observe/advise modes reduce D_void without harming accuracy.
Observable
- {Q_div,99, Q_sat,95, Q_shear,95}, accuracy curve, training loss, gradient norms.
Method
- Train a small tanh-MLP on a 2D classification task for T epochs with fixed seed.
- Run with announcers OFF vs ON (observe) vs ON (advise). Keep optimizer and data identical.
- Record metrics each epoch; compute ΔD_void and accuracy differences.
Acceptance Criteria
- Non-interference: forward outputs identical with announcers in observe mode (unit test).
- Advice utility: advise mode reduces median D_void by ≥10% at equal or better final accuracy on ≥2/3 seeds (N≥5).
Failure Modes
- Poor signal in grad for ReLU at initialization; use tanh or GELU for smoother proxies. Adjust a_sat.

Minimal prototype (to be provided)
- Script: code/physics/memory_steering/void_announcer_demo.py
- Uses the fluids telemetry Bus/Reducer (imported) and a simple MLP.
- Emits logs → derivation/code/outputs/logs/memory_steering and a diagnostic figure with petition markers on hidden-layer index space.

Open Questions / Next Refinements
- Replace proxies with principled Jacobian-trace estimators per layer for divergence analog.
- Define a true graph vorticity via cycle decomposition on neuron-feature graphs.
- Couple universal void dynamics W as a reporter per neuron and test whether W̄→0.6 correlates with reduced D_void.
- Extend to attention: walkers hop on token–head–position graphs with saliency S∝|A|·|V|.

Reproducibility Checklist
- Fixed seeds; record version hash and environment.
- Log exact params and bounds of the advisory policy.
- Keep observe vs advise runs archived with JSON and PNG artifacts.

References
- Fluid mapping powered this construction; see cavity announcers and CLI in [lid_cavity_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:356).
- Bus, Reducer, Walker API: [walkers.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/telemetry/walkers.py:1).