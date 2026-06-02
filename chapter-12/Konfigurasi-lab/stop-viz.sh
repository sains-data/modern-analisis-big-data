#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"
docker compose -f docker-compose-viz.yml down
echo "[OK] viz-superset & viz-postgres dihentikan."
