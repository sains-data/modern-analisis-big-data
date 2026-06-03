#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
mkdir -p "${CASE_ROOT}/data"/{sumber,bronze,silver,gold}
"${PY}" "${CASE_ROOT}/data/scripts/generate_batas_kel.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_gps_collar.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_ndvi_grid.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_smart_patrol.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_edge_events.py"
echo "[OK] Data sumber konservasi siap."
