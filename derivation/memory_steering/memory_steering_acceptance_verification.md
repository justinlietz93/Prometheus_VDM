# Memory Steering — Acceptance & Verification

Tags: [PLAUSIBLE→PROVEN], [STABILITY], [REPRODUCIBILITY], [NON-INTERFERENCE]
Date: 2025-08-21
Owner:Justin K. Lietz

Purpose
- Define quantitative acceptance criteria and a reproducible verification protocol for the “memory steering” mechanism.
- Verify boundedness, stability, fixed-point predictability, signal-to-noise improvement, Lyapunov monotonicity under canonical conditions, and reproducibility.
- Document the canonical “void equilibrium” target W ≈ 0.6 and its parameter mapping.

Starting Assumptions
- Memory variable M_t ∈ [0, 1].
- Steering uses a linear, leaky first-order update with saturation (assumed form):
  M_{t+1} = (1 − λ − g) M_t + g s_t + ξ_t, then clamp M_{t+1} to [0, 1].
  - Parameters: g > 0 (gain), λ > 0 (leak), ξ_t is optional zero-mean noise (default 0).
  - Stability (unclamped, deterministic): pole p = 1 − λ − g with 0 ≤ p < 1 implies stable monotone approach.
  - Fixed point for constant s: M* = g s / (g + λ).
- Canonical “void equilibrium” test: with s ≡ 1 and g = 1.5 λ, the fixed point is M* = 1.5/(1+1.5) = 0.6, matching the observed W ≈ 0.6 note.
- If the actual steering law differs (nonlinear f(s, M), adaptive gains, or additional couplings), we will update p, M*, and acceptance thresholds accordingly. Provide file path + line numbers for the exact rule to refine this doc.

Discrete Formulation
- Update (dt = 1):
  M_{t+1} − M_t = −(λ + g) M_t + g s_t + ξ_t; then clip to [0, 1].
- Step response for s = s1 (constant for t ≥ t_step): M_t = M* + (M_0 − M*) p^t with p = 1 − λ − g.

Continuum Limit (for small λ + g)
- Let dt ≪ 1 and identify κ = λ + g, γ = g. Then
  dM/dt = −κ M + γ s(t) + η(t), 0 ≤ M ≤ 1 with reflective saturation at bounds.
- Time constant τ ≈ 1/κ. In discrete time, τ_d = −1 / ln p; for small κ, τ_d ≈ 1/κ.

Fixed Points & Stability
- Fixed point M* = (g/(g+λ)) s for constant s (unclamped, noise-free).
- Linear stability: |p| < 1 ⇒ stable; for 0 ≤ p < 1, monotone approach without overshoot (in the linear, unclamped regime).
- With saturation, M remains bounded in [0, 1].

Lyapunov Structure (noise-free, constant s)
- Define F_t = 0.5 (M_t − M*)^2. Then M_{t+1} − M* = p (M_t − M*). Hence
  F_{t+1} − F_t = 0.5 (p^2 − 1) (M_t − M*)^2 ≤ 0 for |p| ≤ 1 with strict decrease for |p| < 1 unless M_t = M*.

Acceptance Criteria
1) Boundedness
   - No excursions outside [0, 1] after clamping: count_violations = 0 over default runs.

2) Linear Response & Fixed Point (noise-free, avoid clamp activation)
   - Fit pole from step response:
     - |p_fit − p_pred| ≤ 0.02 (absolute).
     - |M_final − M*| ≤ 1e-2 (mean over last 10% of samples).
     - Overshoot ≤ 0.02 (fraction of step amplitude).

3) Canonical Void Target (W ≈ 0.6)
   - With s ≡ 1 and g = 1.5 λ:
     - |M_final − 0.6| ≤ 0.02 across seeds ∈ {0, 1, 2}.

4) Noise Suppression (SNR Improvement)
   - Input s(t) = s_sig(t) + n(t), where s_sig is a low-frequency sinusoid and n is white noise (σ = 0.05 by default), values clipped to [0, 1].
   - SNR_out − SNR_in ≥ 3 dB for default parameters.

5) Lyapunov Monotonicity (Noise-free Constant s)
   - Fraction of positive ΔF_t = F_{t+1} − F_t ≤ 1% (numerical jitter); median ΔF_t < 0.

6) Reproducibility
   - Same seed ⇒ identical M_t sequence (max_abs_diff ≤ 1e-12).

7) Off-Mode Non-Interference (to be validated in a bridge harness)
   - With g = 0 (steering disabled), host system metrics (if coupled) match baseline within numerical tolerance.

Validation Plan
- Script: Prometheus_FUVDM/derivation/code/physics/memory_steering/memory_steering_acceptance.py
  - Experiments:
    1) Step response: s steps s0→s1; fit pole p from log residuals; verify M*.
    2) Canonical void: s ≡ 1, g = 1.5 λ; check M_final ≈ 0.6.
    3) Noise suppression: compute SNR_in (input) vs SNR_out (output, using a parallel signal-only filter for ground-truth); require ≥ 3 dB improvement.
    4) Boundedness: random s ∈ [0, 1], count post-clamp violations.
    5) Lyapunov: constant s, verify ΔF_t ≤ 0 up to numerical jitter.
    6) Reproducibility: duplicate run with same seed, compare sequences.
  - Outputs:
    - JSON: Prometheus_FUVDM/derivation/code/outputs/logs/memory_steering/memory_steering_acceptance_YYYYMMDDThhmmssZ.json
    - Figures (PNG): Prometheus_FUVDM/derivation/code/outputs/figures/memory_steering/
      - step_response_YYYY....png
      - noise_suppression_YYYY....png
      - lyapunov_YYYY....png
      - canonical_void_YYYY....png

Default Parameters (for acceptance run)
- g = 0.12, λ = 0.08 ⇒ p_pred = 0.80, τ_d ≈ 4.48 steps
- Noise std for SNR test: σ = 0.05
- Seeds: {0, 1, 2}
- Steps: 512 (step at t = 64)

Numerical Validation Results
- Pending. Will be auto-inserted into the JSON log after first run and summarized here if needed.

Open Questions / Next Refinements
- If the actual memory-steering update differs (nonlinear dependence or adaptive control), provide the exact formula or implementation path + lines so we can update p_pred, M*, and Lyapunov claims.
- Bridge into host systems (LBM, RD, walkers) to demonstrate:
  - Non-interference when off (g = 0): metrics identical to baseline.
  - Bounded, predictable effect when on (small g): document gains and any trade-offs.
- Optional: empirical Bode plot (frequency response) for completeness.

Run Instructions
- Activate venv and run:
  .\venv\scripts\activate
  python -m Prometheus_FUVDM.derivation.code.physics.memory_steering.memory_steering_acceptance --seed 0 --steps 512 --g 0.12 --lam 0.08
- Inspect JSON in code/outputs/logs/memory_steering/ and PNGs in code/outputs/figures/memory_steering/.

Reproducibility Gates
- A run is [PROVEN] if all acceptance checks pass. Deviations become [PLAUSIBLE] with a concrete follow-up plan; contradictions generate a RECONCILE note in CORRECTIONS.md.