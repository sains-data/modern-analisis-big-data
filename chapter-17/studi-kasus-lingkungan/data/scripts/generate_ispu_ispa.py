#!/usr/bin/env python3
"""Seri harian ISPU & ISPA per kecamatan (10 kecamatan Riau)."""
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(24)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "kesehatan"
OUT.mkdir(parents=True, exist_ok=True)

KEC = [f"Kecamatan_{i:02d}" for i in range(1, 11)]


def main() -> None:
    rows = []
    start = date(2026, 3, 1)
    for kec in KEC:
        base_ispa = random.randint(5, 30)
        lag_strength = random.uniform(0.3, 0.8)
        for d in range(60):
            dt = start + timedelta(days=d)
            ispu = max(20, min(350, 80 + random.gauss(0, 40) + (20 if d % 7 < 3 else 0)))
            ispa = int(base_ispa + lag_strength * (ispu - 100) / 10 + random.gauss(0, 3))
            ispa = max(0, ispa)
            rows.append(
                {
                    "kecamatan": kec,
                    "tanggal": dt.isoformat(),
                    "ispu": round(ispu, 1),
                    "kunjungan_ispa": ispa,
                }
            )
    pd.DataFrame(rows).to_csv(OUT / "ispu_ispa_harian.csv", index=False)
    print(f"[OK] ispu_ispa_harian.csv ({len(rows)} baris)")


if __name__ == "__main__":
    main()
