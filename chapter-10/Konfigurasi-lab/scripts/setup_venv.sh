#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

bash "$ROOT_DIR/scripts/check_python.sh"

python3 -m venv "$ROOT_DIR/.venv"
source "$ROOT_DIR/.venv/bin/activate"

pip install --upgrade pip
pip install -r "$ROOT_DIR/requirements.txt"

echo "[OK] Virtual environment siap: $ROOT_DIR/.venv"
echo "Aktifkan dengan: source .venv/bin/activate"
