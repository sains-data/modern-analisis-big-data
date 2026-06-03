#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PY="${SCRIPT_DIR}/_py.sh"

command -v docker >/dev/null || exit 0
docker ps --format '{{.Names}}' 2>/dev/null | grep -q ch17-kes-kafka || exit 0

for t in balita.upload.sumut output.alert.kader; do
  docker exec ch17-kes-kafka kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9092 --topic "$t" --partitions 1 --replication-factor 1 2>/dev/null || true
done

KAFKA_BOOTSTRAP=localhost:9094 "${PY}" "${CASE_ROOT}/analitik/streaming/kafka_producer_upload.py" --limit 50
echo "[OK] Kafka topics + sample upload"
