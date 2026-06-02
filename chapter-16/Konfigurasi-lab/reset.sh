#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
docker compose down -v
rm -rf output/bronze/* output/silver/* output/gold/* output/checkpoints/* 2>/dev/null || true
mkdir -p output/{bronze,silver,gold,checkpoints}
bash start.sh
