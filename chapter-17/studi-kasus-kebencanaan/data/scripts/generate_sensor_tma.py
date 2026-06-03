#!/usr/bin/env python3
"""Generator pembacaan TMA 15 menit — termasuk skenario naik ke ORANYE/MERAH."""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

CASE_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = CASE_ROOT / "data" / "sumber" / "sensor" / "tma_musi"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STATIONS = [
    "KAYU_AGUNG", "PALEMBANG_KOTA", "SUNGAI_PINANG", "BANYUASIN_HULU",
    "OGAN_ILIR", "MUARA_KELINGI", "PANGKALAN_BALAI", "TALANG_KELAPA",
    "SEKAYU", "LAHAT_HULU",
]

# Baseline + ramp untuk stasiun referensi (ujian end-to-end)
BASE_TMA = {
    "KAYU_AGUNG": 620,
    "PALEMBANG_KOTA": 580,
}


def tma_series(stasiun_id: str, n: int, start: datetime) -> list[dict]:
    base = BASE_TMA.get(stasiun_id, random.randint(500, 640))
    rows = []
    for i in range(n):
        ts = start + timedelta(minutes=15 * i)
        if stasiun_id == "KAYU_AGUNG":
            # Naik bertahap: uji siaga ORANYE/MERAH di akhir deret (12 jam)
            tma = base + i * 9 + random.uniform(-3, 3)
        else:
            tma = base + random.uniform(-20, 40) + i * 0.5
        rows.append(
            {
                "stasiun_id": stasiun_id,
                "tma_cm": round(max(400, min(1150, tma)), 1),
                "ts": ts.replace(tzinfo=timezone.utc).isoformat(),
            }
        )
    return rows


def main() -> None:
    start = datetime(2026, 5, 27, 0, 0, 0, tzinfo=timezone.utc)
    n_per_station = 48  # 12 jam @ 15 menit
    all_rows = []
    for sid in STATIONS:
        all_rows.extend(tma_series(sid, n_per_station, start))

    out_jsonl = OUT_DIR / "tma_readings.jsonl"
    with out_jsonl.open("w") as f:
        for row in all_rows:
            f.write(json.dumps(row) + "\n")

    # CSV ringkas untuk Bronze
    import csv
    csv_path = OUT_DIR / "tma_readings.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["stasiun_id", "tma_cm", "ts"])
        w.writeheader()
        w.writerows(all_rows)

    print(f"[OK] {out_jsonl} ({len(all_rows)} baris)")


if __name__ == "__main__":
    main()
