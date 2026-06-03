# Konfigurasi Lab Chapter 14

Pipeline **end-to-end e-commerce**: Spark (Silver → Gold) → DuckDB → PostgreSQL → Superset.

Dataset referensi **15.000 transaksi** + 5 tabel Gold CSV dari generator [`synthetic-data/`](../../synthetic-data/README.md), modul `ch14_e2e`. Detail: **[KATALOG-DATA.md](KATALOG-DATA.md)**.

> Runtime: `seed_silver.py` + `pipeline_ecommerce.py` → HDFS Parquet. File `data/*.csv` = referensi statis copula.

## Komponen

| Layer | Teknologi | Output |
|---|---|---|
| Silver | Spark `seed_silver.py` | `hdfs:///datalake/silver/transaksi/` |
| Gold | Spark `pipeline_ecommerce.py` | `tren_bulanan`, `omzet_kategori`, `segmentasi_rfm`, `omzet_kota` (Parquet) |
| Analitik | DuckDB lokal | `app/analitik_duckdb.py` |
| Serving | Spark JDBC | PostgreSQL `viz-postgres` |
| Viz | Superset (Ch.12) | http://localhost:8088 |

## Struktur

```
Konfigurasi-lab/
├── app/
│   ├── seed_silver.py
│   ├── pipeline_ecommerce.py
│   ├── analitik_duckdb.py
│   └── ekspor_postgresql.py
├── data/
│   ├── silver_transaksi.csv          # 15.000 baris (referensi)
│   ├── gold_tren_bulanan.csv         # 12 bulan
│   ├── gold_tren_lanjutan.csv        # MA3/MoM (referensi)
│   ├── gold_omzet_kelas.csv          # 6 kategori
│   ├── gold_omzet_geografis.csv      # 10 kota
│   └── gold_segmentasi_rfm.csv       # 300 partisipan
├── data/gold/          # Parquet lokal dari HDFS (gitignored)
├── KATALOG-DATA.md
├── requirements.txt    # duckdb
├── start-spark.sh / start-viz.sh
└── scripts/
    ├── run_pipeline_full.sh
    ├── export_gold_local.sh
    ├── run_analitik_duckdb.sh
    ├── run_ekspor_postgresql.sh
    └── measure_superset_perf.sh
```

## Setup

```bash
cd sesi-praktikum/chapter-14/Konfigurasi-lab
cp .env.example .env
chmod +x *.sh scripts/*.sh

# Visualisasi (delegasi ke Chapter 12)
bash start-viz.sh

# Spark (reuse vendor Chapter 12)
bash build-spark.sh    # sekali
bash start-spark.sh
bash scripts/setup_hdfs_datalake.sh
```

## Urutan skrip

| Perintah | Fungsi |
|---|---|
| `bash scripts/run_pipeline_full.sh` | Seed Silver + Gold Parquet |
| `bash scripts/verify_hdfs.sh` | Cek HDFS |
| `bash scripts/export_gold_local.sh` | Parquet → `data/gold/` |
| `bash scripts/run_analitik_duckdb.sh` | 4 query OLAP (Tahap 2) |
| `bash scripts/run_ekspor_postgresql.sh` | Gold → PostgreSQL |
| `bash scripts/verify_postgres.sh` | Hitung baris tabel (**12+6+10+~300**) |
| `bash scripts/measure_superset_perf.sh [CHART_ID]` | Uji API (Tahap 4) |

## Perbedaan dengan Chapter 12

| Aspek | Ch.12 | Ch.14 |
|---|---|---|
| Pipeline | `persiapan_analitik` + `metrik_lanjutan` | Satu `pipeline_ecommerce.py` + **RFM** |
| Gold tren | `tren_lanjutan` (CSV) | `tren_bulanan` (Parquet, kolom `mom_growth`) |
| Analitik SQL | — | DuckDB (pengganti Trino) |

Jika Silver dari Bab 12 sudah ada, cukup `bash scripts/run_pipeline_ecommerce.sh` (lewati seed).

## Hentikan

```bash
bash stop-spark.sh
bash stop-viz.sh
```
