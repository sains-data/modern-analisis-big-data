# Konfigurasi Lab Chapter 8

Praktik **Hadoop + Spark + Hive + HBase** (`bigdata-spark`, Docker): Bronze CSV di HDFS → Silver Parquet → Hive SQL → profil HBase.

Dataset **500 transaksi** + **50 pelanggan** dari generator [`synthetic-data/`](../../synthetic-data/README.md) (Gaussian Copula). Detail mapping: **[KATALOG-DATA.md](KATALOG-DATA.md)**.

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Repo | `vendor/bigdata-spark` (auto-clone) |
| Hadoop / Spark / Hive / HBase | 3.4.1 / 3.5.5 / 4.0.1 / 2.5.11 |
| Kontainer | `bigdata-spark` |
| Root datalake HDFS | `/datalake/` |
| Skrip di kontainer | `/opt/spark-jobs/` |
| HBase Thrift (happybase) | `localhost:9090` (di dalam kontainer) |
| Hive Metastore Thrift | `thrift://localhost:9083` |

## Port (dari host)

| Port | Layanan |
|---|---|
| 9870 | HDFS NameNode UI |
| 8088 | YARN |
| 4040 | Spark UI |
| 10001 | HiveServer2 (Beeline) |
| 10002 | Hive Web UI |
| 16010 | HBase Master UI |

## Struktur folder

```
Konfigurasi-lab/
├── build.sh / start.sh / login.sh / stop.sh
├── data/
│   ├── transaksi.csv, pelanggan.csv      # 500 + 50 baris (legacy)
│   ├── catatan_aktivitas.csv             # schema kanonik
│   └── entitas_partisipan.csv
├── KATALOG-DATA.md                       # mapping & volume harapan
├── app/
│   ├── hive_etl.py
│   ├── spark_ke_hbase.py
│   ├── format_benchmark.py
│   ├── silver_orc_hive.py
│   └── event_log_hbase.py
└── scripts/
    ├── ensure_spark_repo.sh
    ├── setup_services.sh
    ├── setup_datalake_bronze.sh
    ├── run_hive_etl.sh
    ├── run_spark_ke_hbase.sh
    └── ...
```

## Setup pertama kali

```bash
cd sesi-praktikum/chapter-8/Konfigurasi-lab
cp .env.example .env
chmod +x *.sh scripts/*.sh
bash scripts/ensure_spark_repo.sh
```

Unduh **semua tarball** ke `vendor/bigdata-spark/` (lihat [README bigdata-spark](https://github.com/sains-data/bigdata-spark)):
- `hadoop-3.4.1.tar.gz`
- `spark-3.5.5-bin-hadoop3.tgz`
- `apache-hive-4.0.1-bin.tar.gz`
- `apache-tez-0.10.4-bin.tar.gz`
- `hbase-2.5.11-bin.tar.gz`
- `apache-zookeeper-3.8.4-bin.tar.gz`

```bash
bash build.sh
bash start.sh
# tunggu bootstrap selesai, lalu:
bash scripts/setup_datalake_bronze.sh
```

## Urutan latihan (dari host)

| Perintah | Latihan |
|---|---|
| `bash scripts/verify_cluster.sh` | 1 |
| `bash scripts/setup_datalake_bronze.sh` | 1 |
| `bash scripts/run_hive_etl.sh` | 2 |
| `bash scripts/run_spark_ke_hbase.sh` | 3 |
| `bash scripts/run_format_benchmark.sh` | 4 |
| `bash scripts/run_silver_orc_hive.sh` | 5A |
| `bash scripts/run_event_log_hbase.sh` | 5B |
| `bash scripts/verify_datalake.sh` | penutup |

Eksplorasi Hive Shell: `bash login.sh` lalu `hive` atau `beeline -u jdbc:hive2://localhost:10001/ -n hive -p hive`.

## Hentikan klaster

```bash
bash stop.sh
```
