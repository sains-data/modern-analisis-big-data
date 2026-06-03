#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
mkdir -p "${CASE_ROOT}/data"/{sumber,bronze,silver,gold}
"${PY}" "${CASE_ROOT}/data/scripts/generate_ruas_jalan.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_gtfs_tmd.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_kelurahan.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_sensor_udara.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_probe_gps.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_bmkg_angin.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_kecelakaan.py"
echo "[OK] Data sumber smart-city siap."
