#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

mkdir -p datalake/bronze/transaksi datalake/silver/transaksi datalake/gold

echo "[OK] venv siap. Aktifkan: source .venv/bin/activate"
python -c "import pyarrow, duckdb, polars; print('dependencies OK')"
