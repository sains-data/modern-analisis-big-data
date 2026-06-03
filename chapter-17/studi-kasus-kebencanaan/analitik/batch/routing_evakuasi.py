#!/usr/bin/env python3
"""
routing_evakuasi.py — KNN shelter terdekat per kelurahan terdampak (lab).
Produksi: Sedona KNN + constraint jalan tidak memotong genangan.
"""
import geopandas as gpd
import pandas as pd

from analitik.lib.config import GOLD, SILVER
from analitik.lib.spatial import knn_shelter

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    pop_path = GOLD / "populasi_terdampak.parquet"
    if not pop_path.exists() or pop_path.stat().st_size == 0:
        print("[SKIP] populasi_terdampak belum ada")
        return

    pop = pd.read_parquet(pop_path)
    if pop.empty:
        return

    kel = gpd.read_parquet(SILVER / "kelurahan_sumsel.parquet")
    shelters = gpd.read_parquet(SILVER / "shelter_kapasitas.parquet")

    agg = pop.groupby("kode_kel", as_index=False).agg(
        estimasi_terdampak=("estimasi_terdampak", "sum"),
        nama_kel=("nama_kel", "first"),
    )
    pts = kel.merge(agg, on="kode_kel")
    pts = pts[pts["estimasi_terdampak"] > 0]

    routes = knn_shelter(pts, shelters)
    routes.to_parquet(GOLD / "rute_evakuasi.parquet", index=False)
    print(f"[OK] gold/rute_evakuasi.parquet ({len(routes)} rute)")


if __name__ == "__main__":
    main()
