#!/usr/bin/env bash
# Unduh FIRMS NASA (opsional) — butuh API key di .env
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

MAP_KEY="${FIRMS_MAP_KEY:-YOUR_FIRMS_API_KEY}"
OUTPUT="${LAB_ROOT}/data/hotspot_sumatera_2024.csv"

if [ "${MAP_KEY}" = "YOUR_FIRMS_API_KEY" ]; then
  echo "[PERINGATAN] FIRMS_MAP_KEY belum diisi di .env"
  echo "  Gunakan data sintetis: bash scripts/prepare_data.sh"
  echo "  Daftar API: https://firms.modaps.eosdis.nasa.gov/api/map_key/"
  exit 1
fi

mkdir -p "${LAB_ROOT}/data"
echo "[1/2] Mengunduh MODIS NRT..."
curl -fsSL -o "${OUTPUT}.tmp" \
  "https://firms.modaps.eosdis.nasa.gov/api/area/csv/${MAP_KEY}/MODIS_NRT/world/10"

echo "[2/2] Filter bbox Sumatera..."
python3 - <<PYEOF
import pandas as pd
from pathlib import Path
out = Path("${OUTPUT}")
df = pd.read_csv("${OUTPUT}.tmp")
df = df[
    (df["longitude"] >= 95.0) & (df["longitude"] <= 109.0) &
    (df["latitude"] >= -6.0) & (df["latitude"] <= 6.0)
]
df.to_csv(out, index=False)
print(f"[OK] {len(df):,} titik → {out}")
PYEOF
rm -f "${OUTPUT}.tmp"
