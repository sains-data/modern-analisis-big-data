#!/usr/bin/env bash
set -euo pipefail

BROKER="localhost:${MOD8_KAFKA_PORT:-9092}"
CONTAINER="modul8-kafka-broker"

docker exec "$CONTAINER" kafka-topics.sh --create \
  --bootstrap-server "$BROKER" \
  --topic transaksi-stream \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

docker exec "$CONTAINER" kafka-topics.sh --create \
  --bootstrap-server "$BROKER" \
  --topic sensor-iot \
  --partitions 2 \
  --replication-factor 1 \
  --if-not-exists

docker exec "$CONTAINER" kafka-topics.sh --create \
  --bootstrap-server "$BROKER" \
  --topic penjualan-agregat \
  --partitions 1 \
  --replication-factor 1 \
  --if-not-exists

docker exec "$CONTAINER" kafka-topics.sh --list --bootstrap-server "$BROKER"
