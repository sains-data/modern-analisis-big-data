#!/usr/bin/env python3
"""ST_Contains hotspot dalam konsesi — gold.rekam_hotspot + agregasi."""
import pandas as pd
import geopandas as gpd

from analitik.lib.config import GOLD, SILVER
from analitik.lib.spatial import join_hotspot_konsesi, points_from_hotspot

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    hs = pd.read_parquet(SILVER / "hotspot_firms_verified.parquet")
    konsesi = gpd.read_parquet(SILVER / "konsesi_riau.parquet")
    gambut = gpd.read_parquet(SILVER / "gambut_riau.parquet")
    gdf = points_from_hotspot(hs)
    joined = join_hotspot_konsesi(gdf, konsesi, gambut)
    joined.to_parquet(GOLD / "rekam_hotspot_terverifikasi.parquet", index=False)

    if joined.empty:
        print("[WARN] Tidak ada hotspot dalam konsesi")
        pd.DataFrame().to_parquet(GOLD / "hotspot_konsesi_agg.parquet", index=False)
        return

    agg = (
        joined.groupby(["nama_perusahaan", "no_izin", "jenis_konsesi"], as_index=False)
        .agg(
            n_hotspot=("hotspot_id", "count"),
            total_frp_mw=("frp", "sum"),
            n_hari_aktif=("acq_date", "nunique"),
        )
    )
    agg["luas_terbakar_ha"] = (agg["total_frp_mw"] * 0.3).round(1)
    agg["status_kepatuhan"] = agg["n_hotspot"].apply(
        lambda n: "MELANGGAR" if n >= 5 else "MEMENUHI"
    )
    agg.to_parquet(GOLD / "hotspot_konsesi_agg.parquet", index=False)
    print(f"[OK] {len(joined)} hotspot dalam konsesi; {len(agg)} perusahaan")


if __name__ == "__main__":
    main()
