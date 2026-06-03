#!/usr/bin/env python3
"""
output_02_export_peta.py — GeoJSON untuk Kepler.gl + kepler_config.json
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, SILVER

OUT = OUTPUT_DIR / "output-2-peta-terdampak"
OUT.mkdir(parents=True, exist_ok=True)


def build_kepler_config() -> dict:
    return {
        "version": "v1",
        "config": {
            "visState": {
                "layers": [
                    {
                        "id": "kelurahan_terdampak",
                        "type": "geojson",
                        "config": {
                            "dataId": "terdampak",
                            "label": "Populasi terdampak",
                            "color": [200, 30, 30],
                            "columns": {"geojson": "geometry"},
                            "visConfig": {
                                "opacity": 0.7,
                                "filled": True,
                                "strokeColor": [80, 20, 20],
                            },
                        },
                        "visualChannels": {
                            "colorField": {"name": "estimasi_terdampak", "type": "integer"},
                            "colorScale": "quantize",
                        },
                    },
                    {
                        "id": "sensor_tma",
                        "type": "point",
                        "config": {
                            "dataId": "sensor",
                            "label": "Sensor TMA",
                            "columns": {"lat": "lat", "lng": "lon"},
                            "visConfig": {"radius": 12},
                        },
                        "visualChannels": {
                            "colorField": {"name": "siaga_order", "type": "integer"},
                            "colorScale": "ordinal",
                        },
                    },
                    {
                        "id": "genangan",
                        "type": "geojson",
                        "config": {
                            "dataId": "genangan",
                            "label": "Genangan aktif",
                            "color": [30, 100, 200],
                            "visConfig": {"opacity": 0.4, "filled": True},
                        },
                    },
                ],
            },
            "mapState": {
                "latitude": -2.99,
                "longitude": 104.75,
                "zoom": 10,
            },
        },
    }


def main() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

    pop = pd.read_parquet(GOLD / "populasi_terdampak.parquet")
    kel = gpd.read_parquet(SILVER / "kelurahan_sumsel.parquet")
    if not pop.empty:
        gdf = kel.merge(pop.groupby("kode_kel", as_index=False)["estimasi_terdampak"].sum(), on="kode_kel")
        gdf.to_file(OUT / "terdampak_latest.geojson", driver="GeoJSON")
    else:
        kel.assign(estimasi_terdampak=0).head(0).to_file(OUT / "terdampak_latest.geojson", driver="GeoJSON")

    gen = gpd.read_parquet(SILVER / "genangan_aktif.parquet")
    gen.to_file(OUT / f"genangan_{ts}.geojson", driver="GeoJSON")
    gen.to_file(OUT / "genangan_latest.geojson", driver="GeoJSON")

    tma = pd.read_parquet(GOLD / "tma_latest.parquet")
    stasiun = gpd.read_parquet(SILVER / "stasiun_tma.parquet")
    sensor = stasiun.merge(tma, on="stasiun_id")
    sensor["lon"] = sensor.geometry.x
    sensor["lat"] = sensor.geometry.y
    sensor.drop(columns=["geometry"], errors="ignore").to_json(
        OUT / "sensor_tma_latest.geojson", orient="records", force_ascii=False, indent=2
    )

    (OUT / "kepler_config.json").write_text(
        json.dumps(build_kepler_config(), indent=2), encoding="utf-8"
    )
    print(f"[OK] Peta → {OUT}")


if __name__ == "__main__":
    main()
