#!/usr/bin/env python3
"""Install repo-tracked git hooks.

Git does not version-control .git/hooks by default. This installer configures
this clone to use the repo's `.githooks/` directory.

Usage:
  python tools/git-hooks/install_hooks.py
"""

from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GITHOOKS_DIR = REPO_ROOT / ".githooks"


def main() -> None:
    if not GITHOOKS_DIR.exists():
        raise SystemExit(f"Missing {GITHOOKS_DIR}")

    subprocess.check_call(["git", "config", "core.hooksPath", str(GITHOOKS_DIR)], cwd=REPO_ROOT)

    # Best-effort: mark hooks executable
    for hook in ["pre-commit", "post-commit"]:
        p = GITHOOKS_DIR / hook
        if p.exists():
            p.chmod(p.stat().st_mode | 0o111)

    print(f"Installed hooks: core.hooksPath={GITHOOKS_DIR}")
    print("Note: auto-push is disabled by default. Set VDM_AUTO_PUSH=1 to enable.")


if __name__ == "__main__":
    main()
