#!/usr/bin/env python3
"""Output 1 — Top 50 desa per kabupaten + GeoJSON."""
from pathlib import Path

import geopandas as gpd
import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, SILVER

OUT = OUTPUT_DIR / "output-1-prioritas-desa"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    prior = pd.read_parquet(GOLD / "prioritas_desa_bulanan.parquet")
    prior.to_csv(OUT / "prioritas_desa_latest.csv", index=False)

    desa = gpd.read_parquet(SILVER / "desa_sumatera_utara.parquet")
    gdf = desa.merge(prior, on="desa_id")
    gdf.to_file(OUT / "prioritas_desa_latest.geojson", driver="GeoJSON")

    print(f"[OK] prioritas {len(prior)} baris → {OUT}")


if __name__ == "__main__":
    main()
