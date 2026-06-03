#!/usr/bin/env python3
"""Simulasi streaming IDW PM2.5 grid /10 menit."""
from __future__ import annotations

import argparse
import json

import pandas as pd

from analitik.lib.config import BRONZE, GOLD, OUTPUT_DIR, SUMBER
from analitik.lib.spatial import idw_pm25
from analitik.lib.traffic import ispu_kategori


def load_sensors() -> pd.DataFrame:
    rows = [json.loads(line) for line in (SUMBER / "udara" / "openaq" / "sensor_stream.jsonl").open()]
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="file")
    _ = parser.parse_args()

    grid = pd.read_parquet(
        __import__("pathlib").Path(__file__).resolve().parents[2] / "data" / "gold" / "kualitas_udara.parquet"
    )[["grid_id", "latitude", "longitude"]]
    sensors = load_sensors()
    angin = pd.read_parquet(BRONZE / "bmkg_angin.parquet")
    wind = float(angin.loc[angin["jam"] == 10, "wind_from_deg"].iloc[0])

    pm = idw_pm25(sensors, grid, wind_from_deg=wind)
    pm[["kategori_ispu", "warna_ispu"]] = pm["pm25_ugm3"].apply(lambda v: pd.Series(ispu_kategori(v)))
    pm["ts_emit"] = "2026-05-27T10:10:00Z"
    pm.to_parquet(GOLD / "iqu_stream.parquet", index=False)
    print(f"[OK] streaming IQU grid {len(pm)} sel")


if __name__ == "__main__":
    main()
