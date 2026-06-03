# Katalog Data — Chapter 9

Dataset latihan orkestrasi **100 catatan aktivitas harian** berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), entitas **`catatan_aktivitas`**. Diekspor ke format legacy **`id, nilai, kategori`** untuk pipeline Airflow → Spark → Hive → Atlas.

> **Dua sumber data:** file referensi statis di `data/` (seed 42) vs **`generate_data.py`** yang dijalankan runtime DAG (seed dari tanggal `{{ ds }}`). Keduanya memakai pola ~3% baris invalid; nilai numerik berbeda per run.

## File sumber

| Path | Format | Volume | Entitas kanonik |
|------|--------|--------|-----------------|
| `data/transaksi_harian.csv` | CSV legacy | **100 baris** (+ header) | `catatan_aktivitas` (subset) |
| `data/catatan_aktivitas_harian.csv` | CSV kanonik | 100 baris | `catatan_aktivitas` |

## Schema legacy — `transaksi_harian.csv`

| Kolom lab | Kolom kanonik | Tipe | Catatan |
|-----------|---------------|------|---------|
| `id` | `id_aktivitas` | string | Format `ACT-xxxxxxxx` |
| `nilai` | `nilai_total` | float | Nilai transaksi (Rp) |
| `kategori` | `kelas_layanan` | string | lowercase: elektronik, fashion, … |

## Schema kanonik — `catatan_aktivitas_harian.csv`

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `id_aktivitas` | string | PK aktivitas |
| `id_partisipan` | string | FK partisipan (`PK-0001` …) |
| `tanggal` | date | Tanggal aktivitas |
| `kelas_layanan` | string | Kelas layanan |
| `nilai_total` | float | Nilai agregat |
| `saluran` | string | Saluran transaksi |
| `unit_geografis` | string | Kota / unit geografis |

## Anomali terkontrol (~3%)

Generator `apply_ch09_bad_rows` menambahkan **3 baris invalid** dari 100 (seed 42):

| # | Baris | Masalah | Dampak ETL (`latihan_etl.py`) |
|---|-------|---------|-------------------------------|
| 1 | 1 | `id` kosong | Ditolak (`id != ""`) |
| 2 | 2 | `nilai` negatif | Ditolak (`nilai > 0`) |
| 3 | 3 | `id` kosong | Ditolak |

**Hasil Silver (harapan):** 100 raw → **97 valid** (3 ditolak, tidak ada duplikat ID).

Runtime `generate_data.py` memakai logika serupa (~3% random): ID kosong atau nilai negatif.

## Distribusi data (referensi statis, seed 42)

| Dimensi | Nilai |
|---------|-------|
| Partisipan (pool) | 30 (`PK-0001` … `PK-0030`) |
| Kelas layanan | 6 kategori (elektronik, fashion, kesehatan, makanan, olahraga, otomotif) |
| Baris invalid | 3 (~3%) |
| Baris valid setelah ETL | **97** |

## Volume pipeline HDFS (per run DAG)

| Layer | Path | Volume (harapan) |
|-------|------|------------------|
| Bronze | `/datalake/bronze/latihan/transaksi_YYYYMMDD.csv` | **100 baris** (+ header) |
| Silver | `/datalake/silver/latihan/` | **~97 baris** Parquet |
| Gold | `/datalake/gold/latihan/` | agregat per `kategori` × `tanggal_proses` |

Alur volume:

```
100 CSV Bronze → Spark filter → ~97 Silver → Gold agregasi per kategori
```

## Skrip runtime vs referensi

| Skrip | Peran | Seed |
|-------|-------|------|
| `scripts/lab/generate_data.py` | Dipanggil task Airflow (`{{ ds }} 100`) | `hash(tanggal)` |
| `data/transaksi_harian.csv` | Referensi statis / inspeksi manual | 42 (modul `ch09_orchestration`) |

## Regenerasi data referensi

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch09_orchestration
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
