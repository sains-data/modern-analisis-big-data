#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
export PYTHONPATH="${CASE_ROOT}:${PYTHONPATH:-}"

"${PY}" "${CASE_ROOT}/analitik/batch/ingest_static.py"
"${PY}" "${CASE_ROOT}/analitik/batch/fitur_la.py"
"${PY}" "${CASE_ROOT}/analitik/batch/model_risiko.py"
"${PY}" "${CASE_ROOT}/analitik/batch/klaster_matkul.py"
"${PY}" "${CASE_ROOT}/analitik/batch/utilisasi_ruang.py"
"${PY}" "${CASE_ROOT}/analitik/batch/skill_gap.py"
"${PY}" "${CASE_ROOT}/analitik/batch/indikator_banpt.py"
"${PY}" "${CASE_ROOT}/analitik/streaming/alert_absensi_pa.py" --source file
"${PY}" "${CASE_ROOT}/output/scripts/output_01_early_warning.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_02_utilisasi_ruang.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_03_laporan_skill_gap.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_04_dashboard_banpt.py"
echo "[OK] Pipeline edukasi selesai."
