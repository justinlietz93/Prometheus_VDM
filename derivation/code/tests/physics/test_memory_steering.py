import numpy as np

from Prometheus_FUVDM.derivation.code.physics.memory_steering.memory_steering_acceptance import run_filter


def test_fixed_point_linear():
    """
    For constant s, the linear, leaky memory converges to M* = g/(g+lam) * s.
    """
    g, lam = 0.12, 0.08
    s_val = 0.7
    s = np.ones(256) * s_val
    M = run_filter(s, g, lam, M0=0.0, rng=np.random.default_rng(0), noise_std=0.0)
    M_star = g * s_val / (g + lam)
    assert abs(np.mean(M[-32:]) - M_star) < 1e-2


def test_boundedness_with_clamp():
    """
    With saturation to [0,1], the memory variable remains within bounds under random inputs.
    """
    g, lam = 0.4, 0.5  # strong damping; p = 0.1
    rng = np.random.default_rng(1)
    s = rng.uniform(0.0, 1.0, size=512)
    M = run_filter(s, g, lam, M0=None, rng=rng, noise_std=0.0)
    assert np.all((M >= 0.0 - 1e-12) & (M <= 1.0 + 1e-12))


def test_reproducibility_strict():
    """
    Same seed and parameters produce identical sequences in deterministic mode.
    """
    g, lam = 0.12, 0.08
    steps = 200
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)
    s1 = np.ones(steps) * 0.3
    s2 = np.ones(steps) * 0.3
    M1 = run_filter(s1, g, lam, M0=None, rng=rng1, noise_std=0.0)
    M2 = run_filter(s2, g, lam, M0=None, rng=rng2, noise_std=0.0)
    assert np.max(np.abs(M1 - M2)) <= 1e-12


def test_canonical_void_target_point6():
    """
    Canonical 'void equilibrium' configuration: s ≡ 1 and g = 1.5 * lam => M* = 0.6.
    """
    lam = 0.1
    g = 1.5 * lam
    steps = 256
    s = np.ones(steps)
    M = run_filter(s, g, lam, M0=0.0, rng=np.random.default_rng(0), noise_std=0.0)
    M_final = float(np.mean(M[-32:]))
    assert abs(M_final - 0.6) <= 0.02