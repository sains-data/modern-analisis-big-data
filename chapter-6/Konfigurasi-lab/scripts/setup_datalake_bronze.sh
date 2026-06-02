#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

LAKE="${DATALAKE_ROOT:-/datalake}"

bash "${SCRIPT_DIR}/copy_spark_jobs.sh"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  start-dfs.sh 2>/dev/null || true
  start-yarn.sh 2>/dev/null || true
  sleep 3
  hdfs dfs -mkdir -p ${LAKE}/bronze/transaksi
  hdfs dfs -mkdir -p ${LAKE}/bronze/pelanggan
  hdfs dfs -mkdir -p ${LAKE}/silver/transaksi
  hdfs dfs -mkdir -p ${LAKE}/gold/per_kategori
  hdfs dfs -mkdir -p ${LAKE}/gold/per_segmen
  hdfs dfs -put -f /tmp/lab-data/transaksi.csv ${LAKE}/bronze/transaksi/
  hdfs dfs -put -f /tmp/lab-data/pelanggan.csv ${LAKE}/bronze/pelanggan/
  echo '=== Struktur datalake ==='
  hdfs dfs -ls -R ${LAKE}/ | head -40
  echo '=== Preview transaksi ==='
  hdfs dfs -cat ${LAKE}/bronze/transaksi/transaksi.csv | head -5
"

echo "[OK] Bronze siap di ${LAKE}/bronze/"
