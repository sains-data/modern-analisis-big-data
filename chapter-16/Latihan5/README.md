# Latihan 5 — Eksplorasi Mandiri & Diskusi Akhir
**Chapter 16** | Estimasi: **30 menit** | **Tahap 5**

## Tujuan

- **DBSCAN** pada hotspot Silver (`ε=0.3°`, `min_pts=10`)
- Verifikasi physical plan spatial join (Tugas C)
- Refleksi arsitektur medallion + orkestrasi Airflow

## Tugas A — DBSCAN

Jalankan sel **Tahap 5** di notebook (atau sesuaikan parameter buku).

Jawab:

1. Berapa kluster terbentuk (exclude noise `-1`)?
2. Kluster dengan **durasi** terpanjang (`durasi_hari`)?
3. Buat pivot **kluster × bulan** (contoh di sel terakhir notebook).

## Tugas B — NDVI (opsional)

Jika tersedia raster Sentinel-2, hitung zonal statistics NDVI per provinsi (`RS_ZonalStats`). Tanpa raster, jelaskan desain pipeline secara naratif.

## Tugas C — Physical plan

Untuk join Tahap 3: strategi apa yang dipilih? Jika `CartesianProduct`, jelaskan penyebab dan perbaikan (index, filter bbox, broadcast).

## Pertanyaan diskusi akhir (buku)

1. Bottleneck pipeline Kafka → Spark → Sedona → dashboard?
2. Model fraud batch vs pola penipuan berubah drastis?
3. Federated query Trino vs ETL salin data?
4. Skenario UAT / interpretasi Gi*?
5. Komponen paling kritis untuk data engineer (Bab 1–16)?

## Siklus medallion

Jika filter `confidence` di Silver terlalu ketat, langkah apa untuk memperbaiki tanpa kehilangan audit trail? (petunjuk: Iceberg time travel — Bab 16 teori)

---

*Chapter 16 selesai.*
