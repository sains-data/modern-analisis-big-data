#!/usr/bin/env python3
"""Output 2 — agregat TPPS: tren provinsi, kab, isokron."""
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, SILVER, TARGET_PREV_NASIONAL

OUT = OUTPUT_DIR / "output-2-dashboard-tpps"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    prev = pd.read_parquet(GOLD / "prevalensi_stunting.parquet")
    akses = pd.read_parquet(GOLD / "skor_aksesibilitas.parquet")

    prov = {
        "bulan": "2026-05",
        "prev_pct_provinsi": round(prev["prev_pct"].mean(), 2),
        "target_pct": TARGET_PREV_NASIONAL,
        "n_desa": len(prev),
    }
    (OUT / "tren_provinsi.json").write_text(json.dumps(prov, indent=2))

    kab = (
        prev.groupby(["kode_kab", "nama_kab"], as_index=False)
        .agg(prev_pct_kab=("prev_pct", "mean"), n_desa=("desa_id", "count"))
        .sort_values("prev_pct_kab", ascending=False)
    )
    kab.to_csv(OUT / "top_kabupaten.csv", index=False)

    top10 = prev.nlargest(10, "prev_pct")[["nama_desa", "nama_kab", "prev_pct", "n_stunting"]]
    top10.to_csv(OUT / "top10_desa_terburuk.csv", index=False)

    isokron = akses.groupby("zona_isokron").size().reset_index(name="n_desa")
    isokron.to_csv(OUT / "isokron_ringkasan.csv", index=False)

    desa = gpd.read_parquet(SILVER / "desa_sumatera_utara.parquet")
    gkab = desa.merge(kab, on=["kode_kab", "nama_kab"])
    gkab.to_file(OUT / "stunting_kab_bulan_ini.geojson", driver="GeoJSON")

    print(f"[OK] dashboard TPPS → {OUT} (prev prov {prov['prev_pct_provinsi']}%)")


if __name__ == "__main__":
    main()
