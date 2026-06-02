# Konfigurasi Lab Chapter 5

Praktik **PySpark pada YARN** dengan klaster Hadoop + Spark (`bigdata-spark`, Docker).

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Repo | `vendor/bigdata-spark` (auto-clone) |
| Hadoop / Spark | 3.4.1 / 3.5.5 (tarball manual) |
| Kontainer | `bigdata-spark` |
| Path HDFS | `/user/lab/modul5` (default, lihat `.env`) |
| Skrip di kontainer | `/opt/spark-jobs/` |
| NameNode UI | http://localhost:9870 |
| YARN UI | http://localhost:8088 |
| Spark UI | http://localhost:4040 |

## Struktur folder

```
Konfigurasi-lab/
├── build.sh / start.sh / login.sh / stop.sh
├── app/
│   ├── hitung_pi.py
│   ├── hitung_pi_cache.py
│   └── analisis_nilai.py
├── data/mahasiswa.csv
└── scripts/
    ├── ensure_spark_repo.sh
    ├── verify_cluster.sh
    ├── setup_hdfs_mahasiswa.sh
    ├── run_hitung_pi.sh
    ├── run_analisis_nilai.sh
    ├── run_hitung_pi_cache.sh
    └── compare_hdfs_sizes.sh
```

## Setup pertama kali

```bash
cd sesi-praktikum/chapter-5/Konfigurasi-lab
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
bash scripts/setup_hdfs_mahasiswa.sh
```

## Urutan latihan (dari host)

| Perintah | Latihan |
|---|---|
| `bash scripts/verify_cluster.sh` | 1 |
| `bash scripts/run_hitung_pi.sh` | 2 |
| `bash scripts/run_analisis_nilai.sh` | 3 |
| `bash scripts/compare_hdfs_sizes.sh` | 4 |
| `SLICES=8 bash scripts/run_hitung_pi.sh` | 5A |
| `bash scripts/run_hitung_pi_cache.sh` | 5B |

## Hentikan klaster

```bash
bash stop.sh
```
