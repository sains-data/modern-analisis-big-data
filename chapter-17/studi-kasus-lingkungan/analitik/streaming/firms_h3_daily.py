#!/usr/bin/env python3
"""Agregat FRP/hotspot per H3 res-7 (tumbling harian)."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, H3_RES, SILVER, SUMBER
from analitik.lib.h3util import latlon_to_h3

GOLD.mkdir(parents=True, exist_ok=True)


def load_events(source: str) -> pd.DataFrame:
    if source == "kafka":
        from kafka import KafkaConsumer
        from analitik.lib.config import KAFKA_TOPIC_FIRMS

        bootstrap = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9095")
        consumer = KafkaConsumer(
            KAFKA_TOPIC_FIRMS,
            bootstrap_servers=bootstrap,
            auto_offset_reset="earliest",
            consumer_timeout_ms=5000,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        rows = [msg.value for msg in consumer]
        return pd.DataFrame(rows)
    return pd.read_parquet(SILVER / "hotspot_firms_verified.parquet")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["file", "kafka"], default="file")
    args = parser.parse_args()

    if args.source == "file" and not (SILVER / "hotspot_firms_verified.parquet").exists():
        df = pd.read_csv(SUMBER / "firms" / "viirs_riau_2025.csv")
        df = df[df["confidence"].isin(["nominal", "high"])]
    else:
        df = load_events(args.source)

    df["h3_id"] = df.apply(
        lambda r: latlon_to_h3(r["latitude"], r["longitude"], H3_RES), axis=1
    )
    agg = (
        df.groupby("h3_id")
        .agg(n_hotspot=("hotspot_id", "count"), sum_frp=("frp", "sum"))
        .reset_index()
    )
    agg.to_parquet(GOLD / "firms_h3_daily.parquet", index=False)
    print(f"[OK] firms_h3_daily — {len(agg)} sel")


if __name__ == "__main__":
    main()
