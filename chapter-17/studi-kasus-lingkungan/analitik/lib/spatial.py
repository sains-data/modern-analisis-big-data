"""Join spasial hotspot × konsesi × gambut."""
from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


def points_from_hotspot(df: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(
        df,
        geometry=[Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])],
        crs="EPSG:4326",
    )
    return gdf


def join_hotspot_konsesi(
    hotspot: gpd.GeoDataFrame,
    konsesi: gpd.GeoDataFrame,
    gambut: gpd.GeoDataFrame | None = None,
) -> pd.DataFrame:
    """ST_Contains: titik dalam poligon konsesi."""
    konsesi = konsesi.to_crs("EPSG:4326")
    joined = gpd.sjoin(hotspot, konsesi, how="inner", predicate="within")
    if gambut is not None:
        gambut = gambut.to_crs("EPSG:4326")
        in_gambut = gpd.sjoin(hotspot, gambut, how="inner", predicate="within")
        joined = joined.merge(
            in_gambut[["hotspot_id"]].drop_duplicates().assign(dalam_gambut=True),
            on="hotspot_id",
            how="left",
        )
        joined["dalam_gambut"] = joined["dalam_gambut"].fillna(False)
    else:
        joined["dalam_gambut"] = True
    return pd.DataFrame(joined.drop(columns="geometry", errors="ignore"))
