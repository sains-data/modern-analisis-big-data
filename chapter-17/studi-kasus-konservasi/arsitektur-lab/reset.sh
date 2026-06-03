#!/usr/bin/env bash
cd "$(dirname "${BASH_SOURCE[0]}")"
docker compose down -v 2>/dev/null || true
rm -rf "$(cd .. && pwd)"/data/{bronze,silver,gold}
echo "[OK] Reset."
