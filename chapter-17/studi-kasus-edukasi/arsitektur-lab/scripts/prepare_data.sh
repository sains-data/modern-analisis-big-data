#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
mkdir -p "${CASE_ROOT}/data"/{sumber,bronze,silver,gold}
"${PY}" "${CASE_ROOT}/data/scripts/generate_mahasiswa_base.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_sia_nilai.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_lms_events.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_absensi.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_keuangan.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_kurikulum.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_lowongan.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_jadwal_ruang.py"
echo "[OK] Data sumber edukasi siap."
