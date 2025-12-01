# Must include all required helper code in /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple

import numpy as np
import sys

# Ensure common helpers on path
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from common.data.results_db import (
    begin_run,
    add_artifacts,
    log_metrics,
    end_run_success,
    end_run_failed,
)
from common.authorization.approval import check_tag_approval
