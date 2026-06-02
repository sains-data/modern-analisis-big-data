#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${SCRIPT_DIR}/copy_spark_jobs.sh" >/dev/null
bash "${SCRIPT_DIR}/install_happybase.sh"
bash "${SCRIPT_DIR}/setup_services.sh"
JOBS_DIR="${SPARK_JOBS_DIR:-/opt/spark-jobs}"
CONTAINER="${SPARK_CONTAINER:-bigdata-spark}"
docker exec "${CONTAINER}" python3 "${JOBS_DIR}/event_log_hbase.py"
