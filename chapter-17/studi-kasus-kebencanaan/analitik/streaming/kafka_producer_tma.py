#!/usr/bin/env python3
"""Publish pembacaan TMA ke topik Kafka sensor.tma.musi."""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from analitik.lib.config import KAFKA_TOPIC_TMA, SUMBER

SUMBER_TMA = SUMBER / "sensor" / "tma_musi" / "tma_readings.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--delay", type=float, default=0.05)
    args = parser.parse_args()

    try:
        from kafka import KafkaProducer
    except ImportError as e:
        raise SystemExit("pip install kafka-python") from e

    bootstrap = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9093")
    producer = KafkaProducer(
        bootstrap_servers=bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    if not SUMBER_TMA.exists():
        raise FileNotFoundError(SUMBER_TMA)

    n = 0
    with SUMBER_TMA.open() as f:
        for line in f:
            if n >= args.limit:
                break
            row = json.loads(line)
            producer.send(KAFKA_TOPIC_TMA, row)
            n += 1
            time.sleep(args.delay)

    producer.flush()
    print(f"[OK] {n} event → {KAFKA_TOPIC_TMA} @ {bootstrap}")


if __name__ == "__main__":
    main()
