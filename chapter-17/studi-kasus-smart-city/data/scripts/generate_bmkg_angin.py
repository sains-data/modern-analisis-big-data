#!/usr/bin/env python3
"""Data angin BMKG untuk bobot IDW."""
from pathlib import Path

import pandas as pd

CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "cuaca" / "bmkg"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    rows = []
    for h in range(24):
        rows.append(
            {
                "jam": h,
                "wind_from_deg": 90 + (h % 8) * 15,
                "wind_speed_ms": 2.5 + (h % 5) * 0.4,
                "ts": f"2026-05-27T{h:02d}:00:00Z",
            }
        )
    pd.DataFrame(rows).to_csv(OUT / "angin_harian.csv", index=False)
    print("[OK] angin_harian.csv")


if __name__ == "__main__":
    main()
