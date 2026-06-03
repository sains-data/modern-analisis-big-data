#!/usr/bin/env python3
"""Batas KEL, konsesi, permukiman — sintetis Leuser."""
import random
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point, Polygon

random.seed(41)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "batas"
OUT.mkdir(parents=True, exist_ok=True)

KEL = Polygon([(96.8, 3.2), (98.2, 3.2), (98.2, 4.8), (96.8, 4.8)])


def main() -> None:
    gpd.GeoDataFrame([{"nama": "Kawasan Ekosistem Leuser", "geometry": KEL}], crs="EPSG:4326").to_file(
        OUT / "kel_leuser.geojson", driver="GeoJSON"
    )

    konsesi = []
    for i in range(4):
        cx, cy = 97.2 + i * 0.35, 3.8 + (i % 2) * 0.25
        konsesi.append(
            {
                "konsesi_id": f"KON{i+1}",
                "nama": f"PT Kebun Leuser {i+1}",
                "geometry": Polygon(
                    [(cx - 0.12, cy - 0.1), (cx + 0.12, cy - 0.1), (cx + 0.12, cy + 0.1), (cx - 0.12, cy + 0.1)]
                ),
            }
        )
    gpd.GeoDataFrame(konsesi, crs="EPSG:4326").to_file(OUT / "konsesi.geojson", driver="GeoJSON")

    desa = [
        {
            "desa_id": "DES001",
            "nama_desa": "Desa Simpang 1",
            "geometry": Point(97.05, 3.52),
        }
    ]
    for i in range(1, 12):
        desa.append(
            {
                "desa_id": f"DES{i+1:03d}",
                "nama_desa": f"Desa Simpang {i+1}",
                "geometry": Point(97.0 + random.uniform(0, 1), 3.5 + random.uniform(0, 1.2)),
            }
        )
    sosial = CASE_ROOT / "data" / "sumber" / "sosial"
    sosial.mkdir(parents=True, exist_ok=True)
    gpd.GeoDataFrame(desa, crs="EPSG:4326").to_file(
        sosial / "permukiman.geojson", driver="GeoJSON"
    )
    print("[OK] batas KEL, konsesi, permukiman")


if __name__ == "__main__":
    main()
