from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.neuroplasticity.revgsp
Purpose: Resonance‑Enhanced Valence‑Gated Synaptic Plasticity (REV‑GSP), organism‑native.

Design constraints
- Pure core; no IO/logging; NumPy + SciPy only.
- Budgeted pair sampling (no global candidate sweep).
- CSR‑safe updates for eligibility traces and weights.
"""

from typing import Any, Dict, List, Tuple
import math
import numpy as np


class RevGSP:
    """
    REV‑GSP learner (class form, organism‑native).
    - No IO/logging. Pure numeric state updates on a Substrate‑like object.
    - Accepts any 'substrate' exposing:
        synaptic_weights (CSR), eligibility_traces (CSR), neuron_polarities (ndarray)
    """

    def __init__(
        self,
        reward_sigmoid_scale: float = 1.5,
        pi_params: dict | None = None,
        rng_seed: int | None = None,
        max_pairs: int = 2048,
        sample_spikes_cap: int | None = None,
    ) -> None:
        """
        Parameters:
          - reward_sigmoid_scale: gain for eta_effective sigmoid
          - pi_params: base params for PI kernel (a±, tau±)
          - rng_seed: deterministic sampling for budgets
          - max_pairs: hard cap on pre/post spike candidate evaluations per tick
          - sample_spikes_cap: optional cap on filtered spike list (down-sample before pairing)
        """
        self.reward_sigmoid_scale = float(reward_sigmoid_scale)
        self.pi_params = pi_params or {
            "a_plus_base": 0.1,
            "a_minus_base": 0.1,
            "tau_plus_base": 20.0,
            "tau_minus_base": 20.0,
        }
        self.rng = np.random.default_rng(rng_seed)
        self.max_pairs = int(max(1, int(max_pairs)))
        self.sample_spikes_cap = None if sample_spikes_cap is None else int(max(1, int(sample_spikes_cap)))

    # --- helpers ---
    def _clamped_normal(self, mu: float, sigma: float, lo: float, hi: float) -> float:
        try:
            val = float(self.rng.normal(mu, sigma))
        except Exception:
            val = float(mu)
        if val < lo:
            val = lo
        if val > hi:
            val = hi
        return float(val)

    def _base_pi(self, delta_t: float) -> float:
        # STDP‑like impulse with constrained bio diversity per call
        a_plus = self._clamped_normal(self.pi_params["a_plus_base"], 0.01, 0.03, 0.07)
        a_minus = self._clamped_normal(self.pi_params["a_minus_base"], 0.01, 0.04, 0.08)
        tau_plus = self._clamped_normal(self.pi_params["tau_plus_base"], 2.0, 18.0, 22.0)
        tau_minus = self._clamped_normal(self.pi_params["tau_minus_base"], 2.0, 18.0, 22.0)
        if delta_t > 0:
            return float(a_plus * math.exp(-delta_t / tau_plus))
        return float(-a_minus * math.exp(delta_t / tau_minus))

    def _eta_effective(self, base_lr: float, total_reward: float) -> float:
        """
        Canonical eta_effective(total_reward):
          eta_mag = base_lr * (1 + (2*sigmoid(k*R) - 1))
          eta_eff = eta_mag * sign(R)
        This strictly gates learning by the sign of the global modulatory factor (SIE).
        """
        k = self.reward_sigmoid_scale
        x = k * float(total_reward)
        mod = 2.0 / (1.0 + math.exp(-x)) - 1.0  # 2*sigmoid - 1 in [-1,1]
        eta_mag = float(base_lr) * (1.0 + mod)
        # Explicit sign gate (sign(0)=0): no weight drift when reward ~ 0
        if total_reward > 0.0:
            return float(eta_mag)
        if total_reward < 0.0:
            return float(-eta_mag)
        return 0.0

    @staticmethod
    def _gamma_from_plv(plv: float, base_decay: float = 0.95, sensitivity: float = 0.1) -> float:
        """
        PLV‑gated eligibility trace decay:
            gamma = base_decay + sensitivity*(PLV - 0.5)
        Clamp to [0, 1] for stability under noisy PLV estimates.
        """
        g = float(base_decay + sensitivity * (float(plv) - 0.5))
        if g < 0.0:
            g = 0.0
        if g > 1.0:
            g = 1.0
        return g

    @staticmethod
    def _temporal_filter(spike_times: List[Tuple[int, int]], window_size: int = 5) -> List[Tuple[int, float]]:
        if len(spike_times) < window_size:
            return spike_times
        out: List[Tuple[int, float]] = []
        for i in range(len(spike_times) - window_size + 1):
            window = spike_times[i : i + window_size]
            avg_time = sum(t for _, t in window) / float(window_size)
            neuron_idx = window[-1][0]
            out.append((neuron_idx, avg_time))
        return out

    @staticmethod
    def _adaptive_window(base_ms: int, max_latency: float) -> int:
        return int(base_ms + float(max_latency))

    @staticmethod
    def _latency_scale(pi_value: float, latency_error: float, max_latency: float) -> float:
        if float(max_latency) > 0.0:
            return float(pi_value) * (1.0 - float(latency_error) / float(max_latency))
        return float(pi_value)

    # --- main API ---
    def adapt(
        self,
        substrate: Any,
        spike_train: List[Tuple[int, int]],
        spike_phases: Dict[Tuple[int, int], float],
        learning_rate: float,
        lambda_decay: float,
        total_reward: float,
        plv: float,
        network_latency_estimate: Dict[str, float],
        time_window_ms: int = 20,
    ) -> tuple[Any, dict]:
        """
        Update substrate in‑place using REV‑GSP rule; returns (substrate, metrics).
        Budgeted: samples pairs from recent spikes only; respects max_pairs and sample_spikes_cap.
        """
        try:
            from scipy.sparse import lil_matrix  # local import to avoid hard dependency at import-time
        except Exception:
            # Cannot operate without scipy
            return substrate, {"eta_effective": 0.0, "gamma": 0.0}

        filtered = self._temporal_filter(spike_train)
        win = self._adaptive_window(int(time_window_ms), float(network_latency_estimate.get("max", 0.0)))

        # Optional down‑sample of filtered spikes to respect complexity cap
        if self.sample_spikes_cap is not None and len(filtered) > self.sample_spikes_cap:
            try:
                idx = self.rng.choice(len(filtered), size=self.sample_spikes_cap, replace=False)
                filtered = [filtered[int(i)] for i in idx]
            except Exception:
                filtered = filtered[: self.sample_spikes_cap]

        W = getattr(substrate, "synaptic_weights", None)
        E = getattr(substrate, "eligibility_traces", None)
        P = getattr(substrate, "neuron_polarities", None)
        if W is None or E is None or P is None:
            return substrate, {"eta_effective": 0.0, "gamma": 0.0}

        # Build PI sparsely
        try:
            shape = W.shape
        except Exception:
            shape = (0, 0)
        PI = lil_matrix(shape, dtype=np.float32)

        # Budgeted pair evaluation to ensure sub‑quadratic behavior
        pairs_evaluated = 0
        break_outer = False
        for pre_neuron, pre_time in filtered:
            if break_outer:
                break
            for post_neuron, post_time in filtered:
                if pre_neuron == post_neuron:
                    continue
                try:
                    # Quick existence check (CSR O(1) average)
                    if W[pre_neuron, post_neuron] == 0:
                        continue
                    delta_t = float(post_time) - float(pre_time)
                    if 0.0 < abs(delta_t) < float(win):
                        base_pi = self._base_pi(delta_t)
                        phase_pre = float(spike_phases.get((pre_neuron, int(pre_time)), 0.0))
                        phase_post = float(spike_phases.get((post_neuron, int(post_time)), 0.0))
                        phase_mod = (1.0 + math.cos(phase_pre - phase_post)) * 0.5
                        pi_val = base_pi * phase_mod
                        pi_val = self._latency_scale(pi_val, float(network_latency_estimate.get("error", 0.0)), float(network_latency_estimate.get("max", 0.0)))
                        PI[pre_neuron, post_neuron] += float(pi_val)
                        pairs_evaluated += 1
                        if pairs_evaluated >= self.max_pairs:
                            break_outer = True
                            break
                except Exception:
                    continue

        PI_csr = PI.tocsr()

        # Eligibility update: E = gamma*E + PI
        gamma = self._gamma_from_plv(float(plv))
        try:
            E *= float(gamma)
        except Exception:
            # fallback reconstruct
            E = E.multiply(float(gamma))
        E += PI_csr

        # Row‑scale by neuron polarity (CSR‑friendly)
        try:
            indptr = E.indptr
            data = E.data
            for i in range(E.shape[0]):
                p = float(P[i])
                if p == 1.0:
                    continue
                start = indptr[i]
                end = indptr[i + 1]
                if end > start:
                    data[start:end] *= p
        except Exception:
            pass

        # Three‑factor update
        eta = self._eta_effective(float(learning_rate), float(total_reward))
        try:
            trace_update = E * float(eta)
            decay_update = W * float(lambda_decay)
            dW = trace_update - decay_update
            W += dW
            # clip
            try:
                W.data = np.clip(W.data, -1.0, 1.0)
            except Exception:
                pass
        except Exception:
            pass

        return substrate, {"eta_effective": float(eta), "gamma": float(gamma)}

    # Compatibility wrapper matching the task board signature
    def adapt_connectome(
        self,
        substrate: Any,
        spike_train: List[Tuple[int, int]],
        spike_phases: Dict[Tuple[int, int], float],
        total_reward: float,
        network_latency: Dict[str, float],
        *,
        max_pairs: int | None = None,
        spike_sampling_cap: int | None = None,
        pi_params: dict | None = None,
        lambda_decay: float = 1e-3,
        base_lr: float = 1e-2,
        plv: float | None = None,
        time_window_ms: int = 20,
    ) -> tuple[Any, dict]:
        """
        Thin compatibility wrapper:
        - Allows per‑call override of budgets and PI parameters.
        - Computes eta from total_reward via internal nonlinearity.
        - Uses network_latency['max'|'error'] to adapt the time window and latency scaling.
        - plv defaults to network_latency.get('plv', 0.5) if not provided.
        """
        # Stash old config and override temporarily
        old_mp = self.max_pairs
        old_cap = self.sample_spikes_cap
        old_pi = dict(self.pi_params) if isinstance(self.pi_params, dict) else self.pi_params

        try:
            if max_pairs is not None:
                self.max_pairs = int(max(1, int(max_pairs)))
            if spike_sampling_cap is not None:
                self.sample_spikes_cap = int(max(1, int(spike_sampling_cap)))
            if pi_params is not None:
                self.pi_params = dict(pi_params)

            use_plv = float(plv if plv is not None else float(network_latency.get("plv", 0.5)))
            return self.adapt(
                substrate=substrate,
                spike_train=spike_train,
                spike_phases=spike_phases,
                learning_rate=float(base_lr),
                lambda_decay=float(lambda_decay),
                total_reward=float(total_reward),
                plv=float(use_plv),
                network_latency_estimate=network_latency,
                time_window_ms=int(time_window_ms),
            )
        finally:
            # Restore config
            self.max_pairs = old_mp
            self.sample_spikes_cap = old_cap
            self.pi_params = old_pi


__all__ = ["RevGSP"]