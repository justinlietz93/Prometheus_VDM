from __future__ import annotations

from fum_rt.physics.harness_logging import enrich_payload, hash_jsonable


def test_enrich_payload_populates_gate_summary() -> None:
    base = {
        "timestamp": "2025-01-01T00:00:00Z",
        "metrics": {"status": "PASS"},
    }
    enriched = enrich_payload(
        base,
        script_name="demo_runner",
        gates={"gate_a": True, "gate_b": False},
        seeds={"seed": 1234},
        budgets={"max_ops": 8},
        hashes={"config": "abc123"},
        outputs={"figure": "/tmp/figure.png"},
        inputs={"tape": "synthetic"},
        notes=["unit-test"],
    )
    assert enriched["gates"] == {"gate_a": True, "gate_b": False}
    assert enriched["gate_summary"]["all_passed"] is False
    assert enriched["gate_summary"]["failed"] == ["gate_b"]
    assert enriched["outputs"]["figure"] == "/tmp/figure.png"
    assert enriched["seeds"]["seed"] == 1234
    assert enriched["budgets"]["max_ops"] == 8
    assert enriched["inputs"]["tape"] == "synthetic"
    assert enriched["notes"] == ["unit-test"]
    assert "repo" in enriched


def test_hash_jsonable_is_stable() -> None:
    payload = {"a": 1, "b": [3, 2, 1]}
    first = hash_jsonable(payload)
    second = hash_jsonable({"b": [3, 2, 1], "a": 1})
    assert first == second
