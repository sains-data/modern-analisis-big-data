"""Indeks tekanan kawasan I = w1*D + w2*P + w3*A + w4*K - w5*R."""
from __future__ import annotations

import pandas as pd

from analitik.lib.config import BOBOT_TEKANAN


def minmax(s: pd.Series) -> pd.Series:
    lo, hi = s.min(), s.max()
    if hi == lo:
        return pd.Series(0.5, index=s.index)
    return (s - lo) / (hi - lo)


def hitung_indeks_tekanan(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["D_n"] = minmax(out["laju_deforestasi"])
    out["P_n"] = minmax(out["lonjakan_ndvi"])
    out["A_n"] = minmax(out["frekuensi_acoustic"])
    out["K_n"] = minmax(out["konflik_historis"])
    out["R_n"] = minmax(out["densitas_patroli"])
    out["indeks_tekanan"] = (
        BOBOT_TEKANAN["D"] * out["D_n"]
        + BOBOT_TEKANAN["P"] * out["P_n"]
        + BOBOT_TEKANAN["A"] * out["A_n"]
        + BOBOT_TEKANAN["K"] * out["K_n"]
        - BOBOT_TEKANAN["R"] * out["R_n"]
    ).round(4)
    return out
