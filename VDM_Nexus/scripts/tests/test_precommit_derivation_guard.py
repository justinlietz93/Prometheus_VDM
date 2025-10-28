import importlib.util
import sys
from pathlib import Path
from types import ModuleType
import pytest


# Utilities to load the guard module fresh per test
def load_guard() -> ModuleType:
    path = Path("VDM_Nexus/scripts/precommit_derivation_guard.py").resolve()
    assert path.exists(), f"Guard not found at {path}"
    spec = importlib.util.spec_from_file_location("vdm_guard", str(path))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


def run_main_with(
    monkeypatch: pytest.MonkeyPatch,
    *,
    mode: str = "ci",
    changed: list[str] = None,
    base: str = "origin/main",
    require_canon: bool = False,
    no_chain_attestation: bool = False,
    chronicles_text: str = "",
) -> int:
    """
    Invoke guard.main() with patched git-change providers and CHRONICLES content.

    - mode: "ci" or "precommit"
    - changed: list of changed file paths (simulates git diff)
    - chronicles_text: content returned by read_file_text(CHRONICLES_PATH)
    """
    guard = load_guard()
    changed = changed or []

    # Patch the git diff providers used by main()
    if mode == "precommit":
        monkeypatch.setattr(guard, "git_changed_files_precommit", lambda: list(changed))
    else:
        monkeypatch.setattr(guard, "git_changed_files_vs_base", lambda _base: list(changed))

    # Patch CHRONICLES loader
    def fake_read_file_text(p: str) -> str:
        return chronicles_text if p == guard.CHRONICLES_PATH else ""
    monkeypatch.setattr(guard, "read_file_text", fake_read_file_text)

    # Build argv
    argv = ["prog", "--mode", mode]
    if mode == "ci":
        argv += ["--base", base]
    if require_canon:
        argv += ["--require-canon"]
    if no_chain_attestation:
        argv += ["--no-chain-attestation"]

    monkeypatch.setattr(sys, "argv", argv)

    # Run and return exit code
    return guard.main()


# -------------------------
# Test cases
# -------------------------


def test_no_derivation_changes_pass(monkeypatch: pytest.MonkeyPatch):
    """
    If no tracked Derivation/ changes are present, guard must PASS.
    """
    rc = run_main_with(monkeypatch, mode="ci", changed=["README.md"])
    assert rc == 0


def test_exclusions_respected(monkeypatch: pytest.MonkeyPatch):
    """
    Files under excluded paths (e.g., Derivation/References/**) should not trigger the guard.
    No CHRONICLES needed when all Derivation changes are excluded.
    """
    rc = run_main_with(monkeypatch, mode="ci", changed=["Derivation/References/paper.pdf"])
    assert rc == 0


def test_derivation_change_without_chronicles_fails(monkeypatch: pytest.MonkeyPatch):
    """
    Any tracked Derivation/ change requires Derivation/CHRONICLES.md in the same diff.
    """
    rc = run_main_with(monkeypatch, mode="ci", changed=["Derivation/README.md"])
    assert rc == 1


def test_chronicles_only_bypass_for_non_legit_change_passes(monkeypatch: pytest.MonkeyPatch):
    """
    Non-legit Derivation change (not matching LEGIT_CHANGE_PATTERNS) may PASS with only CHRONICLES updated.
    """
    changed = ["Derivation/README.md", "Derivation/CHRONICLES.md"]
    rc = run_main_with(monkeypatch, mode="ci", changed=changed)
    assert rc == 0


def test_legit_change_requires_canon_doc_and_chain_attestation(monkeypatch: pytest.MonkeyPatch):
    """
    Legitimate change: run_*.py under Derivation triggers canonical doc update and chain attestation.
    1) Missing canon doc + missing attestation -> FAIL
    2) Canon doc present but missing attestation -> FAIL
    3) Canon doc present + attestation present -> PASS
    """
    run_path = "Derivation/code/physics/metriplectic/run_kg_dispersion.py"
    chronicles = "Derivation/CHRONICLES.md"

    # 1) Missing canon doc + missing attestation
    changed = [run_path, chronicles]
    rc = run_main_with(monkeypatch, mode="ci", changed=changed, chronicles_text="")
    assert rc == 1

    # 2) Canon doc present but missing attestation
    changed2 = [run_path, chronicles, "Derivation/EQUATIONS.md"]
    rc2 = run_main_with(monkeypatch, mode="ci", changed=changed2, chronicles_text="")
    assert rc2 == 1

    # 3) Canon doc present + attestation present
    chron_with_marker = "Some notes\nDependency-Chain-Reviewed: true\nMore notes"
    rc3 = run_main_with(monkeypatch, mode="ci", changed=changed2, chronicles_text=chron_with_marker)
    assert rc3 == 0


def test_require_canon_flag_forces_canon_even_if_not_legit(monkeypatch: pytest.MonkeyPatch):
    """
    --require-canon forces canon doc update requirement even for non-legit Derivation changes.
    """
    # Non-legit change (README) with CHRONICLES updated but no canon doc
    changed = ["Derivation/README.md", "Derivation/CHRONICLES.md"]
    rc = run_main_with(
        monkeypatch,
        mode="ci",
        changed=changed,
        require_canon=True,
        chronicles_text="notes only (no attestation)"
    )
    # Should fail because a canon doc wasn't updated (and also missing attestation, but first condition is enough)
    assert rc == 1

    # Now include a canon doc but still missing attestation -> still fails
    changed2 = changed + ["Derivation/VALIDATION_METRICS.md"]
    rc2 = run_main_with(
        monkeypatch,
        mode="ci",
        changed=changed2,
        require_canon=True,
        chronicles_text="notes only (no attestation)"
    )
    assert rc2 == 1

    # Include attestation marker to pass
    chron_with_marker = "Change rationale\nDependency-Chain-Reviewed: true\n"
    rc3 = run_main_with(
        monkeypatch,
        mode="ci",
        changed=changed2,
        require_canon=True,
        chronicles_text=chron_with_marker
    )
    assert rc3 == 0


def test_precommit_mode_path(monkeypatch: pytest.MonkeyPatch):
    """
    Smoke check precommit mode wiring: behaves like CI with same logic paths.
    """
    # Derivation change without CHRONICLES should fail in precommit mode as well
    rc = run_main_with(monkeypatch, mode="precommit", changed=["Derivation/SCHEMAS.md"])
    assert rc == 1

    # Add CHRONICLES; non-legit -> pass
    rc2 = run_main_with(
        monkeypatch,
        mode="precommit",
        changed=["Derivation/SCHEMAS.md", "Derivation/CHRONICLES.md"],
    )
    assert rc2 == 0


def test_no_chain_attestation_flag_disables_marker_requirement(monkeypatch: pytest.MonkeyPatch):
    """
    --no-chain-attestation disables the Dependency-Chain-Reviewed marker requirement.
    Canon doc is still required for legit changes.
    """
    run_path = "Derivation/code/physics/metriplectic/run_kg_dispersion.py"
    changed = [run_path, "Derivation/CHRONICLES.md", "Derivation/ROADMAP.md"]

    # Without attestation marker but with --no-chain-attestation -> PASS
    rc = run_main_with(
        monkeypatch,
        mode="ci",
        changed=changed,
        no_chain_attestation=True,
        chronicles_text="no attestation"
    )
    assert rc == 0