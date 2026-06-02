#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
GOLD_LOCAL="${LAB_ROOT}/data/gold"

mkdir -p "${GOLD_LOCAL}"

for tabel in tren_bulanan omzet_kategori segmentasi_rfm omzet_kota; do
  rm -rf "${GOLD_LOCAL}/${tabel}"
  mkdir -p "${GOLD_LOCAL}/${tabel}"
  bash "${SCRIPT_DIR}/spark_exec.sh" "
    hdfs dfs -get /datalake/gold/${tabel}/*.parquet /tmp/ch14_${tabel}/ 2>/dev/null || \
    hdfs dfs -get /datalake/gold/${tabel}/ /tmp/ch14_${tabel}/
  "
  docker cp "bigdata-spark:/tmp/ch14_${tabel}/." "${GOLD_LOCAL}/${tabel}/"
  echo "[OK] ${tabel} → ${GOLD_LOCAL}/${tabel}/"
done
