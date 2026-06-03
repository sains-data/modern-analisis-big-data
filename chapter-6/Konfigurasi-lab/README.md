# Konfigurasi Lab Chapter 6

Praktik **Medallion Architecture** (Bronze → Silver → Gold) dengan PySpark pada klaster **Hadoop + Spark** (`bigdata-spark`, Docker).

Dataset Bronze berasal dari entitas sintesis **`catatan_aktivitas`** + **`entitas_partisipan`** — selaras Bab 3–5. Detail: [KATALOG-DATA.md](KATALOG-DATA.md).

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
├── KATALOG-DATA.md
├── app/
│   ├── spark_common.py
│   ├── pipeline_bronze_silver.py
│   ├── analisis_join.py
│   ├── analisis_plan.py
│   ├── window_function.py
│   └── sql_silver.py
├── data/
│   ├── transaksi.csv           ← 16 baris (legacy + anomali)
│   ├── pelanggan.csv           ← 7 baris
│   ├── catatan_aktivitas.csv   ← schema kanonik
│   └── entitas_partisipan.csv
└── scripts/
    ├── setup_datalake_bronze.sh
    ├── run_pipeline_bronze_silver.sh
    └── …
```

## Data latihan (ringkas)

| Layer | Volume harapan |
|-------|----------------|
| Bronze transaksi | 16 baris |
| Silver transaksi | **12 baris** valid |
| Bronze pelanggan | 7 partisipan (C001–C007) |

Partisipan C001–C007 = PK-0001–PK-0007 (nama sama dengan Bab 3 & 5).

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
| `bash scripts/setup_datalake_bronze.sh` | 1 |
| `bash scripts/run_pipeline_bronze_silver.sh` | 2 |
| `bash scripts/run_analisis_join.sh` | 3 |
| `bash scripts/run_analisis_plan.sh` | 4 |
| `bash scripts/run_window_function.sh` | 5A |
| `bash scripts/run_sql_silver.sh` | 5B |

## Regenerasi data sintesis

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch06_medallion
bash scripts/sync_to_chapters.sh
```

## Hentikan klaster

```bash
bash stop.sh
```

## Troubleshooting

| Gejala | Solusi |
|---|---|
| Silver ≠ 12 baris | Regenerasi `ch06_medallion`; jangan ubah CSV manual |
| Anomali tidak sesuai dokumentasi | Sync ulang dari `synthetic-data/` |
| Gold kosong | Pastikan Latihan 2 sukses sebelum `run_analisis_join.sh` |
