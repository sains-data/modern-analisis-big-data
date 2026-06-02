#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"
bash scripts/ensure_spark_repo.sh
# shellcheck source=/dev/null
source "${ROOT_DIR}/.env" 2>/dev/null || true
SPARK_REPO_DIR="${SPARK_REPO_DIR:-${ROOT_DIR}/vendor/bigdata-spark}"
(cd "${SPARK_REPO_DIR}" && bash start.sh)
echo "[INFO] Tunggu bootstrap (~2–5 menit): bash scripts/spark_exec.sh 'tail -20 /tmp/bootstrap.log'"
sleep 15
bash scripts/copy_spark_jobs.sh
bash scripts/install_happybase.sh || true
bash scripts/verify_cluster.sh || echo "[INFO] Ulangi verify setelah bootstrap selesai."
echo ""
echo "[OK] Klaster aktif. Lanjut: bash scripts/setup_services.sh && bash scripts/setup_datalake_bronze.sh"
