#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

chmod +x scripts/*.sh
docker compose up -d
bash scripts/init_topics.sh

echo "[OK] Stack Chapter 10 (Kafka) aktif."
echo "Kafka UI: http://localhost:${MOD8_KAFKA_UI_PORT:-8080}"
