#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"
bash scripts/ensure_spark_repo.sh
# shellcheck source=/dev/null
source "${ROOT_DIR}/.env" 2>/dev/null || true
SPARK_REPO_DIR="${SPARK_REPO_DIR:-${ROOT_DIR}/vendor/bigdata-spark}"
(cd "${SPARK_REPO_DIR}" && bash start.sh)
sleep 10
bash scripts/copy_spark_jobs.sh
echo "[OK] bigdata-spark aktif."
