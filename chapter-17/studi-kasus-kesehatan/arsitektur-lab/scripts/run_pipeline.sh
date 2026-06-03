#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PY="${SCRIPT_DIR}/_py.sh"
export PYTHONPATH="${CASE_ROOT}:${PYTHONPATH:-}"

echo "=== Ingest & z-score WHO ==="
"${PY}" "${CASE_ROOT}/analitik/batch/ingest_static.py"
"${PY}" "${CASE_ROOT}/analitik/batch/kalkulasi_zscore.py"
"${PY}" "${CASE_ROOT}/analitik/batch/agregasi_prevalensi.py"
"${PY}" "${CASE_ROOT}/analitik/batch/aksesibilitas_puskesmas.py"
"${PY}" "${CASE_ROOT}/analitik/batch/indeks_risiko.py"
"${PY}" "${CASE_ROOT}/analitik/batch/spatial_analytics.py"

echo "=== Streaming alert kader ==="
"${PY}" "${CASE_ROOT}/analitik/streaming/alert_kader_stream.py" --source file

echo "=== Output 1–4 ==="
"${PY}" "${CASE_ROOT}/output/scripts/output_01_prioritas_desa.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_02_dashboard_tpps.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_03_alert_kader.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_04_bukti_nakes.py"

echo "[OK] Pipeline selesai."
