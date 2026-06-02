#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${ROOT_DIR}/.env" 2>/dev/null || true
SPARK_REPO_DIR="${SPARK_REPO_DIR:-${ROOT_DIR}/vendor/bigdata-spark}"
if [ -f "${SPARK_REPO_DIR}/stop.sh" ]; then
  (cd "${SPARK_REPO_DIR}" && bash stop.sh)
else
  docker rm -f "${SPARK_CONTAINER:-bigdata-spark}" 2>/dev/null || true
fi
