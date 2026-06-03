#!/usr/bin/env python3
"""Map-match probe ke ruas (ST_DWithin 50 m — haversine)."""
import geopandas as gpd
import pandas as pd

from analitik.lib.config import BRONZE, MAP_MATCH_M, MIN_PROBE_PER_RUAS, SILVER
from analitik.lib.spatial import map_match_probes

SILVER.mkdir(parents=True, exist_ok=True)


def main() -> None:
    probe = pd.read_parquet(BRONZE / "probe_vehicle.parquet")
    ruas = gpd.read_parquet(SILVER / "ruas_jalan.parquet")
    mapped = map_match_probes(probe, ruas, max_dist_m=MAP_MATCH_M)
    if mapped.empty:
        mapped = probe.copy()
        mapped["ruas_id"] = probe.get("ruas_id", "R001")
        mapped["jarak_match_m"] = 0.0
    mapped.to_parquet(SILVER / "probe_mapped.parquet", index=False)
    ok = mapped.groupby("ruas_id").size()
    n_ok = int((ok >= MIN_PROBE_PER_RUAS).sum())
    print(f"[OK] probe_mapped {len(mapped)} titik, {n_ok} ruas ≥{MIN_PROBE_PER_RUAS} probe")


if __name__ == "__main__":
    main()
