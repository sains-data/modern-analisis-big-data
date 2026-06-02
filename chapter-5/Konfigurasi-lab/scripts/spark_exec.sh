#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

CONTAINER="${SPARK_CONTAINER:-bigdata-spark}"

if ! docker inspect "${CONTAINER}" >/dev/null 2>&1; then
  echo "[ERROR] Kontainer '${CONTAINER}' tidak berjalan. Jalankan: bash start.sh"
  exit 1
fi

if [ "$#" -eq 0 ]; then
  docker exec -it "${CONTAINER}" bash
else
  docker exec "${CONTAINER}" bash -lc "$*"
fi
