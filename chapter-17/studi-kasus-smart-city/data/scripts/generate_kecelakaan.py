#!/usr/bin/env python3
"""Titik kecelakaan sintetis."""
import random
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point

random.seed(56)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "kecelakaan"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    rows = []
    for i in range(15):
        rows.append(
            {
                "kecelakaan_id": f"KC{i+1:03d}",
                "ruas_id": f"R{random.randint(1, 25):03d}",
                "severity": random.choice(["ringan", "sedang", "berat"]),
                "geometry": Point(98.65 + random.uniform(0, 0.08), 3.55 + random.uniform(0, 0.12)),
            }
        )
    gpd.GeoDataFrame(rows, crs="EPSG:4326").to_file(OUT / "kecelakaan.geojson", driver="GeoJSON")
    print(f"[OK] kecelakaan.geojson ({len(rows)} titik)")


if __name__ == "__main__":
    main()
