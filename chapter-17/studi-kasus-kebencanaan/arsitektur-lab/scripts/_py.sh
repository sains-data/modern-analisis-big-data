#!/usr/bin/env bash
# Pilih interpreter: venv lokal arsitektur-lab atau python3 sistem
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -x "${LAB_ROOT}/.venv/bin/python" ]; then
  exec "${LAB_ROOT}/.venv/bin/python" "$@"
fi
if ! python3 -c "import geopandas" 2>/dev/null; then
  echo "[INFO] Membuat venv di ${LAB_ROOT}/.venv ..."
  python3 -m venv "${LAB_ROOT}/.venv"
  "${LAB_ROOT}/.venv/bin/pip" install -q -r "${LAB_ROOT}/requirements.txt"
  exec "${LAB_ROOT}/.venv/bin/python" "$@"
fi
exec python3 "$@"
