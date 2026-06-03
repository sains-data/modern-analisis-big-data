#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
export PYTHONPATH="${CASE_ROOT}:${PYTHONPATH:-}"

"${PY}" "${CASE_ROOT}/analitik/batch/ingest_static.py"
"${PY}" "${CASE_ROOT}/analitik/batch/interpolasi_gps.py"
"${PY}" "${CASE_ROOT}/analitik/batch/deteksi_deforestasi.py"
"${PY}" "${CASE_ROOT}/analitik/batch/kde_home_range.py"
"${PY}" "${CASE_ROOT}/analitik/batch/indeks_tekanan.py"
"${PY}" "${CASE_ROOT}/analitik/batch/coverage_gap.py"
"${PY}" "${CASE_ROOT}/analitik/streaming/alert_konflik_stream.py" --source file
"${PY}" "${CASE_ROOT}/output/scripts/output_01_alert_konflik.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_02_bukti_deforestasi.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_03_laporan_kel_eudr.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_04_basis_pergerakan.py"
echo "[OK] Pipeline konservasi selesai."
