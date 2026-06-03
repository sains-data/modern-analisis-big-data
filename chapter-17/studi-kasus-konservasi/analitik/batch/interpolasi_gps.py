#!/usr/bin/env python3
"""Interpolasi gap GPS > 4 jam (linear)."""
import pandas as pd

from analitik.lib.config import BRONZE, GOLD, SILVER

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    gps = pd.read_parquet(BRONZE / "gps_collar.parquet")
    gps["ts"] = pd.to_datetime(gps["ts"], utc=True)
    out = []
    for ind, g in gps.groupby("individu_id"):
        meta = g[["individu_id", "nama_individu"]].iloc[0]
        g = (
            g.sort_values("ts")
            .set_index("ts")[["latitude", "longitude"]]
            .resample("4h")
            .interpolate(method="linear")
            .reset_index()
        )
        g["individu_id"] = meta["individu_id"]
        g["nama_individu"] = meta["nama_individu"]
        out.append(g)
    traj = pd.concat(out, ignore_index=True)
    traj.to_parquet(SILVER / "gps_trajectory.parquet", index=False)
    traj.to_parquet(GOLD / "pergerakan_satwa.parquet", index=False)
    print(f"[OK] gps_trajectory {len(traj)} titik ({traj['individu_id'].nunique()} individu)")


if __name__ == "__main__":
    main()
