#!/usr/bin/env python3
"""Proses upload balita → alert MERAH/ORANYE/KUNING."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

from analitik.lib.alert import classify_alert
from analitik.lib.config import GOLD, KAFKA_TOPIC_ALERT, KAFKA_TOPIC_UPLOAD, SILVER, SUMBER
from analitik.lib.who_lms import add_zscore_tb_u

GOLD.mkdir(parents=True, exist_ok=True)


def load_uploads_file() -> list[dict]:
    path = SUMBER / "eppgbm" / "upload_events.jsonl"
    rows = []
    with path.open() as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def load_uploads_kafka(limit: int = 50) -> list[dict]:
    from kafka import KafkaConsumer

    bootstrap = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9094")
    consumer = KafkaConsumer(
        KAFKA_TOPIC_UPLOAD,
        bootstrap_servers=bootstrap,
        auto_offset_reset="earliest",
        consumer_timeout_ms=5000,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    rows = []
    for msg in consumer:
        rows.append(msg.value)
        if len(rows) >= limit:
            break
    return rows


def process_events(events: list[dict]) -> pd.DataFrame:
    lms = pd.read_parquet(SILVER / "who_lms_standar.parquet")
    alerts = []
    for ev in events:
        bb_prev = ev.get("bb_kg_prev")
        bb = ev["bb_kg"]
        delta_g = None
        if bb_prev is not None:
            delta_g = (bb - bb_prev) * 1000
        row = pd.DataFrame([ev])
        scored = add_zscore_tb_u(row, lms)
        z = float(scored.iloc[0]["z_tb_u"])
        level = classify_alert(
            z,
            delta_bb_gram=delta_g,
            bulan_absen=int(ev.get("bulan_absen", 0)),
        )
        if level:
            alerts.append(
                {
                    "balita_id": ev["balita_id"],
                    "desa_id": ev["desa_id"],
                    "level": level,
                    "z_tb_u": round(z, 3),
                    "delta_bb_gram": delta_g,
                    "ts": ev.get("ts"),
                    "tindak_lanjut": {
                        "MERAH": "Kunjungan 24 jam, rujuk Puskesmas",
                        "ORANYE": "Kunjungan 72 jam, edukasi gizi",
                        "KUNING": "Pemantauan + PMT",
                    }[level],
                }
            )
    return pd.DataFrame(alerts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["file", "kafka"], default="file")
    args = parser.parse_args()

    events = load_uploads_kafka() if args.source == "kafka" else load_uploads_file()
    alerts = process_events(events)
    out_path = GOLD / "alert_kader.parquet"
    alerts.to_parquet(out_path, index=False)

    log_path = Path(__file__).resolve().parents[2] / "output" / "output-3-alert-kader"
    log_path.mkdir(parents=True, exist_ok=True)
    with (log_path / "alert_log_latest.jsonl").open("w") as f:
        for _, r in alerts.iterrows():
            f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")

    print(f"[OK] {len(alerts)} alert dari {len(events)} upload → {out_path}")


if __name__ == "__main__":
    main()
