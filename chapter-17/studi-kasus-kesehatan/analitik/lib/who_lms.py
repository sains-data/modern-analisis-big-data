"""Z-score TB/U dengan parameter LMS WHO (WHO 2006)."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd


def zscore_lms(value: float, l: float, m: float, s: float) -> float:
    if m <= 0 or s <= 0:
        return float("nan")
    if abs(l) < 1e-7:
        return math.log(value / m) / s
    return ((value / m) ** l - 1) / (l * s)


def add_zscore_tb_u(df: pd.DataFrame, lms: pd.DataFrame) -> pd.DataFrame:
    """Join lms on usia_bulan, jenis_kelamin; kolom tb_cm -> z_tb_u."""
    merged = df.merge(
        lms,
        on=["usia_bulan", "jenis_kelamin"],
        how="left",
        suffixes=("", "_lms"),
    )
    z = []
    for _, r in merged.iterrows():
        z.append(zscore_lms(r["tb_cm"], r["L"], r["M"], r["S"]))
    merged["z_tb_u"] = z
    merged["stunting"] = merged["z_tb_u"] < -2
    merged["stunting_berat"] = merged["z_tb_u"] < -3
    return merged
