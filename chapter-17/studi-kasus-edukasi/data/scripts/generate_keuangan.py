#!/usr/bin/env python3
"""Data keuangan mahasiswa."""
import random
from pathlib import Path

import pandas as pd

random.seed(65)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "keuangan"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    base = pd.read_csv(CASE_ROOT / "data" / "sumber" / "sia" / "mahasiswa_base.csv")
    rows = []
    for _, m in base.iterrows():
        risk = m["label_historis_do"]
        rows.append(
            {
                "mahasiswa_id": m["mahasiswa_id"],
                "tunggakan_rp": random.randint(500_000, 8_000_000) if risk else random.randint(0, 500_000),
                "hari_telat_bayar": random.randint(15, 90) if risk else random.randint(0, 10),
                "beasiswa": int(not risk and random.random() < 0.3),
                "bayar_tepat_waktu_pct": random.randint(20, 60) if risk else random.randint(80, 100),
            }
        )
    pd.DataFrame(rows).to_csv(OUT / "keuangan_mhs.csv", index=False)
    print(f"[OK] keuangan_mhs.csv ({len(rows)} baris)")


if __name__ == "__main__":
    main()
