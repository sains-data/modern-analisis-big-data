#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

bash scripts/ensure_hadoop_repo.sh
# shellcheck source=/dev/null
source "${ROOT_DIR}/.env" 2>/dev/null || true
HADOOP_REPO_DIR="${HADOOP_REPO_DIR:-${ROOT_DIR}/vendor/bigdata-hadoop}"

echo "=== Build image bigdata-hadoop ==="
(cd "${HADOOP_REPO_DIR}" && bash build.sh)

echo "[OK] Build selesai."
