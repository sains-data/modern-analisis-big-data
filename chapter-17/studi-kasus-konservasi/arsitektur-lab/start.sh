#!/usr/bin/env bash
cd "$(dirname "${BASH_SOURCE[0]}")"
chmod +x *.sh scripts/*.sh 2>/dev/null || true
docker compose up -d 2>/dev/null || true
sleep 15
bash scripts/prepare_data.sh
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh
