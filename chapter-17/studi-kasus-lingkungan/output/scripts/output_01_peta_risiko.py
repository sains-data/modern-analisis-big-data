#!/usr/bin/env python3
"""Output 1 — GeoJSON H3 + ringkasan WhatsApp."""
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from analitik.lib.config import GOLD, OUTPUT_DIR
from analitik.lib.h3util import h3_to_polygon

OUT = OUTPUT_DIR / "output-1-peta-risiko"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    idx = pd.read_parquet(GOLD / "indeks_risiko_karhutla.parquet")
    polys = []
    for _, r in idx.iterrows():
        coords = h3_to_polygon(r["h3_id"])
        if coords[0] != coords[-1]:
            coords = coords + [coords[0]]
        polys.append(
            {
                "h3_id": r["h3_id"],
                "indeks": r["indeks"],
                "kelas_risiko": r["kelas_risiko"],
                "warna_hex": r["warna_hex"],
                "geometry": Polygon(coords),
            }
        )
    gdf = gpd.GeoDataFrame(polys, crs="EPSG:4326")
    tanggal = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    gdf.to_file(OUT / "peta_risiko_latest.geojson", driver="GeoJSON")

    tinggi = idx[idx["indeks"] >= 0.6]
    msg = (
        f"[BPBD Riau — Peta Risiko Karhutla {tanggal}]\n"
        f"Sel Tinggi+: {len(tinggi[tinggi['indeks'] >= 0.6])}\n"
        f"Sel Sangat Tinggi: {len(tinggi[tinggi['indeks'] >= 0.8])}\n"
        f"Total sel H3: {len(idx)}\n"
    )
    (OUT / "ringkasan_whatsapp.txt").write_text(msg, encoding="utf-8")
    print(f"[OK] peta risiko → {OUT}")


if __name__ == "__main__":
    main()
