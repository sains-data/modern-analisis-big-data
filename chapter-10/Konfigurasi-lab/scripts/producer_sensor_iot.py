import json
import random
import time
import uuid
from datetime import datetime, timezone

from kafka import KafkaProducer

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "sensor-iot"

SENSOR_IDS = [f"sensor-{i:03d}" for i in range(1, 21)]
LOCATIONS = ["gudang-A", "gudang-B", "lantai-1", "lantai-2", "parkir"]

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if k else None,
    acks="all",
)


if __name__ == "__main__":
    sent = 0
    try:
        while True:
            sensor_id = random.choice(SENSOR_IDS)
            event = {
                "event_id": str(uuid.uuid4())[:8],
                "sensor_id": sensor_id,
                "location": random.choice(LOCATIONS),
                "temperature": round(random.uniform(20.0, 45.0), 2),
                "humidity": round(random.uniform(30.0, 90.0), 2),
                "status": random.choice(["normal", "normal", "warning", "critical"]),
                "event_time": datetime.now(timezone.utc).isoformat(),
            }
            producer.send(TOPIC_NAME, key=sensor_id, value=event)
            sent += 1
            if sent % 10 == 0:
                print(f"[{sent}] sensor={sensor_id} temp={event['temperature']}")
            time.sleep(random.uniform(0.2, 1.0))
    except KeyboardInterrupt:
        print(f"\nProducer IoT dihentikan, total={sent}")
    finally:
        producer.flush()
        producer.close()
