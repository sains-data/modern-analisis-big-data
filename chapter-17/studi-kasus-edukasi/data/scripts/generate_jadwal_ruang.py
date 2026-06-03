#!/usr/bin/env python3
"""Jadwal kuliah & kapasitas ruang."""
import random
from pathlib import Path

import pandas as pd

random.seed(67)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "akademik" / "jadwal"
OUT.mkdir(parents=True, exist_ok=True)

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
RUANG = [(f"R{i+1:02d}", random.choice([30, 40, 60, 80, 120])) for i in range(15)]
MK = ["IF101", "IF102", "IF201", "IF202", "IF301", "IF302", "IF401", "MKUM001"]


def main() -> None:
    rows = []
    slot_id = 0
    for hari in HARI:
        for jam in ["08:00", "10:00", "13:00", "15:00"]:
            for ruang_id, kap in random.sample(RUANG, k=3):
                slot_id += 1
                peserta = random.randint(8, kap)
                rows.append(
                    {
                        "slot_id": f"S{slot_id:04d}",
                        "hari": hari,
                        "jam": jam,
                        "ruang_id": ruang_id,
                        "kapasitas": kap,
                        "kode_mk": random.choice(MK),
                        "jumlah_mhs": peserta,
                        "hadir_rata": max(5, peserta - random.randint(0, 15)),
                    }
                )
    pd.DataFrame(rows).to_csv(OUT / "jadwal_ruang.csv", index=False)
    print(f"[OK] jadwal_ruang.csv ({len(rows)} slot)")


if __name__ == "__main__":
    main()
