#!/usr/bin/env bash
# Usage: bash scripts/run_spark_submit.sh hitung_pi.py
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

PY="${1:?Nama file di app/ (mis. hitung_pi.py)}"
shift || true

CONTAINER="${SPARK_CONTAINER:-bigdata-spark}"
JOBS_DIR="${SPARK_JOBS_DIR:-/opt/spark-jobs}"
HDFS_DIR="${HDFS_WORK_DIR:-/user/lab/modul5}"

bash "${SCRIPT_DIR}/copy_spark_jobs.sh" >/dev/null

docker exec \
  -e "HDFS_WORK_DIR=${HDFS_DIR}" \
  -e "SLICES=${SLICES:-4}" \
  -e "JUMLAH_DART=${JUMLAH_DART:-1000000}" \
  "${CONTAINER}" \
  spark-submit \
    --master yarn \
    --deploy-mode client \
    --executor-memory 512m \
    --num-executors 2 \
    "${JOBS_DIR}/${PY}"
