#!/usr/bin/env python3
"""Indikator STBM & DTKS per desa."""
import geopandas as gpd
import pandas as pd
import random
from pathlib import Path

random.seed(55)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = CASE_ROOT / "data" / "sumber" / "stbm"
OUT_DIR.mkdir(parents=True, exist_ok=True)
desa = gpd.read_file(CASE_ROOT / "data" / "sumber" / "batas" / "desa_sumut.geojson")

rows = []
for _, d in desa.iterrows():
    rows.append(
        {
            "desa_id": str(d["desa_id"]),
            "skor_sanitasi": round(random.uniform(40, 95), 1),
            "pct_air_bersih": round(random.uniform(35, 98), 1),
            "pct_miskin": round(random.uniform(8, 45), 1),
            "jumlah_balita": random.randint(15, 120),
            "jumlah_bidan": random.choice([0, 1, 1, 2]),
            "kader_aktif": random.randint(1, 5),
        }
    )

pd.DataFrame(rows).to_csv(OUT_DIR / "stbm_dtks_desa.csv", index=False)
print(f"[OK] stbm_dtks_desa.csv ({len(rows)} desa)")
