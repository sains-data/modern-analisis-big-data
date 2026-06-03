#!/usr/bin/env python3
"""Kelurahan, genangan SAR, shelter — data sintetis DAS Musi (Palembang & hulu)."""
import json
import random
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point, Polygon, box

random.seed(17)

CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber"
OUT.mkdir(parents=True, exist_ok=True)

# Grid kelurahan di sekitar Palembang (-2.99, 104.75)
ORIGIN_LAT, ORIGIN_LON = -2.99, 104.75
KAB = ["Kota Palembang", "Kab. Ogan Ilir", "Kab. Banyuasin"]


def _cell(cx: float, cy: float, w: float = 0.025) -> Polygon:
    return box(cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2)


def main() -> None:
    kel_rows = []
    for i in range(50):
        lat = ORIGIN_LAT + (i % 10) * 0.018 + random.uniform(-0.004, 0.004)
        lon = ORIGIN_LON + (i // 10) * 0.022 + random.uniform(-0.004, 0.004)
        kel_rows.append(
            {
                "kode_kel": f"1671{1000 + i:04d}",
                "nama_kel": f"Kelurahan Contoh {i + 1}",
                "kabupaten": KAB[i % len(KAB)],
                "jumlah_penduduk": random.randint(800, 12000),
                "geometry": _cell(lon, lat),
            }
        )

    kel = gpd.GeoDataFrame(kel_rows, crs="EPSG:4326")
    kel_path = OUT / "kelurahan_sumsel.geojson"
    kel.to_file(kel_path, driver="GeoJSON")

    # Genangan: dua poligon overlap beberapa kelurahan
    gen1 = Polygon(
        [
            (104.72, -3.01),
            (104.78, -3.00),
            (104.79, -2.97),
            (104.74, -2.96),
            (104.71, -2.99),
        ]
    )
    gen2 = Polygon(
        [
            (104.80, -2.95),
            (104.86, -2.94),
            (104.87, -2.90),
            (104.82, -2.89),
            (104.79, -2.92),
        ]
    )
    gen = gpd.GeoDataFrame(
        [
            {"genangan_id": "G1", "snapshot_ts": "2026-05-27T10:00:00Z", "geometry": gen1},
            {"genangan_id": "G2", "snapshot_ts": "2026-05-27T10:00:00Z", "geometry": gen2},
        ],
        crs="EPSG:4326",
    )
    gen.to_file(OUT / "genangan_aktif.geojson", driver="GeoJSON")

    shelters = gpd.GeoDataFrame(
        [
            {"shelter_id": "S1", "nama_shelter": "Posko Haji", "kapasitas": 500,
             "geometry": Point(104.76, -2.98)},
            {"shelter_id": "S2", "nama_shelter": "GOR Jakabaring", "kapasitas": 2000,
             "geometry": Point(104.74, -3.02)},
            {"shelter_id": "S3", "nama_shelter": "Masjid Agung", "kapasitas": 800,
             "geometry": Point(104.83, -2.93)},
            {"shelter_id": "S4", "nama_shelter": "Balai Desa Hulu", "kapasitas": 350,
             "geometry": Point(104.88, -2.91)},
            {"shelter_id": "S5", "nama_shelter": "SDN 12 Evakuasi", "kapasitas": 600,
             "geometry": Point(104.70, -2.96)},
        ],
        crs="EPSG:4326",
    )
    shelters.to_file(OUT / "shelter_kapasitas.geojson", driver="GeoJSON")

    # Titik sensor TMA
    stations = [
        ("KAYU_AGUNG", -3.42, 104.82),
        ("PALEMBANG_KOTA", -2.99, 104.75),
        ("SUNGAI_PINANG", -3.05, 104.78),
        ("BANYUASIN_HULU", -2.88, 104.90),
        ("OGAN_ILIR", -3.12, 104.70),
        ("MUARA_KELINGI", -3.20, 104.85),
        ("PANGKALAN_BALAI", -2.75, 104.95),
        ("TALANG_KELAPA", -3.08, 104.72),
        ("SEKAYU", -2.82, 104.88),
        ("LAHAT_HULU", -3.25, 104.68),
    ]
    sensor_gdf = gpd.GeoDataFrame(
        [
            {"stasiun_id": sid, "nama_stasiun": sid.replace("_", " ").title(),
             "geometry": Point(lon, lat)}
            for sid, lat, lon in stations
        ],
        crs="EPSG:4326",
    )
    sensor_gdf.to_file(OUT / "stasiun_tma.geojson", driver="GeoJSON")

    meta = {"kelurahan": len(kel), "genangan": 2, "shelter": 5, "stasiun": len(stations)}
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2))
    print(f"[OK] {kel_path} ({len(kel)} kelurahan)")
    print(f"[OK] genangan, shelter, stasiun di {OUT}")


if __name__ == "__main__":
    main()
