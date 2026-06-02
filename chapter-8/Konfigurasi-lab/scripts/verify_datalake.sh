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
  hdfs dfs -ls ${LAKE}/bronze/transaksi/ 2>/dev/null || true
  echo ''
  echo '=== Silver ==='
  hdfs dfs -ls -R ${LAKE}/silver/transaksi/ 2>/dev/null | head -15 || true
  echo ''
  echo '=== Gold / benchmark ==='
  hdfs dfs -ls ${LAKE}/gold/ 2>/dev/null || true
  hdfs dfs -ls ${LAKE}/benchmark/ 2>/dev/null || true
  echo ''
  echo '=== Hive tables ==='
  hive -e 'USE datalake; SHOW TABLES;' 2>/dev/null || beeline -u jdbc:hive2://localhost:10001/ -n hive -p hive -e 'USE datalake; SHOW TABLES;' 2>/dev/null || echo '(hive CLI belum siap)'
"
