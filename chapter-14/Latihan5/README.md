# Latihan 5 — Refleksi Big Data End-to-End
**Chapter 14** | Estimasi: **25 menit** | **Tahap 5**

## Tujuan

- Mengidentifikasi **anti-pattern** pada dashboard yang dibuat
- Merencanakan iterasi berikut (siklus hidup 6 langkah)
- Menjawab pertanyaan diskusi final buku

## Tugas A — Anti-pattern

Tinjau dashboard `Analitik E-Commerce 2024`. Catat minimal **3** anti-pattern (lihat Tabel anti-pattern Bab 14) dan perbaikan di Superset:

| Anti-pattern | Perbaikan konkret |
|---|---|
| 1. | |
| 2. | |
| 3. | |

## Tugas B — Siklus hidup dashboard

| Langkah siklus | Rencana iterasi Anda |
|---|---|
| Pertanyaan bisnis baru | |
| Metrik / KPI baru | |
| Perubahan chart | |
| Uji & UAT | |
| Publikasi & refresh | |
| Monitoring penggunaan | |

## Pertanyaan diskusi (buku §14.5)

Jawab singkat (5–8 kalimat per poin):

1. **Bottleneck** pipeline Kafka → Spark → DuckDB/Trino → Superset — bagaimana mengukur dan mengatasinya?
2. Model fraud **batch** vs pola penipuan yang berubah drastis — modifikasi arsitektur?
3. **Federated query** Trino vs ETL salin MySQL ke HDFS — keunggulan dan keterbatasan?
4. Dari UAT Latihan 4 — implikasi desain dashboard?
5. Komponen arsitektur big data paling kritis untuk **data engineer** — berdasarkan praktikum Bab 1–14?

## Ringkasan lab

Setelah latihan ini Anda telah menjalankan:

```
Spark (Silver → Gold Parquet)
    → DuckDB (analitik OLAP)
    → PostgreSQL (serving)
    → Superset (dashboard interaktif)
```

---

*Chapter 14 selesai. Kembali ke materi teori Bab 14 §14.6 (Ringkasan) jika diperlukan.*
