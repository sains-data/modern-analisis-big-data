#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -x "${LAB_ROOT}/.venv/bin/python" ]; then
  exec "${LAB_ROOT}/.venv/bin/python" "$@"
fi
if ! python3 -c "import geopandas, h3" 2>/dev/null; then
  python3 -m venv "${LAB_ROOT}/.venv"
  "${LAB_ROOT}/.venv/bin/pip" install -q -r "${LAB_ROOT}/requirements.txt"
  exec "${LAB_ROOT}/.venv/bin/python" "$@"
fi
exec python3 "$@"
