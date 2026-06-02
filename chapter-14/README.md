# Chapter 14 — Pipeline Big Data End-to-End

Praktik **integrasi**: Spark Medallion (Silver → Gold) → **DuckDB** (analitik gaya Trino) → PostgreSQL → **Superset** (dashboard dari Bab 12).

## Alur cepat

```bash
cd sesi-praktikum/chapter-14/Konfigurasi-lab
cp .env.example .env
bash start-viz.sh          # Superset + PostgreSQL (Chapter 12)
bash build-spark.sh && bash start-spark.sh
bash scripts/run_pipeline_full.sh
bash scripts/run_analitik_duckdb.sh
bash scripts/run_ekspor_postgresql.sh
bash scripts/verify_postgres.sh
# http://localhost:8088 — tambah chart RFM + MoM (Latihan 3–4)
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan ↔ Tahap buku

| Latihan | Tahap | Topik |
|---|---|---|
| [Latihan 1](Latihan1/README.md) | Tahap 1 | Spark ETL `pipeline_ecommerce.py`, Gold Parquet |
| [Latihan 2](Latihan2/README.md) | Tahap 2 | `analitik_duckdb.py`, ekspor Parquet lokal |
| [Latihan 3](Latihan3/README.md) | Tahap 3 | Ekspor JDBC, chart Pie RFM + Line MoM di Superset |
| [Latihan 4](Latihan4/README.md) | Tahap 4 | Checklist kualitas, UAT, `measure_superset_perf.sh` |
| [Latihan 5](Latihan5/README.md) | Tahap 5 | Anti-pattern, siklus hidup dashboard, diskusi |

## Prasyarat

- **Chapter 12** (opsional jika dashboard sudah ada): Superset + skema PostgreSQL `analytics`
- **bigdata-spark**: tarball di `chapter-12/Konfigurasi-lab/vendor/bigdata-spark/` (atau set `SPARK_REPO_DIR` di `.env`)

## Catatan port

- **8088** Superset — bisa bentrok dengan YARN UI Spark; hentikan salah satu jika perlu.
- Gold Bab 14 memakai path `hdfs:///datalake/gold/tren_bulanan/` (Parquet), berbeda dari Ch.12 `tren_lanjutan` (CSV).
