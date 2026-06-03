#!/usr/bin/env python3
import pandas as pd
import geopandas as gpd
from analitik.lib.config import BRONZE, SILVER, SUMBER

for p in (BRONZE, SILVER):
    p.mkdir(parents=True, exist_ok=True)


def main() -> None:
    hs = pd.read_csv(SUMBER / "firms" / "viirs_riau_2025.csv")
    hs = hs[hs["confidence"].isin(["nominal", "high"])]
    hs.to_parquet(BRONZE / "firms_viirs.parquet", index=False)
    hs.to_parquet(SILVER / "hotspot_firms_verified.parquet", index=False)

    gpd.read_file(SUMBER / "konsesi" / "konsesi_riau.geojson").to_parquet(
        SILVER / "konsesi_riau.parquet"
    )
    gpd.read_file(SUMBER / "gambut" / "gambut_riau.geojson").to_parquet(
        SILVER / "gambut_riau.parquet"
    )
    pd.read_csv(SUMBER / "risiko" / "komponen_h3_20260527.csv").to_parquet(
        SILVER / "komponen_risiko_h3.parquet", index=False
    )
    pd.read_csv(SUMBER / "kesehatan" / "ispu_ispa_harian.csv").to_parquet(
        SILVER / "ispu_ispa.parquet", index=False
    )
    print("[OK] ingest Bronze/Silver")


if __name__ == "__main__":
    main()
