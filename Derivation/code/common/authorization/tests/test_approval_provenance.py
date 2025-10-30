import os
import sys
import json
from pathlib import Path
import tempfile
import shutil
import pytest


def make_repo_layout(tmpdir: Path, domain: str):
    # Create repo root and Derivation/code structure
    repo = tmpdir
    deriv = repo / "Derivation"
    code = deriv / "code"
    code.mkdir(parents=True)
    # code_root passed to check_tag_approval should be Derivation/code
    code_root = code
    # Domain dirs
    code_domain = code_root / "physics" / domain
    code_domain.mkdir(parents=True)
    deriv_domain = deriv / domain
    deriv_domain.mkdir(parents=True)
    return repo, deriv, code_root, code_domain, deriv_domain


def test_check_tag_approval_success_with_provenance(tmp_path):
    tmpdir = Path(tmp_path)
    domain = "testdomain"
    tag = "echo_spec-v1"
    repo, deriv, code_root, code_domain, deriv_domain = make_repo_layout(tmpdir, domain)

    # create a spec under code_domain/specs
    specs = code_domain / "specs"
    specs.mkdir()
    spec = specs / "spec.json"
    spec.write_text(json.dumps({"tag": tag, "x": 1}), encoding="utf-8")

    # create proposal under Derivation/<domain>
    proposal = deriv_domain / "T0_PROPOSAL_test.md"
    proposal.write_text("# 1. T0 - test\n\n> Commit: deadbeef\n", encoding="utf-8")

    # create prereg pointing to spec relative to prereg (spec_refs: ["specs/spec.json"]) under code_domain
    prereg = code_domain / f"PRE-REGISTRATION.{tag}.json"
    prereg_obj = {
        "proposal_title": "test",
        "tier_grade": "T0",
        "commit": "deadbeef",
        "spec_refs": ["specs/spec.json"],
    }
    prereg.write_text(json.dumps(prereg_obj, indent=2) + "\n", encoding="utf-8")

    # run stamping helper to populate salted_provenance and header
    sys.path.insert(0, str(code_root))
    from common.provenance.stamp_proposal import stamp
    res = stamp(proposal, prereg)

    # Create approvals DB and set tag_secret so compute_expected_key will match
    dbp = tmpdir / "approval.db"
    os.environ["VDM_APPROVAL_DB"] = str(dbp)
    from common.authorization import approval as ap

    tag_secret = "deadbeefsecret"
    ap.set_tag_secret(dbp, domain, tag, tag_secret)
    # Determine script name the same way check_tag_approval will
    script_name = os.getenv("VDM_RUN_SCRIPT") or (Path(sys.argv[0]).stem if sys.argv and sys.argv[0] else None)
    expected = ap.compute_expected_key(tag_secret, domain, tag, script_name)

    # Write APPROVAL.json into code_domain
    approval = {
        "pre_registered": True,
        "proposal": f"Derivation/{domain}/{proposal.name}",
        "allowed_tags": [tag],
        "schema_dir": str(code_domain / "schemas"),
        "approvals": {
            tag: {
                "schema": f"Derivation/code/physics/{domain}/schemas/{tag}.schema.json",
                "approved_by": "Justin K. Lietz",
                "approved_at": "2025-10-30",
                "approval_key": expected,
            }
        },
        "require_provenance": True,
    }
    (code_domain / "APPROVAL.json").write_text(json.dumps(approval, indent=2) + "\n", encoding="utf-8")

    # Ensure a minimal schema exists so schema validation passes
    (code_domain / "schemas").mkdir(parents=True, exist_ok=True)
    schema_path = code_domain / "schemas" / f"{tag}.schema.json"
    schema_path.write_text(json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "tag": tag}), encoding="utf-8")

    # Run check_tag_approval - should return approved=True
    approved, engineering_only, prop = ap.check_tag_approval(domain, tag, allow_unapproved=False, code_root=code_root)
    assert approved is True
    assert engineering_only is False
    # The function returns the manifest 'proposal' string (relative path). Verify the actual file we created exists.
    assert (deriv_domain / proposal.name).exists()


def test_missing_prereg_fails_when_required(tmp_path):
    tmpdir = Path(tmp_path)
    domain = "nodomain"
    tag = "missing-spec"
    repo, deriv, code_root, code_domain, deriv_domain = make_repo_layout(tmpdir, domain)

    # Create proposal
    proposal = deriv_domain / "T0_PROPOSAL_test.md"
    proposal.write_text("# 1. T0 - test\n\n> Commit: deadbeef\n", encoding="utf-8")

    # Write APPROVAL.json that requires provenance but no prereg/spec exists
    approval = {
        "pre_registered": True,
        "proposal": f"Derivation/{domain}/{proposal.name}",
        "allowed_tags": [tag],
        "schema_dir": str(code_domain / "schemas"),
        "approvals": {tag: {"schema": "", "approved_by": "Justin K. Lietz", "approval_key": "x"}},
        "require_provenance": True,
    }
    (code_domain / "APPROVAL.json").write_text(json.dumps(approval, indent=2) + "\n", encoding="utf-8")

    sys.path.insert(0, str(code_root))
    from common.authorization import approval as ap

    # Ensure DB path set to temp to avoid default discovery
    dbp = tmpdir / "approval2.db"
    os.environ["VDM_APPROVAL_DB"] = str(dbp)

    with pytest.raises(SystemExit):
        ap.check_tag_approval(domain, tag, allow_unapproved=False, code_root=code_root)


def test_mismatched_salted_hash_fails(tmp_path):
    tmpdir = Path(tmp_path)
    domain = "badhash"
    tag = "bad-tag"
    repo, deriv, code_root, code_domain, deriv_domain = make_repo_layout(tmpdir, domain)

    specs = code_domain / "specs"
    specs.mkdir()
    spec = specs / "spec.json"
    spec.write_text(json.dumps({"tag": tag, "x": 1}), encoding="utf-8")

    proposal = deriv_domain / "T0_PROPOSAL_test.md"
    proposal.write_text("# 1. T0 - test\n\n> Commit: deadbeef\n", encoding="utf-8")

    prereg = code_domain / f"PRE-REGISTRATION.{tag}.json"
    prereg_obj = {"proposal_title": "test", "tier_grade": "T0", "commit": "deadbeef", "spec_refs": ["specs/spec.json"]}
    prereg.write_text(json.dumps(prereg_obj, indent=2) + "\n", encoding="utf-8")

    sys.path.insert(0, str(code_root))
    from common.provenance.stamp_proposal import stamp
    stamp(proposal, prereg)

    # Corrupt prereg salted_provenance (tamper base_sha256)
    pdata = json.loads(prereg.read_text(encoding="utf-8"))
    sp = pdata.get("salted_provenance")
    sp["items"][0]["base_sha256"] = "0" * 64
    prereg.write_text(json.dumps(pdata, indent=2) + "\n", encoding="utf-8")

    # Write APPROVAL.json with DB-backed key
    dbp = tmpdir / "approval3.db"
    os.environ["VDM_APPROVAL_DB"] = str(dbp)
    from common.authorization import approval as ap
    tag_secret = "s3cr3t"
    ap.set_tag_secret(dbp, domain, tag, tag_secret)
    script_name = os.getenv("VDM_RUN_SCRIPT") or (Path(sys.argv[0]).stem if sys.argv and sys.argv[0] else None)
    expected = ap.compute_expected_key(tag_secret, domain, tag, script_name)

    approval = {
        "pre_registered": True,
        "proposal": f"Derivation/{domain}/{proposal.name}",
        "allowed_tags": [tag],
        "schema_dir": str(code_domain / "schemas"),
        "approvals": {tag: {"schema": "", "approved_by": "Justin K. Lietz", "approval_key": expected}},
        "require_provenance": True,
    }
    (code_domain / "APPROVAL.json").write_text(json.dumps(approval, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        ap.check_tag_approval(domain, tag, allow_unapproved=False, code_root=code_root)
