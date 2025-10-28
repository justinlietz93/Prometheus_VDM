#!/usr/bin/env python3
"""
VDM Nexus — Approvals Wrapper CLI (Phase 1 · Task 1.2)

Scope and Policy:
- Read-only code under VDM_Nexus/ that shells out to canonical approvals CLI
  at Derivation/code/common/authorization/approve_tag.py.
- Enforces environment precedence for approvals databases:
  CLI flags > environment variables > .env file
- Stores no secrets. Prompts occur only in the underlying canonical CLI.
- Does not import external dependencies.

References:
- Architecture seams (§12.4): VDM_Nexus/NEXUS_ARCHITECTURE.md
- Canon approvals CLI: Derivation/code/common/authorization/approve_tag.py
- IO policy and quarantine helpers: Derivation/code/common/io_paths.py (not called here)

Usage examples:
  # Show resolved environment (what will be passed through)
  python3 VDM_Nexus/scripts/approval_cli.py print-env

  # Dry check that canonical script is resolvable
  python3 VDM_Nexus/scripts/approval_cli.py check

  # Run the canonical approvals CLI, passing all subsequent args verbatim
  # (this wrapper only sets env precedence and logs provenance)
  python3 VDM_Nexus/scripts/approval_cli.py run -- \\
      --domain metriplectic --script run_kg_energy_oscillation.py --tag prereg_v1 --approve

Notes:
- Use the 'run -- ...' form to pass arguments exactly as required by approve_tag.py.
- Exit code mirrors the underlying approve_tag.py process.
"""

from __future__ import annotations

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Tuple


REPO_REL_APPROVE = Path("Derivation/code/common/authorization/approve_tag.py")
DEFAULT_ENV_FILE = Path(".env")


def read_env_file(path: Path) -> Dict[str, str]:
    """
    Minimal .env parser (KEY=VALUE lines; ignores comments/blank lines).
    """
    env: Dict[str, str] = {}
    if not path.is_file():
        return env
    try:
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        # Non-fatal; return what we have
        pass
    return env


def resolve_repo_root(cli_repo_root: str | None) -> Path:
    if cli_repo_root:
        p = Path(cli_repo_root).resolve()
        return p
    # Default: current working directory considered as repo root
    return Path(".").resolve()


def resolve_env(cli_repo_root: str | None,
                cli_approval_db: str | None,
                cli_approval_admin_db: str | None) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Build environment dict with precedence:
      CLI flags > existing process env > .env file
    Returns (resolved_env, provenance_map)
    """
    repo_root = resolve_repo_root(cli_repo_root)
    dotenv = read_env_file(repo_root / DEFAULT_ENV_FILE)

    provenance: Dict[str, str] = {}

    def choose(key: str, cli_val: str | None) -> str | None:
        if cli_val is not None and cli_val != "":
            provenance[key] = "cli"
            return cli_val
        if key in os.environ and os.environ[key] != "":
            provenance[key] = "env"
            return os.environ[key]
        if key in dotenv and dotenv[key] != "":
            provenance[key] = ".env"
            return dotenv[key]
        provenance[key] = "unset"
        return None

    out: Dict[str, str] = {}
    rr = choose("VDM_REPO_ROOT", cli_repo_root)
    if rr:
        out["VDM_REPO_ROOT"] = str(Path(rr).resolve())
    ad = choose("VDM_APPROVAL_DB", cli_approval_db)
    if ad:
        out["VDM_APPROVAL_DB"] = str(Path(ad).resolve())
    aad = choose("VDM_APPROVAL_ADMIN_DB", cli_approval_admin_db)
    if aad:
        out["VDM_APPROVAL_ADMIN_DB"] = str(Path(aad).resolve())

    # GUI-mode hint (harmless here; may be used downstream)
    out.setdefault("VDM_NEXUS", "1")

    return out, provenance


def find_approve_script(repo_root: Path) -> Path:
    p = (repo_root / REPO_REL_APPROVE).resolve()
    return p


def run_approve_tag(repo_root: Path,
                    resolved_env: Dict[str, str],
                    passthrough_args: list[str]) -> int:
    script = find_approve_script(repo_root)
    if not script.is_file():
        print(f"[NEXUS][ERROR] approve_tag.py not found at {script}", file=sys.stderr)
        return 2

    # Prefer invoking with the same Python interpreter
    cmd = [sys.executable, str(script)]
    # Passthrough args are forwarded exactly (after '--')
    cmd.extend(passthrough_args)

    # Merge environment: start from current then overlay resolved
    env = dict(os.environ)
    env.update(resolved_env)

    print("[NEXUS][INFO] Launching canonical approvals CLI")
    print(f"[NEXUS][INFO]   script: {script}")
    print(f"[NEXUS][INFO]   repo_root: {repo_root}")
    print(f"[NEXUS][INFO]   VDM_REPO_ROOT={env.get('VDM_REPO_ROOT','')}")
    print(f"[NEXUS][INFO]   VDM_APPROVAL_DB={env.get('VDM_APPROVAL_DB','')}")
    print(f"[NEXUS][INFO]   VDM_APPROVAL_ADMIN_DB={env.get('VDM_APPROVAL_ADMIN_DB','')}")

    # Inherit stdio so password prompts (if any) are visible/interactive
    try:
        proc = subprocess.run(cmd, cwd=str(repo_root))
        return proc.returncode
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"[NEXUS][ERROR] Could not invoke approvals CLI: {e}", file=sys.stderr)
        return 3


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="VDM Nexus approvals wrapper (env precedence; shells approve_tag.py)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_common(subp: argparse.ArgumentParser):
        subp.add_argument("--repo-root", help="Path to repository root (default: cwd)")
        subp.add_argument("--approval-db", help="Path to approvals DB file (VDM_APPROVAL_DB)")
        subp.add_argument("--approval-admin-db", help="Path to admin approvals DB file (VDM_APPROVAL_ADMIN_DB)")

    ap_check = sub.add_parser("check", help="Verify that approve_tag.py is resolvable")
    add_common(ap_check)

    ap_env = sub.add_parser("print-env", help="Print resolved environment (precedence CLI>env>.env)")
    add_common(ap_env)

    ap_run = sub.add_parser("run", help="Run canonical approve_tag.py with passthrough args (after --)")
    add_common(ap_run)
    ap_run.add_argument("passthrough", nargs=argparse.REMAINDER,
                        help="Arguments to pass verbatim to approve_tag.py; prefix with -- to stop wrapper parsing")

    args = ap.parse_args(argv)

    repo_root = resolve_repo_root(getattr(args, "repo_root", None))
    resolved_env, prov = resolve_env(
        getattr(args, "repo_root", None),
        getattr(args, "approval_db", None),
        getattr(args, "approval_admin_db", None),
    )

    if args.cmd == "check":
        script = find_approve_script(repo_root)
        if script.is_file():
            print(f"[NEXUS][OK] Found: {script}")
            return 0
        print(f"[NEXUS][FAIL] Not found: {script}")
        return 1

    if args.cmd == "print-env":
        print("[NEXUS][ENV] Resolved variables (source in brackets):")
        for k in ("VDM_REPO_ROOT", "VDM_APPROVAL_DB", "VDM_APPROVAL_ADMIN_DB"):
            val = resolved_env.get(k, "")
            src = prov.get(k, "unset")
            print(f"  {k}={val}  [{src}]")
        return 0

    if args.cmd == "run":
        passthrough = getattr(args, "passthrough", [])
        # Drop leading '--' if present from REMAINDER parsing
        if passthrough and passthrough[0] == "--":
            passthrough = passthrough[1:]
        if not passthrough:
            print("[NEXUS][ERROR] No arguments provided for approve_tag.py. "
                  "Use: approval_cli.py run -- <approve_tag.py args>", file=sys.stderr)
            return 2
        return run_approve_tag(repo_root, resolved_env, passthrough)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))