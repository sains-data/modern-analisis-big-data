#!/usr/bin/env python3
"""Trajektori GPS 7 gajah — sampling 4 jam + event streaming."""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

random.seed(42)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "satwa" / "gps_collar"
OUT.mkdir(parents=True, exist_ok=True)

GAJAH = [
    ("G001", "Betina Dewasa Intan", 97.45, 4.1),
    ("G002", "Jantan Dewasa Raja", 97.8, 3.9),
    ("G003", "Betina Muda Sari", 97.3, 4.3),
    ("G004", "Jantan Muda Bento", 97.6, 4.0),
    ("G005", "Betina Dewasa Melati", 97.1, 3.7),
    ("G006", "Jantan Dewasa Guntur", 97.9, 4.2),
    ("G007", "Betina Muda Citra", 97.4, 3.8),
]


def traj(ind_id: str, name: str, clon: float, clat: float, n: int) -> list[dict]:
    rows = []
    t0 = datetime(2026, 5, 1, tzinfo=timezone.utc)
    lon, lat = clon, clat
    for i in range(n):
        lon += random.uniform(-0.008, 0.012)
        lat += random.uniform(-0.006, 0.01)
        ts = t0 + timedelta(hours=4 * i)
        rows.append(
            {
                "individu_id": ind_id,
                "nama_individu": name,
                "latitude": round(lat, 5),
                "longitude": round(lon, 5),
                "ts": ts.isoformat(),
            }
        )
    return rows


def main() -> None:
    all_rows = []
    stream = []
    for ind_id, name, clon, clat in GAJAH:
        rows = traj(ind_id, name, clon, clat, 90)
        all_rows.extend(rows)
        # Satu titik dekat desa untuk alert (G001)
        if ind_id == "G001":
            alert_pt = {
                "individu_id": ind_id,
                "nama_individu": name,
                "latitude": 3.52,
                "longitude": 97.05,
                "ts": "2026-05-27T10:00:00Z",
            }
            stream.append(alert_pt)
        else:
            stream.append(rows[-1])

    pd.DataFrame(all_rows).to_csv(OUT / "gps_all.csv", index=False)
    with (OUT / "gps_stream.jsonl").open("w") as f:
        for s in stream:
            f.write(json.dumps({**s, "event": "gps.fix"}) + "\n")
    print(f"[OK] gps_all.csv ({len(all_rows)} titik), stream {len(stream)}")


if __name__ == "__main__":
    main()
