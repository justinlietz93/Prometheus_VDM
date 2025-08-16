"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import logging, json, os, sys, time


class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "ts": time.time(),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        if record.__dict__.get("extra"):
            base.update(record.__dict__["extra"])
        return json.dumps(base, ensure_ascii=False)


def get_logger(name, log_file=None):
    """
    Structured JSON logger.

    When log_file is provided, prefer a bounded rolling JSONL handler that streams
    trimmed lines into timestamped archived segments under runs/<ts>/archived/<stamp>/.
    Falls back to a plain FileHandler if the rolling handler is unavailable.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # stdout stream handler (always on)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(JsonFormatter())
        logger.addHandler(sh)

        # optional file sink
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            try:
                # Late import to avoid hard dependency during early bootstrap
                from fum_rt.io.logging.rolling_jsonl import RollingJsonlHandler as _RJHandler  # type: ignore
                fh = _RJHandler(log_file)
            except Exception:
                # Safe fallback: non-rolling file handler
                fh = logging.FileHandler(log_file)
            fh.setFormatter(JsonFormatter())
            logger.addHandler(fh)

    return logger
