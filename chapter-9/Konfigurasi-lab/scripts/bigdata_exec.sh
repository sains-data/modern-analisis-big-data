#!/usr/bin/env bash
# Menjalankan perintah di kontainer bigdata-spark (hdfs, hive, python, dll.)
set -euo pipefail
CONTAINER="${BIGDATA_CONTAINER:-bigdata-spark}"
exec docker exec -i "${CONTAINER}" bash -lc "$*"
