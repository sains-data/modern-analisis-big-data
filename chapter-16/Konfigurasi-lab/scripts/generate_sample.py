#!/usr/bin/env python3
"""500 baris hotspot sintetis (format FIRMS) — Bab 16 Langkah 6."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

CENTERS = [
    (0.5, 102.0, "Riau"),
    (1.0, 101.5, "Riau"),
    (-0.5, 104.0, "Jambi"),
    (-2.5, 104.5, "Sumsel"),
    (0.0, 109.0, "Kalimantan Barat"),
]
SATELLITES = ["Terra", "Aqua"]
CONFIDENCES = ["low", "nominal", "nominal", "nominal", "high", "high"]
DAYNIGHT = ["D", "N"]

LAB_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = LAB_ROOT / "data"
OUT = DATA_DIR / "hotspot_sample.csv"
ALIAS = DATA_DIR / "hotspot_sumatera_2024.csv"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    start_date = date(2024, 1, 1)

    for _ in range(500):
        center = random.choice(CENTERS)
        lat = round(max(-6.0, min(6.0, center[0] + random.gauss(0, 0.5))), 4)
        lon = round(max(95.0, min(109.0, center[1] + random.gauss(0, 0.5))), 4)
        acq_date = start_date + timedelta(days=random.randint(0, 364))
        rows.append(
            {
                "latitude": lat,
                "longitude": lon,
                "brightness": round(random.uniform(310, 420), 1),
                "frp": round(random.uniform(5, 180), 1),
                "acq_date": acq_date.isoformat(),
                "confidence": random.choice(CONFIDENCES),
                "satellite": random.choice(SATELLITES),
                "instrument": "MODIS",
                "daynight": random.choice(DAYNIGHT),
                "version": "6.1NRT",
            }
        )

    fieldnames = list(rows[0].keys())
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Alias nama file seperti di buku (Tahap 1)
    ALIAS.write_text(OUT.read_text())
    print(f"[OK] {OUT} ({len(rows)} baris)")
    print(f"[OK] {ALIAS} (symlink teks)")


if __name__ == "__main__":
    main()
