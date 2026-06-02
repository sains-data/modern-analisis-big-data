#!/usr/bin/env bash
# Jalankan spark-submit di dalam bigdata-spark dari host
set -euo pipefail

CONTAINER="${BIGDATA_CONTAINER:-bigdata-spark}"

if ! docker inspect "${CONTAINER}" >/dev/null 2>&1; then
  echo "[ERROR] Kontainer '${CONTAINER}' tidak ditemukan. Jalankan bash start.sh dulu."
  exit 1
fi

docker exec "${CONTAINER}" spark-submit \
  --master yarn \
  --deploy-mode client \
  --executor-memory 512m \
  --num-executors 2 \
  "$@"
