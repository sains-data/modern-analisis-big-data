"""Klasifikasi alert kader Posyandu."""
from __future__ import annotations


def classify_alert(
    z_tb_u: float,
    delta_bb_gram: float | None = None,
    bulan_absen: int = 0,
    z_prev: float | None = None,
) -> str | None:
    """
    MERAH / ORANYE / KUNING / None (normal).
    """
    if delta_bb_gram is not None and delta_bb_gram < -200:
        return "MERAH"
    if z_tb_u < -3:
        return "MERAH"
    if z_prev is not None and (z_prev - z_tb_u) > 0.5:
        return "ORANYE"
    if bulan_absen >= 2:
        return "ORANYE"
    if -2 <= z_tb_u < -1.5:
        return "KUNING"
    return None
