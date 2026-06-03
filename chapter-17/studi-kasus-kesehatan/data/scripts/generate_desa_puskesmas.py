#!/usr/bin/env python3
"""Desa sintetis 3 kabupaten Sumut + titik Puskesmas."""
import random
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point, box

random.seed(33)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "batas"
OUT.mkdir(parents=True, exist_ok=True)

KAB = [
    ("1201", "Kab. Tapanuli Utara", 2.0, 99.0),
    ("1202", "Kab. Tapanuli Tengah", 1.8, 98.7),
    ("1203", "Kab. Mandailing Natal", 0.9, 99.5),
]


def main() -> None:
    desa_rows = []
    idx = 0
    for kode_kab, nama_kab, clat, clon in KAB:
        for i in range(40):
            lat = clat + (i % 8) * 0.04 + random.uniform(-0.01, 0.01)
            lon = clon + (i // 8) * 0.05 + random.uniform(-0.01, 0.01)
            desa_rows.append(
                {
                    "desa_id": f"{kode_kab}{1000 + i:04d}",
                    "nama_desa": f"Desa {nama_kab.split()[-1]} {i + 1}",
                    "kode_kab": kode_kab,
                    "nama_kab": nama_kab,
                    "geometry": box(lon - 0.01, lat - 0.01, lon + 0.01, lat + 0.01),
                }
            )
            idx += 1

    desa = gpd.GeoDataFrame(desa_rows, crs="EPSG:4326")
    desa.to_file(OUT / "desa_sumut.geojson", driver="GeoJSON")

    puskesmas = []
    for kode_kab, nama_kab, clat, clon in KAB:
        for j in range(5):
            puskesmas.append(
                {
                    "puskesmas_id": f"PUS_{kode_kab}_{j}",
                    "nama_puskesmas": f"Puskesmas {nama_kab} {j + 1}",
                    "kode_kab": kode_kab,
                    "geometry": Point(clon + j * 0.08, clat + j * 0.03),
                }
            )
    gpd.GeoDataFrame(puskesmas, crs="EPSG:4326").to_file(
        OUT / "puskesmas.geojson", driver="GeoJSON"
    )
    print(f"[OK] {len(desa)} desa, {len(puskesmas)} puskesmas → {OUT}")


if __name__ == "__main__":
    main()
