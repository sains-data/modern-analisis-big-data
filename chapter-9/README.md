# Chapter 9 — Orkestrasi dan Tata Kelola Data

Praktik chapter ini mengintegrasikan **Apache Airflow** (orkestrasi), **Apache Atlas** (metadata & lineage), dan klaster **HDFS + Spark + Hive** (`bigdata-spark` dari Chapter 5).

Dataset referensi **`transaksi_harian.csv`** (100 baris, ~3% invalid) dihasilkan generator sintesis [`synthetic-data/`](../synthetic-data/README.md) — entitas `catatan_aktivitas`. Runtime DAG memakai `generate_data.py` dengan seed per tanggal.

Sumber materi: bagian **Sesi Praktik: Orkestrasi dan Tata Kelola Data** di `chapter-9.tex`.

## Komponen

| Komponen | Versi / Catatan |
|---|---|
| Airflow | 2.9.x (Docker) |
| Apache Atlas | 2.3.0 (Docker) |
| Spark / Hive | via kontainer `bigdata-spark` |
| Durasi estimasi | ~3 jam (5 latihan) |

## Struktur folder

```
chapter-9/
├── Konfigurasi-lab/     ← Docker Compose Airflow + Atlas + skrip lab
├── Latihan1/ … Latihan5/
└── README.md
```

## Alur setup (ringkas)

| Langkah | Perintah |
|---|---|
| 1 | Setup **Chapter 5** — klaster `bigdata-spark` (HDFS, YARN, Spark, Hive) |
| 2 | `cd Konfigurasi-lab && cp .env.example .env && bash start.sh` |
| 3 | `bash scripts/setup_bigdata_spark.sh` |
| 4 | Kerjakan Latihan 1 → 5 |

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)** · **[KATALOG-DATA.md](Konfigurasi-lab/KATALOG-DATA.md)**

## Data latihan

| File | Volume | Catatan |
|------|--------|---------|
| `transaksi_harian.csv` | **100 baris** | Legacy: `id, nilai, kategori` |
| `catatan_aktivitas_harian.csv` | 100 baris | Schema kanonik + anomali ~3% |
| Silver (hasil ETL) | **~97 baris** | 3 baris invalid ditolak |

Runtime DAG: `generate_data.py {{ ds }} 100` — pola invalid serupa, nilai berbeda per tanggal.

## Port & kredensial (dari host)

| Port | Layanan | URL | Login |
|---|---|---|---|
| 18681 | Airflow Web UI | http://localhost:18681 | `airflow` / `airflow` |
| 22100 | Atlas UI & REST API | http://localhost:22100 | `admin` / `admin` |
| 9870 | HDFS UI (`bigdata-spark`) | http://localhost:9870 | — |
| 8088 | YARN UI | http://localhost:8088 | — |

**Atlas REST:** `http://localhost:22100/api/atlas/v2`

## Daftar latihan

| Latihan | Topik (sesuai bab) | Estimasi |
|---|---|---|
| [Latihan 1](Latihan1/README.md) | DAG Airflow sederhana (Bash, Python, XCom, HDFS) | 20 menit |
| [Latihan 2](Latihan2/README.md) | Integrasi Airflow + Spark (`SparkSubmitOperator`) | 25 menit |
| [Latihan 3](Latihan3/README.md) | Apache Atlas — entitas, klasifikasi PII, lineage | 20 menit |
| [Latihan 4](Latihan4/README.md) | Pipeline end-to-end (Spark + Hive + Atlas, task paralel) | 25 menit |
| [Latihan 5](Latihan5/README.md) | Retry, pencarian Atlas, refleksi | 15 menit |

## Path HDFS latihan

```
hdfs:///datalake/
├── bronze/latihan/    ← CSV hasil ingest
├── silver/latihan/    ← Parquet (Spark ETL)
└── gold/latihan/      ← agregat akhir
```

## Perintah CLI singkat

```bash
docker exec modul7-airflow-scheduler airflow dags list
docker exec bigdata-spark hdfs dfs -ls /datalake/
curl -s -u admin:admin http://localhost:22100/api/atlas/admin/status
```

> Nama kontainer `modul7-*` berasal dari image Docker Compose lab; fungsinya untuk stack Chapter 9.
