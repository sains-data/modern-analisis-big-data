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
bash "${SCRIPT_DIR}/setup_services.sh"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  hdfs dfs -mkdir -p ${LAKE}/bronze/transaksi
  hdfs dfs -mkdir -p ${LAKE}/bronze/pelanggan
  hdfs dfs -mkdir -p ${LAKE}/silver/transaksi
  hdfs dfs -mkdir -p ${LAKE}/silver/transaksi_orc
  hdfs dfs -mkdir -p ${LAKE}/gold
  hdfs dfs -mkdir -p ${LAKE}/benchmark

  hdfs dfs -put -f /tmp/lab-data/transaksi.csv ${LAKE}/bronze/transaksi/data.csv
  hdfs dfs -put -f /tmp/lab-data/pelanggan.csv ${LAKE}/bronze/pelanggan/data.csv

  echo '=== Bronze di HDFS ==='
  hdfs dfs -ls ${LAKE}/bronze/transaksi/
  hdfs dfs -cat ${LAKE}/bronze/transaksi/data.csv | head -3
  echo -n 'Baris transaksi (termasuk header): '
  hdfs dfs -cat ${LAKE}/bronze/transaksi/data.csv | wc -l
"

echo "[OK] Bronze: 500 transaksi + 50 pelanggan di ${LAKE}/bronze/"
