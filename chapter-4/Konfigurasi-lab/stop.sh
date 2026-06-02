#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${ROOT_DIR}/.env" 2>/dev/null || true
HADOOP_REPO_DIR="${HADOOP_REPO_DIR:-${ROOT_DIR}/vendor/bigdata-hadoop}"

if [ -f "${HADOOP_REPO_DIR}/stop.sh" ]; then
  (cd "${HADOOP_REPO_DIR}" && bash stop.sh)
else
  docker rm -f "${HADOOP_CONTAINER:-bigdata-hadoop}" 2>/dev/null || true
fi

echo "[OK] Klaster dihentikan."
