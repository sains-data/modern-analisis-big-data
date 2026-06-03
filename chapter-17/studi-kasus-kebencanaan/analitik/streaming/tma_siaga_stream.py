#!/usr/bin/env python3
"""
tma_siaga_stream.py — Agregasi window 1 jam / slide 15 menit + label siaga.

Mode:
  --source file   : baca bronze/silver sensor (default lab)
  --source kafka  : konsumsi sensor.tma.musi (butuh Kafka aktif)

Setara Spark Structured Streaming di buku Bab 17.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

from analitik.lib.config import (
    BRONZE,
    GOLD,
    KAFKA_TOPIC_TMA,
    SILVER,
    STASIUN_REF,
)
from analitik.lib.siaga import combine_siaga

GOLD.mkdir(parents=True, exist_ok=True)
WINDOW = "60min"
SLIDE = "15min"


def load_events_file() -> pd.DataFrame:
    path = SILVER / "sensor_tma.parquet"
    if not path.exists():
        path = BRONZE / "sensor_tma.parquet"
    df = pd.read_parquet(path)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df


def load_events_kafka(limit: int = 500) -> pd.DataFrame:
    from kafka import KafkaConsumer

    bootstrap = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9093")
    consumer = KafkaConsumer(
        KAFKA_TOPIC_TMA,
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
    if not rows:
        raise RuntimeError("Tidak ada event Kafka — jalankan kafka_producer_tma.py")
    df = pd.DataFrame(rows)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df


def window_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    hujan_path = SILVER / "bmkg_hujan.parquet"
    hujan_map = {}
    if hujan_path.exists():
        hujan = pd.read_parquet(hujan_path)
        hujan_map = hujan.set_index("stasiun_id")["hujan_3jam_mm"].to_dict()

    df = df.set_index("ts").sort_index()
    agg = (
        df.groupby("stasiun_id")
        .resample(SLIDE)
        .agg(tma_max_cm=("tma_cm", "max"), tma_avg_cm=("tma_cm", "mean"), n_readings=("tma_cm", "count"))
        .reset_index()
        .rename(columns={"ts": "window_end"})
    )
    agg["tma_max_cm"] = agg["tma_max_cm"].round(1)
    agg["tma_avg_cm"] = agg["tma_avg_cm"].round(1)
    agg["hujan_3jam_mm"] = agg["stasiun_id"].map(hujan_map).fillna(0)
    agg["siaga"] = agg.apply(
        lambda r: combine_siaga(r["tma_max_cm"], r["hujan_3jam_mm"]), axis=1
    )
    agg["siaga_order"] = agg["siaga"].map({"HIJAU": 0, "KUNING": 1, "ORANYE": 2, "MERAH": 3})
    return agg


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["file", "kafka"], default="file")
    args = parser.parse_args()

    df = load_events_kafka() if args.source == "kafka" else load_events_file()
    hourly = window_aggregate(df)
    hourly.to_parquet(GOLD / "tma_siaga_hourly.parquet", index=False)

    ref = hourly[hourly["stasiun_id"] == STASIUN_REF].tail(1)
    if not ref.empty:
        r = ref.iloc[0]
        print(
            f"[SIAGA] {STASIUN_REF} window={r['window_end']} "
            f"max={r['tma_max_cm']} cm → {r['siaga']}"
        )
    print(f"[OK] gold/tma_siaga_hourly.parquet ({len(hourly)} baris window)")


if __name__ == "__main__":
    main()
