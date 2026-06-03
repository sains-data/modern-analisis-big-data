#!/usr/bin/env python3
"""Ruas jalan sintetis Kota Medan (~25 segmen)."""
import random
from pathlib import Path

import geopandas as gpd
from shapely.geometry import LineString

random.seed(51)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "osm" / "medan"
OUT.mkdir(parents=True, exist_ok=True)

NAMES = [
    "Jl. Gatot Subroto",
    "Jl. Sisingamangaraja",
    "Jl. Imam Bonjol",
    "Jl. Thamrin",
    "Jl. Iskandar Muda",
    "Jl. HM Joni",
    "Jl. Sei Deli",
    "Jl. Pancing",
    "Jl. Setiabudi",
    "Jl. Cemara Asri",
]


def main() -> None:
    rows = []
    clat, clon = 3.595, 98.672
    for i in range(25):
        lat0 = clat + random.uniform(-0.08, 0.08)
        lon0 = clon + random.uniform(-0.1, 0.1)
        lat1 = lat0 + random.uniform(-0.015, 0.015)
        lon1 = lon0 + random.uniform(-0.02, 0.02)
        rows.append(
            {
                "ruas_id": f"R{i+1:03d}",
                "nama_ruas": random.choice(NAMES),
                "kecamatan": random.choice(["Medan Kota", "Medan Petisah", "Medan Timur", "Medan Denai"]),
                "kapasitas_kend_jam": random.choice([800, 1200, 1500, 2000]),
                "geometry": LineString([(lon0, lat0), (lon1, lat1)]),
            }
        )
    gdf = gpd.GeoDataFrame(rows, crs="EPSG:4326")
    gdf.to_file(OUT / "ruas_jalan.geojson", driver="GeoJSON")
    print(f"[OK] ruas_jalan.geojson ({len(gdf)} segmen)")


if __name__ == "__main__":
    main()
