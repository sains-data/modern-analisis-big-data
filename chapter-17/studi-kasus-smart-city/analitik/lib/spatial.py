"""Utilitas spasial — map-match, IDW PM2.5."""
from __future__ import annotations

import math

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def ruas_centroids(ruas: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    out = ruas.copy()
    out["centroid"] = out.geometry.centroid
    out["latitude"] = out["centroid"].y
    out["longitude"] = out["centroid"].x
    return out


def map_match_probes(
    probes: pd.DataFrame,
    ruas: gpd.GeoDataFrame,
    max_dist_m: float = 50,
) -> pd.DataFrame:
    """Nearest ruas centroid dalam max_dist_m (EPSG:4326)."""
    rc = ruas_centroids(ruas)
    rows = []
    for _, p in probes.iterrows():
        best_id, best_d = None, 1e9
        for _, r in rc.iterrows():
            d = haversine_m(p["latitude"], p["longitude"], r["latitude"], r["longitude"])
            if d < best_d:
                best_d, best_id = d, r["ruas_id"]
        if best_id and best_d <= max_dist_m:
            rows.append({**p.to_dict(), "ruas_id": best_id, "jarak_match_m": round(best_d, 1)})
    return pd.DataFrame(rows)


def wind_alpha(sensor_bearing_deg: float, wind_from_deg: float) -> float:
    """Faktor arah angin 0.5–1.5 untuk IDW."""
    diff = abs((sensor_bearing_deg - wind_from_deg + 180) % 360 - 180)
    return 0.5 + (1.0 - diff / 180.0)


def idw_pm25(
    sensors: pd.DataFrame,
    grid: pd.DataFrame,
    wind_from_deg: float = 90.0,
    power: float = 2.0,
) -> pd.DataFrame:
    """IDW PM2.5 ke grid dengan bobot angin."""
    out = []
    for _, g in grid.iterrows():
        num, den = 0.0, 0.0
        for _, s in sensors.iterrows():
            d = max(haversine_m(g["latitude"], g["longitude"], s["latitude"], s["longitude"]), 1.0)
            bearing = math.degrees(
                math.atan2(s["longitude"] - g["longitude"], s["latitude"] - g["latitude"])
            ) % 360
            alpha = wind_alpha(bearing, wind_from_deg)
            w = alpha / (d**power)
            num += w * s["pm25_ugm3"]
            den += w
        pm = num / den if den else float(sensors["pm25_ugm3"].mean())
        out.append({**g.to_dict(), "pm25_ugm3": round(pm, 2)})
    return pd.DataFrame(out)


def coverage_halte(
    kelurahan: gpd.GeoDataFrame,
    halte: gpd.GeoDataFrame,
    radius_m: float,
) -> pd.DataFrame:
    """Persentase permintaan (populasi) dalam radius halte."""
    halte_pts = halte.to_crs("EPSG:4326")
    rows = []
    for _, k in kelurahan.iterrows():
        lat, lon = k.geometry.y, k.geometry.x
        covered = False
        for _, h in halte_pts.iterrows():
            if haversine_m(lat, lon, h.geometry.y, h.geometry.x) <= radius_m:
                covered = True
                break
        rows.append(
            {
                "kelurahan_id": k["kelurahan_id"],
                "nama_kelurahan": k["nama_kelurahan"],
                "kecamatan": k["kecamatan"],
                "populasi": k["populasi"],
                "demand_trip_hari": k["demand_trip_hari"],
                "tercover_halte": covered,
            }
        )
    df = pd.DataFrame(rows)
    total_pop = df["populasi"].sum()
    covered_pop = df.loc[df["tercover_halte"], "populasi"].sum()
    df["coverage_pct"] = round(100 * covered_pop / total_pop, 2) if total_pop else 0
    # Per kelurahan: 100% jika ada halte dalam radius, else 0
    df["coverage_pct"] = df["tercover_halte"].map({True: 100.0, False: 0.0})
    return df
