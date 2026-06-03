#!/usr/bin/env python3
"""Hotspot VIIRS sintetis — format FIRMS, bbox Riau."""
import csv
import json
import random
import uuid
from datetime import date, timedelta
from pathlib import Path

random.seed(22)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "firms"
OUT.mkdir(parents=True, exist_ok=True)

# Bias ke area konsesi ~101.5–102.5, 0.4–0.9
CENTERS = [(101.6, 0.55), (101.9, 0.65), (102.2, 0.5), (101.4, 0.75)]


def main() -> None:
    rows = []
    start = date(2025, 6, 1)
    for i in range(1200):
        c = random.choice(CENTERS)
        lat = round(max(0.1, min(2.0, c[1] + random.gauss(0, 0.15))), 4)
        lon = round(max(99.5, min(104.0, c[0] + random.gauss(0, 0.12))), 4)
        conf = random.choice(["nominal", "nominal", "high", "low"])
        if conf == "low" and random.random() > 0.3:
            continue
        d = start + timedelta(days=random.randint(0, 300))
        rows.append(
            {
                "hotspot_id": f"HS{uuid.uuid4().hex[:8]}",
                "latitude": lat,
                "longitude": lon,
                "brightness": round(random.uniform(310, 420), 1),
                "frp": round(random.uniform(5, 180), 1),
                "acq_date": d.isoformat(),
                "confidence": conf,
                "satellite": "N",
                "instrument": "VIIRS",
            }
        )

    path = OUT / "viirs_riau_2025.csv"
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    with (OUT / "viirs_stream.jsonl").open("w") as f:
        for r in rows[:150]:
            r2 = {**r, "ts": f"{r['acq_date']}T12:00:00Z"}
            f.write(json.dumps(r2) + "\n")
    print(f"[OK] {path} ({len(rows)} hotspot)")


if __name__ == "__main__":
    main()
