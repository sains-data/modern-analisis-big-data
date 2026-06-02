#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${SCRIPT_DIR}/run_seed_silver.sh"
bash "${SCRIPT_DIR}/run_pipeline_ecommerce.sh"
echo "[OK] Pipeline Ch.14 selesai (Silver + Gold Parquet)."
