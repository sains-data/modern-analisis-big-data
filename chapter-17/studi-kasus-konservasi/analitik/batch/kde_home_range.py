#!/usr/bin/env python3
"""KDE home range 50% / 95% + overlap konsesi."""
import geopandas as gpd
import numpy as np
import pandas as pd

from analitik.lib.config import GOLD, SILVER
from analitik.lib.spatial import kde_contour_polygon, overlap_pct

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    traj = pd.read_parquet(SILVER / "gps_trajectory.parquet")
    konsesi = gpd.read_parquet(SILVER / "konsesi.parquet")
    polys = []
    for ind, g in traj.groupby("individu_id"):
        lats = g["latitude"].values
        lons = g["longitude"].values
        p50 = kde_contour_polygon(lats, lons, quantile=0.5)
        p95 = kde_contour_polygon(lats, lons, quantile=0.05)
        if p50 is None:
            continue
        polys.append(
            {
                "individu_id": ind,
                "nama_individu": g["nama_individu"].iloc[0],
                "tipe": "core_50",
                "geometry": p50,
            }
        )
        if p95 is not None:
            polys.append(
                {"individu_id": ind, "nama_individu": g["nama_individu"].iloc[0], "tipe": "extent_95", "geometry": p95}
            )
    gdf = gpd.GeoDataFrame(polys, crs="EPSG:4326")
    core = gdf[gdf["tipe"] == "core_50"]
    ov = overlap_pct(core, konsesi) if not core.empty else pd.DataFrame()
    if not ov.empty:
        gdf = gdf.merge(ov, on="individu_id", how="left")
    gdf.to_parquet(GOLD / "home_range_kde.parquet")
    print(f"[OK] home_range_kde {len(gdf)} poligon")


if __name__ == "__main__":
    main()
