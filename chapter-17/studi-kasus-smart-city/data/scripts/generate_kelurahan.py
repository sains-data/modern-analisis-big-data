#!/usr/bin/env python3
"""Kelurahan Medan + permintaan perjalanan harian."""
import random
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

random.seed(53)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "sosial" / "populasi"
OUT.mkdir(parents=True, exist_ok=True)

KECAMATAN = ["Medan Kota", "Medan Petisah", "Medan Timur", "Medan Denai", "Medan Johor"]
CLAT, CLON = 3.595, 98.672


def main() -> None:
    halte_path = CASE_ROOT / "data" / "sumber" / "transport" / "gtfs_tmd" / "halte_coords.csv"
    halte_coords = []
    if halte_path.exists():
        hc = pd.read_csv(halte_path)
        halte_coords = list(zip(hc["lat"], hc["lon"]))

    rows = []
    for i in range(24):
        pop = random.randint(8000, 45000)
        if i < len(halte_coords):
            lat, lon = halte_coords[i]
            lat += random.uniform(-0.001, 0.001)
            lon += random.uniform(-0.001, 0.001)
        else:
            lat = CLAT + random.uniform(-0.09, 0.09)
            lon = CLON + random.uniform(-0.09, 0.09)
        rows.append(
            {
                "kelurahan_id": f"KEL{i+1:03d}",
                "nama_kelurahan": f"Kelurahan Medan {i+1}",
                "kecamatan": KECAMATAN[i % len(KECAMATAN)],
                "populasi": pop,
                "demand_trip_hari": int(pop * random.uniform(0.15, 0.35)),
                "geometry": Point(lon, lat),
            }
        )
    gdf = gpd.GeoDataFrame(rows, crs="EPSG:4326")
    gdf.to_file(OUT / "kelurahan_medan.geojson", driver="GeoJSON")
    print(f"[OK] kelurahan_medan.geojson ({len(gdf)} kelurahan)")


if __name__ == "__main__":
    main()
