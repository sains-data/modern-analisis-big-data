#!/usr/bin/env python3
"""GTFS sintetis Trans Metro Deli — 10 rute, 18 halte."""
import random
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point

random.seed(52)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "transport" / "gtfs_tmd"
OUT.mkdir(parents=True, exist_ok=True)

CLAT, CLON = 3.595, 98.672


def main() -> None:
    stops = []
    halte_coords = []
    for i in range(18):
        lat = CLAT + random.uniform(-0.06, 0.06)
        lon = CLON + random.uniform(-0.06, 0.06)
        halte_coords.append((lat, lon))
        stops.append(
            {
                "stop_id": f"H{i+1:03d}",
                "stop_name": f"Halte TMD {i+1}",
                "route_id": f"RT{(i % 10)+1:02d}",
                "geometry": Point(lon, lat),
            }
        )
    gpd.GeoDataFrame(stops, crs="EPSG:4326").to_file(OUT / "halte.geojson", driver="GeoJSON")
    pd.DataFrame({"lat": [c[0] for c in halte_coords], "lon": [c[1] for c in halte_coords]}).to_csv(
        OUT / "halte_coords.csv", index=False
    )

    routes = []
    for i in range(10):
        pts = [(CLON + random.uniform(-0.05, 0.05), CLAT + random.uniform(-0.04, 0.04)) for _ in range(5)]
        routes.append(
            {
                "route_id": f"RT{i+1:02d}",
                "route_name": f"Koridor TMD {i+1}",
                "headway_menit": random.choice([10, 15, 20]),
                "geometry": LineString(pts),
            }
        )
    gpd.GeoDataFrame(routes, crs="EPSG:4326").to_file(OUT / "routes.geojson", driver="GeoJSON")
    pd.DataFrame(stops).drop(columns="geometry", errors="ignore").to_csv(OUT / "stops.csv", index=False)
    print(f"[OK] GTFS TMD — {len(stops)} halte, {len(routes)} rute")


if __name__ == "__main__":
    main()
