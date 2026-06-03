# Chapter 8 — Struktur & Penyimpanan Big Data

Praktik **Hive, HBase, Parquet/ORC** pada klaster **Hadoop + Spark + Hive + HBase** (Docker): Bronze → Silver → SQL → profil NoSQL.

Dataset **`transaksi.csv`** (500 baris) + **`pelanggan.csv`** (50 baris) dihasilkan generator sintesis [`synthetic-data/`](../synthetic-data/README.md) — entitas `catatan_aktivitas` dan `entitas_partisipan` **tanpa anomali terkontrol** (fokus skala & penyimpanan).

## Alur cepat

```bash
cd sesi-praktikum/chapter-8/Konfigurasi-lab
cp .env.example .env
# unduh 6 tarball ke vendor/bigdata-spark/
bash build.sh && bash start.sh
bash scripts/setup_datalake_bronze.sh
bash scripts/run_hive_etl.sh
bash scripts/run_spark_ke_hbase.sh
bash scripts/run_format_benchmark.sh
bash stop.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)** · **[KATALOG-DATA.md](Konfigurasi-lab/KATALOG-DATA.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Setup klaster & Bronze HDFS |
| [Latihan 2](Latihan2/README.md) | `hive_etl.py` — Spark + Hive |
| [Latihan 3](Latihan3/README.md) | `spark_ke_hbase.py` — HBase |
| [Latihan 4](Latihan4/README.md) | `format_benchmark.py` |
| [Latihan 5](Latihan5/README.md) | ORC Hive & row key HBase |

## Data latihan

| File | Volume Bronze | Catatan |
|------|---------------|---------|
| `transaksi.csv` | **500 baris** | Silver tetap 500 (ID unik) |
| `pelanggan.csv` | **50 baris** | Dimensi referensi |
| HBase `profil_pelanggan` | **49 profil** | PLG-0046 tanpa transaksi |

Schema legacy Bab 8: `total_nilai` (bukan `jumlah`×`kuantitas`); ID format `TRX-00001`, `PLG-0001`.

## File eksekusi

| Path | Fungsi |
|---|---|
| `data/transaksi.csv`, `pelanggan.csv` | Input Bronze (legacy) |
| `data/catatan_aktivitas.csv`, `entitas_partisipan.csv` | Schema kanonik |
| `KATALOG-DATA.md` | Mapping, distribusi, volume harapan |
| `app/hive_etl.py` | Bronze → Silver + Hive |
| `app/spark_ke_hbase.py` | Silver → HBase profil |
