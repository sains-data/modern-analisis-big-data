#!/usr/bin/env bash
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OK=0
c() { [ -f "$1" ] && echo "  [OK] $1" || { echo "  [MISS] $1"; OK=1; }; }
echo "=== Gold & Output ==="
c "${CASE_ROOT}/data/gold/indeks_risiko_karhutla.parquet"
c "${CASE_ROOT}/data/gold/hotspot_konsesi_agg.parquet"
c "${CASE_ROOT}/data/gold/korelasi_ispu_ispa.parquet"
c "${CASE_ROOT}/output/output-1-peta-risiko/peta_risiko_latest.geojson"
c "${CASE_ROOT}/output/output-2-akuntabilitas-konsesi/akuntabilitas_latest.csv"
c "${CASE_ROOT}/output/output-3-dashboard-ispu-ispa/korelasi_ringkasan.csv"
c "${CASE_ROOT}/output/output-4-emisi-karbon/emisi_per_konsesi_latest.csv"
exit "${OK}"
