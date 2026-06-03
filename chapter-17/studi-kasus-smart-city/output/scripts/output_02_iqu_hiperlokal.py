#!/usr/bin/env python3
"""Output 2 — IQU hiperlokal grid 500 m."""
import geopandas as gpd
from shapely.geometry import Point

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-2-iqu-hiperlokal"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    pm = __import__("pandas").read_parquet(GOLD / "kualitas_udara.parquet")
    gdf = gpd.GeoDataFrame(
        pm,
        geometry=[Point(lon, lat) for lon, lat in zip(pm["longitude"], pm["latitude"])],
        crs="EPSG:4326",
    )
    gdf.to_file(OUT / "iqu_grid_latest.geojson", driver="GeoJSON")
    alert = gdf[gdf["kategori_ispu"].isin(["TIDAK SEHAT", "SANGAT TIDAK SEHAT", "BERBAHAYA"])]
    if not alert.empty:
        alert.to_file(OUT / "iqu_peringatan.geojson", driver="GeoJSON")
    print(f"[OK] IQU → {OUT} ({len(gdf)} sel, {len(alert)} peringatan)")


if __name__ == "__main__":
    main()
