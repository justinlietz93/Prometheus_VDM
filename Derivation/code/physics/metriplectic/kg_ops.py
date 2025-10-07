#!/usr/bin/env python3
from __future__ import annotations
import numpy as np
from typing import Tuple


def _omega(N: int, dx: float) -> np.ndarray:
    k_cyc = np.fft.fftfreq(N, d=dx)
    return 2.0 * np.pi * k_cyc


def spectral_laplacian(u: np.ndarray, dx: float) -> np.ndarray:
    N = u.size
    om = _omega(N, dx)
    U = np.fft.fft(u)
    return np.fft.ifft(-(om * om) * U).real


def spectral_grad(u: np.ndarray, dx: float) -> np.ndarray:
    N = u.size
    om = _omega(N, dx)
    U = np.fft.fft(u)
    return np.fft.ifft(1j * om * U).real


def kg_energy(phi: np.ndarray, pi: np.ndarray, dx: float, c: float, m: float) -> float:
    dphi = spectral_grad(phi, dx)
    kin = 0.5 * float(np.sum(pi * pi) * dx)
    grad = 0.5 * (c * c) * float(np.sum(dphi * dphi) * dx)
    pot = 0.5 * (m * m) * float(np.sum(phi * phi) * dx)
    return kin + grad + pot


def kg_verlet_step(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, c: float, m: float) -> Tuple[np.ndarray, np.ndarray]:
    # pi half-step
    lap_phi = spectral_laplacian(phi, dx)
    pi_half = pi + 0.5 * dt * ((c * c) * lap_phi - (m * m) * phi)
    # phi full-step
    phi_new = phi + dt * pi_half
    # pi half-step with updated phi
    lap_phi_new = spectral_laplacian(phi_new, dx)
    pi_new = pi_half + 0.5 * dt * ((c * c) * lap_phi_new - (m * m) * phi_new)
    return phi_new, pi_new
