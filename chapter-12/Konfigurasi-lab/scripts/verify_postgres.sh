#!/usr/bin/env bash
set -euo pipefail

echo "=== Tabel di PostgreSQL ==="
docker exec viz-postgres psql -U superset -d analytics -c "\dt" 2>/dev/null || {
  echo "[ERROR] viz-postgres tidak berjalan. Jalankan: bash start-viz.sh"
  exit 1
}

echo ""
docker exec viz-postgres psql -U superset -d analytics -c "
  SELECT 'tren_bulanan' AS tabel, COUNT(*) FROM tren_bulanan
  UNION ALL SELECT 'omzet_kategori', COUNT(*) FROM omzet_kategori
  UNION ALL SELECT 'omzet_kota', COUNT(*) FROM omzet_kota;
"
