#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

CH12_ENSURE="$(cd "${SCRIPT_DIR}/../../../chapter-12/Konfigurasi-lab" && pwd)/scripts/ensure_spark_repo.sh"
if [ -f "${CH12_ENSURE}" ]; then
  export SPARK_REPO_DIR="${SPARK_REPO_DIR:-${LAB_ROOT}/../../chapter-12/Konfigurasi-lab/vendor/bigdata-spark}"
  bash "${CH12_ENSURE}"
else
  bash "${SCRIPT_DIR}/ensure_spark_repo_local.sh"
fi
