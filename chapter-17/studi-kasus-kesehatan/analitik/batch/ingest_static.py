#!/usr/bin/env python3
"""Ingest sumber → Bronze/Silver."""
from pathlib import Path

import geopandas as gpd
import pandas as pd

from analitik.lib.config import BRONZE, SILVER, SUMBER

for p in (BRONZE, SILVER):
    p.mkdir(parents=True, exist_ok=True)


def main() -> None:
    pd.read_csv(SUMBER / "who" / "who_lms_tb_u.csv").to_parquet(
        SILVER / "who_lms_standar.parquet", index=False
    )
    epp = pd.read_csv(SUMBER / "eppgbm" / "eppgbm_202605.csv", dtype={"desa_id": str})
    epp.to_parquet(BRONZE / "eppgbm.parquet", index=False)
    desa = gpd.read_file(SUMBER / "batas" / "desa_sumut.geojson")
    desa["desa_id"] = desa["desa_id"].astype(str)
    desa.to_parquet(SILVER / "desa_sumatera_utara.parquet")
    gpd.read_file(SUMBER / "batas" / "puskesmas.geojson").to_parquet(
        SILVER / "puskesmas.parquet"
    )
    stbm = pd.read_csv(SUMBER / "stbm" / "stbm_dtks_desa.csv", dtype={"desa_id": str})
    stbm.to_parquet(SILVER / "stbm_dtks.parquet", index=False)
    print("[OK] Bronze/Silver ingest")


if __name__ == "__main__":
    main()
