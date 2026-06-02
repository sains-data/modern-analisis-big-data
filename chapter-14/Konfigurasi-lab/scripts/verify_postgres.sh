#!/usr/bin/env bash
set -euo pipefail

echo "=== Tabel di PostgreSQL (Ch.14) ==="
docker exec viz-postgres psql -U superset -d analytics -c "\dt" 2>/dev/null || {
  echo "[ERROR] viz-postgres tidak berjalan."
  echo "  cd sesi-praktikum/chapter-12/Konfigurasi-lab && bash start-viz.sh"
  exit 1
}

docker exec viz-postgres psql -U superset -d analytics -c "
  SELECT 'tren_bulanan' AS tabel, COUNT(*) FROM tren_bulanan
  UNION ALL SELECT 'omzet_kategori', COUNT(*) FROM omzet_kategori
  UNION ALL SELECT 'omzet_kota', COUNT(*) FROM omzet_kota
  UNION ALL SELECT 'segmentasi_rfm', COUNT(*) FROM segmentasi_rfm;
"
