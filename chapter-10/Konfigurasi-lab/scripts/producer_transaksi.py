import json
import random
import time
import uuid
from datetime import datetime, timezone

from kafka import KafkaProducer

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "transaksi-stream"

CHANNELS = ["mobile", "web", "atm", "teller"]
PRODUCTS = ["elektronik", "fashion", "makanan", "kesehatan", "otomotif"]
USER_IDS = [f"usr-{i:04d}" for i in range(1, 51)]

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if k else None,
    acks="all",
    enable_idempotence=True,
    retries=3,
)


def buat_event():
    user_id = random.choice(USER_IDS)
    event_time = datetime.now(timezone.utc)
    return {
        "event_id": str(uuid.uuid4())[:8],
        "user_id": user_id,
        "product": random.choice(PRODUCTS),
        "channel": random.choice(CHANNELS),
        "amount": round(random.uniform(10_000, 5_000_000), 2),
        "event_time": event_time.isoformat(),
    }, user_id


if __name__ == "__main__":
    sent = 0
    try:
        while True:
            event, key = buat_event()
            producer.send(TOPIC_NAME, key=key, value=event)
            sent += 1
            if sent % 10 == 0:
                print(f"[{sent}] id={event['event_id']} user={key} amount={event['amount']}")
            time.sleep(random.uniform(0.1, 0.5))
    except KeyboardInterrupt:
        print(f"\nProducer dihentikan, total={sent}")
    finally:
        producer.flush()
        producer.close()
