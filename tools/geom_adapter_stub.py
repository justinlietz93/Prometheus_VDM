"""Reference adapter implementations for geometry bundle runs.

These adapters are primarily intended for smoke-testing the geometry
bundle workflow. They produce deterministic synthetic activations so
that the pipeline can be validated without requiring a fully wired
model. Replace them with project-specific adapters that interface with
your actual checkpoints and model layers.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

try:  # pragma: no cover - optional import for type checking only
    from .geom_bundle_builder import GeometryProbeAdapter, GeometryRunConfig
except ImportError:  # pragma: no cover - fallback when executed standalone
    GeometryProbeAdapter = object  # type: ignore
    GeometryRunConfig = object  # type: ignore


class DeterministicRandomAdapter:
    """Generate deterministic synthetic activations for testing."""

    def __init__(self) -> None:
        self._rng: Optional[np.random.Generator] = None
        self._neurons_per_layer: dict[str, int] = {}

    def prepare(self, config: GeometryRunConfig) -> None:  # type: ignore[override]
        seed = config.seeds[0] if config.seeds else 0
        self._rng = np.random.default_rng(seed)
        self._neurons_per_layer = {layer: 128 for layer in config.layers}

    def load_checkpoint(self, step: int) -> None:  # type: ignore[override]
        if self._rng is None:
            raise RuntimeError("Adapter not prepared.")
        seed = int(step) * 2654435761 % (2 ** 32)
        self._rng = np.random.default_rng(seed)

    def encode_concepts(self, concepts: Sequence[str], layer_name: str) -> np.ndarray:  # type: ignore[override]
        if self._rng is None:
            raise RuntimeError("Adapter not prepared.")
        neurons = self._neurons_per_layer.get(layer_name, 128)
        matrix = self._rng.normal(size=(len(concepts), neurons)).astype(np.float32)
        return matrix


__all__ = ["DeterministicRandomAdapter"]

