# Konfigurasi Lab Chapter 6

Praktik **Medallion Architecture** (Bronze → Silver → Gold) dengan PySpark pada klaster **Hadoop + Spark** (`bigdata-spark`, Docker).

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Repo | `vendor/bigdata-spark` (auto-clone) |
| Hadoop / Spark | 3.4.1 / 3.5.5 (tarball manual) |
| Kontainer | `bigdata-spark` |
| Root datalake HDFS | `/datalake/` |
| Skrip di kontainer | `/opt/spark-jobs/` |
| NameNode UI | http://localhost:9870 |
| YARN UI | http://localhost:8088 |
| Spark UI | http://localhost:4040 |

## Struktur folder

```
Konfigurasi-lab/
├── build.sh / start.sh / login.sh / stop.sh
├── app/
│   ├── spark_common.py
│   ├── pipeline_bronze_silver.py
│   ├── analisis_join.py
│   ├── analisis_plan.py
│   ├── window_function.py
│   └── sql_silver.py
├── data/
│   ├── transaksi.csv
│   └── pelanggan.csv
└── scripts/
    ├── ensure_spark_repo.sh
    ├── verify_cluster.sh
    ├── setup_datalake_bronze.sh
    ├── verify_datalake.sh
    ├── run_pipeline_bronze_silver.sh
    ├── run_analisis_join.sh
    ├── run_analisis_plan.sh
    ├── run_window_function.sh
    └── run_sql_silver.sh
```

## Setup pertama kali

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
cp .env.example .env
chmod +x *.sh scripts/*.sh
bash scripts/ensure_spark_repo.sh
```

Unduh ke `vendor/bigdata-spark/`:
- [hadoop-3.4.1.tar.gz](https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz)
- [spark-3.5.5-bin-hadoop3.tgz](https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz)

```bash
bash build.sh
bash start.sh
bash scripts/setup_datalake_bronze.sh
```

## Urutan latihan (dari host)

| Perintah | Latihan |
|---|---|
| `bash scripts/verify_cluster.sh` | 1 (prasyarat) |
| `bash scripts/setup_datalake_bronze.sh` | 1 |
| `bash scripts/verify_datalake.sh` | 1 |
| `bash scripts/run_pipeline_bronze_silver.sh` | 2 |
| `bash scripts/run_analisis_join.sh` | 3 |
| `bash scripts/run_analisis_plan.sh` | 4 |
| `bash scripts/run_window_function.sh` | 5A |
| `bash scripts/run_sql_silver.sh` | 5B |

## Hentikan klaster

```bash
bash stop.sh
```
