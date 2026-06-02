#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

SPARK_REPO_DIR="${SPARK_REPO_DIR:-${LAB_ROOT}/vendor/bigdata-spark}"

if [ ! -d "${SPARK_REPO_DIR}/.git" ]; then
  echo "=== Clone bigdata-spark ==="
  mkdir -p "$(dirname "${SPARK_REPO_DIR}")"
  git clone https://github.com/sains-data/bigdata-spark.git "${SPARK_REPO_DIR}"
fi

export SPARK_REPO_DIR
echo "[OK] Repo: ${SPARK_REPO_DIR}"

MISSING=0
for f in \
  hadoop-3.4.1.tar.gz \
  spark-3.5.5-bin-hadoop3.tgz \
  apache-hive-4.0.1-bin.tar.gz \
  apache-tez-0.10.4-bin.tar.gz \
  hbase-2.5.11-bin.tar.gz \
  apache-zookeeper-3.8.4-bin.tar.gz
do
  if [ ! -f "${SPARK_REPO_DIR}/${f}" ]; then
    echo "[MISSING] ${SPARK_REPO_DIR}/${f}"
    MISSING=1
  fi
done

if [ "${MISSING}" -eq 1 ]; then
  echo ""
  echo "Unduh tarball ke vendor/bigdata-spark/ (lihat README repo bigdata-spark):"
  echo "  https://github.com/sains-data/bigdata-spark"
  exit 1
fi
