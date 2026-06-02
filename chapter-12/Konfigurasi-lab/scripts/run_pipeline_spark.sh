#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${SCRIPT_DIR}/run_buat_data_viz.sh"
bash "${SCRIPT_DIR}/run_persiapan_analitik.sh"
bash "${SCRIPT_DIR}/run_metrik_lanjutan.sh"
echo "[OK] Gold layer siap. Jalankan ekspor setelah viz-postgres aktif:"
echo "  bash start-viz.sh && bash scripts/run_ekspor_postgresql.sh"
