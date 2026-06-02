# Studi Kasus Kesehatan — Analitik Stunting Sumatera Utara

**Bab 17 · Studi Kasus 3** | Provinsi Sumatera Utara | Problem-based learning + Scrum (3 sprint)

## Ringkasan skenario

**Dinkes Provinsi Sumatera Utara** membutuhkan sistem untuk menjawab: *desa mana yang harus diprioritaskan?* Data tersebar di e-PPGBM, DTKS, STBM, Fasyankes—format dan hak akses berbeda. Target nasional: prevalensi stunting dari **30,1%** menuju **&lt;14%** (2024).

## Tiga pertanyaan analitik

| # | Pertanyaan | Teknik inti |
|---|---|---|
| 1 | **Di mana** klaster desa stunting berulang? | DBSCAN spasial, Moran's I |
| 2 | **Faktor apa** paling dominan antardesa? | Regresi spasial multidimensi |
| 3 | **Desa mana** sulit dijangkau Puskesmas? | Isokron OSRM/OSM (30/60/90 menit) |

## Navigasi folder

| Folder | Isi | Dokumen detail |
|---|---|---|
| [arsitektur-lab](arsitektur-lab/README.md) | Kafka, Airflow, OSRM, MinIO/Iceberg | [PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md) |
| [data](data/README.md) | Katalog Tabel 17.10 + medallion | [KATALOG-DATA.md](data/KATALOG-DATA.md) |
| [analitik](analitik/README.md) | Batch bulanan, alert streaming, z-score WHO | [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) |
| [output](output/README.md) | Empat artefak ke Dinkes/TPPS/kader | [PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md) |

## Product backlog (ringkas)

| Sprint | Fokus | Definisi selesai (contoh) |
|---|---|---|
| **1** | Bronze + LMS WHO + 5 dimensi indeks | Skema valid; z-score 10 sampel manual |
| **2** | Streaming alert &lt;30 dtk; prevalensi desa; isokron OSRM | Semua desa punya waktu tempuh |
| **3** | Dashboard TPPS + peta prioritas + retro | Demo Dinkes; ekspor PDF |

Detail: [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) · `chapter-17.tex` §Studi Kasus Kesehatan.

## Lampiran praktikum

Rencana pemetaan: [LAMPIRAN.md](LAMPIRAN.md).

## Status repositori

| Komponen | Status |
|---|---|
| Dokumentasi Markdown | ✅ |
| Implementasi teknis | 🔜 Lampiran |
