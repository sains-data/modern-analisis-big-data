#!/usr/bin/env python3
"""Waktu tempuh desa → Puskesmas terdekat (simulasi OSRM via haversine)."""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from analitik.lib.config import GOLD, KECEPATAN_RATA_KMH, SILVER

GOLD.mkdir(parents=True, exist_ok=True)


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    import math
    r = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def main() -> None:
    desa = gpd.read_parquet(SILVER / "desa_sumatera_utara.parquet")
    pusk = gpd.read_parquet(SILVER / "puskesmas.parquet")
    desa["centroid"] = desa.geometry.centroid
    rows = []
    for _, d in desa.iterrows():
        c = d["centroid"]
        best_km, best_id, best_name = 1e9, None, None
        subset = pusk[pusk["kode_kab"] == d["kode_kab"]]
        if subset.empty:
            subset = pusk
        for _, p in subset.iterrows():
            km = haversine_km(c.y, c.x, p.geometry.y, p.geometry.x)
            if km < best_km:
                best_km, best_id, best_name = km, p["puskesmas_id"], p["nama_puskesmas"]
        menit = round(best_km / KECEPATAN_RATA_KMH * 60, 1)
        zona = (
            "30" if menit <= 30 else "60" if menit <= 60 else "90" if menit <= 90 else "90+"
        )
        blank = menit > 60
        rows.append(
            {
                "desa_id": d["desa_id"],
                "puskesmas_id": best_id,
                "nama_puskesmas": best_name,
                "jarak_km": round(best_km, 2),
                "waktu_tempuh_menit": menit,
                "zona_isokron": zona,
                "blank_zone": blank,
            }
        )
    out = pd.DataFrame(rows)
    out.to_parquet(GOLD / "skor_aksesibilitas.parquet", index=False)
    n_blank = int(out["blank_zone"].sum())
    print(f"[OK] gold/skor_aksesibilitas — blank zone (>60 mnt): {n_blank} desa")


if __name__ == "__main__":
    main()
