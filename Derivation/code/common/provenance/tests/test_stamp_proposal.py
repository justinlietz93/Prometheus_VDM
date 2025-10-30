import sys
from pathlib import Path
import json


def setup_code_root():
    # Ensure Derivation/code is on sys.path so `common.provenance` imports work
    p = Path(__file__).resolve()
    code_root = p.parents[3]
    sys.path.insert(0, str(code_root))


def test_stamp_creates_header_and_writes_prereg(tmp_path):
    setup_code_root()
    from common.provenance.stamp_proposal import stamp

    # Create minimal proposal and prereg/spec in same dir
    d = tmp_path / "work"
    d.mkdir()
    spec = d / "spec.json"
    spec.write_text(json.dumps({"tag": "test-spec", "value": 123}), encoding="utf-8")

    prereg = d / "PRE-REGISTRATION.test.json"
    prereg_obj = {
        "proposal_title": "test",
        "tier_grade": "T0",
        "commit": "deadbeef",
        "spec_refs": ["spec.json"],
    }
    prereg.write_text(json.dumps(prereg_obj, indent=2) + "\n", encoding="utf-8")

    proposal = d / "T0_PROPOSAL_test.md"
    proposal.write_text("# 1. T0 - test\n\n> Commit: deadbeef\n", encoding="utf-8")

    res = stamp(proposal, prereg)

    # prereg should now contain salted_provenance
    pdata = json.loads(prereg.read_text(encoding="utf-8"))
    assert "salted_provenance" in pdata
    sp = pdata["salted_provenance"]
    assert sp["schema"].startswith("vdm.provenance.salted_hash")
    assert sp["items"][0]["base_sha256"]

    # proposal should contain the header line
    txt = proposal.read_text(encoding="utf-8")
    assert "Salted Provenance:" in txt

    # result dict should include expected keys and match prereg manifest
    assert "prereg_manifest" in res
    from hashlib import sha256

    expected = sha256(prereg.read_bytes()).hexdigest()
    assert res["prereg_manifest"] == expected
