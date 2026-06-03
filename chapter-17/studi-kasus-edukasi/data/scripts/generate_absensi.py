#!/usr/bin/env python3
"""Absensi per sesi + stream alert (>3 minggu absen)."""
import json
import random
from pathlib import Path

import pandas as pd

random.seed(64)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "absensi"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    base = pd.read_csv(CASE_ROOT / "data" / "sumber" / "sia" / "mahasiswa_base.csv")
    rows = []
    stream = []
    alert_mhs = None
    for idx, m in base.iterrows():
        risk = m["label_historis_do"]
        for minggu in range(1, 15):
            hadir = random.random() > (0.35 if risk else 0.08)
            rows.append(
                {
                    "mahasiswa_id": m["mahasiswa_id"],
                    "kode_mk": "IF101",
                    "minggu_ke": minggu,
                    "hadir": int(hadir),
                    "ts": f"2026-05-{min(minggu, 27):02d}T10:00:00Z",
                }
            )
        # Satu mahasiswa risiko: absen 4 minggu berturut untuk demo alert
        if alert_mhs is None and risk:
            alert_mhs = m["mahasiswa_id"]
            for w in range(12, 16):
                rows.append(
                    {
                        "mahasiswa_id": alert_mhs,
                        "kode_mk": "IF201",
                        "minggu_ke": w,
                        "hadir": 0,
                        "ts": f"2026-05-27T10:00:00Z",
                    }
                )
            stream.append(
                {
                    "mahasiswa_id": alert_mhs,
                    "kode_mk": "IF201",
                    "hadir": 0,
                    "minggu_beruntun_absen": 4,
                    "ts": "2026-05-27T10:00:01Z",
                    "event": "absensi.sesi",
                }
            )

    pd.DataFrame(rows).to_csv(OUT / "absensi_sesi.csv", index=False)
    with (OUT / "absensi_stream.jsonl").open("w") as f:
        for s in stream:
            f.write(json.dumps(s) + "\n")
    print(f"[OK] absensi_sesi.csv ({len(rows)} baris), alert stream {len(stream)}")


if __name__ == "__main__":
    main()
