#!/usr/bin/env bash
# Memanggil spark-submit di kontainer bigdata-spark (HDFS + YARN Modul 9)
set -euo pipefail
CONTAINER="${BIGDATA_CONTAINER:-bigdata-spark}"
exec docker exec -i "${CONTAINER}" /opt/spark/bin/spark-submit "$@"
