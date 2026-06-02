#!/usr/bin/env bash
set -euo pipefail

echo "=== Menghentikan kontainer bigdata-spark ==="
docker compose down
echo "[OK] Kontainer dihentikan. Data HDFS tetap di volume Docker."
echo "Hapus volume HDFS: docker compose down -v"
