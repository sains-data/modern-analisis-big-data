#!/usr/bin/env bash
# Ukur login + sample chart API — Bab 14 Tahap 4
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

BASE="${SUPERSET_URL:-http://localhost:8088}"
USER="${SUPERSET_USER:-admin}"
PASS="${SUPERSET_PASSWORD:-admin}"
CHART_ID="${1:-1}"

TOKEN=$(curl -s -X POST "${BASE}/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${USER}\",\"password\":\"${PASS}\",\"provider\":\"db\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('access_token',''))")

if [ -z "${TOKEN}" ]; then
  echo "[ERROR] Login Superset gagal. Pastikan ${BASE} aktif."
  exit 1
fi

echo "[OK] Token didapat"
echo "=== Waktu respons chart/data (CHART_ID=${CHART_ID}) ==="
/usr/bin/time -p curl -s -o /dev/null \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -X POST "${BASE}/api/v1/chart/data" \
  -d "{\"datasource\":{\"id\":${CHART_ID},\"type\":\"table\"},\"queries\":[{\"metrics\":[\"count\"],\"row_limit\":100}]}"

echo ""
echo "Ganti CHART_ID: bash scripts/measure_superset_perf.sh <id>"
