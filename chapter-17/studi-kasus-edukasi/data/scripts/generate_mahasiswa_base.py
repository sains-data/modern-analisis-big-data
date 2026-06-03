#!/usr/bin/env python3
"""Roster mahasiswa — hanya mahasiswa_id hash, tanpa NIM di disk."""
import random
from pathlib import Path

import pandas as pd

from analitik.lib.privacy import hash_nim

random.seed(61)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "sia"
OUT.mkdir(parents=True, exist_ok=True)

PRODI = ["Teknik Informatika", "Teknik Elektro", "Teknik Industri", "Sistem Informasi"]
N_MHS = 500


def main() -> None:
    rows = []
    for i in range(N_MHS):
        mid = hash_nim(f"2021{i+1:04d}")
        at_risk = random.random() < 0.18
        rows.append(
            {
                "mahasiswa_id": mid,
                "angkatan": random.choice([2021, 2022, 2023, 2024]),
                "prodi": random.choice(PRODI),
                "dosen_pa_id": f"PA{random.randint(1, 25):03d}",
                "semester_aktif": random.randint(1, 8),
                "label_historis_do": int(at_risk),
                "status_aktif": 1,
            }
        )
    pd.DataFrame(rows).to_csv(OUT / "mahasiswa_base.csv", index=False)
    print(f"[OK] mahasiswa_base.csv ({N_MHS} mahasiswa, anonim)")


if __name__ == "__main__":
    main()
