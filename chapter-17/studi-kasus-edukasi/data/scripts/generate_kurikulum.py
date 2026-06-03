#!/usr/bin/env python3
"""Kurikulum CPL per mata kuliah."""
from pathlib import Path

import pandas as pd

CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "akademik"
OUT.mkdir(parents=True, exist_ok=True)

MK_CPL = [
    ("IF101", "Algoritma", "algoritma pemrograman struktur data logika"),
    ("IF102", "Struktur Data", "struktur data algoritma kompleksitas"),
    ("IF201", "Basis Data", "sql database normalisasi query"),
    ("IF202", "Jaringan", "jaringan tcp ip routing protokol"),
    ("IF301", "Machine Learning", "machine learning statistik python model"),
    ("IF302", "Cloud Computing", "cloud aws docker kubernetes microservices"),
    ("IF401", "Skripsi", "penelitian metodologi laporan"),
    ("IF303", "Keamanan Siber", "cybersecurity encryption network security"),
]


def main() -> None:
    pd.DataFrame(
        [{"kode_mk": k, "nama_mk": n, "deskripsi_cpl": d} for k, n, d in MK_CPL]
    ).to_csv(OUT / "kurikulum_cpl.csv", index=False)
    print(f"[OK] kurikulum_cpl.csv ({len(MK_CPL)} MK)")


if __name__ == "__main__":
    main()
