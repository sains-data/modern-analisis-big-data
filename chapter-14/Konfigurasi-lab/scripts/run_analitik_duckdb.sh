#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ ! -d "${LAB_ROOT}/data/gold/tren_bulanan" ] || [ -z "$(ls -A "${LAB_ROOT}/data/gold/tren_bulanan" 2>/dev/null || true)" ]; then
  echo "[INFO] Gold lokal kosong — ekspor dari HDFS..."
  bash "${SCRIPT_DIR}/export_gold_local.sh"
fi

if [ ! -d "${LAB_ROOT}/.venv" ]; then
  python3 -m venv "${LAB_ROOT}/.venv"
  "${LAB_ROOT}/.venv/bin/pip" install -q -r "${LAB_ROOT}/requirements.txt"
fi

"${LAB_ROOT}/.venv/bin/python" "${LAB_ROOT}/app/analitik_duckdb.py"
