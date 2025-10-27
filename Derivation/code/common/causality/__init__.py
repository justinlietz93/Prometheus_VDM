"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Common causality helpers (order-only diagnostics)

Lightweight utilities to:
- Build an event DAG from timestamped events (with optional edge inference)
- Check acyclicity and compute a transitive reduction (TR)
- Sample Alexandrov intervals and estimate Myrheim–Meyer dimension d̂
- Analyze diamond growth |I| vs Δt and summarize diagnostics

Design:
- Dependency-minimal (pure Python + math/random; numpy optional in callers)
- Bounded algorithms with caps for large graphs
- Reusable across domains; no IO, no approvals; safe for CI hygiene

Modules:
- event_dag: DAG building, acyclicity, TR
- intervals: interval sampling, ordering fraction r, d̂ mapping, scaling
- diagnostics: convenience wrappers for one-shot summaries
"""

from .event_dag import (
	build_event_dag,
	is_acyclic,
	transitive_reduction,
)
from .intervals import (
	sample_intervals,
	ordering_fraction,
	dim_from_order_fraction,
	fit_diamond_scaling,
)
from .diagnostics import (
	dag_summary,
	interval_summary,
	full_causality_summary,
)

__all__ = [
	# event_dag
	"build_event_dag",
	"is_acyclic",
	"transitive_reduction",
	# intervals
	"sample_intervals",
	"ordering_fraction",
	"dim_from_order_fraction",
	"fit_diamond_scaling",
	# diagnostics
	"dag_summary",
	"interval_summary",
	"full_causality_summary",
]

