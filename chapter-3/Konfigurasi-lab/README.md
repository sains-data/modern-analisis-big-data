# Konfigurasi Lab Chapter 3

Praktik chapter ini membangun **data lake** sederhana berbasis Docker:
- **MinIO** — storage layer (S3-compatible)
- **Python container** — compute layer (`boto3`, `pandas`, `pyarrow`)
- Alur **Medallion**: Bronze → Silver → Gold

Dataset **`sample_users.csv`** (51 baris) dihasilkan generator sintesis Gaussian Copula — lihat [KATALOG-DATA.md](KATALOG-DATA.md).

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
├── KATALOG-DATA.md          ← schema & volume harapan
├── scripts/
│   └── init_buckets.sh
├── app/
│   ├── s3_client.py
│   ├── upload_bronze.py
│   ├── transform.py
│   ├── aggregate.py
│   └── verify_pipeline.py
├── raw-data/
│   └── sample_users.csv     ← 51 baris (sintesis, seed 42)
└── data/                    ← volume persisten MinIO (gitignored)
```

## Data latihan (ringkas)

| Kolom | Contoh |
|-------|--------|
| `id`, `name`, `age` | Profil partisipan |
| `city` | Jakarta, Surabaya, … (10 kota) |
| `salary` | Pendapatan Rp (~5,8 jt – 19,4 jt); baris 3 null |
| `join_date` | 2018-01-01 s/d 2024-06-30 |

Anomali sengaja: **null salary** (baris 3) dan **duplikat penuh** (baris 5 = baris 51).

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

| Layer | Key | Volume harapan |
|---|---|---|
| Bronze | `bronze/users/sample_users.csv` | 51 baris |
| Silver | `silver/users/users_clean.parquet` | 50 baris |
| Gold | `gold/summary/city_summary.parquet` | 10 baris (per kota) |

Contoh output `transform.py`:

```
Bronze: 51 baris, 6 kolom
Silver: 50 baris setelah transformasi
```

Contoh output `aggregate.py`: tabel 10 kota dengan `avg_salary`, `total_karyawan`, `avg_usia`.

## 4) Perintah mc manual (opsional)

Gunakan kontainer **`bigdata-mc`** (bukan `bigdata-minio`):

```bash
docker exec -it bigdata-mc mc alias set local http://minio:9000 admin admin123
docker exec -it bigdata-mc mc ls local/bronze --recursive
```

## 5) Regenerasi data sintesis

Jika file CSV perlu diperbarui dari generator pusat:

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch03_minio
bash scripts/sync_to_chapters.sh
```

## 6) Hentikan stack

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
| `sample_users.csv` tidak ditemukan | Pastikan file ada di `raw-data/` dan volume ter-mount; jalankan sync dari `synthetic-data/` |
| Silver ≠ 50 baris | Pastikan CSV belum diubah manual; regenerasi via `synthetic-data/scripts/generate.sh ch03_minio` |
