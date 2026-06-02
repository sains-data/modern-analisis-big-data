# Panduan Analitik — Kota Medan

## Pemetaan sprint

| Sprint | Fokus |
|---|---|
| 1 | Bronze + Kafka producers + definisi ambang |
| 2 | 3 streaming queries + batch gap & korelasi |
| 3 | Dashboard + ekspor + jawaban pertanyaan klien |

## 1. Estimasi kecepatan ruas (streaming Q1)

- Input: `probe.kendaraan`, `gps.tmd`  
- Map-match: `ST_DWithin` 50 m (EPSG:32647)  
- Window sliding **5 menit**; agregat tiap **15 detik** ke `output.kondisi.jalan`  
- `MODE()` level LANCAR/PADAT/MACET  
- File: `analitik/streaming/probe_kecepatan_ruas.py`  
- SQL referensi: cuplikan buku `probe_mapped` CTE  

## 2. Interpolasi PM₂.₅ IDW (streaming Q2)

- Input: `sensor.udara` + angin BMKG  
- Grid **500 m**; refresh **10 menit**  
- Bobot angin pada IDW  
- File: `analitik/streaming/idw_pm25_grid.py`  

## 3. Korelasi PM₂.₅–volume (streaming Q3)

- Join stream kondisi jalan × grid udara  
- Tumbling window **1 jam**; simpan Pearson per ruas  
- Window analisis buku: **4 jam** di Gold `korelasi_pm25`  
- File: `analitik/streaming/korelasi_pm25_volume.py`  

## 4. Batch — pola historis & LSTM

**Task:** `pola_historis` — rekap jam × ruas untuk training LSTM prediksi kemacetan (opsional).

## 5. Batch — estimasi emisi

**Task:** `estimasi_emisi` — volume × emission factor per tipe kendaraan (IPCC).

## 6. Batch — gap analysis TMD

**Task:** `gap_tmd`

- Permintaan estimasi per kelurahan  
- Coverage halte dalam radius **400 m**  
- Flag coverage **&lt; 30%**  
- Output: `gold.gap_tmd_kelurahan` terurut  

## 7. Batch — kecelakaan

Join titik kecelakaan × kondisi jalan × cuaca waktu kejadian; DBSCAN klaster (opsional).

## 8. Analitik spasial — Gi*

Hotspot kemacetan per ruas per jam (probe historis).

## Product backlog

| Sprint | User story | Peran |
|---|---|---|
| 1 | Bronze + skema valid | Data Engineer |
| 1 | 5 topik Kafka + producer | Data Engineer |
| 1 | Ambang kemacetan & ISPU | Product Owner |
| 2 | Kecepatan ruas lag ≤10, 15 dtk | Data Engineer |
| 2 | Grid PM₂.₅ lengkap | Data Scientist |
| 2 | Korelasi Gold hari ini | Data Scientist |
| 2 | Gap TMD kelurahan | Data Scientist |
| 3 | Dashboard ATCS + filter kecamatan | BI Developer |
| 3 | PDF/CSV emisi bulanan | BI Developer |
| 3 | Sprint Review 2 pertanyaan klien | Scrum Master |

## Pertanyaan klien (Sprint Review)

Contoh buku:

- Berapa lama rekomendasi rute alternatif setelah macet?  
- Apakah kebijakan ganjil-genap efektif menurunkan PM₂.₅?  

Jawab dengan bukti dari Gold layer.

## Rujukan kode buku

- `output_01_atcs_dashboard.py` — ATCS + rute alternatif  
- Output 2–4 (IQU, optimasi TMD, emisi) — `chapter-17.tex`  
