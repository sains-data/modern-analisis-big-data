#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"
docker compose -f docker-compose-viz.yml up -d
echo "[INFO] Tunggu ~2–3 menit inisialisasi Superset."
echo "  Superset : http://localhost:8088 (admin/admin)"
echo "  Postgres : localhost:5432 (superset/superset, DB analytics)"
curl -sf -o /dev/null -w "health HTTP %{http_code}\n" http://localhost:8088/health || true
