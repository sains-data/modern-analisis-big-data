#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_ROOT="$(cd "${ROOT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"
mkdir -p "${CASE_ROOT}/data"/{bronze,silver,gold,sumber}
mkdir -p "${CASE_ROOT}/output"/{output-1-peta-risiko,output-2-akuntabilitas-konsesi,output-3-dashboard-ispu-ispa,output-4-emisi-karbon}
docker compose up -d 2>/dev/null || true
sleep 20
bash scripts/prepare_data.sh
bash scripts/init_kafka.sh 2>/dev/null || true
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh
