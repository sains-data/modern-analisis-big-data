#!/usr/bin/env python3
"""Alert gajah < 2000 m dari permukiman."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

from analitik.lib.config import ALERT_JARAK_M, GOLD, OUTPUT_DIR, SILVER, SUMBER
from analitik.lib.spatial import haversine_m

GOLD.mkdir(parents=True, exist_ok=True)


def load_latest_gps() -> pd.DataFrame:
    path = SUMBER / "satwa" / "gps_collar" / "gps_stream.jsonl"
    rows = []
    with path.open() as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)


def main() -> None:
    gps = load_latest_gps()
    desa = gpd.read_parquet(SILVER / "permukiman.parquet")
    alerts = []
    for _, g in gps.iterrows():
        best_d, best_name = 1e9, None
        for _, d in desa.iterrows():
            dist = haversine_m(g["latitude"], g["longitude"], d.geometry.y, d.geometry.x)
            if dist < best_d:
                best_d, best_name = dist, d["nama_desa"]
        if best_d <= ALERT_JARAK_M:
            alerts.append(
                {
                    "individu_id": g["individu_id"],
                    "nama_individu": g["nama_individu"],
                    "desa_terdekat": best_name,
                    "jarak_m": round(best_d, 0),
                    "latitude": g["latitude"],
                    "longitude": g["longitude"],
                    "rekomendasi": "Jauhi ternak, gunakan api pengusir, hubungi BBKSDA",
                    "ts": g.get("ts"),
                }
            )
    alert_df = pd.DataFrame(alerts)
    alert_df.to_parquet(GOLD / "alert_konflik.parquet", index=False)

    out = OUTPUT_DIR / "output-1-alert-konflik"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "alert_konflik_latest.jsonl").open("w") as f:
        for _, r in alert_df.iterrows():
            f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")
    print(f"[OK] {len(alerts)} alert konflik")


if __name__ == "__main__":
    main()
