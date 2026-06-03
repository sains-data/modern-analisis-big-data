#!/usr/bin/env bash
set -euo pipefail
BUCKET="${MINIO_BUCKET:-banjir-musi}"

if ! docker ps --format '{{.Names}}' | grep -q ch17-ban-minio; then
  echo "[SKIP] MinIO tidak berjalan"
  exit 0
fi

docker exec ch17-ban-mc mc alias set local http://minio:9000 minioadmin minioadmin 2>/dev/null || \
  docker run --rm --network "$(docker inspect ch17-ban-minio --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}')" \
    minio/mc alias set local http://minio:9000 minioadmin minioadmin

NET=$(docker inspect ch17-ban-minio --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}' | head -1)
docker run --rm --network "${NET}" minio/mc mb -p "local/${BUCKET}" 2>/dev/null || true
echo "[OK] Bucket MinIO: ${BUCKET}"
