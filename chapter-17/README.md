# Chapter 17 — Studi Kasus Sistem Big Data Multimodal di Sumatera

Bab ini menyajikan **studi kasus berbasis masalah nyata** (PBL + Scrum 3 sprint), bukan lab terpandu seperti Bab 3–16. Implementasi teknis dan skrip praktikum akan dilengkapi di **Lampiran**; folder di repositori ini berisi **kerangka dokumentasi** per studi kasus.

## Studi kasus di Bab 17

| Folder | Domain | Judul (ringkas) |
|---|---|---|
| [studi-kasus-kebencanaan](studi-kasus-kebencanaan/README.md) | Kebencanaan | Peringatan dini banjir DAS Musi |
| [studi-kasus-lingkungan](studi-kasus-lingkungan/README.md) | Lingkungan | Monitoring karhutla & akuntabilitas konsesi Riau |
| [studi-kasus-kesehatan](studi-kasus-kesehatan/README.md) | Kesehatan | Analitik stunting & prioritas desa Sumatera Utara |
| [studi-kasus-konservasi](studi-kasus-konservasi/README.md) | Konservasi | Pemantauan KEL, edge ML, konflik gajah–manusia |
| [studi-kasus-smart-city](studi-kasus-smart-city/README.md) | Smart city | ATCS, IQU, TMD & emisi — Kota Medan |
| [studi-kasus-edukasi](studi-kasus-edukasi/README.md) | Edukasi | Big data manajemen akademik & learning analytics PT |

Saat ini tersedia: **enam studi kasus** (dokumentasi lengkap; implementasi teknis di Lampiran).

## Struktur standar per studi kasus

```
studi-kasus-<domain>/
├── README.md                 # Halaman utama studi kasus
├── arsitektur-lab/           # Lingkungan Docker, Kafka, lakehouse
├── data/                     # Katalog sumber data + medallion Bronze/Silver/Gold
├── analitik/                 # Pipeline streaming/batch, model, query
└── output/                   # Deliverable ke pemangku kebijakan
```

## Metodologi (ringkas)

- **3 sprint** × 1 minggu: (1) data & Bronze, (2) pipeline + analitik, (3) output + retrospective  
- Peran: Product Owner, Data Engineer, Data Scientist, BI Developer, Scrum Master  

Rujukan teori: `sesi-praktikum/chapter-17.tex` §17.0–§17.1.

## Prasyarat kompetensi

Bab 4–16 (HDFS/Spark, Kafka, lakehouse, Sedona, visualisasi) sebagai fondasi teknis sebelum mengerjakan studi kasus.
