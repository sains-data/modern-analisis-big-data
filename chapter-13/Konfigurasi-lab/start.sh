#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"
docker compose -f docker-compose-monitoring.yml up -d
echo "[INFO] Tunggu ~30 detik, lalu: bash scripts/verify_stack.sh"
