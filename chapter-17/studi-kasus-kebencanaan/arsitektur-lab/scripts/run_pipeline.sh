#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PY="${SCRIPT_DIR}/_py.sh"

export PYTHONPATH="${CASE_ROOT}:${PYTHONPATH:-}"

echo "=== Batch: ingest + agregasi TMA ==="
"${PY}" "${CASE_ROOT}/analitik/batch/ingest_static.py"
"${PY}" "${CASE_ROOT}/analitik/batch/aggregate_tma.py"

echo "=== Streaming (replay/file): window siaga ==="
"${PY}" "${CASE_ROOT}/analitik/streaming/tma_siaga_stream.py" --source file

echo "=== Spatial: populasi terdampak + routing ==="
"${PY}" "${CASE_ROOT}/analitik/batch/populasi_terdampak.py"
"${PY}" "${CASE_ROOT}/analitik/batch/routing_evakuasi.py"

echo "=== Output 1–4 ==="
"${PY}" "${CASE_ROOT}/output/scripts/output_01_level_siaga.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_02_export_peta.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_03_logistik.py"
"${PY}" "${CASE_ROOT}/output/scripts/output_04_after_action.py"

echo "[OK] Pipeline analitik + output selesai"
