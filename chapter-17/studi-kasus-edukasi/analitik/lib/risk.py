"""Klasifikasi tingkat risiko."""
from __future__ import annotations

from analitik.lib.config import RISIKO_LEVEL


def tingkat_risiko(prob: float) -> str:
    for threshold, level in RISIKO_LEVEL:
        if prob >= threshold:
            return level
    return "RENDAH"
