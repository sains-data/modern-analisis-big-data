"""Klasifikasi lalu lintas & ISPU."""
from __future__ import annotations

from analitik.lib.config import AMBANG_LANCAR, AMBANG_PADAT, ISPU_PM25


def level_kecepatan(kmh: float) -> str:
    if kmh >= AMBANG_LANCAR:
        return "LANCAR"
    if kmh >= AMBANG_PADAT:
        return "PADAT"
    return "MACET"


def warna_kemacetan(level: str) -> str:
    return {"LANCAR": "#4caf50", "PADAT": "#ffeb3b", "MACET": "#f44336"}.get(level, "#9e9e9e")


def ispu_kategori(pm25: float) -> tuple[str, str]:
    for lo, hi, nama, warna in ISPU_PM25:
        if lo <= pm25 <= hi:
            return nama, warna
    return "BERBAHAYA", "#7e0023"
