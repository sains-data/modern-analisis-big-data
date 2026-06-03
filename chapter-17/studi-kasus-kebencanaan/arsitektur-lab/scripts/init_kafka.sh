#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PY="${SCRIPT_DIR}/_py.sh"
TOPIC="${KAFKA_TOPIC_TMA:-sensor.tma.musi}"

if ! docker ps --format '{{.Names}}' | grep -q ch17-ban-kafka; then
  echo "[SKIP] Kafka tidak berjalan — lewati init_kafka"
  exit 0
fi

docker exec ch17-ban-kafka kafka-topics --create \
  --if-not-exists \
  --bootstrap-server localhost:9092 \
  --topic "${TOPIC}" \
  --partitions 1 \
  --replication-factor 1 2>/dev/null || true

docker exec ch17-ban-kafka kafka-topics --create \
  --if-not-exists \
  --bootstrap-server localhost:9092 \
  --topic alert.banjir.musi \
  --partitions 1 \
  --replication-factor 1 2>/dev/null || true

echo "=== Publish sample TMA ke Kafka ==="
KAFKA_BOOTSTRAP=localhost:9093 "${PY}" \
  "${CASE_ROOT}/analitik/streaming/kafka_producer_tma.py" --limit 120

echo "[OK] Topik ${TOPIC} siap"
