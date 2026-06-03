#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
export PYTHONPATH="${CASE_ROOT}:${PYTHONPATH:-}"

"${PY}" "${CASE_ROOT}/analitik/batch/ingest_static.py"
"${PY}" "${CASE_ROOT}/analitik/batch/map_match_probe.py"
"${PY}" "${CASE_ROOT}/analitik/batch/agregasi_lalu_lintas.py"
"${PY}" "${CASE_ROOT}/analitik/batch/idw_pm25.py"
"${PY}" "${CASE_ROOT}/analitik/batch/korelasi_pm25.py"
"${PY}" "${CASE_ROOT}/analitik/batch/gap_tmd.py"
"${PY}" "${CASE_ROOT}/analitik/batch/estimasi_emisi.py"
"${PY}" "${CASE_ROOT}/analitik/streaming/probe_kecepatan_ruas.py" --source file
"${PY}" "${CASE_ROOT}/analitik/streaming/idw_pm25_grid.py" --source file
"${PY}" "${CASE_ROOT}/analitik/streaming/korelasi_pm25_volume.py" --source file
"${PY}" "${CASE_ROOT}/output/scripts/output_01_atcs_dashboard.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_02_iqu_hiperlokal.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_03_optimasi_tmd.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_04_laporan_emisi.py"
echo "[OK] Pipeline smart-city selesai."
