#!/usr/bin/env python3
"""Publish event upload e-PPGBM ke Kafka."""
import json
import os
import time
from pathlib import Path

from analitik.lib.config import KAFKA_TOPIC_UPLOAD, SUMBER

PATH = SUMBER / "eppgbm" / "upload_events.jsonl"


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    from kafka import KafkaProducer

    bootstrap = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9094")
    producer = KafkaProducer(
        bootstrap_servers=bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    n = 0
    with PATH.open() as f:
        for line in f:
            if n >= args.limit:
                break
            producer.send(KAFKA_TOPIC_UPLOAD, json.loads(line))
            n += 1
            time.sleep(0.02)
    producer.flush()
    print(f"[OK] {n} → {KAFKA_TOPIC_UPLOAD}")


if __name__ == "__main__":
    main()
