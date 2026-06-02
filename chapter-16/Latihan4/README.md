# Latihan 4 — Analisis Statistik Spasial Gi*
**Chapter 16** | Estimasi: **40 menit** | **Tahap 4**

## Tujuan

- Menghitung bobot spasial (band 50 km)
- Menjalankan **Getis-Ord Gi*** (`g_local`, `star=True`)
- Mengklasifikasi Hot/Cold Spot dan menyimpan `output/gold/gi_star/`

## Prasyarat

- [ ] Latihan 1–3 selesai
- [ ] Checkpoint directory: `output/checkpoints/`

## Langkah kerja

Jalankan sel **Tahap 4** di notebook.

> Jika import `sedona.spark.stats` gagal, periksa versi image `apache/sedona:latest` atau jalankan ulang container setelah `docker compose pull`.

## Tabel hasil Gi*

| Klasifikasi | Jumlah titik | % |
|---|---|---|
| Hot Spot 99% | | |
| Hot Spot 95% | | |
| Tidak Signifikan | | |
| Cold Spot 95% | | |

## Refleksi

1. Apakah Hot Spot 99% berarti kebakaran pasti lebih parah?
2. Kapan Moran's I global menjadi prasyarat berguna sebelum Gi*?

---

*Lanjut **Latihan 5 — Eksplorasi Mandiri (Tahap 5)**.*
