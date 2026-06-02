#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${LAB_ROOT}"

if [ ! -d .venv ]; then
  echo "[ERROR] venv belum ada. Jalankan: bash setup.sh"
  exit 1
fi
# shellcheck source=/dev/null
source .venv/bin/activate
cd app
