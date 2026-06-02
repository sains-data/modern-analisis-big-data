# Konfigurasi Lab Chapter 3

Praktik chapter ini membangun **data lake** sederhana berbasis Docker:
- **MinIO** — storage layer (S3-compatible)
- **Python container** — compute layer (`boto3`, `pandas`, `pyarrow`)
- Alur **Medallion**: Bronze → Silver → Gold

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Storage | `bigdata-minio` |
| MinIO client (mc) | `bigdata-mc` |
| Compute | `bigdata-compute` |
| MinIO API | http://localhost:9000 |
| MinIO Console | http://localhost:9001 |
| Kredensial | `admin` / `admin123` |
| Jaringan Docker | `bigdata-chapter3-net` |

## Struktur folder

```
Konfigurasi-lab/
├── docker-compose.yml
├── start.sh / stop.sh
├── scripts/
│   └── init_buckets.sh
├── app/
│   ├── s3_client.py
│   ├── upload_bronze.py
│   ├── transform.py
│   ├── aggregate.py
│   └── verify_pipeline.py
├── raw-data/
│   └── sample_users.csv
└── data/              ← volume persisten MinIO (gitignored)
```

## 1) Prasyarat

- Docker Engine + Docker Compose
- RAM minimal 8 GB
- Windows: disarankan WSL2

## 2) Jalankan stack

```bash
cd sesi-praktikum/chapter-3/Konfigurasi-lab
chmod +x start.sh stop.sh scripts/init_buckets.sh
bash start.sh
```

`start.sh` akan:
1. `docker compose up -d` (MinIO, mc, compute)
2. Membuat bucket `bronze`, `silver`, `gold` via `init_buckets.sh`

Verifikasi:

```bash
docker compose ps
docker exec bigdata-compute python -c "import boto3; print('boto3 OK')"
docker exec bigdata-mc mc ls local/
```

Buka MinIO Console: http://localhost:9001 (`admin` / `admin123`)

## 3) Pipeline latihan (urutan skrip)

Jalankan dari host (setelah `start.sh`):

```bash
docker exec -it bigdata-compute python upload_bronze.py
docker exec -it bigdata-compute python transform.py
docker exec -it bigdata-compute python aggregate.py
docker exec -it bigdata-compute python verify_pipeline.py
```

Object yang dihasilkan:

| Layer | Key |
|---|---|
| Bronze | `bronze/users/sample_users.csv` |
| Silver | `silver/users/users_clean.parquet` |
| Gold | `gold/summary/city_summary.parquet` |

## 4) Perintah mc manual (opsional)

Gunakan kontainer **`bigdata-mc`** (bukan `bigdata-minio`):

```bash
docker exec -it bigdata-mc mc alias set local http://minio:9000 admin admin123
docker exec -it bigdata-mc mc ls local/bronze --recursive
```

## 5) Hentikan stack

```bash
bash stop.sh
```

Data MinIO tetap di folder `data/` sampai dihapus manual.

## Troubleshooting

| Gejala | Solusi |
|---|---|
| Compute gagal `connection refused` ke MinIO | Tunggu healthcheck MinIO hijau: `docker compose ps` |
| `curl` healthcheck gagal | Pastikan image `minio/minio:latest` terbaru, atau jalankan ulang `docker compose up -d` |
| Bucket tidak ada | `bash scripts/init_buckets.sh` |
| `sample_users.csv` tidak ditemukan | Pastikan file ada di `raw-data/` dan volume ter-mount |
