#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

mkdir -p output/{bronze,silver,gold,checkpoints} data notebooks

echo "=== Chapter 16: Spark + Sedona Jupyter + MinIO ==="
docker compose up -d

echo "Menunggu layanan (30–90 detik, image Sedona ~3 GB pertama kali)..."
sleep 30

bash scripts/prepare_data.sh
bash scripts/init_minio.sh
bash scripts/verify_stack.sh

echo ""
echo "[OK] Lab spasial aktif."
