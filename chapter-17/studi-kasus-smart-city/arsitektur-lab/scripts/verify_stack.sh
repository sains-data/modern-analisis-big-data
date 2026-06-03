#!/usr/bin/env bash
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OK=0
c() { [ -f "$1" ] && echo "  [OK] $1" || { echo "  [MISS] $1"; OK=1; }; }
c "${CASE_ROOT}/data/gold/lalu_lintas.parquet"
c "${CASE_ROOT}/data/gold/kualitas_udara.parquet"
c "${CASE_ROOT}/data/gold/gap_tmd_kelurahan.parquet"
c "${CASE_ROOT}/output/output-1-atcs/kondisi_jalan_latest.geojson"
c "${CASE_ROOT}/output/output-2-iqu-hiperlokal/iqu_grid_latest.geojson"
c "${CASE_ROOT}/output/output-3-optimasi-tmd/rekomendasi_tmd_latest.pdf"
c "${CASE_ROOT}/output/output-4-laporan-emisi/emisi_kecamatan_latest.pdf"
exit "${OK}"
