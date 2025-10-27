"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
CLI argument parser for the FUM runtime.

Behavior:
- Mirrors the legacy make_parser() previously defined in fum_rt/nexus.py exactly.
- Kept here to reduce nexus.py size and improve separation of concerns.
"""

import argparse


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument('--neurons', type=int, default=1000)
    p.add_argument('--k', type=int, default=12)
    p.add_argument('--hz', type=int, default=10)
    p.add_argument('--domain', type=str, default='biology_consciousness')
    p.add_argument('--viz-every', type=int, default=10)
    p.add_argument('--log-every', type=int, default=1)
    p.add_argument('--checkpoint-every', type=int, default=0)
    p.add_argument('--checkpoint-keep', type=int, default=5)
    p.add_argument('--duration', type=int, default=None)
    p.add_argument('--use-time-dynamics', dest='use_time_dynamics', action='store_true')
    p.add_argument('--no-time-dynamics', dest='use_time_dynamics', action='store_false')
    p.set_defaults(use_time_dynamics=True)
    p.add_argument('--seed', type=int, default=0)

    # Ultra-scale/sparse flags
    p.add_argument('--sparse-mode', dest='sparse_mode', action='store_true')
    p.add_argument('--dense-mode', dest='sparse_mode', action='store_false')
    # Aliases
    p.add_argument('--sparse', dest='sparse_mode', action='store_true')
    p.add_argument('--dense', dest='sparse_mode', action='store_false')
    p.set_defaults(sparse_mode=None)
    p.add_argument('--threshold', type=float, default=0.15)
    p.add_argument('--lambda-omega', dest='lambda_omega', type=float, default=0.1)
    p.add_argument('--candidates', type=int, default=64)
    p.add_argument('--walkers', type=int, default=256)
    p.add_argument('--hops', type=int, default=3)
    p.add_argument('--status-interval', dest='status_interval', type=int, default=1)
    p.add_argument('--bundle-size', dest='bundle_size', type=int, default=3)
    p.add_argument('--prune-factor', dest='prune_factor', type=float, default=0.10)

    # Text→connectome stimulation (symbol→group)
    p.add_argument('--stim-group-size', dest='stim_group_size', type=int, default=4)
    p.add_argument('--stim-amp', dest='stim_amp', type=float, default=0.05)
    p.add_argument('--stim-decay', dest='stim_decay', type=float, default=0.90)
    p.add_argument('--stim-max-symbols', dest='stim_max_symbols', type=int, default=64)

    # Self-speak and topology-spike detection (void-native)
    p.add_argument('--speak-auto', dest='speak_auto', action='store_true')
    p.add_argument('--no-speak-auto', dest='speak_auto', action='store_false')
    p.set_defaults(speak_auto=True)
    p.add_argument('--speak-z', dest='speak_z', type=float, default=1.0)
    p.add_argument('--speak-hysteresis', dest='speak_hysteresis', type=float, default=1.0)
    p.add_argument('--speak-cooldown-ticks', dest='speak_cooldown_ticks', type=int, default=10)
    p.add_argument('--speak-valence-thresh', dest='speak_valence_thresh', type=float, default=0.01)
    p.add_argument('--b1-half-life-ticks', dest='b1_half_life_ticks', type=int, default=50)

    # Announcement bus / ADC tuning
    p.add_argument('--bus-capacity', dest='bus_capacity', type=int, default=65536)
    p.add_argument('--bus-drain', dest='bus_drain', type=int, default=2048)
    p.add_argument('--r-attach', dest='r_attach', type=float, default=0.25)
    p.add_argument('--ttl-init', dest='ttl_init', type=int, default=120)
    p.add_argument('--split-patience', dest='split_patience', type=int, default=6)

    # Engram loader (optional)
    p.add_argument('--load-engram', dest='load_engram', type=str, default=None)
    # Optional embedded control server (disabled by default to avoid duplicate UI)
    p.add_argument('--control-server', dest='control_server', action='store_true')
    p.add_argument('--no-control-server', dest='control_server', action='store_false')
    p.set_defaults(control_server=False)
    # Allow explicit reuse of an existing run directory (resume), otherwise a new timestamp dir is used
    p.add_argument('--run-dir', dest='run_dir', type=str, default=None)

    return p


__all__ = ["make_parser"]