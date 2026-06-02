#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${ROOT_DIR}/scripts/ensure_spark_repo.sh"
# shellcheck source=/dev/null
source "${ROOT_DIR}/.env" 2>/dev/null || true
SPARK_REPO_DIR="${SPARK_REPO_DIR:-${ROOT_DIR}/../../chapter-12/Konfigurasi-lab/vendor/bigdata-spark}"
(cd "${SPARK_REPO_DIR}" && bash build.sh)
