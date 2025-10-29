"""Utilities for resolving canonical Derivation paths (read-only).

This module implements the Task 0.3 path resolver contract:
- Resolve the repository root using CLI overrides, environment variables,
  or filesystem traversal.
- Ensure resolved paths remain within the Derivation/ tree.
- Provide helper functions for git metadata and file hashes without
  performing any write operations.

All functions are safe for use in read-only tooling (e.g., canon sync,
resolver printers, dashboard scaffolding).  No function in this module
creates, modifies, or deletes files.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
import subprocess
from pathlib import Path
from typing import Iterable, Mapping, Optional, Tuple

__all__ = [
    "CanonPathError",
    "CanonResolver",
    "FileMetadata",
]


class CanonPathError(RuntimeError):
    """Raised when a canonical path cannot be resolved safely."""


@dataclass
class FileMetadata:
    """Lightweight metadata describing a canonical file."""

    path: Path
    exists: bool
    size_bytes: Optional[int]
    sha256: Optional[str]
    last_commit: Optional[str]


def _candidate_roots(
    explicit: Optional[Path], env: Mapping[str, str], start: Path
) -> Iterable[Path]:
    """Yield candidate repository roots in precedence order."""

    if explicit is not None:
        yield explicit

    env_root = env.get("VDM_REPO_ROOT")
    if env_root:
        yield Path(env_root)

    yield start

    # Also allow resolving relative to the script directory so tooling works
    # when invoked from nested paths (e.g., build trees).
    yield Path(__file__).resolve().parents[2]


def _walk_up(path: Path, max_depth: int = 10) -> Iterable[Path]:
    """Walk upward from *path*, yielding each ancestor (inclusive)."""

    current = path
    depth = 0
    while True:
        yield current
        depth += 1
        if depth >= max_depth or current.parent == current:
            break
        current = current.parent


def _hash_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


class CanonResolver:
    """Resolve repository-relative canon paths with guard rails."""

    def __init__(self, repo_root: Path) -> None:
        repo_root = repo_root.resolve()
        derivation = repo_root / "Derivation"
        if not derivation.is_dir():
            raise CanonPathError(
                f"Repository root '{repo_root}' does not contain Derivation/"
            )
        self._repo_root = repo_root
        self._derivation_root = derivation

    @property
    def repo_root(self) -> Path:
        return self._repo_root

    @property
    def derivation_root(self) -> Path:
        return self._derivation_root

    @classmethod
    def from_sources(
        cls,
        explicit: Optional[str] = None,
        *,
        env: Optional[Mapping[str, str]] = None,
        start: Optional[Path] = None,
    ) -> "CanonResolver":
        """Resolve a repository root honouring CLI/env precedence."""

        env = env or os.environ
        start = start or Path.cwd()

        explicit_path = Path(explicit).expanduser().resolve() if explicit else None

        for candidate in _candidate_roots(explicit_path, env, start):
            for root in _walk_up(Path(candidate).expanduser().resolve()):
                if (root / "Derivation").is_dir():
                    return cls(root)
        raise CanonPathError(
            "Unable to resolve repository root. Set VDM_REPO_ROOT or pass --repo-root."
        )

    def resolve(self, canon_path: str) -> Tuple[Path, Optional[str]]:
        """Resolve *canon_path* within Derivation/ and return (path, fragment)."""

        raw = canon_path.strip()
        if not raw:
            raise CanonPathError("Empty canonical path")

        path_part, fragment = self._split_fragment(raw)
        target = Path(path_part)
        if target.is_absolute():
            resolved = target.resolve()
        else:
            resolved = (self.repo_root / target).resolve()

        try:
            resolved.relative_to(self.derivation_root)
        except ValueError as exc:
            raise CanonPathError(
                f"Path '{canon_path}' escapes Derivation/: {resolved}"
            ) from exc

        return resolved, fragment

    @staticmethod
    def _split_fragment(value: str) -> Tuple[str, Optional[str]]:
        if "#" not in value:
            return value, None
        base, fragment = value.split("#", 1)
        frag = fragment.strip() or None
        return base.strip(), frag

    def git_head(self) -> Optional[str]:
        return self._git(["rev-parse", "HEAD"])

    def git_last_commit(self, path: Path) -> Optional[str]:
        try:
            relative = path.relative_to(self.repo_root)
        except ValueError:
            relative = path
        return self._git(["log", "-n", "1", "--pretty=%H", "--", str(relative)])

    def _git(self, args: Iterable[str]) -> Optional[str]:
        try:
            cp = subprocess.run(
                ["git", *args],
                cwd=str(self.repo_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return None
        if cp.returncode != 0:
            return None
        return (cp.stdout or "").strip() or None

    def metadata(self, path: Path) -> FileMetadata:
        try:
            exists = path.is_file()
        except OSError:
            exists = False

        size_bytes: Optional[int] = None
        sha256: Optional[str] = None
        if exists:
            try:
                size_bytes = path.stat().st_size
            except OSError:
                size_bytes = None
            try:
                sha256 = _hash_file(path)
            except OSError:
                sha256 = None

        last_commit = self.git_last_commit(path) if exists else None

        return FileMetadata(
            path=path,
            exists=exists,
            size_bytes=size_bytes,
            sha256=sha256,
            last_commit=last_commit,
        )


if __name__ == "__main__":
    raise SystemExit(
        "canon_paths.py is a support module and should not be executed directly"
    )
