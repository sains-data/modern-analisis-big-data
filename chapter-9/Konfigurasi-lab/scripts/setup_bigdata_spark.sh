#!/usr/bin/env bash
# Salin skrip lab ke bigdata-spark dan siapkan direktori HDFS Modul 7
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONTAINER="${BIGDATA_CONTAINER:-bigdata-spark}"

if ! docker inspect "${CONTAINER}" >/dev/null 2>&1; then
  echo "[ERROR] Kontainer '${CONTAINER}' tidak ditemukan. Jalankan bigdata-spark (Modul 9) dulu."
  exit 1
fi

echo "=== Menyalin skrip lab ke ${CONTAINER} ==="
docker exec "${CONTAINER}" mkdir -p /opt/scripts /opt/spark-jobs
docker cp "${LAB_ROOT}/scripts/lab/generate_data.py" "${CONTAINER}:/opt/scripts/generate_data.py"
docker cp "${LAB_ROOT}/scripts/lab/latihan_etl.py" "${CONTAINER}:/opt/spark-jobs/latihan_etl.py"
docker cp "${LAB_ROOT}/scripts/lab/pipeline_gold.py" "${CONTAINER}:/opt/spark-jobs/pipeline_gold.py"
docker exec "${CONTAINER}" chmod +x /opt/scripts/generate_data.py

echo "=== Membuat direktori HDFS /datalake ==="
docker exec "${CONTAINER}" bash -lc "
  start-dfs.sh 2>/dev/null || true
  start-yarn.sh 2>/dev/null || true
  sleep 5
  hdfs dfs -mkdir -p /datalake/bronze/latihan
  hdfs dfs -mkdir -p /datalake/silver/latihan
  hdfs dfs -mkdir -p /datalake/gold/latihan
  hdfs dfs -ls /datalake/
"

echo "[OK] bigdata-spark siap untuk latihan Modul 7."
