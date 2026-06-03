#!/usr/bin/env python3
"""15 stasiun udara + stream JSONL."""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

random.seed(54)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "udara" / "openaq"
OUT.mkdir(parents=True, exist_ok=True)

CLAT, CLON = 3.595, 98.672


def main() -> None:
    sensors = []
    for i in range(15):
        sensors.append(
            {
                "sensor_id": f"AQ{i+1:02d}",
                "nama": f"Stasiun Udara {i+1}",
                "latitude": round(CLAT + random.uniform(-0.07, 0.07), 5),
                "longitude": round(CLON + random.uniform(-0.08, 0.08), 5),
                "pm25_ugm3": round(random.uniform(18, 85), 1),
            }
        )
    df = pd.DataFrame(sensors)
    df.to_csv(OUT / "sensor_latest.csv", index=False)

    hist = []
    t0 = datetime(2026, 5, 27, 0, 0, tzinfo=timezone.utc)
    for h in range(24):
        ts = t0 + timedelta(hours=h)
        for s in sensors:
            hist.append(
                {
                    **s,
                    "pm25_ugm3": round(s["pm25_ugm3"] + random.uniform(-8, 12), 1),
                    "ts": ts.isoformat(),
                }
            )
    pd.DataFrame(hist).to_csv(OUT / "sensor_harian.csv", index=False)

    stream = []
    for s in sensors:
        stream.append({**s, "ts": "2026-05-27T10:00:00Z", "event": "sensor.udara"})
    with (OUT / "sensor_stream.jsonl").open("w") as f:
        for row in stream:
            f.write(json.dumps(row) + "\n")
    print(f"[OK] sensor udara {len(sensors)} stasiun")


if __name__ == "__main__":
    main()
