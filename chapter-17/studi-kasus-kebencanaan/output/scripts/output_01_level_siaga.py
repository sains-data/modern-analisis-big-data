#!/usr/bin/env python3
"""
output_01_level_siaga.py — Notifikasi level siaga untuk operator BPBD.
Setara output_01 di buku; Airflow Senin 07:00 → di lab dijalankan setelah pipeline.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, STASIUN_REF

OUT = OUTPUT_DIR / "output-1-level-siaga"
OUT.mkdir(parents=True, exist_ok=True)

TEMPLATE = """[BPBD Sumsel — Peringatan Dini Banjir DAS Musi]
Waktu: {waktu}
Stasiun referensi: {stasiun} ({nama})
TMA maksimum: {tma} cm
Hujan 3 jam: {hujan} mm
LEVEL SIAGA: {siaga}

Tindakan:
{tindakan}
"""


TINDAKAN = {
    "HIJAU": "- Pemantauan rutin",
    "KUNING": "- Siaga tim BPBD\n- Informasi lurah/RW",
    "ORANYE": "- Evakuasi preventif zona rendah\n- Aktifkan posko",
    "MERAH": "- Evakuasi masif\n- Tutup jalan terdampak",
}


def main() -> None:
    hourly = pd.read_parquet(GOLD / "tma_siaga_hourly.parquet")
    latest = pd.read_parquet(GOLD / "tma_latest.parquet")
    ref_latest = latest[latest["stasiun_id"] == STASIUN_REF].iloc[0]
    siaga = ref_latest["siaga"]
    tma = ref_latest["tma_cm"]
    rain = ref_latest.get("hujan_3jam_mm", 0)
    ref_hourly = hourly[hourly["stasiun_id"] == STASIUN_REF].sort_values("window_end").iloc[-1]

    waktu = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    alert = {
        "waktu": waktu,
        "stasiun_id": STASIUN_REF,
        "tma_cm": float(tma),
        "hujan_3jam_mm": float(rain),
        "siaga": siaga,
        "siaga_order": int(ref_latest["siaga_order"]),
    }

    (OUT / "alert_latest.json").write_text(json.dumps(alert, indent=2, ensure_ascii=False))

    # Semua stasiun ORANYE/MERAH
    krit = latest[latest["siaga"].isin(["ORANYE", "MERAH"])]
    krit.to_json(OUT / "stasiun_siaga_tinggi.json", orient="records", force_ascii=False, indent=2)

    msg = TEMPLATE.format(
        waktu=waktu,
        stasiun=STASIUN_REF,
        nama="Kayu Agung",
        tma=tma,
        hujan=rain,
        siaga=siaga,
        tindakan=TINDAKAN.get(siaga, ""),
    )
    (OUT / "notifikasi_template.txt").write_text(msg, encoding="utf-8")
    print(f"[OK] Siaga {STASIUN_REF}: {siaga} → {OUT}")


if __name__ == "__main__":
    main()
