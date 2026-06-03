"""Indeks risiko karhutla I = 0.25G + 0.25F + 0.20H + 0.15(1-N) + 0.15(1-D)."""
from __future__ import annotations

import pandas as pd

from analitik.lib.config import BOBOT, KELAS_RISIKO


def hitung_indeks(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["indeks"] = (
        BOBOT["G"] * out["G"]
        + BOBOT["F"] * out["F"]
        + BOBOT["H"] * out["H"]
        + BOBOT["N"] * (1 - out["N"])
        + BOBOT["D"] * (1 - out["D"])
    ).round(4)
    return out


def kelas_dari_indeks(val: float) -> tuple[str, str]:
    for lo, hi, nama, warna in KELAS_RISIKO:
        if lo <= val < hi:
            return nama, warna
    return "Sangat Tinggi", "#f44336"


def tambah_kelas(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    k = out["indeks"].apply(kelas_dari_indeks)
    out["kelas_risiko"] = k.apply(lambda x: x[0])
    out["warna_hex"] = k.apply(lambda x: x[1])
    return out
