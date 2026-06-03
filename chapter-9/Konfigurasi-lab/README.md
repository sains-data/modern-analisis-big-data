# Konfigurasi Lab Chapter 9 — Airflow & Atlas
> Apache Airflow 2.9.1 · Apache Atlas 2.3.0 · Docker Compose · bigdata-spark (Chapter 5)

> **Catatan arsitektur:** Chapter 9 memakai **dua lingkungan** yang saling melengkapi:
> 1. **`bigdata-spark`** (Chapter 5) — HDFS, YARN, Spark, Hive untuk komputasi & penyimpanan data
> 2. **Stack Docker** (folder ini) — Airflow + Atlas + dependensi (ZooKeeper, Kafka, HBase, Solr, PostgreSQL)
>
> Pola instalasi Airflow/Atlas **mengacu** pada repositori [`Data-Lakehouse-Metadata`](../../../../Data-Lakehouse-Metadata) — image resmi, port host `18681` / `22100`, backend Atlas JanusGraph + Solr (bukan paket biner Atlas embedded BerkeleyDB).

Dataset referensi **100 catatan aktivitas harian** dari generator [`synthetic-data/`](../../synthetic-data/README.md). Detail: **[KATALOG-DATA.md](KATALOG-DATA.md)**.

> Runtime pipeline memanggil `scripts/lab/generate_data.py` (seed per `{{ ds }}`). File di `data/` = referensi statis volume, schema, dan anomali.

---

## Daftar Isi

1. [Prasyarat](#1-prasyarat)
2. [Struktur Folder](#2-struktur-folder)
3. [Persiapan bigdata-spark (Modul 9)](#3-persiapan-bigdata-spark-modul-9)
4. [Menjalankan Stack Airflow + Atlas](#4-menjalankan-stack-airflow--atlas)
5. [Inisialisasi Skrip Lab & HDFS](#5-inisialisasi-skrip-lab--hdfs)
6. [Verifikasi Lingkungan](#6-verifikasi-lingkungan)
7. [Mengakses UI Airflow dan Atlas](#7-mengakses-ui-airflow-dan-atlas)
8. [Cara Kerja Integrasi Airflow ↔ bigdata-spark](#8-cara-kerja-integrasi-airflow--bigdata-spark)
9. [Checklist Sebelum Latihan](#9-checklist-sebelum-latihan)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prasyarat

| Komponen | Versi / Status | Cara Cek |
|---|---|---|
| Docker Engine | ≥ 24.0 | `docker --version` |
| Docker Compose | ≥ 2.20 | `docker compose version` |
| RAM tersedia | Min **10 GB** (Atlas + Airflow + bigdata-spark) | `free -h` |
| Kontainer `bigdata-spark` | Dari Modul 9 | `docker ps \| grep bigdata-spark` |
| Git | 2.x | `git --version` |

> **Urutan bab:** Selesaikan setup **Chapter 5** (`bigdata-spark`) terlebih dahulu, lalu kembali ke folder ini.

---

## 2. Struktur Folder

```
Konfigurasi-lab/
├── docker-compose.yml       ← ZK, Kafka, HBase, Solr, Atlas, Airflow, Postgres
├── start.sh / stop.sh
├── .env.example             ← override port jika bentrok
├── data/
│   ├── transaksi_harian.csv           # 100 baris (legacy)
│   └── catatan_aktivitas_harian.csv   # schema kanonik
├── KATALOG-DATA.md
├── airflow/
│   └── Dockerfile           ← apache/airflow:2.9.1-python3.10 + provider Spark/Hive
├── atlas-conf/              ← atlas-application.properties, hbase-site.xml
├── hbase-conf/
├── solr/atlas-config/       ← core Solr JanusGraph (dari Atlas 2.3.0)
├── scripts/
│   ├── setup_bigdata_spark.sh
│   ├── spark_submit_bigdata.sh
│   ├── bigdata_exec.sh
│   ├── airflow_connections_init.sh
│   └── lab/
│       ├── generate_data.py
│       ├── latihan_etl.py
│       └── pipeline_gold.py
└── dags/                    ← salin/tempel DAG dari latihan ke sini
```

Path HDFS yang dipakai latihan:

```
hdfs:///
└── datalake/
    ├── bronze/latihan/    ← CSV hasil ingest
    ├── silver/latihan/    ← Parquet hasil Spark ETL
    └── gold/latihan/      ← agregat akhir
```

---

## 3. Persiapan bigdata-spark (Chapter 5)

### 3.1 — Pastikan kontainer berjalan

```bash
# Dari direktori bigdata-spark/
bash start.sh
docker ps | grep bigdata-spark
docker exec bigdata-spark jps
# Harus ada: NameNode, DataNode, ResourceManager, NodeManager
```

### 3.2 — (Opsional) Expose HiveServer2 untuk Latihan 4

Jika belum ada, tambahkan port `10000` di `docker-compose.yml` milik `bigdata-spark`:

```yaml
ports:
  - "10000:10000"   # HiveServer2 — opsional untuk Latihan 4
```

Lalu restart kontainer:

```bash
docker compose down && docker compose up -d
```

---

## 4. Menjalankan Stack Airflow + Atlas

Semua langkah di folder **`Konfigurasi-lab/`** (terminal host/WSL):

```bash
cd Konfigurasi-lab
cp .env.example .env          # opsional: ubah port jika bentrok
chmod +x start.sh stop.sh scripts/*.sh
bash start.sh
```

`start.sh` akan:

1. Build image Airflow custom (Python 3.10 + provider Spark/Hive)
2. Menjalankan ZooKeeper → Kafka → HBase → Solr → init core Solr Atlas
3. Menjalankan Apache Atlas (`sburn/apache-atlas:2.3.0`)
4. Init DB Airflow + user admin + koneksi Spark/Hive
5. Menjalankan Airflow webserver & scheduler

**Waktu startup pertama:** Atlas membutuhkan **3–5 menit** (JanusGraph + HBase + Solr).

Pantau log Atlas:

```bash
docker compose logs -f atlas | grep -E "started|ERROR|WARN"
# Tunggu hingga muncul: Atlas Server started!!!
```

---

## 5. Inisialisasi Skrip Lab & HDFS

Setelah **kedua** stack (bigdata-spark + Airflow/Atlas) berjalan:

```bash
bash scripts/setup_bigdata_spark.sh
```

Script ini:

- Menyalin `generate_data.py`, `latihan_etl.py`, `pipeline_gold.py` ke dalam `bigdata-spark`
- Membuat direktori `/datalake/{bronze,silver,gold}/latihan/` di HDFS

Verifikasi:

```bash
docker exec bigdata-spark ls -la /opt/scripts/generate_data.py
docker exec bigdata-spark hdfs dfs -ls /datalake/
```

---

## 6. Verifikasi Lingkungan

Jalankan dari terminal host:

```bash
echo "=== Verifikasi Lab Chapter 9 ==="

printf "%-35s" "bigdata-spark (jps):"
docker exec bigdata-spark jps 2>/dev/null | grep -q NameNode \
  && echo "OK" || echo "GAGAL"

printf "%-35s" "Airflow webserver:"
docker inspect -f '{{.State.Running}}' modul7-airflow-webserver 2>/dev/null \
  | grep -q true && echo "BERJALAN" || echo "TIDAK BERJALAN"

printf "%-35s" "Airflow UI (HTTP):"
CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:18681/health)
[ "$CODE" = "200" ] && echo "OK ($CODE)" || echo "GAGAL ($CODE)"

printf "%-35s" "Atlas REST API:"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -u admin:admin http://localhost:22100/api/atlas/admin/status)
[ "$STATUS" = "200" ] && echo "OK ($STATUS)" || echo "GAGAL ($STATUS)"

printf "%-35s" "HDFS /datalake:"
docker exec bigdata-spark hdfs dfs -ls /datalake 2>/dev/null \
  | grep -q datalake && echo "OK" || echo "GAGAL"

printf "%-35s" "Koneksi Airflow:"
docker exec modul7-airflow-scheduler airflow connections list 2>/dev/null \
  | grep -cE "spark|hive" | xargs -I{} echo "{} koneksi (harus ≥ 3)"
```

---

## 7. Mengakses UI Airflow dan Atlas

### Apache Airflow

```
http://localhost:18681
```

| | |
|---|---|
| **Username** | `airflow` |
| **Password** | `airflow` |

File DAG ditempatkan di `Konfigurasi-lab/dags/`. Scheduler memuat perubahan otomatis (~30 detik).

### Apache Atlas

```
http://localhost:22100
```

| | |
|---|---|
| **Username** | `admin` |
| **Password** | `admin` |

**REST API base URL (untuk script Python latihan):**

```
http://localhost:22100/api/atlas/v2
```

> Port **22100** di host memetakan ke port internal **21000** di container Atlas — sama seperti konfigurasi `LHMETA_ATLAS_PORT` di Data-Lakehouse-Metadata.

---

## 8. Cara Kerja Integrasi Airflow ↔ bigdata-spark

Airflow berjalan di container terpisah. Task yang membutuhkan HDFS/Spark/Hive memanggil **`bigdata-spark`** via Docker socket:

| Mekanisme | File | Fungsi |
|---|---|---|
| `SparkSubmitOperator` | `scripts/spark_submit_bigdata.sh` | `docker exec bigdata-spark spark-submit ...` |
| `BashOperator` (HDFS/Hive) | `scripts/bigdata_exec.sh` | `docker exec bigdata-spark bash -lc '...'` |
| Koneksi `spark_default` | `scripts/airflow_connections_init.sh` | Terdaftar otomatis saat `airflow-init` |

**Contoh perintah BashOperator di DAG:**

```python
bash_command=(
    "/opt/airflow/scripts/bigdata_exec.sh "
    "'python /opt/scripts/generate_data.py {{ ds }} 100 "
    "> /tmp/transaksi_{{ ds_nodash }}.csv && "
    "hdfs dfs -put -f /tmp/transaksi_{{ ds_nodash }}.csv "
    "/datalake/bronze/latihan/'"
),
```

**CLI Airflow dari host:**

```bash
docker exec modul7-airflow-scheduler airflow dags list
docker exec modul7-airflow-scheduler airflow dags trigger latihan_pipeline_transaksi
```

---

## 9. Checklist Sebelum Latihan

**Modul 9 (bigdata-spark):**
- [ ] `docker ps` menampilkan `bigdata-spark` status Up
- [ ] `docker exec bigdata-spark jps` menampilkan 4 proses Hadoop
- [ ] `bash scripts/setup_bigdata_spark.sh` selesai tanpa error

**Stack Modul 7:**
- [ ] `curl -s http://localhost:18681/health` → HTTP 200
- [ ] Login Airflow `http://localhost:18681` dengan `airflow / airflow`
- [ ] `curl -u admin:admin http://localhost:22100/api/atlas/admin/status` → HTTP 200
- [ ] Login Atlas `http://localhost:22100` dengan `admin / admin`
- [ ] `docker exec modul7-airflow-scheduler airflow connections list | grep spark` menampilkan `spark_default`

**Skrip lab:**
- [ ] `/opt/scripts/generate_data.py` ada di `bigdata-spark`
- [ ] `/opt/spark-jobs/latihan_etl.py` dan `pipeline_gold.py` ada di `bigdata-spark`
- [ ] `hdfs dfs -ls /datalake/bronze/latihan/` dapat dijalankan

---

## 10. Troubleshooting

### Atlas — startup lama atau HTTP 502

Atlas membutuhkan HBase + Solr healthy. Cek:

```bash
docker compose ps
docker compose logs --tail=50 atlas
docker compose logs --tail=30 hbase solr
```

Jika Solr core gagal dibuat, ulangi init:

```bash
docker compose stop atlas solr solr-atlas-init
docker compose rm -f atlas solr-atlas-init
docker compose up -d solr solr-atlas-init atlas
```

### Atlas — TLS / keystore error

Pastikan `atlas-conf/atlas-application.properties` berisi `atlas.enableTLS=false` (sudah diset selaras Data-Lakehouse-Metadata).

### Airflow task Spark gagal — "Cannot connect to Docker daemon"

Pastikan Docker socket ter-mount dan grup GID benar:

```bash
export DOCKER_GID=$(getent group docker | cut -d: -f3)
docker compose up -d --force-recreate airflow-scheduler airflow-webserver
```

### Airflow task HDFS gagal — "No such file or directory: hdfs"

Jalankan ulang `bash scripts/setup_bigdata_spark.sh` dan pastikan Hadoop aktif di `bigdata-spark`:

```bash
docker exec bigdata-spark bash -lc "start-dfs.sh && start-yarn.sh && jps"
```

### Port bentrok

Salin `.env.example` → `.env`, ubah `MOD7_AIRFLOW_WEB_PORT` atau `MOD7_ATLAS_PORT`, lalu:

```bash
docker compose down
docker compose up -d
```

---

## Ringkasan Port

| Port Host | Layanan | URL | Kredensial |
|---|---|---|---|
| **18681** | Airflow Web UI | http://localhost:18681 | airflow / airflow |
| **22100** | Atlas Web UI & REST API | http://localhost:22100 | admin / admin |
| 18987 | Solr Admin (debug) | http://localhost:18987/solr/ | — |
| 19017 | HBase Master UI (debug) | http://localhost:19017 | — |
| 15437 | PostgreSQL (debug) | localhost:15437 | admin / admin123 |
| 9870 | HDFS UI (Modul 9) | http://localhost:9870 | — |
| 8088 | YARN UI (Modul 9) | http://localhost:8088 | — |

---

*Lingkungan siap — lanjut ke [Latihan 1](../Latihan1/README.md).*
