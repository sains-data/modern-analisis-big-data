#!/usr/bin/env python3
import geopandas as gpd
import pandas as pd
from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-4-basis-pergerakan"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    hr = gpd.read_parquet(GOLD / "home_range_kde.parquet")
    hr.to_file(OUT / "home_range_latest.geojson", driver="GeoJSON")
    # Trajektori: koordinat dibulatkan untuk privasi demo
    traj = pd.read_parquet(GOLD / "pergerakan_satwa.parquet")
    traj_pub = traj.copy()
    traj_pub["latitude"] = (traj_pub["latitude"].round(2))
    traj_pub["longitude"] = (traj_pub["longitude"].round(2))
    traj_pub.to_parquet(OUT / "pergerakan_anonim.parquet", index=False)
    print(f"[OK] basis pergerakan → {OUT}")


if __name__ == "__main__":
    main()
