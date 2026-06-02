# Chapter 3 — Desain Arsitektur dan Platform Big Data

Praktik **Data Lake** sederhana dengan MinIO (S3-compatible) dan Python, mengikuti pola **Medallion** (Bronze → Silver → Gold).

## Alur cepat

```bash
cd sesi-praktikum/chapter-3/Konfigurasi-lab
bash start.sh
docker exec -it bigdata-compute python upload_bronze.py
docker exec -it bigdata-compute python transform.py
docker exec -it bigdata-compute python aggregate.py
docker exec -it bigdata-compute python verify_pipeline.py
```

Panduan lengkap: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Setup & verifikasi stack |
| [Latihan 2](Latihan2/README.md) | Bucket Medallion & ingest Bronze |
| [Latihan 3](Latihan3/README.md) | Transform Bronze → Silver |
| [Latihan 4](Latihan4/README.md) | Agregasi Silver → Gold |
| [Latihan 5](Latihan5/README.md) | Verifikasi E2E & latihan lanjutan |

## File eksekusi (di `Konfigurasi-lab/`)

| Path | Fungsi |
|---|---|
| `docker-compose.yml` | MinIO, `mc`, compute Python |
| `start.sh` / `stop.sh` | Jalankan / hentikan stack |
| `scripts/init_buckets.sh` | Buat bucket bronze/silver/gold |
| `raw-data/sample_users.csv` | Data mentah latihan |
| `app/upload_bronze.py` | Ingest ke Bronze |
| `app/transform.py` | Bronze → Silver (Parquet) |
| `app/aggregate.py` | Silver → Gold |
| `app/verify_pipeline.py` | Cek object wajib di ketiga layer |
