#!/usr/bin/env python3
"""Simulasi join stream korelasi PM2.5 ↔ volume."""
from __future__ import annotations

import argparse

import pandas as pd

from analitik.lib.config import GOLD

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="file")
    _ = parser.parse_args()

    lintas = pd.read_parquet(GOLD / "kondisi_jalan_stream.parquet")
    korel = pd.read_parquet(GOLD / "korelasi_pm25.parquet")
    joined = lintas.merge(korel[["ruas_id", "pearson_r", "pm25_estimasi"]], on="ruas_id", how="left")
    joined.to_parquet(GOLD / "korelasi_stream.parquet", index=False)
    print(f"[OK] korelasi_stream {len(joined)} ruas")


if __name__ == "__main__":
    main()
