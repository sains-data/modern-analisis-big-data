#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

HDFS_DIR="${HDFS_WORK_DIR:-/user/lab/modul5}"

bash "${SCRIPT_DIR}/copy_spark_jobs.sh"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  start-dfs.sh 2>/dev/null || true
  start-yarn.sh 2>/dev/null || true
  sleep 3
  hdfs dfsadmin -report | head -25
  hdfs dfs -mkdir -p ${HDFS_DIR}
  hdfs dfs -put -f /tmp/lab-data/mahasiswa.csv ${HDFS_DIR}/mahasiswa.csv
  hdfs dfs -ls ${HDFS_DIR}/
  hdfs dfs -cat ${HDFS_DIR}/mahasiswa.csv | head -5
"

echo "[OK] Data di ${HDFS_DIR}/mahasiswa.csv"
