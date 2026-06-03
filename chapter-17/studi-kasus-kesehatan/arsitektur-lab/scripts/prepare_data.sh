#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PY="${SCRIPT_DIR}/_py.sh"
mkdir -p "${CASE_ROOT}/data"/{sumber,bronze,silver,gold}

"${PY}" "${CASE_ROOT}/data/scripts/generate_who_lms.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_desa_puskesmas.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_eppgbm_balita.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_stbm_dtks.py"
echo "[OK] Data sumber siap."
