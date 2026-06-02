#!/usr/bin/env bash
# Salin file data latihan ke /tmp di dalam kontainer Hadoop.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

CONTAINER="${HADOOP_CONTAINER:-bigdata-hadoop}"

for f in latihan.txt dataset_wordcount.txt; do
  src="${LAB_ROOT}/data/${f}"
  if [ ! -f "${src}" ]; then
    echo "[ERROR] Tidak ada: ${src}"
    exit 1
  fi
  docker cp "${src}" "${CONTAINER}:/tmp/${f}"
  echo "  [OK] /tmp/${f}"
done
