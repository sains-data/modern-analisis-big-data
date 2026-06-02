#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${LAB_ROOT}"

echo "=== Docker Compose ==="
docker compose ps

echo ""
echo "=== HTTP checks ==="
curl -sf -o /dev/null -w "Jupyter : %{http_code}\n" http://localhost:8888/login || echo "Jupyter : DOWN"
curl -sf -o /dev/null -w "MinIO  : %{http_code}\n" http://localhost:9020/minio/health/live || echo "MinIO  : DOWN"
curl -sf -o /dev/null -w "Spark  : %{http_code}\n" http://localhost:8081 || echo "Spark UI: DOWN"

echo ""
echo "=== Data files ==="
for f in data/hotspot_sample.csv data/hotspot_sumatera_2024.csv data/batas_kecamatan_sumatera.geoparquet; do
  if [ -f "${f}" ]; then
    echo "  [OK] ${f}"
  else
    echo "  [MISSING] ${f} — jalankan: bash scripts/prepare_data.sh"
  fi
done

echo ""
echo "Buka notebook: http://localhost:8888 (token: sedona123)"
echo "  notebooks/analitik_spasial.ipynb"
