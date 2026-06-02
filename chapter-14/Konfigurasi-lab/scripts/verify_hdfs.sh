#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  echo '=== Silver ==='
  hdfs dfs -du -h /datalake/silver/transaksi/ 2>/dev/null || echo '(kosong)'
  echo ''
  echo '=== Gold ==='
  hdfs dfs -ls /datalake/gold/
  echo ''
  for g in tren_bulanan omzet_kategori segmentasi_rfm omzet_kota; do
    echo \"--- \$g ---\"
    hdfs dfs -du -h /datalake/gold/\$g/ 2>/dev/null || echo '(kosong)'
  done
"
