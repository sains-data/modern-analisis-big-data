#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
export PYTHONPATH="${CASE_ROOT}:${PYTHONPATH:-}"

"${PY}" "${CASE_ROOT}/analitik/batch/ingest_static.py"
"${PY}" "${CASE_ROOT}/analitik/batch/join_akuntabilitas.py"
"${PY}" "${CASE_ROOT}/analitik/streaming/firms_h3_daily.py" --source file
"${PY}" "${CASE_ROOT}/analitik/batch/indeks_risiko_h3.py"
"${PY}" "${CASE_ROOT}/analitik/batch/korelasi_ispu_ispa.py"
"${PY}" "${CASE_ROOT}/analitik/batch/emisi_karbon.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_01_peta_risiko.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_02_akuntabilitas.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_03_dashboard_ispu_ispa.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_04_emisi_karbon.py"
echo "[OK] Pipeline lingkungan selesai."
