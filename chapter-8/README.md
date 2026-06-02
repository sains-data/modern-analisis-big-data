# Chapter 8 — Struktur & Penyimpanan Big Data

Praktik **Hive, HBase, Parquet/ORC** pada klaster **Hadoop + Spark + Hive + HBase** (Docker): Bronze → Silver → SQL → profil NoSQL.

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

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Setup klaster & Bronze HDFS |
| [Latihan 2](Latihan2/README.md) | `hive_etl.py` — Spark + Hive |
| [Latihan 3](Latihan3/README.md) | `spark_ke_hbase.py` — HBase |
| [Latihan 4](Latihan4/README.md) | `format_benchmark.py` |
| [Latihan 5](Latihan5/README.md) | ORC Hive & row key HBase |
