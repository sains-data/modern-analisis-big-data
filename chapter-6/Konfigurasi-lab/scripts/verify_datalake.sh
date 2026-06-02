#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

LAKE="${DATALAKE_ROOT:-/datalake}"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  echo '=== Bronze ==='
  hdfs dfs -ls ${LAKE}/bronze/transaksi/ 2>/dev/null || echo '(kosong)'
  hdfs dfs -ls ${LAKE}/bronze/pelanggan/ 2>/dev/null || echo '(kosong)'
  echo ''
  echo '=== Silver ==='
  hdfs dfs -ls -R ${LAKE}/silver/transaksi/ 2>/dev/null | head -20 || echo '(kosong)'
  echo ''
  echo '=== Gold ==='
  hdfs dfs -ls ${LAKE}/gold/per_kategori/ 2>/dev/null || echo '(kosong)'
  hdfs dfs -ls ${LAKE}/gold/per_segmen/ 2>/dev/null || echo '(kosong)'
"
