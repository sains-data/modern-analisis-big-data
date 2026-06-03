#!/usr/bin/env python3
"""Tabel LMS WHO 2006 (TB/U) — subset usia 0–60 bulan, L/P."""
import csv
from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "who"
OUT.mkdir(parents=True, exist_ok=True)

# Nilai LMS disederhanakan (bukan tabel WHO penuh) untuk lab
def row(usia: int, jk: str, l: float, m: float, s: float) -> dict:
    return {"usia_bulan": usia, "jenis_kelamin": jk, "L": l, "M": m, "S": s}


def main() -> None:
    rows = []
    for usia in range(0, 61):
        for jk, base_m in [("L", 49.0 + usia * 0.9), ("P", 48.0 + usia * 0.85)]:
            rows.append(row(usia, jk, 1.0, base_m, 0.04))

    path = OUT / "who_lms_tb_u.csv"
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] {path} ({len(rows)} baris)")


if __name__ == "__main__":
    main()
