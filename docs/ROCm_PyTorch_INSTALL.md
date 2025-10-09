# PyTorch on AMD ROCm - Installation Guide

Your system reports ROCm agents gfx908 (MI100) and gfx1100 (RX 7900 XTX). Use ROCm wheels for PyTorch instead of the default CPU wheels.

Quick start (recommended):

1. Install base deps:

   - pip install -r requirements.txt

2. Install ROCm PyTorch stack (use the latest published ROCm wheel index supported by PyTorch; compatible with ROCm 6.4.3):

   - pip install --index-url <https://download.pytorch.org/whl/rocm6.2> torch torchvision torchaudio

Notes:

- PyTorch currently publishes ROCm wheels under rocm6.0/6.1/6.2. With ROCm 6.4.3 installed, rocm6.2 wheels are typically compatible. If a newer rocm6.4 index appears upstream, prefer that.
- Verify GPU visibility in PyTorch:

   - python -c "import torch; print(torch.__version__, getattr(torch.version, 'hip', None), torch.cuda.is_available())"

- Optional: use requirements-rocm.txt with the ROCm index to manage versions.

Troubleshooting:

- If torch cannot find HIP/ROCm, ensure rocminfo shows your GPUs and that HIP runtime packages are installed.
- Some third-party libs like opencv-python may pull CPU-only builds; that’s fine-they don’t use ROCm.
