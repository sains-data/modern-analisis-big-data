#!/usr/bin/env bash
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OK=0
c() { [ -f "$1" ] && echo "  [OK] $1" || { echo "  [MISS] $1"; OK=1; }; }
c "${CASE_ROOT}/data/gold/deforestasi_aktif.parquet"
c "${CASE_ROOT}/data/gold/tekanan_kawasan.parquet"
c "${CASE_ROOT}/data/gold/home_range_kde.parquet"
c "${CASE_ROOT}/output/output-1-alert-konflik/alert_konflik_latest.jsonl"
c "${CASE_ROOT}/output/output-2-bukti-deforestasi/deforestasi_latest.geojson"
c "${CASE_ROOT}/output/output-3-laporan-kel-eudr/laporan_kel_latest.pdf"
c "${CASE_ROOT}/output/output-4-basis-pergerakan/home_range_latest.geojson"
exit "${OK}"
