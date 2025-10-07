#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple
import json
import sys
import os


def check_tag_approval(domain: str, tag: str, allow_unapproved: bool, code_root: Path) -> Tuple[bool, bool, Optional[str]]:
    """
    Simple shared utility to enforce proposal-based tag approval.

    Looks for an APPROVAL.json file under Derivation/<domain>/ with the shape:
    {
      "pre_registered": true,
      "proposal": "derivation/<domain>/PROPOSAL_*.md",
      "allowed_tags": ["tag1", "tag2", ...]
    }

    - Returns (approved, engineering_only, proposal_path)
    - If not approved and allow_unapproved=False, exits with code 2 and an error message.
    - If not approved and allow_unapproved=True, engineering_only=True (artifacts should be quarantined by caller).
    """
    derivation_dir = code_root.parent  # Derivation/
    apath = derivation_dir / domain / "APPROVAL.json"
    approved = False
    proposal: Optional[str] = None
    try:
        if apath.exists():
            with apath.open("r", encoding="utf-8") as f:
                adata = json.load(f)
            allowed = set(adata.get("allowed_tags", []))
            proposal = adata.get("proposal")
            approved = bool(adata.get("pre_registered", False) and proposal and (tag in allowed))
    except Exception:
        approved = False

    if not approved and not allow_unapproved:
        print(
            (
                f"ERROR: tag '{tag}' is not approved for domain '{domain}'. "
                f"Add it to {apath} with pre_registered=true and a proposal path, "
                f"or pass --allow-unapproved for engineering-only (artifacts will be quarantined)."
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    engineering_only = not approved
    # Publish minimal policy context to environment so io helpers can enforce
    os.environ["VDM_POLICY_APPROVED"] = "1" if approved else "0"
    os.environ["VDM_POLICY_ENGINEERING"] = "1" if engineering_only else "0"
    os.environ["VDM_POLICY_TAG"] = str(tag)
    os.environ["VDM_POLICY_DOMAIN"] = str(domain)
    if proposal:
        os.environ["VDM_POLICY_PROPOSAL"] = str(proposal)
    return approved, engineering_only, proposal
