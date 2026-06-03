#!/usr/bin/env python3
"""Poligon konsesi (5) + gambut Riau sintetis."""
import random
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Polygon

random.seed(21)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "konsesi"
OUT.mkdir(parents=True, exist_ok=True)

PERUSAHAAN = [
    ("PT Sawit Riau Satu", "SI-RIU-001", "HGU"),
    ("PT Kebun Nusantara Dua", "SI-RIU-002", "HGU"),
    ("PT Agro Gambut Tiga", "SI-RIU-003", "HGU"),
    ("PT Plasma Rakyat Empat", "SI-RIU-004", "Plasma"),
    ("PT HTI Gambut Lima", "SI-RIU-005", "HTI"),
]


def poly(cx: float, cy: float, w=0.25) -> Polygon:
    return Polygon(
        [(cx - w, cy - w), (cx + w, cy - w), (cx + w, cy + w), (cx - w, cy + w)]
    )


def main() -> None:
    konsesi_rows = []
    for i, (nama, izin, jenis) in enumerate(PERUSAHAAN):
        cx, cy = 101.5 + i * 0.35, 0.5 + (i % 3) * 0.2
        konsesi_rows.append(
            {
                "konsesi_id": f"K{i+1}",
                "nama_perusahaan": nama,
                "no_izin": izin,
                "jenis_konsesi": jenis,
                "luas_ha": round(random.uniform(5000, 25000), 1),
                "geometry": poly(cx, cy),
            }
        )
    gpd.GeoDataFrame(konsesi_rows, crs="EPSG:4326").to_file(
        OUT / "konsesi_riau.geojson", driver="GeoJSON"
    )

    gambut_dir = CASE_ROOT / "data" / "sumber" / "gambut"
    gambut_dir.mkdir(parents=True, exist_ok=True)
    gambut = Polygon(
        [(101.0, 0.2), (103.5, 0.2), (103.5, 1.2), (101.0, 1.2)]
    )
    gpd.GeoDataFrame(
        [{"gambut_id": "GRIAU1", "kedalaman_m": 2.5, "geometry": gambut}],
        crs="EPSG:4326",
    ).to_file(gambut_dir / "gambut_riau.geojson", driver="GeoJSON")

    print(f"[OK] {len(konsesi_rows)} konsesi + gambut Riau")


if __name__ == "__main__":
    main()
