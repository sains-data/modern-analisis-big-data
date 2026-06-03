#!/usr/bin/env python3
"""Deteksi deforestasi: delta NDVI > 0.2."""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from analitik.lib.config import BRONZE, GOLD, NDVI_DROP_THRESHOLD

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    ndvi = pd.read_parquet(BRONZE / "ndvi_grid.parquet")
    defor = ndvi[ndvi["delta_ndvi"] > NDVI_DROP_THRESHOLD].copy()
    defor["luas_ha"] = 100  # sel ~1 km² lab
    gdf = gpd.GeoDataFrame(
        defor,
        geometry=[Point(r.longitude, r.latitude) for _, r in defor.iterrows()],
        crs="EPSG:4326",
    )
    gdf.to_parquet(GOLD / "deforestasi_aktif.parquet")
    print(f"[OK] deforestasi_aktif {len(defor)} sel (ΔNDVI>{NDVI_DROP_THRESHOLD})")


if __name__ == "__main__":
    main()
