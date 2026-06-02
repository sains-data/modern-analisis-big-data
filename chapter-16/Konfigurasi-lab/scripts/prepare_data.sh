#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

mkdir -p "${LAB_ROOT}/output"/{bronze,silver,gold,checkpoints}
mkdir -p "${LAB_ROOT}/data"

if [ -d "${LAB_ROOT}/.venv" ]; then
  PY="${LAB_ROOT}/.venv/bin/python"
else
  PY="python3"
fi

echo "=== Generate hotspot sample ==="
"${PY}" "${SCRIPT_DIR}/generate_sample.py"

echo "=== Generate batas kecamatan (GeoParquet) ==="
if ! "${PY}" -c "import geopandas" 2>/dev/null; then
  echo "[INFO] Membuat venv lokal untuk geopandas..."
  python3 -m venv "${LAB_ROOT}/.venv"
  "${LAB_ROOT}/.venv/bin/pip" install -q -r "${LAB_ROOT}/requirements.txt"
  PY="${LAB_ROOT}/.venv/bin/python"
fi
"${PY}" "${SCRIPT_DIR}/generate_batas_kecamatan.py"

echo "[OK] Data siap di ${LAB_ROOT}/data/"
