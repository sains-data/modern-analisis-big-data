"""Join spasial kelurahan × genangan (setara Sedona ST_Intersects)."""
from __future__ import annotations

import geopandas as gpd
import pandas as pd

from analitik.lib.config import CRS_METRIC, CRS_WGS84


def estimasi_populasi_terdampak(
    kelurahan: gpd.GeoDataFrame,
    genangan: gpd.GeoDataFrame,
    pop_col: str = "jumlah_penduduk",
) -> pd.DataFrame:
    """
    Proporsi luas intersection / luas kelurahan × populasi.
    Asumsi kepadatan merata (disebutkan di katalog data).
    """
    kel = kelurahan.to_crs(CRS_METRIC).copy()
    gen = genangan.to_crs(CRS_METRIC).copy()
    kel["_area_kel"] = kel.geometry.area
    rows = []

    for _, g_row in gen.iterrows():
        g_geom = g_row.geometry
        subset = kel[kel.intersects(g_geom)]
        for _, k_row in subset.iterrows():
            inter = k_row.geometry.intersection(g_geom)
            if inter.is_empty:
                continue
            frac = inter.area / k_row["_area_kel"]
            est = int(round(k_row[pop_col] * frac))
            if est <= 0:
                continue
            rows.append(
                {
                    "kode_kel": k_row["kode_kel"],
                    "nama_kel": k_row["nama_kel"],
                    "kabupaten": k_row.get("kabupaten", ""),
                    "genangan_id": g_row.get("genangan_id", "G1"),
                    "luas_intersect_m2": round(inter.area, 1),
                    "frac_area": round(frac, 4),
                    "estimasi_terdampak": est,
                    "jumlah_penduduk": int(k_row[pop_col]),
                }
            )

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def knn_shelter(
    points: gpd.GeoDataFrame,
    shelters: gpd.GeoDataFrame,
    id_col: str = "kode_kel",
) -> pd.DataFrame:
    """Shelter terdekat (jarak Euclidean centroid) — simplifikasi lab."""
    pts = points.to_crs(CRS_METRIC)
    sh = shelters.to_crs(CRS_METRIC)
    rows = []
    for _, p in pts.iterrows():
        dists = sh.geometry.distance(p.geometry)
        idx = dists.idxmin()
        s = sh.loc[idx]
        rows.append(
            {
                id_col: p[id_col],
                "nama_kel": p.get("nama_kel", ""),
                "estimasi_terdampak": int(p.get("estimasi_terdampak", 0)),
                "shelter_id": s["shelter_id"],
                "nama_shelter": s["nama_shelter"],
                "kapasitas": int(s["kapasitas"]),
                "jarak_m": round(float(dists.loc[idx]), 1),
            }
        )
    return pd.DataFrame(rows)
