#!/usr/bin/env python3
"""Z-score TB/U + validasi rentang BB/TB."""
import pandas as pd

from analitik.lib.config import BRONZE, GOLD, SILVER
from analitik.lib.who_lms import add_zscore_tb_u

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    balita = pd.read_parquet(BRONZE / "eppgbm.parquet")
    lms = pd.read_parquet(SILVER / "who_lms_standar.parquet")

    balita = balita[(balita["bb_kg"] >= 1) & (balita["bb_kg"] <= 50)]
    balita = balita[(balita["tb_cm"] >= 30) & (balita["tb_cm"] <= 130)]
    balita = balita[(balita["usia_bulan"] >= 0) & (balita["usia_bulan"] <= 60)]

    scored = add_zscore_tb_u(balita, lms)
    scored.to_parquet(SILVER / "data_balita.parquet", index=False)
    scored.to_parquet(GOLD / "rekam_tumbuh_balita.parquet", index=False)

    n_st = int(scored["stunting"].sum())
    print(f"[OK] silver/data_balita — stunting: {n_st}/{len(scored)} ({100*n_st/len(scored):.1f}%)")


if __name__ == "__main__":
    main()
