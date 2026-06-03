"""Klasifikasi level siaga banjir dari TMA dan hujan."""
from __future__ import annotations

from analitik.lib.config import (
    HUJAN_KUNING_MIN,
    HUJAN_MERAH_MIN,
    HUJAN_ORANYE_MIN,
    TMA_HIJAU_MAX,
    TMA_KUNING_MAX,
    TMA_ORANYE_MAX,
)

LEVEL_ORDER = {"HIJAU": 0, "KUNING": 1, "ORANYE": 2, "MERAH": 3}


def level_from_tma(tma_cm: float) -> str:
    if tma_cm >= TMA_ORANYE_MAX:
        return "MERAH"
    if tma_cm >= TMA_KUNING_MAX:
        return "ORANYE"
    if tma_cm >= TMA_HIJAU_MAX:
        return "KUNING"
    return "HIJAU"


def level_from_hujan(hujan_3jam_mm: float) -> str:
    if hujan_3jam_mm >= HUJAN_MERAH_MIN:
        return "MERAH"
    if hujan_3jam_mm >= HUJAN_ORANYE_MIN:
        return "ORANYE"
    if hujan_3jam_mm >= HUJAN_KUNING_MIN:
        return "KUNING"
    return "HIJAU"


def combine_siaga(tma_cm: float, hujan_3jam_mm: float = 0.0) -> str:
    """Ambil level lebih tinggi antara TMA dan hujan."""
    tma_lv = level_from_tma(tma_cm)
    rain_lv = level_from_hujan(hujan_3jam_mm)
    return tma_lv if LEVEL_ORDER[tma_lv] >= LEVEL_ORDER[rain_lv] else rain_lv
