#!/usr/bin/env python3
"""Output 1 — GeoJSON ATCS + rekomendasi rute alternatif."""
import json

import geopandas as gpd
import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, SILVER

OUT = OUTPUT_DIR / "output-1-atcs"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    ruas = gpd.read_parquet(SILVER / "ruas_jalan.parquet")
    lintas = pd.read_parquet(GOLD / "lalu_lintas.parquet")
    merged = ruas.merge(lintas, on="ruas_id", how="left")
    merged.to_file(OUT / "kondisi_jalan_latest.geojson", driver="GeoJSON")

    macet = merged[merged["level_kemacetan"] == "MACET"]
    alt = []
    for _, r in macet.iterrows():
        alt_ruas = merged[
            (merged["level_kemacetan"] == "LANCAR")
            & (merged["kecamatan"] == r["kecamatan"])
        ].head(2)
        alt.append(
            {
                "ruas_macet": r["ruas_id"],
                "nama_ruas": r["nama_ruas"],
                "alternatif": alt_ruas[["ruas_id", "nama_ruas", "avg_kecepatan"]].to_dict("records"),
                "rekomendasi_dtk": 15,
            }
        )
    (OUT / "rute_alternatif_latest.json").write_text(
        json.dumps(alt, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[OK] ATCS → {OUT} ({len(macet)} koridor MACET)")


if __name__ == "__main__":
    main()
