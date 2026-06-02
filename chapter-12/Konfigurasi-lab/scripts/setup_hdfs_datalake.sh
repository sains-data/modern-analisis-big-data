#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  start-dfs.sh 2>/dev/null || true
  start-yarn.sh 2>/dev/null || true
  sleep 3
  hdfs dfs -mkdir -p /datalake/silver/transaksi
  hdfs dfs -mkdir -p /datalake/gold/tren_bulanan
  hdfs dfs -mkdir -p /datalake/gold/tren_lanjutan
  hdfs dfs -mkdir -p /datalake/gold/omzet_kategori
  hdfs dfs -mkdir -p /datalake/gold/omzet_kota
  hdfs dfs -ls /datalake/
"
