#!/usr/bin/env python3
"""Alert absen >3 minggu berturut → dosen PA."""
from __future__ import annotations

import argparse
import json

import pandas as pd

from analitik.lib.config import ABSEN_MINGGU_ALERT, GOLD, OUTPUT_DIR, SILVER, SUMBER

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="file")
    _ = parser.parse_args()

    path = SUMBER / "absensi" / "absensi_stream.jsonl"
    rows = [json.loads(line) for line in path.open()]
    alerts = [r for r in rows if r.get("minggu_beruntun_absen", 0) >= ABSEN_MINGGU_ALERT]

    bimbingan = pd.read_parquet(SILVER / "bimbingan_akademik.parquet")
    alert_df = pd.DataFrame(alerts).merge(bimbingan, on="mahasiswa_id", how="left")
    alert_df.to_parquet(GOLD / "alert_absensi_pa.parquet", index=False)

    out = OUTPUT_DIR / "output-1-early-warning-pa"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "alert_absensi_stream.jsonl").open("w") as f:
        for _, r in alert_df.iterrows():
            f.write(
                json.dumps(
                    {
                        "mahasiswa_id": r["mahasiswa_id"],
                        "dosen_pa_id": r.get("dosen_pa_id"),
                        "kode_mk": r.get("kode_mk"),
                        "minggu_beruntun_absen": int(r.get("minggu_beruntun_absen", 0)),
                        "tindak_lanjut": "Hubungi mahasiswa & orang tua dalam 72 jam",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    print(f"[OK] alert absensi PA: {len(alert_df)} mahasiswa")


if __name__ == "__main__":
    main()
