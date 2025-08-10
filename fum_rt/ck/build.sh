
    #!/usr/bin/env bash
    set -euo pipefail
    python3 - <<'PY'
import sys, os, subprocess, textwrap
from pathlib import Path
code = r"""
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os

hipcc = os.environ.get("HIPCC", "hipcc")

ext = Extension(
    "fum_ck",
    sources=["ck/hip_spmv.cpp"],
    extra_compile_args=[f"-std=c++17"],
    # You may need to add include/library paths for pybind11 and HIP here.
)

setup(
    name="fum_ck",
    version="0.0.1",
    ext_modules=[ext],
)
"""
Path("setup.py").write_text(code)
subprocess.check_call([sys.executable, "setup.py", "build_ext", "--inplace"])
PY
