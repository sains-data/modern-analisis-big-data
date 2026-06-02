#!/usr/bin/env bash
# Generate dataset Modul 9 ke HDFS (Bronze + Silver)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

bash "${LAB_ROOT}/scripts/spark_submit.sh" \
  --conf spark.sql.shuffle.partitions=20 \
  /opt/modul9/scripts/buat_data_ml.py

echo ""
echo "[OK] Verifikasi:"
docker exec bigdata-spark hdfs dfs -ls /datalake/silver/transaksi/
