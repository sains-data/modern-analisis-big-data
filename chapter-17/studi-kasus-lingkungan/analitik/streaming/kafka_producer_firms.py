#!/usr/bin/env python3
import argparse
import json
import os
import time
from pathlib import Path

from analitik.lib.config import KAFKA_TOPIC_FIRMS, SUMBER

PATH = SUMBER / "firms" / "viirs_stream.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    from kafka import KafkaProducer

    producer = KafkaProducer(
        bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP", "localhost:9095"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    n = 0
    with PATH.open() as f:
        for line in f:
            if n >= args.limit:
                break
            producer.send(KAFKA_TOPIC_FIRMS, json.loads(line))
            n += 1
            time.sleep(0.02)
    producer.flush()
    print(f"[OK] {n} → {KAFKA_TOPIC_FIRMS}")


if __name__ == "__main__":
    main()
