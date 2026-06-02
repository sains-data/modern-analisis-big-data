#!/usr/bin/env python3
"""Poligon kecamatan sintetis Sumatera untuk spatial join (Tahap 3)."""
from pathlib import Path

import geopandas as gpd
from shapely.geometry import box

LAB_ROOT = Path(__file__).resolve().parent.parent
OUT = LAB_ROOT / "data" / "batas_kecamatan_sumatera.geoparquet"

# (nama, kabupaten, provinsi, lat, lon, half_size_deg)
KECAMATAN = [
    ("Kec. Siak", "Siak", "Riau", 0.5, 102.0, 0.8),
    ("Kec. Pelalawan", "Pelalawan", "Riau", 1.0, 101.5, 0.7),
    ("Kec. Bungo", "Bungo", "Jambi", -0.5, 104.0, 0.75),
    ("Kec. Musi Banyuasin", "Musi Banyuasin", "Sumsel", -2.5, 104.5, 0.9),
    ("Kec. Ketapang", "Ketapang", "Kalimantan Barat", 0.0, 109.0, 0.85),
    ("Kec. Dumai", "Dumai", "Riau", 1.7, 101.4, 0.5),
    ("Kec. Ogan Ilir", "Ogan Ilir", "Sumsel", -3.2, 104.8, 0.6),
    ("Kec. Sarolangun", "Sarolangun", "Jambi", -2.3, 102.7, 0.55),
    ("Kec. Lahat", "Lahat", "Sumsel", -3.8, 103.5, 0.5),
    ("Kec. Sanggau", "Sanggau", "Kalimantan Barat", 0.1, 110.5, 0.6),
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for i, (nama, kab, prov, clat, clon, half) in enumerate(KECAMATAN):
        records.append(
            {
                "id_kecamatan": f"K{i:03d}",
                "nama_kecamatan": nama,
                "kabupaten": kab,
                "provinsi": prov,
                "geometry": box(clon - half, clat - half, clon + half, clat + half),
            }
        )

    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
    gdf = gdf.rename_geometry("geom")
    gdf.to_parquet(OUT, index=False)
    print(f"[OK] {OUT} ({len(gdf)} kecamatan)")


if __name__ == "__main__":
    main()
