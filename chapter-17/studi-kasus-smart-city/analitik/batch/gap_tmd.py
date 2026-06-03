#!/usr/bin/env python3
"""Gap analysis TMD — coverage halte radius 400 m."""
import geopandas as gpd
import pandas as pd

from analitik.lib.config import GOLD, SILVER, TMD_COVERAGE_MIN, TMD_RADIUS_M
from analitik.lib.spatial import coverage_halte

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    kel = gpd.read_parquet(SILVER / "kelurahan.parquet")
    halte = gpd.read_parquet(SILVER / "halte_tmd.parquet")
    gap = coverage_halte(kel, halte, radius_m=TMD_RADIUS_M)
    gap["underserved"] = gap["coverage_pct"] / 100 < TMD_COVERAGE_MIN
    gap = gap.sort_values(["underserved", "demand_trip_hari"], ascending=[False, False])
    gap.to_parquet(GOLD / "gap_tmd_kelurahan.parquet", index=False)
    n_under = int(gap["underserved"].sum())
    print(f"[OK] gap_tmd — {n_under} kelurahan underserved (<{TMD_COVERAGE_MIN*100:.0f}%)")


if __name__ == "__main__":
    main()
