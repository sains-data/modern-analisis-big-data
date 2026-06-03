"""Indeks risiko multifaktor 5 dimensi."""
from __future__ import annotations

import pandas as pd

from analitik.lib.config import BOBOT_INDEKS


def minmax_norm(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.5, index=series.index)
    return (series - lo) / (hi - lo)


def hitung_indeks_total(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kolom input mentah: prev_pct, skor_sanitasi, pct_miskin, waktu_tempuh_menit, pct_air_bersih.
    Skor tinggi = risiko tinggi (akses: waktu tempuh dinormalisasi).
    """
    out = df.copy()
    out["d1_prevalensi"] = minmax_norm(out["prev_pct"])
    out["d2_sanitasi"] = 1 - minmax_norm(out["skor_sanitasi"])
    out["d3_kemiskinan"] = minmax_norm(out["pct_miskin"])
    out["d4_akses"] = minmax_norm(out["waktu_tempuh_menit"])
    out["d5_air_bersih"] = 1 - minmax_norm(out["pct_air_bersih"])

    out["indeks_total"] = sum(
        out[col] * w for col, w in BOBOT_INDEKS.items()
    )
    return out
