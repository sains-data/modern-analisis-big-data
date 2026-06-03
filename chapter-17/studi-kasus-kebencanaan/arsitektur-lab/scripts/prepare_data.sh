#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PY="${SCRIPT_DIR}/_py.sh"

mkdir -p "${CASE_ROOT}/data"/{sumber,bronze,silver,gold}

echo "=== Generate data sintetis DAS Musi ==="
"${PY}" "${CASE_ROOT}/data/scripts/generate_spatial_layers.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_sensor_tma.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_bmkg_hujan.py"

echo "[OK] Data sumber di ${CASE_ROOT}/data/sumber/"
