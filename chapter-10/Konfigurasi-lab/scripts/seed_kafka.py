import argparse
import json
import time

from kafka import KafkaProducer

KAFKA_SERVER = "localhost:9092"


def seed(topic: str, filepath: str, delay: float = 0.02):
    with open(filepath, "r", encoding="utf-8") as f:
        events = json.load(f)

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        acks="all",
        enable_idempotence=True,
    )

    for ev in events:
        key = ev.get("user_id") or ev.get("sensor_id")
        producer.send(topic, key=key, value=ev)
        time.sleep(delay)

    producer.flush()
    producer.close()
    print(f"[OK] Seed selesai: {len(events)} event ke {topic}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="transaksi-stream")
    parser.add_argument("--file", default="data/transaksi_historis.json")
    parser.add_argument("--delay", type=float, default=0.02)
    args = parser.parse_args()
    seed(args.topic, args.file, args.delay)
