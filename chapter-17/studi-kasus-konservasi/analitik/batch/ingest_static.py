#!/usr/bin/env python3
import geopandas as gpd
import pandas as pd
from analitik.lib.config import BRONZE, SILVER, SUMBER

for p in (BRONZE, SILVER):
    p.mkdir(parents=True, exist_ok=True)


def main() -> None:
    pd.read_csv(SUMBER / "satwa" / "gps_collar" / "gps_all.csv").to_parquet(
        BRONZE / "gps_collar.parquet", index=False
    )
    pd.read_csv(SUMBER / "satelit" / "ndvi_grid.csv").to_parquet(
        BRONZE / "ndvi_grid.parquet", index=False
    )
    pd.read_csv(SUMBER / "patroli" / "smart_patrol_flat.csv").to_parquet(
        BRONZE / "smart_patrol.parquet", index=False
    )
    pd.read_csv(SUMBER / "edge" / "acoustic_classified.csv").to_parquet(
        BRONZE / "acoustic_events.parquet", index=False
    )
    gpd.read_file(SUMBER / "batas" / "kel_leuser.geojson").to_parquet(SILVER / "kel_leuser.parquet")
    gpd.read_file(SUMBER / "batas" / "konsesi.geojson").to_parquet(SILVER / "konsesi.parquet")
    gpd.read_file(SUMBER / "sosial" / "permukiman.geojson").to_parquet(SILVER / "permukiman.parquet")
    print("[OK] ingest")


if __name__ == "__main__":
    main()
