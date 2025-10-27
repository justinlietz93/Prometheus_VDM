#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from common.policy_enforcer import scan_physics_roots


@pytest.mark.policy
def test_physics_scripts_import_approval_and_io_paths():
    """
    Enforce that runnable physics scripts use the shared approval and io helpers.

    To avoid surprise failures, this test only fails when the environment variable
    VDM_ENFORCE_POLICY is set to '1'. Otherwise it will be skipped with a note.
    """
    if os.getenv("VDM_ENFORCE_POLICY") != "1":
        pytest.skip("Policy enforcement disabled (set VDM_ENFORCE_POLICY=1 to enable)")
    repo_root = Path(__file__).resolve().parents[3]
    violations = scan_physics_roots(repo_root)
    if violations:
        messages = "\n".join(f"{v.path} :: {v.reason}" for v in violations)
        pytest.fail("Policy violations detected:\n" + messages)
