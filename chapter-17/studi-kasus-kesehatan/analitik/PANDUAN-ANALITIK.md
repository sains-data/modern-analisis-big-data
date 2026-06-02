# Panduan Analitik — Stunting Sumatera Utara

## Pemetaan sprint

| Sprint | Fokus | Artefak |
|---|---|---|
| 1 | Bronze + LMS + dimensi indeks | `silver.who_lms_standar`, dokumen bobot |
| 2 | Streaming alert + prevalensi + OSRM | `gold.*`, `analitik/streaming/` |
| 2 | DBSCAN / Moran's I (opsional) | `analitik/notebooks/` |
| 3 | Export TPPS & prioritas desa | [../output/](../output/) |

## 1. Z-score WHO (batch)

**Task:** `kalkulasi_zscore`

- Join `data_balita` × `who_lms_standar` pada `usia_bulan`, `jenis_kelamin`  
- Hitung z-score TB/U (formula LMS di buku)  
- Klasifikasi: stunting jika z &lt; −2  

File: `analitik/sql/zscore_prevalensi_desa.sql` (pola cuplikan buku).

## 2. Agregasi prevalensi per desa

**Task:** `agregasi_desa`

```sql
-- Ringkas: prev_pct = 100 * n_stunting / n_balita
-- HAVING COUNT(*) >= 10
```

Output: `gold.prevalensi_stunting`.

## 3. Isokron aksesibilitas (OSRM)

**Task:** `join_aksesibilitas`

- Centroid desa → Puskesmas terdekat via OSRM  
- Kategori: ≤30, ≤60, ≤90, &gt;90 menit  
- **Blank zone:** &gt; 60 menit (standar Kemkes)  

File rencana: `analitik/batch/osrm_waktu_tempuh.py`

## 4. Indeks risiko multifaktor

**Task:** `indeks_risiko`

- Gabung: prevalensi, sanitasi, kemiskinan, akses Puskesmas, air bersih  
- Normalisasi + bobot (disetujui PO) → `indeks_total`  
- Rank top 50 per kabupaten (Output 1)  

## 5. Streaming — alert kader

**Topik:** `balita.upload.sumut` → `output.alert.kader`

| Level | Pemicu (ringkas) | Respons |
|---|---|---|
| MERAH | ΔBB &gt; 200 g/bulan atau z TB/U &lt; −3 | Kunjungan 24 jam, rujuk Puskesmas |
| ORANYE | Turun z &gt; 0,5 SD atau absen 2 bulan | Kunjungan 72 jam |
| KUNING | z antara −2 dan −1,5 | Pemantauan + PMT |

Validasi stream: BB 1–50 kg, TB 30–130 cm, usia 0–60 bulan.

File buku: `output_03_alert_kader.py` → `analitik/streaming/`.

## 6. Analitik spasial (pertanyaan 1–2)

| Metode | Tujuan |
|---|---|
| **DBSCAN** | Klaster desa prevalensi tinggi berulang |
| **Moran's I** | Autokorelasi spasial dampak/program |
| **Regresi spasial** | Faktor dominan (sanitasi, kemiskinan, akses) |
| **XGBoost** | Prediksi risiko 3 bulan (opsional) |

## 7. Deteksi desa KRONIS

Desa **3 bulan berturut** di top 50 kabupaten → flag `KRONIS` (masalah struktural).

Logika: `output_01_prioritas_desa.py` (buku).

## Product backlog

| Sprint | User story | Peran |
|---|---|---|
| 1 | Bronze lengkap, non-null kunci | Data Engineer |
| 1 | 5 dimensi indeks disetujui | Product Owner |
| 1 | LMS join + validasi 10 sampel | Data Scientist |
| 2 | Alert &lt; 30 dtk, lag &lt; 5 | Data Engineer |
| 2 | Prevalensi + isokron lengkap | Data Scientist |
| 3 | Dashboard TPPS + PDF | BI Developer |
| 3 | Peta isokron GeoJSON 3 zona | BI Developer |
| 3 | Retrospective | Scrum Master |

## Rujukan kode buku

- `output_01_prioritas_desa.py`  
- `output_02_dashboard_tpps.py`  
- `output_03_alert_kader.py`  
- `output_04_*` — basis bukti tenaga kesehatan (triwulanan)  

Implementasi di Lampiran Bab 17.
