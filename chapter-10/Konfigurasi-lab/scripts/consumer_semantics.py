"""
consumer_semantics.py
Membaca event dari Kafka dan menghitung duplikat untuk analisis delivery semantics.
"""

import json

from kafka import KafkaConsumer

KAFKA_SERVER = "localhost:9092"
TOPIC = "transaksi-stream"
GROUP_ID = "analisis-duplikat-lab"
TARGET = 100

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    group_id=GROUP_ID,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

seen_ids = set()
total = 0
duplikat = 0
per_channel = {}

print(f"[Consumer] Membaca {TARGET} event dari topic '{TOPIC}'...\n")

for msg in consumer:
    event = msg.value
    event_id = event.get("event_id", "")
    channel = event.get("channel", "unknown")
    total += 1
    per_channel[channel] = per_channel.get(channel, 0) + 1

    if event_id in seen_ids:
        duplikat += 1
        print(f"  [DUPLIKAT] event_id={event_id} partition={msg.partition} offset={msg.offset}")
    else:
        seen_ids.add(event_id)

    consumer.commit()

    if total >= TARGET:
        break

print(f"\n{'=' * 50}")
print(" RINGKASAN ANALISIS DELIVERY SEMANTICS")
print(f"{'=' * 50}")
print(f" Total event dibaca : {total}")
print(f" Event ID unik      : {len(seen_ids)}")
print(f" Duplikat terdeteksi: {duplikat}")
print(f" Rasio duplikat     : {duplikat / total * 100:.1f}%")
print("\n Distribusi per channel:")
for ch, count in sorted(per_channel.items(), key=lambda x: -x[1]):
    print(f"   {ch:<10} : {count:>4} event ({count / total * 100:.1f}%)")
print(f"{'=' * 50}")

consumer.close()
