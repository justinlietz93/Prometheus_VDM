"""Geometry bundle automation for VDM instrumentation runs.

This script orchestrates the end-to-end workflow described in the
user's geometry data capture checklist (sections A-J). It handles run
directory provisioning, provenance capture, activation logging hooks,
quality checks, and packaging. The heavy lifting of model-specific
forward passes is delegated to a pluggable adapter that must implement
the :class:`GeometryProbeAdapter` protocol.

Usage (basic)::

    python tools/geom_bundle_builder.py --config path/to/config.json \
        --adapter dotted.module:AdapterClass

The configuration file may follow the ``geom_config.json`` template
described in the specification. All generated artifacts follow the
expected directory layout so downstream geometry analysis can consume
them immediately.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import logging
import random
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import List, Mapping, MutableMapping, Optional, Protocol, Sequence

import numpy as np


LOGGER = logging.getLogger("geom_bundle_builder")


def _run_cmd(args: Sequence[str]) -> str:
    try:
        completed = subprocess.run(
            args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:  # pragma: no cover - environment specific
        LOGGER.debug("Command failed %s: %s", args, exc)
        return ""
    return completed.stdout.strip()


def _detect_rocm_versions() -> Mapping[str, str]:
    versions: MutableMapping[str, str] = {}
    rocm_info = _run_cmd(["rocminfo"])
    if rocm_info:
        versions["rocminfo"] = rocm_info.splitlines()[0]
    driver_version = _run_cmd(["rocm-smi", "--showdriverversion"])
    if driver_version:
        versions["rocm_smi_driver"] = driver_version
    return versions


def _detect_gpu_names() -> Sequence[str]:
    result = _run_cmd(["rocm-smi", "--showproductname"])
    if not result:
        return []
    names: List[str] = []
    for line in result.splitlines():
        if "card" in line.lower():
            names.append(line.strip())
    return names


def _collect_python_packages() -> Mapping[str, str]:
    try:
        from importlib.metadata import distributions
    except ImportError:  # pragma: no cover - Python <3.8 not supported here
        return {}
    packages: MutableMapping[str, str] = {}
    for dist in distributions():
        name = dist.metadata.get("Name")
        if not name:
            continue
        packages[name.lower()] = dist.version
    return dict(sorted(packages.items()))


class GeometryProbeAdapter(Protocol):
    """Adapter contract for model-specific activation capture."""

    def prepare(self, config: "GeometryRunConfig") -> None:
        """Perform any one-time setup before checkpoints are processed."""

    def load_checkpoint(self, step: int) -> None:
        """Load the checkpoint corresponding to ``step``."""

    def encode_concepts(self, concepts: Sequence[str], layer_name: str) -> np.ndarray:
        """Return a matrix with shape ``(len(concepts), neurons)`` for ``layer_name``."""


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


def _default_storage_root() -> Path:
    primary = Path("/mnt/ironwolf/Data/VDM-dumps")
    if primary.exists():
        return primary
    fallback = Path.home() / "Documents" / "VDM-dumps"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def _generate_run_directory(root: Path) -> Path:
    hostname = socket.gethostname()
    date_str = time.strftime("%Y%m%d")
    suffix = random.randint(0, 999999)
    run_dir = root / hostname / date_str / f"VDM_geom_{suffix:06d}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def _check_disk_space(path: Path) -> None:
    usage = shutil.disk_usage(str(path))
    free_gb = usage.free / (1024 ** 3)
    if free_gb < 10:
        raise RuntimeError(f"Insufficient disk space ({free_gb:.2f} GB). Aborting run.")


def _ensure_clean_git_repo(config: GeometryRunConfig) -> None:
    status = _run_cmd(["git", "status", "--short"])
    if status and not config.allow_dirty:
        raise RuntimeError("Working tree is dirty. Commit or stash changes or set allow_dirty=true.")


def _load_adapter(config: GeometryRunConfig, adapter_override: Optional[str]) -> GeometryProbeAdapter:
    adapter_path = adapter_override or config.adapter_path
    if not adapter_path:
        raise RuntimeError("An adapter path must be provided via config or CLI.")
    module_name, _, attr = adapter_path.partition(":")
    if not attr:
        raise RuntimeError("Adapter path must be in 'module:ClassName' format.")
    module: ModuleType = import_module(module_name)
    adapter_cls = getattr(module, attr)
    adapter: GeometryProbeAdapter = adapter_cls()  # type: ignore[assignment]
    adapter.prepare(config)
    return adapter


def _collect_provenance(run_dir: Path, config: GeometryRunConfig) -> None:
    provenance = {
        "git_commit": _run_cmd(["git", "rev-parse", "HEAD"]),
        "git_branch": _run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "git_status": _run_cmd(["git", "status", "--short"]),
        "python": sys.version,
        "packages": _collect_python_packages(),
        "rocm": _detect_rocm_versions(),
        "seeds": list(config.seeds),
        "hostname": socket.gethostname(),
        "gpus": list(_detect_gpu_names()),
        "probe_mode": config.probe_mode,
    }
    _write_json(run_dir / "provenance.json", provenance)


def _save_config_artifacts(run_dir: Path, config: GeometryRunConfig) -> None:
    _write_json(run_dir / "concepts.json", {"concepts": list(config.concepts)})
    _write_json(run_dir / "layers.json", {"layers": list(config.layers)})
    _write_json(run_dir / "steps.json", {"steps": list(config.steps)})
    _write_json(
        run_dir / "geom_config.json",
        {
            "storage_root": str(config.storage_root),
            "concepts": list(config.concepts),
            "layers": list(config.layers),
            "steps": list(config.steps),
            "batch_size": config.batch_size,
            "max_bundle_mb": config.max_bundle_mb,
            "allow_dirty": config.allow_dirty,
            "probe_mode": config.probe_mode,
            "seeds": list(config.seeds),
            "adapter_path": config.adapter_path,
            "create_thumbs": config.create_thumbs,
        },
    )


def _validate_matrix(matrix: np.ndarray, concepts: Sequence[str]) -> None:
    if matrix.ndim != 2:
        raise ValueError(f"Activation matrix must be 2-D; got shape {matrix.shape}.")
    if matrix.shape[0] != len(concepts):
        raise ValueError(
            f"Activation matrix first dimension {matrix.shape[0]} does not match concept count {len(concepts)}."
        )
    if matrix.shape[1] < 64:
        raise ValueError("Activation matrix must expose at least 64 neurons per layer.")


def _compute_stats(matrix: np.ndarray) -> Mapping[str, object]:
    mean_vec = matrix.mean(axis=0)
    std_vec = matrix.std(axis=0)
    near_zero_fraction = float(np.mean(np.isclose(matrix, 0.0, atol=1e-6)))
    variances = matrix.var(axis=0)
    topk_idx = np.argsort(variances)[-10:][::-1]
    stats = {
        "mean": mean_vec.tolist(),
        "std": std_vec.tolist(),
        "near_zero_fraction": near_zero_fraction,
        "top_variance_indices": topk_idx.tolist(),
        "top_variance_values": variances[topk_idx].tolist(),
    }
    return stats


def _compute_pca(matrix: np.ndarray, n_components: int = 3) -> Mapping[str, object]:
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    u, s, vh = np.linalg.svd(centered, full_matrices=False)
    total_variance = float((s ** 2).sum())
    components = vh[:n_components]
    explained = (s[:n_components] ** 2) / total_variance if total_variance else np.zeros_like(s[:n_components])

    whitened = centered / (np.std(centered, axis=0, keepdims=True) + 1e-9)
    _, s2, vh2 = np.linalg.svd(whitened, full_matrices=False)
    sanity = float(np.abs(np.diag(components @ vh2[:n_components].T)).mean())
    return {
        "components": components.tolist(),
        "explained_variance_ratio": explained[:n_components].tolist(),
        "total_variance": total_variance,
        "sanity_alignment": sanity,
        "alt_singular_values": s2[:n_components].tolist(),
    }


def _maybe_render_thumb(run_dir: Path, layer: str, step: int, matrix: np.ndarray) -> Optional[Path]:  # pragma: no cover - plotting
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        LOGGER.warning("matplotlib not available; skipping PCA thumbnail for %s step %s", layer, step)
        return None
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    u, s, vh = np.linalg.svd(centered, full_matrices=False)
    pc = centered @ vh[:2].T
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.scatter(pc[:, 0], pc[:, 1], s=30)
    ax.set_title(f"PCA2 {layer} step {step}")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    outdir = run_dir / "thumbs" / layer
    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / f"pca2_step-{step}.png"
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


def _append_index(run_dir: Path, payload: Mapping[str, object]) -> None:
    index_path = run_dir / "index.jsonl"
    with index_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def _run_activation_pass(
    adapter: GeometryProbeAdapter,
    config: GeometryRunConfig,
    run_dir: Path,
) -> None:
    qc_dir = run_dir / "qc"
    qc_dir.mkdir(parents=True, exist_ok=True)
    acts_root = run_dir / "acts"
    acts_root.mkdir(exist_ok=True)

    for step in config.steps:
        LOGGER.info("Processing step %s", step)
        adapter.load_checkpoint(step)
        for layer in config.layers:
            layer_start = time.perf_counter()
            LOGGER.info("  Capturing layer %s", layer)
            matrix = adapter.encode_concepts(config.concepts, layer).astype(np.float32)
            _validate_matrix(matrix, config.concepts)
            layer_dir = acts_root / layer
            layer_dir.mkdir(parents=True, exist_ok=True)
            acts_path = layer_dir / f"acts_step-{step}.npy"
            np.save(acts_path, matrix)
            meta = {
                "layer": layer,
                "step": step,
                "concepts": list(config.concepts),
                "neurons": int(matrix.shape[1]),
                "notes": "eval mode; canonical probe",
                "dtype": str(matrix.dtype),
                "shape": list(matrix.shape),
                "capture_seconds": time.perf_counter() - layer_start,
            }
            _write_json(layer_dir / f"meta_step-{step}.json", meta)
            stats = _compute_stats(matrix)
            _write_json(qc_dir / f"{layer}_step-{step}_stats.json", stats)
            pca = _compute_pca(matrix)
            _write_json(qc_dir / f"{layer}_step-{step}_pca.json", pca)
            thumb_path = None
            if config.create_thumbs:
                thumb_path = _maybe_render_thumb(run_dir, layer, step, matrix)
            _append_index(
                run_dir,
                {
                    "layer": layer,
                    "step": step,
                    "acts_path": str(acts_path.relative_to(run_dir)),
                    "meta_path": str((layer_dir / f"meta_step-{step}.json").relative_to(run_dir)),
                    "stats_path": str((qc_dir / f"{layer}_step-{step}_stats.json").relative_to(run_dir)),
                    "pca_path": str((qc_dir / f"{layer}_step-{step}_pca.json").relative_to(run_dir)),
                    "thumb_path": str(thumb_path.relative_to(run_dir)) if thumb_path else None,
                    "shape": list(matrix.shape),
                },
            )


def _compute_directory_size_bytes(path: Path) -> int:
    total = 0
    for sub_path in path.rglob("*"):
        if sub_path.is_file():
            total += sub_path.stat().st_size
    return total


def _zip_bundle(run_dir: Path) -> Path:
    bundle_path = run_dir.parent / "VDM_geom_bundle.zip"
    if bundle_path.exists():
        bundle_path.unlink()
    archive_base = shutil.make_archive(str(bundle_path.with_suffix("")), "zip", run_dir)
    return Path(archive_base)


def _bundle_summary(run_dir: Path) -> Mapping[str, object]:
    size_bytes = _compute_directory_size_bytes(run_dir)
    return {
        "path": str(run_dir),
        "size_mb": size_bytes / (1024 ** 2),
    }


def run_workflow(config: GeometryRunConfig, adapter_override: Optional[str]) -> Mapping[str, object]:
    LOGGER.info("Starting geometry bundle workflow")
    _check_disk_space(config.storage_root)
    _ensure_clean_git_repo(config)
    run_dir = _generate_run_directory(config.storage_root)
    LOGGER.info("Run directory: %s", run_dir)
    _collect_provenance(run_dir, config)
    _save_config_artifacts(run_dir, config)
    adapter = _load_adapter(config, adapter_override)
    _run_activation_pass(adapter, config, run_dir)
    size_mb = _bundle_summary(run_dir)["size_mb"]
    if size_mb > config.max_bundle_mb:
        raise RuntimeError(
            f"Bundle size {size_mb:.2f} MB exceeds configured maximum {config.max_bundle_mb} MB."
        )
    bundle_zip = _zip_bundle(run_dir)
    summary = {
        "run_dir": str(run_dir),
        "bundle_zip": str(bundle_zip),
        "concept_count": len(config.concepts),
        "layer_count": len(config.layers),
        "step_count": len(config.steps),
        "bundle_mb": size_mb,
    }
    LOGGER.info(
        "Bundle ready -> %s ; concepts=%s layers=%s steps=%s size=%.2f MB",
        summary["bundle_zip"],
        summary["concept_count"],
        summary["layer_count"],
        summary["step_count"],
        summary["bundle_mb"],
    )
    return summary


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="VDM geometry bundle automation")
    parser.add_argument("--config", type=Path, required=True, help="Path to geometry config JSON file")
    parser.add_argument(
        "--adapter",
        type=str,
        default=None,
        help="Adapter override in 'module:ClassName' format (overrides config adapter_path)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = _parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper()))
    with args.config.open("r", encoding="utf-8") as stream:
        config_data = json.load(stream)
    config = GeometryRunConfig.from_json(config_data, _default_storage_root())
    summary = run_workflow(config, args.adapter)
    print(
        "Bundle ready -> {bundle_zip} ; concepts={concept_count} layers={layer_count} steps={step_count} size={bundle_mb:.2f} MB".format(
            **summary
        )
    )


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()

