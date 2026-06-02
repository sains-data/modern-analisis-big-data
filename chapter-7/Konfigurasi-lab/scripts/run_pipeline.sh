#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${SCRIPT_DIR}/run_bronze.sh"
bash "${SCRIPT_DIR}/run_silver.sh"
bash "${SCRIPT_DIR}/run_gold.sh"
bash "${SCRIPT_DIR}/run_validasi.sh"
echo "[OK] Pipeline medallion Arrow selesai."
