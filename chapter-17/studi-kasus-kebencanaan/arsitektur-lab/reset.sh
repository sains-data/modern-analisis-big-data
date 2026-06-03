#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
docker compose down -v
CASE_ROOT="$(cd .. && pwd)"
rm -rf "${CASE_ROOT}/data/bronze" "${CASE_ROOT}/data/silver" "${CASE_ROOT}/data/gold"
rm -f "${CASE_ROOT}/output"/output-*/*.{json,geojson,pdf,txt,md} 2>/dev/null || true
echo "[OK] Volume Docker dan layer medallion di-reset."
