#!/usr/bin/env bash
# Usage: bash scripts/run_spark_submit.sh hive_etl.py
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

PY="${1:?Nama file di app/ (mis. hive_etl.py)}"

CONTAINER="${SPARK_CONTAINER:-bigdata-spark}"
JOBS_DIR="${SPARK_JOBS_DIR:-/opt/spark-jobs}"

bash "${SCRIPT_DIR}/copy_spark_jobs.sh" >/dev/null

docker exec "${CONTAINER}" \
  spark-submit \
    --master yarn \
    --deploy-mode client \
    --executor-memory 512m \
    --num-executors 2 \
    --py-files "${JOBS_DIR}/spark_common.py" \
    "${JOBS_DIR}/${PY}"
