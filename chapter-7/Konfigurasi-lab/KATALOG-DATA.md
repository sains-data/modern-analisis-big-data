# Katalog Data — Chapter 7

Dataset latihan **identik dengan Bab 6** — generator sintesis Gaussian Copula (`synthetic-data/`), entitas `catatan_aktivitas` + `entitas_partisipan`. Perbedaan Bab 7: pipeline **Medallion lokal** (PyArrow / DuckDB / Polars), bukan HDFS + Spark.

## File sumber

| Path | Format | Volume | Entitas kanonik |
|------|--------|--------|-----------------|
| `data/transaksi.csv` | CSV legacy | **16 baris** (+ header) | `catatan_aktivitas` |
| `data/pelanggan.csv` | CSV legacy | **7 baris** (+ header) | `entitas_partisipan` |
| `data/catatan_aktivitas.csv` | CSV kanonik | 16 baris | `catatan_aktivitas` |
| `data/entitas_partisipan.csv` | CSV kanonik | 7 baris | `entitas_partisipan` |

Mapping kolom legacy ↔ kanonik: lihat [Bab 6 KATALOG-DATA.md](../../chapter-6/Konfigurasi-lab/KATALOG-DATA.md).

## Anomali terkontrol (sama Bab 6)

| ID | Masalah |
|----|---------|
| TRX001 | Duplikat penuh |
| TRX011 | `id_pelanggan` kosong |
| TRX012 | `jumlah` negatif |
| TRX013 | `kuantitas` = 0 |
| TRX014 | `kota` lowercase → `INITCAP` di Silver |

## Volume pipeline lokal (harapan)

| Layer | Path lokal | Volume |
|-------|------------|--------|
| CSV mentah | `data/transaksi.csv` | 16 baris |
| Bronze | `datalake/bronze/transaksi/batch_001.parquet` | **15 baris** (dedup di Bronze) |
| Silver | `datalake/silver/transaksi/` | **12 baris** valid |
| Gold | `datalake/gold/*.parquet` | agregat dari 12 baris |

Alur volume:

```
16 CSV → Bronze dedup 15 → Silver validasi 12 → Gold agregasi
```

Perbandingan dengan Bab 6 (Spark):

| Tahap | Bab 6 (HDFS) | Bab 7 (lokal) |
|-------|--------------|---------------|
| Dedup | Silver (`dropDuplicates`) | **Bronze** (`group_by`) |
| Validasi | Silver (filter) | Silver (SQL WHERE) |
| Baris Silver akhir | 12 | 12 |

## Path datalake lokal

```
datalake/
├── bronze/transaksi/batch_001.parquet
├── silver/transaksi/tahun=YYYY/bulan=M/*.parquet
└── gold/
    ├── per_kategori.parquet
    ├── per_segmen.parquet
    └── top_produk.parquet
```

## Regenerasi data

Dataset Bab 7 disalin dari export Bab 6 (`ch07_medallion_local`):

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch06_medallion
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
