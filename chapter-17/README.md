# Chapter 17 — Studi Kasus Sistem Big Data Multimodal di Sumatera

Bab ini menyajikan **studi kasus berbasis masalah nyata** (PBL + Scrum 3 sprint), bukan lab terpandu seperti Bab 3–16. Implementasi teknis dan skrip praktikum akan dilengkapi di **Lampiran**; folder di repositori ini berisi **kerangka dokumentasi** per studi kasus.

## Studi kasus di Bab 17

| Folder | Domain | Judul (ringkas) |
|---|---|---|
| [studi-kasus-kebencanaan](studi-kasus-kebencanaan/README.md) | Kebencanaan | Peringatan dini banjir DAS Musi — **[instruksi eksperimen](studi-kasus-kebencanaan/eksperimen/README.md)** ✅ kode |
| [studi-kasus-lingkungan](studi-kasus-lingkungan/README.md) | Lingkungan | Karhutla Riau — **[eksperimen](studi-kasus-lingkungan/eksperimen/README.md)** ✅ kode |
| [studi-kasus-kesehatan](studi-kasus-kesehatan/README.md) | Kesehatan | Stunting Sumut — **[instruksi eksperimen](studi-kasus-kesehatan/eksperimen/README.md)** ✅ kode |
| [studi-kasus-konservasi](studi-kasus-konservasi/README.md) | Konservasi | KEL Leuser — **[eksperimen](studi-kasus-konservasi/eksperimen/README.md)** ✅ kode |
| [studi-kasus-smart-city](studi-kasus-smart-city/README.md) | Smart city | ATCS Medan — **[eksperimen](studi-kasus-smart-city/eksperimen/README.md)** ✅ kode |
| [studi-kasus-edukasi](studi-kasus-edukasi/README.md) | Edukasi | Big data PT — **[eksperimen](studi-kasus-edukasi/eksperimen/README.md)** ✅ kode |

Saat ini tersedia: **enam studi kasus** lengkap dengan kode lab.

## Struktur standar per studi kasus

```
studi-kasus-<domain>/
├── README.md                 # Halaman utama studi kasus
├── eksperimen/               # Instruksi praktikum (mulai di sini) — semua studi kasus ✅
├── arsitektur-lab/           # Eksekusi kode / Docker / Kafka
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
