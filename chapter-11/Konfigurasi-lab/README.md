# Konfigurasi Lab Chapter 11

Stack ini menyiapkan satu kontainer `bigdata-spark` untuk HDFS + YARN + Spark MLlib, lalu menjalankan script latihan dari folder repo.

## 1) Prasyarat

- Docker + Docker Compose aktif
- RAM minimal 8 GB
- Dua file binary sudah ada di folder `Konfigurasi-lab/`:
  - `hadoop-3.4.1.tar.gz`
  - `spark-3.5.5-bin-hadoop3.tgz`

## 2) Build dan start stack

```bash
cd Konfigurasi-lab
bash build.sh
bash start.sh
```

Verifikasi:

```bash
docker ps | rg bigdata-spark
docker exec bigdata-spark cat /tmp/bootstrap.log
docker exec bigdata-spark jps
```

## 3) Inisialisasi data latihan

```bash
bash scripts/init_data.sh
```

Data akan dibuat ke:
- `hdfs:///datalake/bronze/transaksi/`
- `hdfs:///datalake/silver/transaksi/`

## 4) Menjalankan script latihan

Semua script sudah tersedia di `Konfigurasi-lab/scripts/`.

Contoh:

```bash
bash scripts/spark_submit.sh /opt/modul9/scripts/linear_regression.py
bash scripts/spark_submit.sh /opt/modul9/scripts/klasifikasi_dt.py
bash scripts/spark_submit.sh /opt/modul9/scripts/kmeans_elbow.py
bash scripts/spark_submit.sh /opt/modul9/scripts/pipeline_ml_e2e.py
bash scripts/spark_submit.sh /opt/modul9/scripts/inference.py
```

## 5) Daftar script

| File | Dipakai di |
|---|---|
| `scripts/buat_data_ml.py` | Latihan 1 |
| `scripts/linear_regression.py` | Latihan 2 (regresi) |
| `scripts/klasifikasi_dt.py` | Latihan 2 (klasifikasi) |
| `scripts/kmeans_elbow.py` | Latihan 3 |
| `scripts/pipeline_ml_e2e.py` | Latihan 4 |
| `scripts/inference.py` | Latihan 4 |
| `scripts/eksplorasi_regparam.py` | Latihan 5 |
| `scripts/eksplorasi_maxdepth.py` | Latihan 5 |

## 6) Hentikan stack

```bash
bash stop.sh
```
