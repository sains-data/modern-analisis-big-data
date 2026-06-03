#!/usr/bin/env python3
"""DBSCAN klaster desa + Moran's I sederhana (prevalensi)."""
import geopandas as gpd
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

from analitik.lib.config import GOLD, SILVER


def morans_i(values: np.ndarray, weights: np.ndarray) -> float:
    n = len(values)
    if n < 3:
        return float("nan")
    x = values - values.mean()
    den = (weights.sum() * (x ** 2).sum()) / n
    if den == 0:
        return float("nan")
    num = (weights * np.outer(x, x)).sum()
    return (n / weights.sum()) * (num / den)


def main() -> None:
    prev = pd.read_parquet(GOLD / "prevalensi_stunting.parquet")
    desa = gpd.read_parquet(SILVER / "desa_sumatera_utara.parquet")
    gdf = desa.merge(prev, on="desa_id")
    gdf = gdf.to_crs("EPSG:3857")
    coords = np.column_stack([gdf.geometry.centroid.x, gdf.geometry.centroid.y])
    db = DBSCAN(eps=8000, min_samples=3).fit(coords)
    gdf["klaster_dbscan"] = db.labels_
    n_klaster = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)

    # Moran's I: bobot jarak inverse (subset 120 desa max untuk kecepatan)
    sample = gdf.head(min(120, len(gdf))).copy()
    vals = sample["prev_pct"].values
    cents = np.column_stack([sample.geometry.centroid.x, sample.geometry.centroid.y])
    dist = np.sqrt(((cents[:, None, :] - cents[None, :, :]) ** 2).sum(axis=2))
    np.fill_diagonal(dist, np.inf)
    w = 1 / dist
    w[np.isinf(w)] = 0
    mi = morans_i(vals, w)

    out = gdf[["desa_id", "prev_pct", "klaster_dbscan"]].drop_duplicates()
    out.to_parquet(GOLD / "klaster_spasial.parquet", index=False)
    print(f"[OK] DBSCAN: {n_klaster} klaster | Moran's I (sampel): {mi:.3f}")


if __name__ == "__main__":
    main()
