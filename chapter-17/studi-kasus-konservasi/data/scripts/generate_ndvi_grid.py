#!/usr/bin/env python3
"""Grid 1 km² NDVI bulan t dan t-1."""
import random
from pathlib import Path

import pandas as pd

random.seed(43)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "satelit"
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for lat_i in range(32, 48):
    for lon_i in range(968, 982):
        lat = lat_i / 10
        lon = lon_i / 10
        ndvi_prev = round(random.uniform(0.55, 0.85), 3)
        drop = random.choice([0, 0, 0, 0.15, 0.22, 0.25, 0.3])
        ndvi_now = round(max(0.1, ndvi_prev - drop), 3)
        rows.append(
            {
                "grid_id": f"G{lat_i}_{lon_i}",
                "latitude": lat,
                "longitude": lon,
                "ndvi_bulan_lalu": ndvi_prev,
                "ndvi_bulan_ini": ndvi_now,
                "delta_ndvi": round(ndvi_prev - ndvi_now, 3),
            }
        )

def main() -> None:
    pd.DataFrame(rows).to_csv(OUT / "ndvi_grid.csv", index=False)
    print(f"[OK] ndvi_grid.csv ({len(rows)} sel)")


if __name__ == "__main__":
    main()
