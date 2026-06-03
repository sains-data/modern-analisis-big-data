#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
docker compose down -v 2>/dev/null || true
CASE_ROOT="$(cd .. && pwd)"
rm -rf "${CASE_ROOT}/data/bronze" "${CASE_ROOT}/data/silver" "${CASE_ROOT}/data/gold"
echo "[OK] Reset medallion."
