# Panduan Analitik — Pemantauan KEL

## Pemetaan sprint

| Sprint | Fokus |
|---|---|
| 1 | Bronze statis + GPS Silver + bobot \(I_{\text{tekanan}}\) |
| 2 | Streaming alert; KDE; deforestasi Gold |
| 3 | Rute patroli; ekspor EUDR/GFW; retrospective edge |

## 1. Interpolasi GPS (Sprint 1 spike)

- Sampling 4 jam → interpolasi linear untuk gap &gt; 4 jam  
- Validasi: plot trajektori 7 individu  
- File: `analitik/notebooks/gps_interpolasi.ipynb`

## 2. Flatten SMART Patrol

- JSON hierarkis → tabel flat (satu baris per segmen)  
- Kolom: `patrol_id`, `ranger`, `durasi_jam`, `geom`, `tanggal`  
- File: `analitik/batch/ingest_smart_flatten.py`

## 3. Deteksi deforestasi (batch)

**Task:** `deteksi_deforestasi`

- Bandingkan NDVI bulan \(t\) vs \(t-1\)  
- Flag piksel: \(\Delta \text{NDVI} &gt; 0{,}2\)  
- Tulis `gold.deforestasi_aktif`  

Sedona: `RS_MapAlgebra` atau raster diff.

## 4. KDE home range

**Task:** `rekonstruksi_home_range`

- UDAF KDE 2D per `individu_id`  
- Kontur **50%** (core) dan **95%** (extent)  
- `ST_Intersection` dengan poligon konsesi → `% overlap`  

## 5. Streaming — alert konflik gajah

**Topik:** `gps.collar.leuser` → `output.alert.konflik`

- `ST_KNN` permukiman terdekat (k=1)  
- Filter `ST_Distance` &lt; 2000 m (UTM EPSG:32647)  
- Pesan: individu, jarak, arah, rekomendasi  

File buku: `output_01_alert_konflik.py` → `analitik/streaming/`.

## 6. Gi* hotspot konflik

- Input: `gold.konflik_georeferensi` historis  
- Korelasi dengan pergerakan GPS terkini  
- Sedona `g_local` (Bab 16)  

## 7. Coverage gap & rute patroli

**Task:** `coverage_gap`

- Grid 1 km² dengan \(I_{\text{tekanan}}\) tinggi + rendah \(R\)  
- **Least-cost path** / optimasi rute harian untuk ranger  
- Export **GPX** (Sprint 3 DoD)  

## 8. Random Forest (opsional)

Prediksi probabilitas deforestasi bulan depan dari fitur historis.

## Product backlog

| Sprint | User story | Peran |
|---|---|---|
| 1 | Bronze statis lengkap | Data Engineer |
| 1 | GPS interpolasi, trajektori OK | Data Scientist |
| 1 | Bobot indeks tekanan | Product Owner |
| 2 | Alert &lt; 5 mnt | Data Engineer |
| 2 | KDE + overlap konsesi | Data Scientist |
| 2 | Peta deforestasi Gold | Data Scientist |
| 3 | Dashboard rute + GPX | BI Developer |
| 3 | PDF/GeoJSON format GFW | BI Developer |
| 3 | Retrospective edge | Scrum Master |

## Rujukan kode buku

- `output_01_alert_konflik.py`  
- Output 2–4 (deforestasi, EUDR, basis pergerakan) — cuplikan di `chapter-17.tex`  
