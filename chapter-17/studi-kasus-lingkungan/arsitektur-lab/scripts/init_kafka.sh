#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
command -v docker >/dev/null || exit 0
docker ps --format '{{.Names}}' 2>/dev/null | grep -q ch17-ling-kafka || exit 0
for t in hotspot.firms.riau ispa.kecamatan.riau; do
  docker exec ch17-ling-kafka kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9092 --topic "$t" --partitions 1 --replication-factor 1 2>/dev/null || true
done
KAFKA_BOOTSTRAP=localhost:9095 "${PY}" "${CASE_ROOT}/analitik/streaming/kafka_producer_firms.py" --limit 100
