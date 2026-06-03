#!/usr/bin/env python3
"""Probe vehicle GPS — map-match ke ruas; R001 sengaja MACET."""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import geopandas as gpd
import pandas as pd

random.seed(55)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "probe" / "gps"
OUT.mkdir(parents=True, exist_ok=True)

TIPE = ["mobil", "motor", "angkot", "bus"]


def main() -> None:
    ruas = gpd.read_file(CASE_ROOT / "data" / "sumber" / "osm" / "medan" / "ruas_jalan.geojson")
    ruas["lat"] = ruas.geometry.centroid.y
    ruas["lon"] = ruas.geometry.centroid.x

    rows = []
    t0 = datetime(2026, 5, 27, 6, 0, tzinfo=timezone.utc)
    for slot in range(20):
        ts = t0 + timedelta(minutes=15 * slot)
        for _, r in ruas.iterrows():
            n_probe = random.randint(4, 12)
            if r["ruas_id"] == "R001":
                speed_base = random.uniform(8, 18)
            elif r["ruas_id"] in ("R002", "R003"):
                speed_base = random.uniform(22, 38)
            else:
                speed_base = random.uniform(35, 55)
            for _ in range(n_probe):
                rows.append(
                    {
                        "probe_id": f"P{len(rows)+1:05d}",
                        "vehicle_type": random.choice(TIPE),
                        "ruas_id": r["ruas_id"],
                        "latitude": round(r["lat"] + random.uniform(-0.0003, 0.0003), 5),
                        "longitude": round(r["lon"] + random.uniform(-0.0003, 0.0003), 5),
                        "speed_kmh": round(speed_base + random.uniform(-3, 3), 1),
                        "ts": ts.isoformat(),
                    }
                )

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "probe_harian.csv", index=False)

    stream = []
    latest = df[df["ts"] == df["ts"].max()]
    for _, r in latest.head(50).iterrows():
        stream.append({**r.to_dict(), "event": "probe.kendaraan"})
    with (OUT / "probe_stream.jsonl").open("w") as f:
        for row in stream:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[OK] probe_harian.csv ({len(df)} titik), stream {len(stream)}")


if __name__ == "__main__":
    main()
