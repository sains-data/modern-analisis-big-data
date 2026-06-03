#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OK=0

check_file() {
  if [ -f "$1" ]; then
    echo "  [OK] $1"
  else
    echo "  [MISS] $1"
    OK=1
  fi
}

echo "=== Artefak Gold & Output ==="
check_file "${CASE_ROOT}/data/gold/tma_siaga_hourly.parquet"
check_file "${CASE_ROOT}/data/gold/populasi_terdampak.parquet"
check_file "${CASE_ROOT}/data/gold/rute_evakuasi.parquet"
check_file "${CASE_ROOT}/output/output-1-level-siaga/alert_latest.json"
check_file "${CASE_ROOT}/output/output-2-peta-terdampak/terdampak_latest.geojson"
check_file "${CASE_ROOT}/output/output-2-peta-terdampak/kepler_config.json"
check_file "${CASE_ROOT}/output/output-3-logistik/logistik_ringkasan.pdf"
check_file "${CASE_ROOT}/output/output-4-after-action/after_action_latest.md"

if command -v docker >/dev/null 2>&1 && docker ps --format '{{.Names}}' 2>/dev/null | grep -q ch17-ban-kafka; then
  echo "  [OK] Kafka container aktif"
else
  echo "  [INFO] Kafka tidak aktif (pipeline file-mode tetap jalan)"
fi

exit "${OK}"
