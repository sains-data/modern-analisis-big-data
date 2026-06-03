#!/usr/bin/env python3
"""Komponen G,F,H,N,D per sel H3 res-7 di Riau."""
import random
from pathlib import Path

import h3
import pandas as pd

random.seed(23)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "risiko"
OUT.mkdir(parents=True, exist_ok=True)


def to_cell(lat: float, lon: float, res: int) -> str:
    if hasattr(h3, "latlng_to_cell"):
        return h3.latlng_to_cell(lat, lon, res)
    return h3.geo_to_h3(lat, lon, res)


cells = set()
for lat in [i * 0.05 for i in range(20, 45)]:
    for lon in [99.5 + i * 0.05 for i in range(0, 90)]:
        if 0.1 <= lat <= 2.0:
            cells.add(to_cell(lat, lon, 7))

rows = []
for cid in cells:
    rows.append(
        {
            "h3_id": cid,
            "G": round(random.uniform(0.3, 1.0), 3),
            "F": round(random.uniform(0.2, 0.95), 3),
            "H": round(random.uniform(0.0, 0.9), 3),
            "N": round(random.uniform(0.15, 0.85), 3),
            "D": round(random.uniform(0.1, 0.9), 3),
            "tanggal": "2026-05-27",
        }
    )

pd.DataFrame(rows).to_csv(OUT / "komponen_h3_20260527.csv", index=False)
print(f"[OK] {len(rows)} sel H3")
