#!/usr/bin/env bash
# Latihan 4: bandingkan ukuran CSV vs Parquet
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

HDFS_DIR="${HDFS_WORK_DIR:-/user/lab/modul5}"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  echo '=== CSV ==='
  hdfs dfs -du -h ${HDFS_DIR}/mahasiswa.csv
  echo '=== Parquet (hasil_nilai) ==='
  hdfs dfs -du -h ${HDFS_DIR}/hasil_nilai/ 2>/dev/null || echo '(belum ada — jalankan run_analisis_nilai.sh)'
"
