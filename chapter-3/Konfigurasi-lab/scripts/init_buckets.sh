#!/usr/bin/env bash
# Membuat bucket Medallion di MinIO (bronze, silver, gold).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

MINIO_USER="${MINIO_ROOT_USER:-admin}"
MINIO_PASS="${MINIO_ROOT_PASSWORD:-admin123}"

echo "Menunggu MinIO siap..."
for i in $(seq 1 30); do
  if docker exec bigdata-minio curl -sf http://localhost:9000/minio/health/live >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

docker exec bigdata-mc mc alias set local http://minio:9000 "${MINIO_USER}" "${MINIO_PASS}" >/dev/null

for bucket in bronze silver gold; do
  docker exec bigdata-mc mc mb --ignore-existing "local/${bucket}"
  echo "  [OK] bucket: ${bucket}"
done

docker exec bigdata-mc mc ls local/
