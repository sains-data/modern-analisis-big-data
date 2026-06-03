#!/usr/bin/env python3
"""Curah hujan kumulatif 3 jam — stasiun hulu DAS Musi."""
import csv
import random
from pathlib import Path

random.seed(7)

CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "hidrologi" / "bmkg_hujan"
OUT.mkdir(parents=True, exist_ok=True)

STATIONS = ["KAYU_AGUNG", "SEKAYU", "PANGKALAN_BALAI", "LAHAT_HULU"]


def main() -> None:
    rows = []
    for sid in STATIONS:
        h3 = 85.0 if sid == "KAYU_AGUNG" else random.uniform(10, 45)
        rows.append(
            {
                "stasiun_id": sid,
                "hujan_3jam_mm": round(h3, 1),
                "ts": "2026-05-27T10:00:00Z",
            }
        )

    path = OUT / "hujan_kumulatif_3jam.csv"
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] {path}")


if __name__ == "__main__":
    main()
