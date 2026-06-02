#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

CONTAINER="${SPARK_CONTAINER:-bigdata-spark}"
JOBS_DIR="${SPARK_JOBS_DIR:-/opt/spark-jobs}"

docker exec "${CONTAINER}" mkdir -p "${JOBS_DIR}" /tmp/lab-data

for py in spark_common.py pipeline_bronze_silver.py analisis_join.py analisis_plan.py window_function.py sql_silver.py; do
  docker cp "${LAB_ROOT}/app/${py}" "${CONTAINER}:${JOBS_DIR}/${py}"
  echo "  [OK] ${JOBS_DIR}/${py}"
done

for csv in transaksi.csv pelanggan.csv; do
  docker cp "${LAB_ROOT}/data/${csv}" "${CONTAINER}:/tmp/lab-data/${csv}"
  echo "  [OK] /tmp/lab-data/${csv}"
done
