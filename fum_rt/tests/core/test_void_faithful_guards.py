import io
import os
import re

# CI guard: Ensure void-faithful reducers do not peek global structures
# and CoreEngine wiring does not scan W/CSR/adjacency for maps.

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _read(path: str) -> str:
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_reducers_event_only_no_scans():
    reducers = [
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "base_decay_map.py"),
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "heatmap.py"),
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "excitationmap.py"),
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "inhibitionmap.py"),
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "memorymap.py"),
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "trailmap.py"),
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "coldmap.py"),
    ]
    banned = re.compile(r"(synaptic|weights|adj\b|csr|coo|tocoo|tocsr|toarray)", re.IGNORECASE)
    for p in reducers:
        src = _read(p)
        # Allow docstrings/comments to mention words? Keep strict: no banned anywhere in reducer sources.
        assert not banned.search(src), f"Reducer {p} contains forbidden global-scan identifier"


def test_engine_maps_wiring_no_scans():
    # Check CoreEngine wiring for no scans and proper reducer folds
    eng = os.path.join(REPO_ROOT, "core", "engine", "core_engine.py")
    src = _read(eng)
    banned = re.compile(r"(synaptic_weights|eligibility_traces|\.adj\b|toarray|tocsr|csr|coo)", re.IGNORECASE)
    assert not banned.search(src), "CoreEngine must not scan W/CSR/adjacency when building maps/frame"

    # Ensure we actually fold the three reducers
    assert "self._heat_map.fold" in src
    assert "self._exc_map.fold" in src
    assert "self._inh_map.fold" in src

    # Header tokens are defined in maps_frame builder, validate there
    mf = os.path.join(REPO_ROOT, "core", "engine", "maps_frame.py")
    src_mf = _read(mf)
    for token in ('"topic": "maps/frame"', '"channels": ["heat", "exc", "inh"]', '"dtype": "f32"', '"endianness": "LE"'):
        assert token in src_mf, f"Missing header token in maps/frame builder: {token}"

def test_memory_kernel_no_laplacian_or_matmul():
    """
    Guard: memory kernel implementations must not introduce dense/matmul/Laplacian ops.
    Applies to core/memory/field.py (owner) and maps/memorymap.py (proxy/view).
    """
    import os, re
    REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    mem_files = [
        os.path.join(REPO_ROOT, "core", "memory", "field.py"),
        os.path.join(REPO_ROOT, "core", "cortex", "maps", "memorymap.py"),
    ]
    banned = re.compile(r"(laplacian|matmul|toarray|tocsr|csr|coo)", re.IGNORECASE)
    for p in mem_files:
        with open(p, "r", encoding="utf-8") as f:
            src = f.read()
        assert not banned.search(src), f"Memory kernel must not include dense/matmul/laplacian ops: {p}"