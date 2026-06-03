#!/usr/bin/env python3
import geopandas as gpd
import pandas as pd
from analitik.lib.config import BRONZE, SILVER, SUMBER

for p in (BRONZE, SILVER):
    p.mkdir(parents=True, exist_ok=True)


def main() -> None:
    gpd.read_file(SUMBER / "osm" / "medan" / "ruas_jalan.geojson").to_parquet(BRONZE / "jalan_medan.parquet")
    gpd.read_file(SUMBER / "transport" / "gtfs_tmd" / "halte.geojson").to_parquet(BRONZE / "gtfs_halte.parquet")
    gpd.read_file(SUMBER / "transport" / "gtfs_tmd" / "routes.geojson").to_parquet(BRONZE / "gtfs_routes.parquet")
    pd.read_csv(SUMBER / "udara" / "openaq" / "sensor_harian.csv").to_parquet(
        BRONZE / "sensor_udara.parquet", index=False
    )
    pd.read_csv(SUMBER / "probe" / "gps" / "probe_harian.csv").to_parquet(
        BRONZE / "probe_vehicle.parquet", index=False
    )
    gpd.read_file(SUMBER / "kecelakaan" / "kecelakaan.geojson").to_parquet(BRONZE / "kecelakaan.parquet")
    pd.read_csv(SUMBER / "cuaca" / "bmkg" / "angin_harian.csv").to_parquet(
        BRONZE / "bmkg_angin.parquet", index=False
    )

    gpd.read_file(SUMBER / "osm" / "medan" / "ruas_jalan.geojson").to_parquet(SILVER / "ruas_jalan.parquet")
    gpd.read_file(SUMBER / "sosial" / "populasi" / "kelurahan_medan.geojson").to_parquet(
        SILVER / "kelurahan.parquet"
    )
    gpd.read_file(SUMBER / "transport" / "gtfs_tmd" / "halte.geojson").to_parquet(SILVER / "halte_tmd.parquet")
    print("[OK] ingest")


if __name__ == "__main__":
    main()
