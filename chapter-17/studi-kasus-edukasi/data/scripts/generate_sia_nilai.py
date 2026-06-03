#!/usr/bin/env python3
"""Nilai SIA per mahasiswa — korelasi dengan label risiko."""
import random
from pathlib import Path

import pandas as pd

random.seed(62)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "sia" / "nilai"
OUT.mkdir(parents=True, exist_ok=True)

MK = [
    ("IF101", "Algoritma", True),
    ("IF102", "Struktur Data", True),
    ("IF201", "Basis Data", True),
    ("IF202", "Jaringan Komputer", True),
    ("IF301", "Machine Learning", True),
    ("IF302", "Cloud Computing", False),
    ("IF401", "Skripsi", True),
    ("MKUM001", "Pancasila", False),
]


def grade(risk: int) -> str:
    if risk:
        return random.choices(["A", "B", "C", "D", "E"], weights=[5, 10, 25, 35, 25])[0]
    return random.choices(["A", "B", "C", "D", "E"], weights=[25, 35, 25, 10, 5])[0]


def main() -> None:
    base = pd.read_csv(CASE_ROOT / "data" / "sumber" / "sia" / "mahasiswa_base.csv")
    rows = []
    for _, m in base.iterrows():
        risk = m["label_historis_do"]
        for kode, nama, wajib in MK:
            g = grade(risk)
            rows.append(
                {
                    "mahasiswa_id": m["mahasiswa_id"],
                    "kode_mk": kode,
                    "nama_mk": nama,
                    "mk_wajib": wajib,
                    "semester": m["semester_aktif"],
                    "nilai_huruf": g,
                    "nilai_indeks": {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0}[g],
                    "sks": 3,
                }
            )
    pd.DataFrame(rows).to_csv(OUT / "nilai_semester.csv", index=False)
    print(f"[OK] nilai_semester.csv ({len(rows)} baris)")


if __name__ == "__main__":
    main()
