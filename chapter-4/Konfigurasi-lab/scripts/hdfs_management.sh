#!/usr/bin/env bash
# Latihan 5: cp, mv, du, hapus output, opsional re-run WordCount
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RE_RUN="${1:-}"

bash "${SCRIPT_DIR}/hadoop_exec.sh" "
  hdfs dfs -cp /user/latihan/latihan.txt /user/latihan/latihan_backup.txt
  hdfs dfs -mkdir -p /user/latihan/arsip
  hdfs dfs -mv /user/latihan/latihan_backup.txt /user/latihan/arsip/
  echo '=== du -h ==='
  hdfs dfs -du -h /user/latihan/
  echo '=== hapus output (jika ada) ==='
  hdfs dfs -rm -r -f /user/latihan/output || true
  hdfs dfs -ls /user/latihan/
"

if [ "${RE_RUN}" = "--rerun-wordcount" ]; then
  bash "${SCRIPT_DIR}/run_wordcount.sh"
fi

echo "[OK] Manajemen HDFS selesai."
