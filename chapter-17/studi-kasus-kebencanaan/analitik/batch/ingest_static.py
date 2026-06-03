#!/usr/bin/env python3
"""
ingest_static.py — Promosi sumber → Bronze → Silver (lapisan statis).
Setara job Airflow harian: batas admin, genangan SAR, shelter, stasiun.
"""
from pathlib import Path

import geopandas as gpd
import pandas as pd

from analitik.lib.config import BRONZE, SILVER, SUMBER

SUMBER.mkdir(parents=True, exist_ok=True)
BRONZE.mkdir(parents=True, exist_ok=True)
SILVER.mkdir(parents=True, exist_ok=True)


def copy_geo(name: str, bronze_name: str, silver_name: str) -> None:
    src = SUMBER / name
    if not src.exists():
        raise FileNotFoundError(src)
    gdf = gpd.read_file(src)
    if not gdf.geometry.is_valid.all():
        gdf = gdf.make_valid()
    gdf = gdf.set_crs("EPSG:4326", allow_override=True)
    bronze_path = BRONZE / f"{bronze_name}.parquet"
    silver_path = SILVER / f"{silver_name}.parquet"
    gdf.to_parquet(bronze_path)
    gdf.to_parquet(silver_path)
    print(f"[OK] {src.name} → bronze/silver ({len(gdf)} fitur)")


def ingest_sensor_csv() -> None:
    csv_path = SUMBER / "sensor" / "tma_musi" / "tma_readings.csv"
    df = pd.read_csv(csv_path)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.drop_duplicates(subset=["stasiun_id", "ts"])
    BRONZE.mkdir(parents=True, exist_ok=True)
    df.to_parquet(BRONZE / "sensor_tma.parquet", index=False)
    df.to_parquet(SILVER / "sensor_tma.parquet", index=False)
    print(f"[OK] sensor_tma ({len(df)} baris)")


def ingest_bmkg() -> None:
    path = SUMBER / "hidrologi" / "bmkg_hujan" / "hujan_kumulatif_3jam.csv"
    df = pd.read_csv(path)
    df.to_parquet(BRONZE / "bmkg_hujan.parquet", index=False)
    df.to_parquet(SILVER / "bmkg_hujan.parquet", index=False)
    print(f"[OK] bmkg_hujan ({len(df)} baris)")


def main() -> None:
    copy_geo("kelurahan_sumsel.geojson", "batas_kelurahan", "kelurahan_sumsel")
    copy_geo("genangan_aktif.geojson", "genangan_sar", "genangan_aktif")
    copy_geo("shelter_kapasitas.geojson", "shelter", "shelter_kapasitas")
    copy_geo("stasiun_tma.geojson", "stasiun_tma", "stasiun_tma")
    ingest_sensor_csv()
    ingest_bmkg()


if __name__ == "__main__":
    main()
