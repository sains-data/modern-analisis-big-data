# Chapter 6 — Spark SQL & Medallion Architecture

Praktik pipeline **Bronze → Silver → Gold** di HDFS dengan PySpark pada klaster **Hadoop + Spark** (YARN).

## Alur cepat

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
cp .env.example .env
# unduh hadoop + spark tarball ke vendor/bigdata-spark/
bash build.sh && bash start.sh
bash scripts/setup_datalake_bronze.sh
bash scripts/run_pipeline_bronze_silver.sh
bash scripts/run_analisis_join.sh
bash scripts/run_analisis_plan.sh
bash stop.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Struktur datalake & upload Bronze |
| [Latihan 2](Latihan2/README.md) | `pipeline_bronze_silver.py` |
| [Latihan 3](Latihan3/README.md) | `analisis_join.py` — Silver ke Gold |
| [Latihan 4](Latihan4/README.md) | `analisis_plan.py` — execution plan |
| [Latihan 5](Latihan5/README.md) | Window function & Spark SQL |
