"""Utilitas spasial — jarak, KDE sederhana."""
from __future__ import annotations

import math

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon
from sklearn.neighbors import KernelDensity


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def kde_contour_polygon(
    lats: np.ndarray,
    lons: np.ndarray,
    bandwidth: float = 0.02,
    quantile: float = 0.5,
) -> Polygon | None:
    """KDE 2D → poligon kontur approx (grid sampling)."""
    if len(lats) < 5:
        return None
    xy = np.column_stack([lons, lats])
    kde = KernelDensity(bandwidth=bandwidth).fit(xy)
    xmin, xmax = lons.min() - 0.05, lons.max() + 0.05
    ymin, ymax = lats.min() - 0.05, lats.max() + 0.05
    xx, yy = np.meshgrid(
        np.linspace(xmin, xmax, 40),
        np.linspace(ymin, ymax, 40),
    )
    grid = np.column_stack([xx.ravel(), yy.ravel()])
    z = np.exp(kde.score_samples(grid)).reshape(xx.shape)
    thresh = np.quantile(z, quantile)
    mask = z >= thresh
    if not mask.any():
        return None
    # bounding box simplification
    ys, xs = np.where(mask)
    return Polygon(
        [
            (xx[ys.min(), xs.min()], yy[ys.min(), xs.min()]),
            (xx[ys.min(), xs.max()], yy[ys.min(), xs.max()]),
            (xx[ys.max(), xs.max()], yy[ys.max(), xs.max()]),
            (xx[ys.max(), xs.min()], yy[ys.max(), xs.min()]),
        ]
    )


def overlap_pct(home: gpd.GeoDataFrame, konsesi: gpd.GeoDataFrame) -> pd.DataFrame:
    konsesi = konsesi.to_crs(home.crs)
    rows = []
    for _, h in home.iterrows():
        inter = konsesi[konsesi.intersects(h["geometry"])]
        if inter.empty:
            rows.append({"individu_id": h["individu_id"], "pct_overlap": 0.0})
            continue
        area_h = h.geometry.area
        area_i = sum(
            h.geometry.intersection(k.geometry).area for _, k in inter.iterrows()
        )
        rows.append(
            {
                "individu_id": h["individu_id"],
                "pct_overlap": round(100 * area_i / area_h, 2) if area_h else 0,
            }
        )
    return pd.DataFrame(rows)
