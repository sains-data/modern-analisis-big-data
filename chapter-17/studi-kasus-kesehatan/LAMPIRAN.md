# Lampiran Praktikum — Studi Kasus Kesehatan

## Rencana isi Lampiran

| Komponen | Target folder |
|---|---|
| Docker: Kafka, Airflow, OSRM, MinIO | `arsitektur-lab/` |
| Sample e-PPGBM, LMS WHO, batas desa Sumut | `data/sumber/` |
| DAG `stunting_sumut_monthly` (tgl 5) | `analitik/batch/` |
| `output_03_alert_kader.py` streaming | `analitik/streaming/` |
| Extract OSM Sumut + `osrm-extract` | `arsitektur-lab/osrm/` |
| Export Superset TPPS | `output/output-2-dashboard-tpps/` |

## Hambatan (antisipasi Sprint 1)

1. **Spike mapping kolom** e-PPGBM antar versi update.  
2. **OSRM extract** OSM Sumut (~500 MB) — 30–60 menit, jadwalkan hari pertama Sprint 1.

## Versi

| Versi | Tanggal | Catatan |
|---|---|---|
| 0.1 | 2026-05 | Kerangka dokumentasi |
