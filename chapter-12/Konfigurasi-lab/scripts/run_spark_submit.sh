#!/usr/bin/env bash
# Usage: bash scripts/run_spark_submit.sh buat_data_viz.py
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

PY="${1:?Nama file di app/}"
CONTAINER="${SPARK_CONTAINER:-bigdata-spark}"
JOBS_DIR="${SPARK_JOBS_DIR:-/opt/spark-jobs}"

bash "${SCRIPT_DIR}/copy_spark_jobs.sh" >/dev/null

EXTRA_JARS=""
if [ "${PY}" = "ekspor_postgresql.py" ]; then
  bash "${SCRIPT_DIR}/install_jdbc_driver.sh" >/dev/null
  EXTRA_JARS="--jars /opt/spark/jars/postgresql-42.7.3.jar"
fi

docker exec \
  -e "PG_JDBC_URL=${PG_JDBC_URL:-jdbc:postgresql://host.docker.internal:5432/analytics}" \
  -e "PG_USER=${PG_USER:-superset}" \
  -e "PG_PASSWORD=${PG_PASSWORD:-superset}" \
  "${CONTAINER}" \
  spark-submit \
    --master yarn \
    --deploy-mode client \
    --executor-memory 512m \
    --num-executors 2 \
    ${EXTRA_JARS} \
    --py-files "${JOBS_DIR}/spark_common.py" \
    "${JOBS_DIR}/${PY}"
