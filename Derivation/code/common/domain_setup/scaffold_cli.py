#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Experiment scaffolding CLI

Creates a new proposed experiment skeleton with the minimum, machine-readable
artifacts required by the PROPOSAL template:
- Derivation/{domain}/{Tier}_PROPOSAL_{Experiment}.md
- Derivation/code/physics/{domain}/APPROVAL.json
- Derivation/code/physics/{domain}/PRE-REGISTRATION.json
- Derivation/code/physics/{domain}/schemas/{tag}.schema.json
- Derivation/code/physics/{domain}/specs/{run}.{version}.json
- Derivation/code/physics/{domain}/run_{experiment}.py
- Derivation/code/physics/{domain}/README.md

Usage:
  python Derivation/code/common/domain_setup/scaffold_cli.py \
    --domain plasma \
    --experiment ceg_harness \
    --tier T0 \
    --run-name ceg_harness \
    --version 0.1.0 \
    --tag ceg_harness-0.1.0 \
    --author "Justin K. Lietz" \
    --contact "justin@neuroca.ai" \
    --summary "Initial concept scaffolding"

Notes:
- The CLI auto-detects the repo root relative to this file.
- It will NOT overwrite existing files unless --force is provided.
- The --force flag should trigger an admin password check that matches the admin APPROVAL check password.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import secrets
import subprocess
import shutil
import sys
from typing import Dict, Any

HERE = Path(__file__).resolve()
# repo_root = .../Prometheus_VDM
REPO_ROOT = HERE.parents[4]
TEMPLATES_DIR = REPO_ROOT / "Derivation" / "Templates"
DOMAIN_TEMPLATE_DIR = REPO_ROOT / "Derivation" / "code" / "common" / "domain_setup" / "{domain-name}"

# Ensure 'Derivation/code' is on sys.path for package imports like common.authorization
CODE_ROOT = REPO_ROOT / "Derivation" / "code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))


def git_rev() -> str:
    try:
        git_bin = shutil.which("git")
        if not git_bin:
            return "<unknown>"
        result = subprocess.run([git_bin, "rev-parse", "HEAD"], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return "<unknown>"


def salted_hash(commit: str) -> str:
    salt = secrets.token_hex(16)
    import hashlib

    return hashlib.sha256(f"{commit}:{salt}".encode()).hexdigest()


def write_text(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        print(f"SKIP (exists): {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"WROTE: {path}")


def write_json(path: Path, obj: Dict[str, Any] | list, *, force: bool) -> None:
    if path.exists() and not force:
        print(f"SKIP (exists): {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE: {path}")


def render_proposal_header(tier: str, experiment: str, contact: str, summary: str) -> str:
    commit = git_rev()
    prov = salted_hash(commit)
    created = dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    header = (
        f"# 1. {tier} - {experiment}\n\n"
        f"> Created Date:  \n"
        f"> {commit}  \n"
        f"> {prov}  \n"
        f"> Proposer contact(s):  (<{contact}>)\n"
        f"> Short summary (one sentence TL;DR):  {summary}\n\n"
    )
    return header


def generate_proposal(domain: str, tier: str, experiment: str, contact: str, summary: str, *, force: bool) -> Path:
    template_path = TEMPLATES_DIR / "PROPOSAL_PAPER_TEMPLATE.md"
    proposal_dir = REPO_ROOT / "Derivation" / domain
    proposal_dir.mkdir(parents=True, exist_ok=True)
    proposal_path = proposal_dir / f"{tier}_PROPOSAL_{experiment}.md"

    template = template_path.read_text(encoding="utf-8")
    # Replace only the first title section and the small header block with concrete values
    header = render_proposal_header(tier, experiment, contact, summary)

    # Replace the first line title and initial metadata block.
    # Strategy: find the line that starts with '# 1. ' and replace that line, then insert header block.
    lines = template.splitlines()
    out_lines = []
    replaced_title = False
    inserted_header = False
    for i, ln in enumerate(lines):
        if not replaced_title and ln.startswith("# 1. "):
            out_lines.append(f"# 1. {tier} - {experiment}")
            replaced_title = True
            # Skip following quoted block in template and insert our header instead.
            # Consume subsequent lines starting with '>' from the template's header block.
            j = i + 1
            # Collect lines to skip (original quoted header block)
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                j += 1
            out_lines.append("")
            out_lines.append(header.strip())
            inserted_header = True
            # Continue from j
            for k in range(j, len(lines)):
                out_lines.append(lines[k])
            break
    if not replaced_title:
        # Fallback: prepend header to template
        out = header + "\n" + template
    else:
        out = "\n".join(out_lines) + "\n"

    write_text(proposal_path, out, force=force)
    return proposal_path


def generate_approval(domain: str, tier: str, experiment: str, run_name: str, version: str, tag: str, author: str, *, force: bool) -> Path:
    domain_dir = REPO_ROOT / "Derivation" / "code" / "physics" / domain
    approval_path = domain_dir / "APPROVAL.json"
    schema_dir = str(domain_dir / "schemas")
    schema_rel = f"Derivation/code/physics/{domain}/schemas/{tag}.schema.json"

    manifest = [
        {
            "preflight_name": "preflight",
            "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
            "author": author,
            "requires_approval": True,
            "pre_commit_hook": True,
            "notes": f"Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at Derivation/{domain}/ and approved."
        },
        {
            "pre_registered": True,
            "proposal": f"Derivation/{domain}/{tier}_PROPOSAL_{experiment}.md",
            "allowed_tags": [tag],
            "schema_dir": schema_dir,
            "approvals": {
                tag: {
                    "schema": schema_rel,
                    "approved_by": "<approver>",
                    "approved_at": "<auto-generated>",
                    "approval_key": "<hashed-key>"
                }
            }
        }
    ]
    write_json(approval_path, manifest, force=force)
    return approval_path


def generate_prereg(domain: str, tier: str, experiment: str, spec_rel: str, contact: str, *, force: bool) -> Path:
    prereg_path = REPO_ROOT / "Derivation" / "code" / "physics" / domain / "PRE-REGISTRATION.json"
    commit = git_rev()
    obj = {
        "proposal_title": experiment,
        "tier_grade": tier,
        "commit": commit,
        "salted_provenance": salted_hash(commit),
        "contact": [contact],
        "hypotheses": [
            {"id": "H1", "statement": "<testable statement>", "direction": "increase|decrease|no-change"}
        ],
        "variables": {
            "independent": ["<var1>", "<var2>"],
            "dependent": ["<response>"],
            "controls": ["<control1>"]
        },
        "pass_fail": [
            {"metric": "<name>", "operator": ">=|<=|==|!=", "threshold": 0, "unit": "<unit>"}
        ],
        "spec_refs": [spec_rel],
        "registration_timestamp": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    write_json(prereg_path, obj, force=force)
    return prereg_path


def generate_schema(domain: str, tag: str, *, force: bool) -> Path:
    path = REPO_ROOT / "Derivation" / "code" / "physics" / domain / "schemas" / f"{tag}.schema.json"
    obj = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:{domain}:{tag}",
        "title": f"{tag} schema",
        "type": "object",
        "properties": {},
        "required": []
    }
    write_json(path, obj, force=force)
    return path


def generate_spec(domain: str, run_name: str, version: str, tag: str, *, force: bool) -> Path:
    path = REPO_ROOT / "Derivation" / "code" / "physics" / domain / "specs" / f"{run_name}.{version}.json"
    schema_ref = f"Derivation/code/physics/{domain}/schemas/{tag}.schema.json"
    obj = {
        "run_name": run_name,
        "version": version,
        "tag": tag,
        "schema_ref": schema_ref,
        "parameters": {},
        "seeds": [0]
    }
    write_json(path, obj, force=force)
    return path


def generate_runner_and_readme(domain: str, experiment: str, *, force: bool) -> None:
    dst_dir = REPO_ROOT / "Derivation" / "code" / "physics" / domain
    dst_dir.mkdir(parents=True, exist_ok=True)

    # README
    readme_tmpl = (DOMAIN_TEMPLATE_DIR / "README.md").read_text(encoding="utf-8")
    readme = readme_tmpl.replace("{domain name}", domain)
    write_text(dst_dir / "README.md", readme, force=force)

    # Runner
    runner_tmpl = (DOMAIN_TEMPLATE_DIR / "run_{experiment_name}.py").read_text(encoding="utf-8")
    runner = runner_tmpl.replace("{experiment_name}", experiment)
    write_text(dst_dir / f"run_{experiment}.py", runner, force=force)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Scaffold a new experiment")
    p.add_argument("--domain", required=True, help="Domain name (e.g., plasma, gravity)")
    p.add_argument("--experiment", required=True, help="Experiment identifier (e.g., ceg_harness)")
    p.add_argument("--tier", required=True, choices=[f"T{i}" for i in range(10)], help="Tier grade T0–T9")
    p.add_argument("--run-name", required=False, help="Run name (defaults to experiment)")
    p.add_argument("--version", default="0.1.0", help="Spec version (semver)")
    p.add_argument("--tag", required=False, help="Tag name (defaults to <experiment>-<version>)")
    p.add_argument("--author", default="<author>", help="Author name for APPROVAL manifest")
    p.add_argument("--contact", default="<email>", help="Contact email for proposal/prereg")
    p.add_argument("--summary", default="<fill in>", help="Short TL;DR summary for proposal header")
    p.add_argument("--force", action="store_true", help="Overwrite existing files")

    args = p.parse_args(argv)

    # If --force is requested, require admin password verification against approvals admin DB
    if args.force:
        try:
            import getpass  # standard lib
            from common.authorization.approval import get_admin_db_path, ensure_admin_verified  # type: ignore
        except Exception as e:
            print(f"ERROR: Unable to load approval admin utilities for --force check: {e}", file=sys.stderr)
            return 12
        admin_db = get_admin_db_path()
        if not admin_db:
            print("ERROR: No approvals admin DB path could be resolved. Set VDM_APPROVAL_ADMIN_DB or VDM_APPROVAL_DB, or configure via .env.", file=sys.stderr)
            return 13
        try:
            password = getpass.getpass("Admin password (for approvals DB) to proceed with --force (won't echo): ")
        except Exception as e:
            print(f"ERROR: Unable to read admin password: {e}", file=sys.stderr)
            return 14
        if not password:
            print("ERROR: A non-empty admin password is required to use --force.", file=sys.stderr)
            return 15
        if not ensure_admin_verified(admin_db, password):
            print("ERROR: Admin password did not match stored approvals admin password.", file=sys.stderr)
            return 16

    domain = args.domain.strip()
    experiment = args.experiment.strip()
    tier = args.tier.strip().upper()
    run_name = (args.run_name or experiment).strip()
    version = args.version.strip()
    tag = (args.tag or f"{experiment}-{version}").strip()

    # Ensure base dirs
    (REPO_ROOT / "Derivation" / "code" / "physics" / domain / "schemas").mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "Derivation" / "code" / "physics" / domain / "specs").mkdir(parents=True, exist_ok=True)

    # Generate artifacts
    spec_path = generate_spec(domain, run_name, version, tag, force=args.force)
    schema_path = generate_schema(domain, tag, force=args.force)
    approval_path = generate_approval(domain, tier, experiment, run_name, version, tag, args.author, force=args.force)
    generate_runner_and_readme(domain, experiment, force=args.force)

    # Proposal and preregistration
    proposal_path = generate_proposal(domain, tier, experiment, args.contact, args.summary, force=args.force)
    spec_rel = str(spec_path.relative_to(REPO_ROOT))
    prereg_path = generate_prereg(domain, tier, experiment, spec_rel, args.contact, force=args.force)

    print("\nScaffold complete. Artifacts:")
    for pth in [proposal_path, approval_path, prereg_path, schema_path, spec_path, (REPO_ROOT / "Derivation" / "code" / "physics" / domain / f"run_{experiment}.py"), (REPO_ROOT / "Derivation" / "code" / "physics" / domain / "README.md")]:
        print(" -", pth.relative_to(REPO_ROOT))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
