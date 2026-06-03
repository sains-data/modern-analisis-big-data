#!/usr/bin/env bash
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OK=0
c() { [ -f "$1" ] && echo "  [OK] $1" || { echo "  [MISS] $1"; OK=1; }; }
c "${CASE_ROOT}/data/gold/dataset_model_risiko.parquet"
c "${CASE_ROOT}/data/gold/profil_risiko_mahasiswa.parquet"
c "${CASE_ROOT}/data/gold/skill_gap_kurikulum.parquet"
c "${CASE_ROOT}/output/output-1-early-warning-pa/notifikasi_pa_latest.csv"
c "${CASE_ROOT}/output/output-2-utilisasi-ruang/utilisasi_ruang_latest.csv"
c "${CASE_ROOT}/output/output-3-skill-gap/laporan_skill_gap_latest.pdf"
c "${CASE_ROOT}/output/output-4-banpt/indikator_banpt_latest.pdf"
exit "${OK}"
