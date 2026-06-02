#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${LAB_ROOT}"

if ! docker inspect ch16-minio >/dev/null 2>&1; then
  echo "[ERROR] ch16-minio tidak berjalan. Jalankan: bash start.sh"
  exit 1
fi

SAMPLE="${LAB_ROOT}/data/hotspot_sample.csv"
if [ ! -f "${SAMPLE}" ]; then
  bash "${SCRIPT_DIR}/prepare_data.sh"
fi

echo "=== Inisialisasi bucket geodata di MinIO ==="
docker compose exec -T mc mc alias set local http://minio:9000 minioadmin minioadmin --api S3v4
docker compose exec -T mc mc mb local/geodata --ignore-existing
docker compose cp "${SAMPLE}" mc:/tmp/hotspot_sample.csv
docker compose exec -T mc mc cp /tmp/hotspot_sample.csv local/geodata/raw/hotspot_sample.csv
docker compose exec -T mc mc ls local/geodata/raw/

echo ""
echo "[OK] MinIO Console: http://localhost:9021 (minioadmin / minioadmin)"
