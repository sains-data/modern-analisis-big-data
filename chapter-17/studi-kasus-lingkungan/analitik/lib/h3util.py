"""Wrapper H3 v3/v4."""
from __future__ import annotations

import h3


def latlon_to_h3(lat: float, lon: float, res: int = 7) -> str:
    if hasattr(h3, "latlng_to_cell"):
        return h3.latlng_to_cell(lat, lon, res)
    return h3.geo_to_h3(lat, lon, res)


def h3_to_polygon(h3_id: str) -> list[tuple[float, float]]:
    if hasattr(h3, "cell_to_boundary"):
        boundary = h3.cell_to_boundary(h3_id)
        return [(lon, lat) for lat, lon in boundary]
    boundary = h3.h3_to_geo_boundary(h3_id, geo_json=True)
    return [(c[0], c[1]) for c in boundary["coordinates"][0]]
