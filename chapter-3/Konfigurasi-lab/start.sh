#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

mkdir -p data

echo "=== Chapter 3: menjalankan MinIO + compute ==="
docker compose up -d

echo "=== Membuat bucket Medallion ==="
bash scripts/init_buckets.sh

echo ""
echo "[OK] Stack Chapter 3 aktif."
echo "  MinIO API     : http://localhost:9000"
echo "  MinIO Console : http://localhost:9001  (admin / admin123)"
echo ""
echo "Langkah berikutnya (Latihan 2):"
echo "  docker exec -it bigdata-compute python upload_bronze.py"
