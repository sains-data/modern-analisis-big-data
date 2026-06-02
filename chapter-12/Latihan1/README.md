# Latihan 1 — Persiapan Lingkungan dan Data
**Chapter 12 · Visualisasi dan Eksplorasi Data** | Estimasi: **30 menit** | **Tahap 1** (Bab 12)

## Tujuan

- Menjalankan **Superset + PostgreSQL** (`docker-compose-viz.yml`)
- Menyiapkan klaster **Spark** untuk generate data Silver
- Membuat dataset **15.000 transaksi, 12 bulan** (`buat_data_viz.py`)

## Prasyarat

- [ ] [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Docker aktif, RAM ≥ 8 GB

## Referensi buku

- Kontainer: `viz-postgres`, `viz-superset`
- Silver: `hdfs:///datalake/silver/transaksi/`
- Skrip: `Konfigurasi-lab/app/buat_data_viz.py`

## Langkah kerja

### 1) Stack visualisasi

```bash
cd sesi-praktikum/chapter-12/Konfigurasi-lab
cp .env.example .env
bash start-viz.sh
```

Verifikasi: http://localhost:8088 (`admin` / `admin`) — tunggu 2–3 menit jika belum siap.

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8088/health
# Harus 200
```

### 2) Klaster Spark

```bash
bash build-spark.sh    # sekali: unduh tarball ke vendor/bigdata-spark/
bash start-spark.sh
bash scripts/spark_exec.sh "jps"
```

### 3) Folder HDFS & generate data

```bash
bash scripts/run_buat_data_viz.py
```

Output yang diharapkan: **15.000 baris** ke `hdfs:///datalake/silver/transaksi/`, ringkasan omzet per bulan (efek musiman bulan 11 lebih tinggi).

```bash
bash scripts/spark_exec.sh "hdfs dfs -du -h /datalake/silver/transaksi/"
```

> Jika data Silver dari bab sebelumnya sudah ada, Anda boleh melewati langkah 3 dan lanjut Latihan 2.

## Catatan hasil

| Item | Nilai |
|---|---|
| Status `viz-superset` | |
| Status `bigdata-spark` | |
| Baris Silver | ~15.000 |
| Bulan dengan omzet tertinggi (preview) | (biasanya bulan 11) |

## Refleksi

1. Mengapa Superset tidak membaca HDFS langsung?
2. Apa fungsi PostgreSQL dalam pipeline ini?

---

*Latihan 1 selesai. Lanjut **Latihan 2 — Persiapan Data Analitik (Tahap 2)**.*
