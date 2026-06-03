#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OK=0
check() { [ -f "$1" ] && echo "  [OK] $1" || { echo "  [MISS] $1"; OK=1; }; }

echo "=== Gold & Output ==="
check "${CASE_ROOT}/data/gold/prevalensi_stunting.parquet"
check "${CASE_ROOT}/data/gold/indeks_risiko.parquet"
check "${CASE_ROOT}/data/gold/prioritas_desa_bulanan.parquet"
check "${CASE_ROOT}/output/output-1-prioritas-desa/prioritas_desa_latest.csv"
check "${CASE_ROOT}/output/output-2-dashboard-tpps/stunting_kab_bulan_ini.geojson"
check "${CASE_ROOT}/output/output-3-alert-kader/alert_log_latest.jsonl"
check "${CASE_ROOT}/output/output-4-bukti-nakes/laporan_nakes_ringkasan.pdf"
exit "${OK}"
