#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${ROOT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

mkdir -p "${CASE_ROOT}/data"/{bronze,silver,gold,sumber}
mkdir -p "${CASE_ROOT}/output"/{output-1-level-siaga,output-2-peta-terdampak,output-3-logistik,output-4-after-action}

echo "=== Chapter 17 — Studi Kasus Kebencanaan (Kafka + MinIO) ==="
docker compose up -d

echo "Menunggu Kafka & MinIO..."
sleep 25

bash scripts/prepare_data.sh
bash scripts/init_kafka.sh
bash scripts/init_minio.sh
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh

echo ""
echo "[OK] Pipeline selesai. Artefak di ${CASE_ROOT}/output/"
